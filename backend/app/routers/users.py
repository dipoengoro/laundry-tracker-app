import logging
import os
import textwrap
from datetime import datetime
from ftplib import all_errors

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
from app import schemas, crud, database, models, auth, hashing, email_utils, minio_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user.email}")

    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user_by_email:
        logger.warning(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = crud.create_user(db=db, user=user)
    logger.info(f"User registered successfully: {new_user.email}")
    return new_user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {form_data.username}")

    user = crud.get_user_by_email(db, email=form_data.username)

    if not user:
        logger.warning(f"Login failed: User not found - {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, )

    if not hashing.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid password for user - {form_data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, )

    access_token = auth.create_access_token(data={"sub": str(user.id)})

    logger.info(f"Login successful for user: {user.email}")

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """
    Mengambil data user yang sedang login.
    """
    logger.info(f"User info requested: {current_user.email}")

    if current_user.foto_profil_url:
        current_user.foto_profil_url = minio_client.get_presigned_url(
            current_user.foto_profil_url
        )
    return current_user


@router.post("/me/image-upload-url", response_model=schemas.PresignedUrl)
async def generate_profile_upload_url(
        upload_data: schemas.ImageUploadRequest,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user),
):
    """Generate a pre-signed URL for uploading a profile image."""
    logger.info(f"Profile image upload URL requested for user: {current_user.email}")

    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if upload_data.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only image files (JPEG, PNG, GIF) are allowed"
        )
    file_extension = upload_data.file_name.split(".")[-1]
    object_name = f"user_images/{current_user.id}_{datetime.now().timestamp()}.{file_extension}"

    presigned_url_data = minio_client.create_presigned_upload_url(
        object_name=object_name
    )
    current_user.foto_profil_url = object_name
    db.commit()
    logger.info(f"Generated upload URL for {object_name}")
    return {"url": presigned_url_data['url'], "fields": presigned_url_data['fields']}
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(database.get_db)):
    logger.info(f"Password reset requested for: {request.email}")

    user = crud.get_user_by_email(db, email=request.email)
    if user:
        token = crud.create_reset_token(db, email=user.email)

        email_body = textwrap.dedent(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <p>Halo {user.username},</p>
                <p>Anda menerima email ini karena ada permintaan untuk mereset password akun Anda.</p>
                <p>Gunakan token berikut untuk mereset password Anda:</p>
                <h3 style="font-family: monospace;">{token}</h3>
                <p>Jika Anda tidak merasa melakukan permintaan ini, abaikan saja email ini.</p>
            </body>
        </html>
        """)

        try:
            await email_utils.send_email(subject="Reset Password Akun Laundry Tracker", recipient=user.email,
                body=email_body)
            logger.info(f"Password reset email sent to: {user.email}")
        except Exception as e:
            logger.error(f"Failed to send reset email: {e}")

    return {"message": "If an account with that email exists, we sent you a passwordr reset token."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    logger.info("Password reset attempt with token")

    user = crud.reset_user_password(db, token_str=request.token, new_password=request.new_password)

    if not user:
        logger.warning("Password reset failed: Invalid or expired token")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    logger.info(f"Password reset successful for user: {user.email}")
    return {"message": "Password has been reset successfully."}


@router.put("/me", response_model=schemas.UserOut)
def update_current_user(
        user_update: schemas.UserUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"User update for: {current_user.email}")

    if user_update.email:
        existing_user = db.query(models.User).filter(models.User.email == user_update.email,
                                                     models.User.id != current_user.id).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use by another account")

        current_user.email = user_update.email

    if current_user.foto_profil_url:
        current_user.foto_profil_url = minio_client.get_presigned_url(
            current_user.foto_profil_url
        )

    db.commit()
    db.refresh(current_user)
    logger.info(f"User updated successfully: {current_user.email}")
    return current_user


@router.post("/logout")
def logout(current_user: models.User = Depends(auth.get_current_user)):
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}
