import secrets
from sqlalchemy.orm import Session
from app import models, schemas, hashing
from datetime import datetime, timezone, timedelta

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.get_password_hash(user.password)

    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_pakaian_by_user(db: Session, user_id: int):
    """Mengambil semua pakaian milik satu user."""
    return db.query(models.Pakaian).filter(
        models.Pakaian.pemilik_id == user_id,
        models.Pakaian.deleted_at == None
        ).all()

def create_user_pakaian(db: Session, pakaian: schemas.PakaianCreate, user_id: int):
    """Membuat item pakaian baru untuk seorang user."""
    db_pakaian = models.Pakaian(**pakaian.model_dump(), pemilik_id=user_id)

    db.add(db_pakaian)
    db.commit()
    db.refresh(db_pakaian)
    return db_pakaian

def create_laundry_session(db: Session, user_id: int, session_data: schemas.SesiLaundryCreate):
    """Membuat sesi laundry baru untuk seorang user."""
    # 1. Buat objek SesiLaundry utama
    db_session = models.SesiLaundry(pemilik_id=user_id)
    db.add(db_session)

    # 2. Ambil objek Pakaian dari DB berdasarkan ID dan pastikan milik user
    pakaian_objects = db.query(models.Pakaian).filter(
        models.Pakaian.id.in_(session_data.item_pakaian_ids),
        models.Pakaian.pemilik_id == user_id
    ).all()

    # Validasi jika ada ID pakaian yang tidak valid atau bukan milik user
    if len(pakaian_objects) != len(session_data.item_pakaian_ids):
        return None
    
    # 3. Tambahkan pakaian ke sesi laundry
    db_session.item_pakaian.extend(pakaian_objects)

    # 4. Simpan semua perubahan ke database
    db.commit()
    db.refresh(db_session)
    return db_session

def get_laundry_sessions_by_user(db: Session, user_id: int):
    """Mengambil semua sesi laundry milik satu user."""
    return db.query(models.SesiLaundry).filter(models.SesiLaundry.pemilik_id == user_id).all()


def get_pakaian_by_id(db: Session, pakaian_id: int):
    """Mengambil satu item pakaian berdasarkan ID-nya."""
    return db.query(models.Pakaian).filter(
        models.Pakaian.id == pakaian_id,
        models.Pakaian.deleted_at == None
        ).first()

def update_pakaian(db: Session, db_pakaian: models.Pakaian, pakaian_update: schemas.PakaianUpdate):
    """Meng-update data item pakaian."""
    # Ambil data dari skema sebagai dictionary
    update_data = pakaian_update.model_dump(exclude_unset=True)

    # Loop melalui data dan update field di objek SQLAlchemy
    for key, value in update_data.items():
        setattr(db_pakaian, key, value)

    db.add(db_pakaian)
    db.commit()
    db.refresh(db_pakaian)
    return db_pakaian

def soft_delete_pakaian(db: Session, db_pakaian: models.Pakaian):
    """Melakukan soft delete pada item pakaian."""
    db_pakaian.deleted_at = datetime.now(timezone.utc)
    db.add(db_pakaian)
    db.commit()
    return {"message": "Pakaian successfully moved to trash"}

def get_laundry_session_by_id(db: Session, session_id: int):
    """Mengambil satu sesi laundry berdasarkan ID-nya."""
    return db.query(models.SesiLaundry).filter(models.SesiLaundry.id == session_id).first()

def update_laundry_status(db: Session, db_session: models.SesiLaundry, new_status: schemas.StatusLaundry):
    """Meng-update status dari sebuah sesi laundry."""
    db_session.status = new_status.value
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def create_reset_token(db: Session, email: str) -> str:
    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.email == email).delete()

    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=1)

    db_token = models.PasswordResetToken(email=email, token=token, expires_at=expires)
    db.add(db_token)
    db.commit()
    return token

def reset_user_password(db: Session, token_str: str, new_password: str):
    db_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken == token_str).first()

    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        return None
    
    user = get_user_by_email(db, email=db_token.email)
    if not user:
        return None
    
    user.hashed_password = hashing.get_password_hash(new_password)
    db.add(user)

    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token_str).delete()

    db.commit()
    return user