import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, auth, models, database, minio_client

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/clothing",
    tags=["Clothing"],
    dependencies=[Depends(auth.get_current_user)]
)


def _validate_clothing_item_ownership(
        db_clothing_item: models.ClothingItem,
        user_id: int
):
    """
    Validates that a clothing item exists and belongs to the current user.
    Raises HTTPException 404 if not found or ownership mismatch.
    """
    if db_clothing_item is None:
        logger.warning(f"Clothing item not found (Attempted by User: {user_id})")
        raise HTTPException(status_code=404, detail="Clothing item not found")

    if db_clothing_item.owner_id != user_id:
        logger.warning(f"User {user_id} tried to access unauthorized clothing {db_clothing_item.id}")
        raise HTTPException(status_code=404, detail="Clothing item not found")


@router.post(
    "/", response_model=schemas.ClothingItem,
    status_code=status.HTTP_201_CREATED
)
def create_clothing_item(
        clothing_item: schemas.ClothingItemCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.ClothingItem:
    """
    Creates a new clothing item for the currently logged-in user.
    """
    logger.info(f"User {current_user.id} creating new clothing: {clothing_item.name}")
    return crud.create_user_clothing_item(db=db, clothing_item=clothing_item, user_id=current_user.id)


@router.get(
    "/",
    response_model=List[schemas.ClothingItem]
)
def read_clothing_items(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> List[models.ClothingItem]:
    """
    Retrieves a list of all (non-soft-deleted) clothing items
    for the currently logged-in user.
    Generates pre-signed URLs for photos.
    """
    logger.info(f"User {current_user.id} fetching all clothing.")
    clothing_item_list = crud.get_clothing_items_by_user(db, user_id=current_user.id)

    for item in clothing_item_list:
        if item.photo_url:
            item.photo_url = minio_client.get_presigned_url(item.photo_url)
    return clothing_item_list


@router.get(
    "/{clothing_item_id}",
    response_model=schemas.ClothingItem
)
def read_single_pakaian(
        clothing_item_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.ClothingItem:
    """
    Retrieves details for a single clothing item by its ID.
    Ensures the item belongs to the logged-in user.
    Generates a pre-signed URL for the photo.
    """
    logger.info(f"User {current_user.id} fetching clothing ID: {clothing_item_id}")

    db_clothing_item = crud.get_clothing_item_by_id(db, clothing_item_id=clothing_item_id)

    _validate_clothing_item_ownership(db_clothing_item, current_user.id)

    if db_clothing_item.photo_url:
        db_clothing_item.photo_url = minio_client.get_presigned_url(db_clothing_item.photo_url)

    return db_clothing_item


@router.put(
    "/{clothing_item_id}",
    response_model=schemas.ClothingItem
)
def update_single_pakaian(
        clothing_item_id: int,
        clothing_update: schemas.ClothingItemUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.ClothingItem:
    """
    Updates text details for a specific clothing item.
    Ensures the item belongs to the logged-in user.
    """
    logger.info(f"User {current_user.id} updating clothing ID: {clothing_item_id}")

    db_clothing_item = crud.get_clothing_item_by_id(db, clothing_item_id=clothing_item_id)

    _validate_clothing_item_ownership(db_clothing_item, current_user.id)

    return crud.update_clothing_item(db=db, db_clothing_item=db_clothing_item, pakaian_update=clothing_update)


@router.delete(
    "/{clothing_item_id}",
    status_code=status.HTTP_200_OK
)
def soft_delete_single_clothing_item(
        clothing_item_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> dict:
    """
    Soft-deletes a clothing item.
    Ensures the item belongs to the user and is not in an active laundry session.
    """
    logger.info(f"User {current_user.id} attempting soft delete clothing ID: {clothing_item_id}")

    db_clothing_item = crud.get_clothing_item_by_id(db, clothing_item_id=clothing_item_id)

    _validate_clothing_item_ownership(db_clothing_item, current_user.id)

    active_session = db.query(models.LaundrySession).join(models.LaundrySession.clothing_items).filter(
        models.LaundrySession.owner_id == current_user.id,
        models.ClothingItem.id == clothing_item_id,
        models.LaundrySession.status != schemas.LaundryStatus.completed,
        models.LaundrySession.status != schemas.LaundryStatus.taken
    ).first()

    if active_session:
        logger.warning(f"Delete failed: Clothing {clothing_item_id} is in active session {active_session.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete clothing that is in an active laundry session."
        )

    logger.info(f"Soft deleting clothing ID: {clothing_item_id}")
    return crud.soft_delete_clothing_item(db=db, db_clothing_item=db_clothing_item)


@router.post(
    "/{clothing_item_id}/image-upload-url",
    response_model=schemas.PresignedUrl
)
async def generate_upload_url(
        clothing_item_id: int,
        upload_data: schemas.ImageUploadRequest,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> dict:
    """
    Generates a pre-signed S3/MinIO URL for uploading a clothing photo.
    Saves the object name (file path) to the DB.
    """
    logger.info(f"User {current_user.id} requesting upload URL for clothing ID: {clothing_item_id}")

    db_clothing_item = crud.get_clothing_item_by_id(db, clothing_item_id=clothing_item_id)

    _validate_clothing_item_ownership(db_clothing_item, current_user.id)

    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if upload_data.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only image files (JPEG, PNG, GIF) are allowed")

    file_extension = upload_data.file_name.split(".")[-1]
    object_name = f"clothing_images/{current_user.id}/{clothing_item_id}_{datetime.now().timestamp()}.{file_extension}"

    presigned_url_data = minio_client.create_presigned_upload_url(object_name=object_name)

    if not crud.update_clothing_item_photo_url(db, clothing_item_id, object_name):
        raise HTTPException(status_code=500, detail="Failed to update clothing photo URL in DB")

    return {"url": presigned_url_data['url'], "fields": presigned_url_data['fields']}


class ImageUploadRequest(schemas.BaseModel):
    file_name: str
    content_type: str
