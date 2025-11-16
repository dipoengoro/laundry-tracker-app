from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_photo_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class ClothingItemBase(BaseModel):
    name: str
    category: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None
    washing_instructions: Optional[str] = None
    fades_easily: bool = False
    photo_url: str | None = None

class ClothingItemCreate(ClothingItemBase):
    pass

class ClothingItem(ClothingItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class LaundrySessionCreate(BaseModel):
    clothing_item_ids: List[int]

class LaundrySession(BaseModel):
    id: int
    status: str
    date_received: datetime
    estimated_completion: Optional[datetime] = None
    clothing_items: List[ClothingItem] = []

    class Config:
        from_attributes = True


class ClothingItemUpdate(ClothingItemBase):
    pass

class LaundryStatus(str, Enum):
    received = "Received"
    washing = "Washing"
    drying = "Drying"
    ironing = "Ironing"
    completed = "Completed"
    taken = "Taken"

class LaundrySessionUpdateStatus(BaseModel):
    status: LaundryStatus

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PresignedUrl(BaseModel):
    url: str
    fields: dict

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class ImageUploadRequest(BaseModel):
    file_name: str
    content_type: str