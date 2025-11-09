import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from sqlalchemy.orm import Session

from app import models, schemas, hashing


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Membuat user baru dan menyimpannya ke database.

    Melakukan hashing password sebelum menyimpan ke database.

    Args:
        db (Session): Sesi database SQLAlchemy yang aktif.
        user (schemas.UserCreate): Skema Pydantic berisi data user baru.

    Returns:
        models.User: Objek user SQLAlchemy (model) yang baru dibuat.
    """
    hashed_password = hashing.get_password_hash(user.password)

    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Mengambil satu user dari database berdasarkan email.

    Args:
        db (Session): Sesi database SQLAlchemy.
        email (str): Email user yang dicari.

    Returns:
        Optional[models.User]: Objek user jika ditemukan, None jika tidak.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: int) -> Optional[models.User]:
    """
    Mengambil satu user dari database berdasarkan ID.

    Args:
        db (Session): Sesi database SQLAlchemy.
        id (int): ID user yang dicari.

    Returns:
        Optional[models.User]: Objek user jika ditemukan, None jika tidak.
    """
    return db.query(models.User).filter(models.User.id == id).first()


def get_pakaian_by_user(db: Session, user_id: int) -> List[models.Pakaian]:
    """
    Mengambil semua pakaian (yang tidak di-soft-delete) milik satu user.

    Args:
        db (Session): Sesi database SQLAlchemy.
        user_id (int): ID user pemilik pakaian.

    Returns:
        List[models.Pakaian]: Daftar objek pakaian milik user (bisa kosong).
    """
    return db.query(models.Pakaian).filter(models.Pakaian.pemilik_id == user_id,
                                           models.Pakaian.deleted_at == None).all()


def create_user_pakaian(db: Session, pakaian: schemas.PakaianCreate, user_id: int) -> models.Pakaian:
    """
    Membuat item pakaian baru untuk seorang user.

    Args:
        db (Session): Sesi database SQLAlchemy.
        pakaian (schemas.PakaianCreate): Skema data pakaian baru.
        user_id (int): ID user pemilik.

    Returns:
        models.Pakaian: Objek pakaian yang baru dibuat.
    """
    db_pakaian = models.Pakaian(**pakaian.model_dump(), pemilik_id=user_id)

    db.add(db_pakaian)
    db.commit()
    db.refresh(db_pakaian)
    return db_pakaian


def create_laundry_session(db: Session, user_id: int, session_data: schemas.SesiLaundryCreate) -> Optional[
    models.SesiLaundry]:
    """
    Membuat sesi laundry baru untuk seorang user.

    Validasi akan gagal (return None) jika salah satu ID pakaian tidak ditemukan atau bukan milik user.

    Args:
        db (Session): Sesi database SQLAlchemy.
        user_id (int): ID user pemilik sesi.
        session_data (schemas.SesiLaundryCreate): Skema berisi list ID pakaian.

    Returns:
        Optional[models.SesiLaundry]: Objek sesi laundry jika berhasil, None jika gagal validasi.
    """
    # 1. Buat objek SesiLaundry utama
    db_session = models.SesiLaundry(pemilik_id=user_id)
    db.add(db_session)

    # 2. Ambil objek Pakaian dari DB berdasarkan ID dan pastikan milik user
    pakaian_objects = db.query(models.Pakaian).filter(models.Pakaian.id.in_(session_data.item_pakaian_ids),
        models.Pakaian.pemilik_id == user_id).all()

    # Validasi jika ada ID pakaian yang tidak valid atau bukan milik user
    if len(pakaian_objects) != len(session_data.item_pakaian_ids):
        db.rollback()
        return None

    # 3. Tambahkan pakaian ke sesi laundry
    db_session.item_pakaian.extend(pakaian_objects)

    # 4. Simpan semua perubahan ke database
    db.commit()
    db.refresh(db_session)
    return db_session


def get_laundry_sessions_by_user(db: Session, user_id: int) -> List[models.SesiLaundry]:
    """
    Mengambil semua sesi laundry milik satu user.

    Args:
        db (Session): Sesi database SQLAlchemy.
        user_id (int): ID user pemilik sesi.

    Returns:
        List[models.SesiLaundry]: Daftar objek sesi laundry.
    """
    return db.query(models.SesiLaundry).filter(models.SesiLaundry.pemilik_id == user_id).all()


def get_pakaian_by_id(db: Session, pakaian_id: int) -> Optional[models.Pakaian]:
    """
    Mengambil satu item pakaian (non-soft-delete) berdasarkan ID-nya.

    Args:
        db (Session): Sesi database SQLAlchemy.
        pakaian_id (int): ID item pakaian yang dicari.

    Returns:
        Optional[models.Pakaian]: Objek pakaian jika ditemukan, None jika tidak.
    """
    return db.query(models.Pakaian).filter(models.Pakaian.id == pakaian_id, models.Pakaian.deleted_at == None).first()


def update_pakaian(db: Session, db_pakaian: models.Pakaian, pakaian_update: schemas.PakaianUpdate) -> models.Pakaian:
    """
    Meng-update data item pakaian yang ada di database.

    Args:
        db (Session): Sesi database SQLAlchemy.
        db_pakaian (models.Pakaian): Objek pakaian (model) yang ingin di-update.
        pakaian_update (schemas.PakaianUpdate): Skema data baru.

    Returns:
        models.Pakaian: Objek pakaian yang sudah di-update.
    """
    # Ambil data dari skema sebagai dictionary
    update_data = pakaian_update.model_dump(exclude_unset=True)

    # Loop melalui data dan update field di objek SQLAlchemy
    for key, value in update_data.items():
        setattr(db_pakaian, key, value)

    db.add(db_pakaian)
    db.commit()
    db.refresh(db_pakaian)
    return db_pakaian


def soft_delete_pakaian(db: Session, db_pakaian: models.Pakaian) -> dict:
    """
    Melakukan soft delete pada item pakaian dengan mengisi kolom 'deleted_at'.

    Args:
        db (Session): Sesi database SQLAlchemy.
        db_pakaian (models.Pakaian): Objek pakaian (model) yang ingin dihapus.

    Returns:
        dict: Pesan konfirmasi sukses.
    """
    db_pakaian.deleted_at = datetime.now(timezone.utc)
    db.add(db_pakaian)
    db.commit()
    return {"message": "Pakaian successfully moved to trash"}


def get_laundry_session_by_id(db: Session, session_id: int) -> Optional[models.SesiLaundry]:
    """
    Mengambil satu sesi laundry berdasarkan ID-nya.

    Args:
        db (Session): Sesi database SQLAlchemy.
        session_id (int): ID sesi laundry yang dicari.

    Returns:
        Optional[models.SesiLaundry]: Objek sesi laundry jika ditemukan, None jika tidak.
    """
    return db.query(models.SesiLaundry).filter(models.SesiLaundry.id == session_id).first()


def update_laundry_status(db: Session, db_session: models.SesiLaundry,
                          new_status: schemas.StatusLaundry) -> models.SesiLaundry:
    """
    Meng-update status dari sebuah sesi laundry.

    Args:
        db (Session): Sesi database SQLAlchemy.
        db_session (models.SesiLaundry): Objek sesi laundry yang ingin di-update.
        new_status (schemas.StatusLaundry): Enum status baru.

    Returns:
        models.SesiLaundry: Objek sesi laundry yang sudah di-update.
    """
    db_session.status = new_status.value
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def create_reset_token(db: Session, email: str) -> str:
    """
    Membuat token reset password baru, menghapus token lama jika ada.

    Args:
        db (Session): Sesi database SQLAlchemy.
        email (str): Email user yang me-request reset.

    Returns:
        str: String token unik yang aman.
    """
    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.email == email).delete()

    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=1)

    db_token = models.PasswordResetToken(email=email, token=token, expires_at=expires)
    db.add(db_token)
    db.commit()
    return token


def reset_user_password(db: Session, token_str: str, new_password: str) -> Optional[models.User]:
    """
    Me-reset password user menggunakan token yang valid.

    Args:
        db (Session): Sesi database SQLAlchemy.
        token_str (str): Token reset yang diterima user.
        new_password (str): Password baru (plain text).

    Returns:
        Optional[models.User]: Objek user jika berhasil, None jika token invalid/expired.
    """
    db_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token_str).first()

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


def update_pakaian_foto_url(db: Session, pakaian_id: int, foto_url: str) -> Optional[models.Pakaian]:
    """
    Meng-update path/object_name foto (foto_url) untuk item pakaian.

    Fungsi ini sebaiknya dipanggil setelah pre-signed URL dibuat,
    untuk menyimpan object_name (path file di MinIO) ke database.

    Args:
        db (Session): Sesi database SQLAlchemy.
        pakaian_id (int): ID pakaian yang ingin di-update.
        foto_url (str): Path/object_name baru yang akan disimpan.

    Returns:
        Optional[models.Pakaian]: Objek pakaian yang sudah di-update, None jika tidak ditemukan.
    """
    db_pakaian = get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian:
        db_pakaian.foto_url = foto_url
        db.add(db_pakaian)
        db.commit()
        db.refresh(db_pakaian)
    return db_pakaian
