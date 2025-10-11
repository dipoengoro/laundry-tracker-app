import os
import shutil
import textwrap
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app import schemas, crud, database, models, auth, hashing, email_utils
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = crud.create_user(db=db, user=user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)

    if not user or not hashing.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": str(user.id)}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """
    Mengambil data user yang sedang login.
    """
    return current_user


@router.put("/me/picture", response_model=schemas.UserOut)
def update_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengunggah dan mengubah foto profil user."""
    IMAGE_DIR = "static/images/"

    os.makedirs(IMAGE_DIR, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"{current_user.id}_{datetime.now().timestamp()}.{file_extension}"
    file_path = os.path.join(IMAGE_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    public_url = f"/static/images/{file_name}"
    current_user.foto_profil_url = public_url
    db.commit()
    db.refresh(current_user)

    return current_user

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: schemas.ForgotPasswordRequest,
    db: Session = Depends(database.get_db)
):
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

        await email_utils.send_email(
            subject="Reset Password Akun Laundry Tracker",
            recipient=user.email,
            body=email_body
        )
    return {"message": "If an account with that email exists, we sent you a passwordr reset token."}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    request: schemas.ResetPasswordRequest,
    db: Session = Depends(database.get_db)
):
    user = crud.reset_user_password(db, token_str=request.token, new_password=request.new_password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    return {"message": "Password has been reset successfully."}

@router.put("/me", response_model=schemas.UserOut)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if user_update.email:
        current_user.email = user_update.email

    db.commit()
    db.refresh(current_user)
    return current_user