import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, auth, models, database

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/laundry-sessions",
    tags=["Laundry Sessions"],
    dependencies=[Depends(auth.get_current_user)]
)


@router.post(
    "/",
    response_model=schemas.LaundrySession,
    status_code=status.HTTP_201_CREATED
)
def create_new_laundry_session(
        session_data: schemas.LaundrySessionCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.LaundrySession:
    """
    Creates a new laundry session for the logged-in user.
    Validates that all submitted clothing items exist and belong to the user.
    """
    logger.info(
        f"User {current_user.id} creating new laundry session with {len(session_data.clothing_item_ids)} items."
    )

    new_session = crud.create_laundry_session(
        db=db, user_id=current_user.id, session_data=session_data
    )

    if new_session is None:
        logger.warning(
            f"Failed session creation for user {current_user.id}: Invalid clothing items."
        )
        raise HTTPException(
            status_code=404,
            detail="One or more clothing items not found or do not belong to the user."
        )

    logger.info(
        f"Session {new_session.id} created successfully for User {current_user.id}."
    )
    return new_session


@router.get(
    "/",
    response_model=List[schemas.LaundrySession]
)
def read_user_laundry_session(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> List[models.LaundrySession]:
    """
    Retrieves the history of all laundry sessions for the logged-in user.
    """
    logger.info(f"User {current_user.id} fetching their laundry sessions.")
    return crud.get_laundry_sessions_by_user(db=db, user_id=current_user.id)


@router.put(
    "/{session_id}/status",
    response_model=schemas.LaundrySession
)
def update_laundry_session_status(
        session_id: int,
        status_update: schemas.LaundrySessionUpdateStatus,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_user)
) -> models.LaundrySession:
    """
    Updates the status of a specific laundry session.
    Ensures the session belongs to the logged-in user.
    """
    logger.info(
        f"User {current_user.id} updating status for session {session_id} to '{status_update.status.value}'."
    )
    db_session = crud.get_laundry_session_by_id(db, session_id=session_id)

    if db_session is None or db_session.owner_id != current_user.id:
        logger.warning(f"User {current_user.id} failed to update session {session_id}: Not found or unauthorized.")
        raise HTTPException(status_code=404, detail="Laundry session not found")

    updated_session = crud.update_laundry_status(
        db=db, db_session=db_session, new_status=status_update.status
    )
    return updated_session
