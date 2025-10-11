from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    foto_profil_url = Column(String, nullable=True)
    pakaian = relationship("Pakaian", back_populates="pemilik")
    sesi_laundry = relationship("SesiLaundry")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Pakaian(Base):
    __tablename__ = "pakaian"

    id = Column(Integer, primary_key=True, index=True)
    nama_pakaian = Column(String, index=True, nullable=False)
    kategori = Column(String)
    jenis_pakaian = Column(String)
    warna = Column(String)
    bahan = Column(String)
    petunjuk_pencucian = Column(String)
    mudah_luntur = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    pemilik_id = Column(Integer, ForeignKey("users.id"))
    foto_url = Column(String, nullable=True)
    pemilik = relationship("User", back_populates="pakaian")
    pass

detail_sesi_laundry = Table('detail_sesi_laundry', Base.metadata, Column('sesi_id', Integer, ForeignKey('sesi_laundry.id'), primary_key=True), Column('pakaian_id', Integer, ForeignKey('pakaian.id'), primary_key=True))

class SesiLaundry(Base):
    __tablename__ = "sesi_laundry"

    id = Column(Integer, primary_key=True, index=True)
    tanggal_masuk = Column(DateTime(timezone=True), server_default=func.now())
    estimasi_selesai = Column(DateTime(timezone=True))
    status = Column(String, default="Diterima")
    pemilik_id = Column(Integer, ForeignKey("users.id"))

    item_pakaian = relationship("Pakaian", secondary=detail_sesi_laundry)

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    email = Column(String, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)