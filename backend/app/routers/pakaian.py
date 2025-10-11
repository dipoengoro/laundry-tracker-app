import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, auth, models, database
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

@router.post("/{pakaian_id}/image", response_model=schemas.Pakaian)
def upload_pakaian_image(
    pakaian_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengunggah gambar untuk item pakaian tertentu."""
    # 1. Ambil data pakaian dan validasi kepemilikan
    db_pakaian = crud.get_pakaian_by_id(db, pakaian_id=pakaian_id)
    if db_pakaian is None or db_pakaian.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pakaian not found")
    
    IMAGE_DIR = "static/images/pakaian/"
    os.makedirs(IMAGE_DIR, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    file_name = f"{pakaian_id}_{datetime.now().timestamp()}.{file_extension}"
    file_path = os.path.join(IMAGE_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    public_url = f"/{file_path}"
    db_pakaian.foto_url = public_url
    db.commit()
    db.refresh(db_pakaian)

    return db_pakaian