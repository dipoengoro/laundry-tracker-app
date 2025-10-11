from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, auth, models, database

router = APIRouter(
    prefix="/laundry",
    tags=["Laundry"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.post("/", response_model=schemas.SesiLaundry, status_code=status.HTTP_201_CREATED)
def create_new_laundry_session(
    session_data: schemas.SesiLaundryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Membuat sesi laundry baru dengan menambahkan beberapa item pakaian."""
    new_session = crud.create_laundry_session(
        db=db, user_id=current_user.id, session_data=session_data
    )
    if new_session is None:
        raise HTTPException(
            status_code=404,
            detail="One or more clothing items not found or do not belong to the user."
        )
    return new_session

@router.get("/", response_model=List[schemas.SesiLaundry])
def read_user_laundry_session(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengambil riwayat semua sesi laundry milik user."""
    return crud.get_laundry_sessions_by_user(db=db, user_id=current_user.id)

@router.put("/{sesi_id}/status", response_model=schemas.SesiLaundry)
def update_laundry_session_status(
    sesi_id: int,
    status_update: schemas.SesiLaundryUpdateStatus,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Mengubah status dari sebuah laundry."""
    db_session = crud.get_laundry_session_by_id(db, session_id=sesi_id)

    if db_session is None or db_session.pemilik_id != current_user.id:
        raise HTTPException(status_code=404, detail="Laundry session not found")
    
    updated_session = crud.update_laundry_status(
        db=db, db_session=db_session, new_status=status_update.status
    )
    return updated_session