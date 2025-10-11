from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, auth, models, database

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(auth.get_current_admin_user)]
)

@router.patch("/user/{user_id}/make-admin", response_model=schemas.UserOut)
def make_user_admin(user_id: int, db: Session = Depends(database.get_db)):
    """Menjadikan seorang user sebagai admin."""
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status=404, detail="User not found")
    
    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)
    return db_user