import os
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, auth, models, database, minio_client
from datetime import datetime

router = APIRouter(
    prefix="/pakaian",
    tags=["Pakaian"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.Pakaian, status_code=status.HTTP_201_CREATED)
def create_pakaian(
    pakaian: schemas.PakaianCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Membuat item pakaian baru untuk user yang sedang login."""
    return crud.create_user_pakaian(db=db, pakaian=pakaian, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Pakaian])
def read_pakaian(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengambil daftar semua pakaian milik user yang sedang login."""
    pakaian_list = crud.get_pakaian_by_user(db, user_id=current_user.id)
    for pakaian in pakaian_list:
        if pakaian.foto_url:
            pakaian.foto_url = minio_client.get_presigned_url(pakaian.foto_url)
    return pakaian_list

@router.get("/{pakaian_id}", response_model=schemas.Pakaian)
def read_single_pakaian(
    pakaian_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengambil detail satu item pakaian"""
    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian is None:
        raise HTTPException(status_code=404, detail="Pakaian not found")
    
    # Pemeriksaan keamanan: Pastikan pakaian ini milik user yang sedang login
    if db_pakaian.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pakaian not found")
    
    if db_pakaian.foto_url:
        db_pakaian.foto_url = minio_client.get_presigned_url(db_pakaian.foto_url)
    
    return db_pakaian

@router.put("/{pakaian_id}", response_model=schemas.Pakaian)
def update_single_pakaian(
    pakaian_id: int,
    pakaian_update: schemas.PakaianUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengubah detail item pakaian."""
    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian is None or db_pakaian.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pakaian not found")
    
    return crud.update_pakaian(db=db, db_pakaian=db_pakaian, pakaian_update=pakaian_update)

@router.delete("/{pakaian_id}", status_code=status.HTTP_200_OK)
def soft_delete_single_pakaian(
    pakaian_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Menghapus item pakaian."""
    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian is None or db_pakaian.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pakaian not found")
    
    sesi_aktif = db.query(models.SesiLaundry).join(models.SesiLaundry.item_pakaian).filter(
        models.SesiLaundry.pemilik_id == current_user.id,
        models.Pakaian.id == pakaian_id,
        models.SesiLaundry.status != "Selesai",
        models.SesiLaundry.status != "Diambil"
    ).first()

    if sesi_aktif:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete clothing that is in an active laundry session."
        )
    
    return crud.soft_delete_pakaian(db=db, db_pakaian=db_pakaian)

class PakaianImageUpload(schemas.BaseModel):
    file_name: str
    content_type: str

@router.post("/{pakaian_id}/image-upload-url", response_model=schemas.PresignedUrl)
async def generate_upload_url(
    pakaian_id: int,
    upload_data: PakaianImageUpload,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Generate a pre-signed URL for uploading an image."""
    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian is None or db_pakaian.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pakaian not found")

    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if upload_data.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only image files (JPEG, PNG, GIF) are allowed"
        )

    file_extension = upload_data.file_name.split(".")[-1]
    object_name = f"clothing_images/{current_user.id}/{pakaian_id}_{datetime.now().timestamp()}.{file_extension}"

    presigned_url_data = minio_client.create_presigned_upload_url(object_name=object_name)

    db_pakaian.foto_url = object_name
    db.commit()

    return {"url": presigned_url_data['url'], "fields": presigned_url_data['fields']}