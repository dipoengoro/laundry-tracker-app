from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    foto_profil_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None

class PakaianBase(BaseModel):
    nama_pakaian: str
    kategori: str | None = None
    jenis_pakaian: str | None = None
    warna: str | None = None
    bahan: str | None = None
    petunjuk_pencucian: str | None = None
    mudah_luntur: bool = False
    foto_url: str | None = None

class PakaianCreate(PakaianBase):
    pass

class Pakaian(PakaianBase):
    id: int
    pemilik_id: int

    class Config:
        from_attributes = True

class SesiLaundryCreate(BaseModel):
    item_pakaian_ids: list[int]

class SesiLaundry(BaseModel):
    id: int
    status: str
    tanggal_masuk: datetime
    estimasi_selesai: datetime | None = None
    item_pakaian: list[Pakaian]

    class Config:
        from_attributes = True


class PakaianUpdate(PakaianBase):
    pass

class StatusLaundry(str, Enum):
    diterima = "Diterima"
    dicuci = "Dicuci"
    dikeringkan = "Dikeringkan"
    disetrika = "Disetrika"
    selesai = "Selesai"
    diambil = "Diambil"

class SesiLaundryUpdateStatus(BaseModel):
    status: StatusLaundry

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PresignedUrl(BaseModel):
    url: str
    fields: dict

class UserUpdate(BaseModel):
    email: EmailStr | None = None