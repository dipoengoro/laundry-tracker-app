import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, auth, models, database, minio_client

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pakaian",
    tags=["Pakaian"],
    dependencies=[Depends(auth.get_current_user)]
)


class ImageUploadRequest(schemas.BaseModel):
    file_name: str
    content_type: str


@router.post("/", response_model=schemas.Pakaian, status_code=status.HTTP_201_CREATED)
def create_pakaian(
        pakaian: schemas.PakaianCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.Pakaian:
    """
    Membuat item pakaian baru untuk user yang sedang login.
    """
    logger.info(f"User {current_user.id} creating new clothing: {pakaian.nama_pakaian}")
    return crud.create_user_pakaian(db=db, pakaian=pakaian, user_id=current_user.id)


@router.get("/", response_model=List[schemas.Pakaian])
def read_pakaian(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> List[models.Pakaian]:
    """
    Mengambil daftar semua pakaian (non-soft-delete)
    milik user yang sedang login.

    Pre-signed URL untuk foto akan di-generate jika ada.
    """
    logger.info(f"User {current_user.id} fetching all clothing.")
    pakaian_list = crud.get_pakaian_by_user(db, user_id=current_user.id)

    for pakaian in pakaian_list:
        if pakaian.foto_url:
            pakaian.foto_url = minio_client.get_presigned_url(pakaian.foto_url)
    return pakaian_list


@router.get("/{pakaian_id}", response_model=schemas.Pakaian)
def read_single_pakaian(
        pakaian_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.Pakaian:
    """
    Mengambil detail satu item pakaian berdasarkan ID.

    Memastikan pakaian tersebut milik user yang sedang login.
    Pre-signed URL untuk foto akan di-generate jika ada.
    """
    logger.info(f"User {current_user.id} fetching clothing ID: {pakaian_id}")

    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)

    _validate_pakaian_ownership(db_pakaian, current_user.id)

    if db_pakaian.foto_url:
        db_pakaian.foto_url = minio_client.get_presigned_url(db_pakaian.foto_url)

    return db_pakaian


@router.put("/{pakaian_id}", response_model=schemas.Pakaian)
def update_single_pakaian(
        pakaian_id: int,
        pakaian_update: schemas.PakaianUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.Pakaian:
    """
    Mengubah detail item pakaian (data teks saja, bukan foto).

    Memastikan pakaian tersebut milik user yang sedang login.
    """
    logger.info(f"User {current_user.id} updating clothing ID: {pakaian_id}")

    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)

    _validate_pakaian_ownership(db_pakaian, current_user.id)

    return crud.update_pakaian(db=db, db_pakaian=db_pakaian, pakaian_update=pakaian_update)


@router.delete("/{pakaian_id}", status_code=status.HTTP_200_OK)
def soft_delete_single_pakaian(
        pakaian_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> dict:
    """
    Menghapus (soft delete) item pakaian.

    Memastikan pakaian tersebut milik user dan tidak sedang dalam sesi laundry aktif.
    """
    logger.info(f"User {current_user.id} attempting soft delete clothing ID: {pakaian_id}")

    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)

    _validate_pakaian_ownership(db_pakaian, current_user.id)

    sesi_aktif = db.query(models.SesiLaundry).join(models.SesiLaundry.item_pakaian).filter(
        models.SesiLaundry.pemilik_id == current_user.id,
        models.Pakaian.id == pakaian_id,
        models.SesiLaundry.status != "Selesai",
        models.SesiLaundry.status != "Diambil"
    ).first()

    if sesi_aktif:
        logger.warning(f"Delete failed: Clothing {pakaian_id} is in active session {sesi_aktif.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete clothing that is in an active laundry session."
        )

    logger.info(f"Soft deleting clothing ID: {pakaian_id}")
    return crud.soft_delete_pakaian(db=db, db_pakaian=db_pakaian)


@router.post("/{pakaian_id}/image-upload-url", response_model=schemas.PresignedUrl)
async def generate_upload_url(
        pakaian_id: int,
        upload_data: ImageUploadRequest,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> dict:
    """
    Generate pre-signed URL S3/MinIO untuk upload foto pakaian.

    Endpoint ini akan menyimpan object_name (path file) ke DB
    sebelum mengembalikan URL untuk di-upload oleh client.
    """
    logger.info(f"User {current_user.id} requesting upload URL for clothing ID: {pakaian_id}")

    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)

    _validate_pakaian_ownership(db_pakaian, current_user.id)

    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if upload_data.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only image files (JPEG, PNG, GIF) are allowed")

    file_extension = upload_data.file_name.split(".")[-1]
    object_name = f"clothing_images/{current_user.id}/{pakaian_id}_{datetime.now().timestamp()}.{file_extension}"

    presigned_url_data = minio_client.create_presigned_upload_url(object_name=object_name)

    if not crud.update_pakaian_foto_url(db, pakaian_id, object_name):
        raise HTTPException(status_code=500, detail="Failed to update clothing photo URL in DB")

    return {"url": presigned_url_data['url'], "fields": presigned_url_data['fields']}

def _validate_pakaian_ownership(
        db_pakaian: models.Pakaian,
        user_id: int
):
    """
    Helper untuk validasi kepemilikan pakaian.
    Melempar HTTPException 404 jika pakaian tidak ada atau bukan milik user.
    """
    if db_pakaian is None:
        logger.warning(f"Pakaian not found (User: {user_id})")
        raise HTTPException(status_code=404, detail="Pakaian not found")

    if db_pakaian.pemilik_id != user_id:
        logger.warning(f"User {user_id} tried to access unauthorized clothing {db_pakaian.id}")
        raise HTTPException(status_code=404, detail="Pakaian not found")
