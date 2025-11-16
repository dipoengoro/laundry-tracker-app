import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from sqlalchemy.orm import Session

from app import models, schemas, hashing


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user and saves it to the database.

    Performs password hashing before saving.

    Args:
        db (Session): The active SQLAlchemy database session.
        user (schemas.UserCreate): Pydantic schema with new user data.

    Returns:
        models.User: The newly created User SQLAlchemy model object.
    """
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


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Gets a single user from the database by their email.

    Args:
        db (Session): The SQLAlchemy database session.
        email (str): The user's email to search for.

    Returns:
        Optional[models.User]: The User object if found, else None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: int) -> Optional[models.User]:
    """
    Gets a single user from the database by their ID.

    Args:
        db (Session): The SQLAlchemy database session.
        id (int): The user's ID to search for.

    Returns:
        Optional[models.User]: The User object if found, else None.
    """
    return db.query(models.User).filter(models.User.id == id).first()


def get_clothing_items_by_user(db: Session, user_id: int) -> List[models.ClothingItem]:
    """
    Gets all (non-soft-deleted) clothing items for a specific user.

    Args:
        db (Session): The SQLAlchemy database session.
        user_id (int): The ID of the user who owns the items.

    Returns:
        List[models.ClothingItem]: A list of ClothingItem objects (can be empty).
    """
    return db.query(models.ClothingItem).filter(
        models.ClothingItem.owner_id == user_id,
        models.ClothingItem.deleted_at == None
    ).all()


def create_user_clothing_item(
        db: Session,
        clothing_item: schemas.ClothingItemCreate,
        user_id: int
) -> models.ClothingItem:
    """
    Creates a new clothing item for a specific user.

    Args:
        db (Session): The SQLAlchemy database session.
        clothing_item (schemas.ClothingItemCreate): Schema with the new clothing data.
        user_id (int): The ID of the owner user.

    Returns:
        models.ClothingItem: The newly created ClothingItem object.
    """
    db_clothing_item = models.ClothingItem(**clothing_item.model_dump(), owner_id=user_id)

    db.add(db_clothing_item)
    db.commit()
    db.refresh(db_clothing_item)
    return db_clothing_item


def get_clothing_item_by_id(db: Session, clothing_item_id: int) -> Optional[models.ClothingItem]:
    """
    Gets a single (non-soft-deleted) clothing item by its ID.

    Args:
        db (Session): The SQLAlchemy database session.
        clothing_item_id (int): The ID of the clothing item.

    Returns:
        Optional[models.ClothingItem]: The ClothingItem object if found, else None.
    """
    return db.query(models.ClothingItem).filter(
        models.ClothingItem.id == clothing_item_id,
        models.ClothingItem.deleted_at == None
    ).first()


def update_clothing_item(
        db: Session,
        db_clothing_item: models.ClothingItem,
        clothing_item_update: schemas.ClothingItemUpdate
) -> models.ClothingItem:
    """
    Updates data for a clothing item in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        db_clothing_item (models.ClothingItem): The SQLAlchemy model object to update.
        clothing_update (schemas.ClothingItemUpdate): Schema with the new data.

    Returns:
        models.ClothingItem: The updated ClothingItem object.
    """
    # Ambil data dari skema sebagai dictionary
    update_data = clothing_item_update.model_dump(exclude_unset=True)

    # Loop melalui data dan update field di objek SQLAlchemy
    for key, value in update_data.items():
        setattr(db_clothing_item, key, value)

    db.add(db_clothing_item)
    db.commit()
    db.refresh(db_clothing_item)
    return db_clothing_item


def soft_delete_clothing_item(
        db: Session,
        db_clothing_item: models.ClothingItem
) -> dict:
    """
    Soft deletes a clothing item by setting its 'deleted_at' timestamp.

    Args:
        db (Session): The SQLAlchemy database session.
        db_clothing_item (models.ClothingItem): The model object to soft delete.

    Returns:
        dict: A confirmation message.
    """
    db_clothing_item.deleted_at = datetime.now(timezone.utc)
    db.add(db_clothing_item)
    db.commit()
    return {"message": "Clothing item successfully moved to trash"}


def update_clothing_item_photo_url(
        db: Session,
        clothing_item_id: int,
        photo_url: str
) -> Optional[models.ClothingItem]:
    """
    Updates the photo_url (MinIO object name) for a specific clothing item.

    Called after generating a pre-signed URL to save the object path.

    Args:
        db (Session): The SQLAlchemy database session.
        clothing_item_id (int): The ID of the clothing item to update.
        photo_url (str): The new object name (path) to save.

    Returns:
        Optional[models.ClothingItem]: The updated ClothingItem, or None if not found.
    """
    db_clothing_item = get_clothing_item_by_id(db, clothing_item_id=clothing_item_id)

    if db_clothing_item:
        db_clothing_item.photo_url = photo_url
        db.add(db_clothing_item)
        db.commit()
        db.refresh(db_clothing_item)

    return db_clothing_item


def create_laundry_session(
        db: Session,
        user_id: int,
        session_data: schemas.LaundrySessionCreate
) -> Optional[models.LaundrySession]:
    """
    Creates a new laundry session for a user.

    Validation fails (returns None) if any clothing item IDs
    are not found or do not belong to the user.

    Args:
        db (Session): The SQLAlchemy database session.
        user_id (int): The ID of the session owner.
        session_data (schemas.LaundrySessionCreate): Schema containing the list of clothing item IDs.

    Returns:
        Optional[models.LaundrySession]: The new LaundrySession object, or None if validation fails.
    """
    # 1. Buat objek LaundrySession utama
    db_session = models.LaundrySession(owner_id=user_id)
    db.add(db_session)

    # 2. Ambil objek Pakaian dari DB berdasarkan ID dan pastikan milik user
    clothing_items = db.query(models.ClothingItem).filter(
        models.ClothingItem.id.in_(session_data.clothing_item_ids),
        models.ClothingItem.owner_id == user_id
    ).all()

    # Validasi jika ada ID pakaian yang tidak valid atau bukan milik user
    if len(clothing_items) != len(session_data.clothing_item_ids):
        db.rollback()
        return None

    # 3. Tambahkan pakaian ke sesi laundry
    db_session.clothing_items.extend(clothing_items)

    # 4. Simpan semua perubahan ke database
    db.commit()
    db.refresh(db_session)
    return db_session


def get_laundry_sessions_by_user(
        db: Session,
        user_id: int
) -> List[models.LaundrySession]:
    """
    Gets all laundry sessions for a specific user.

    Args:
        db (Session): The SQLAlchemy database session.
        user_id (int): The ID of the session owner.

    Returns:
        List[models.LaundrySession]: A list of LaundrySession objects.
    """
    return db.query(models.LaundrySession).filter(models.LaundrySession.owner_id == user_id).all()


def get_laundry_session_by_id(
        db: Session,
        session_id: int
) -> Optional[models.LaundrySession]:
    """
    Gets a single laundry session by its ID.

    Args:
        db (Session): The SQLAlchemy database session.
        session_id (int): The ID of the laundry session.

    Returns:
        Optional[models.LaundrySession]: The LaundrySession object if found, else None.
    """
    return db.query(models.LaundrySession).filter(models.LaundrySession.id == session_id).first()


def update_laundry_status(
        db: Session,
        db_session: models.LaundrySession,
        new_status: schemas.LaundryStatus
) -> models.LaundrySession:
    """
    Updates the status of a laundry session.

    Args:
        db (Session): The SQLAlchemy database session.
        db_session (models.LaundrySession): The session object to update.
        new_status (schemas.LaundryStatus): The new status enum value.

    Returns:
        models.LaundrySession: The updated LaundrySession object.
    """
    db_session.status = new_status.value
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def create_reset_token(db: Session, email: str) -> str:
    """
    Creates a new password reset token, invalidating any old ones.

    Args:
        db (Session): The SQLAlchemy database session.
        email (str): The user's email requesting the reset.

    Returns:
        str: A unique, secure token string.
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
    Resets a user's password using a valid token.

    Args:
        db (Session): The SQLAlchemy database session.
        token_str (str): The reset token provided by the user.
        new_password (str): The new plain-text password.

    Returns:
        Optional[models.User]: The User object if successful, else None.
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