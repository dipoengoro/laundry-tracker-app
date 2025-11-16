from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    profile_photo_url = Column(String, nullable=True)
    clothing_items = relationship("ClothingItem", back_populates="owner")
    laundry_sessions = relationship("LaundrySession")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String)
    type = Column(String)
    color = Column(String)
    material = Column(String)
    washing_instructions = Column(String)
    fades_easily = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    photo_url = Column(String, nullable=True)
    owner = relationship("User", back_populates="clothing_items")


laundry_session_details = Table(
    'laundry_session_details',
    Base.metadata,
    Column('session_id', Integer, ForeignKey('laundry_sessions.id'), primary_key=True),
    Column('clothing_item_id', Integer, ForeignKey('clothing_items.id'), primary_key=True)
)


class LaundrySession(Base):
    __tablename__ = "laundry_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date_received = Column(DateTime(timezone=True), server_default=func.now())
    estimated_completion = Column(DateTime(timezone=True))
    status = Column(String, default="Received")
    owner_id = Column(Integer, ForeignKey("users.id"))

    clothing_items = relationship("ClothingItem", secondary=laundry_session_details)


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    email = Column(String, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
