import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, auth, database, minio_client

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(auth.get_current_admin_user)]
)


@router.patch(
    "/user/{user_id}/make-admin",
    response_model=schemas.UserOut
)
def make_user_admin(
        user_id: int,
        db: Session = Depends(database.get_db)
) -> schemas.UserOut:
    """
    Promotes a regular user to be an admin user.
    """
    logger.warning(f"Admin action: Attempting to make User {user_id} an admin.")

    db_user = crud.get_user_by_id(db, user_id=user_id)

    if db_user is None:
        logger.error(f"Admin action failed: User {user_id} not found.")
        raise HTTPException(status=404, detail="User not found")

    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)

    logger.info(f"Admin action successful: User {user_id} is now an admin.")

    if db_user.profile_photo_url:
        db_user.profile_photo_url = minio_client.get_presigned_url(db_user.profile_photo_url)

    return db_user
