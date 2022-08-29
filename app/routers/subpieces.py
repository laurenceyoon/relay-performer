from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..core.helpers import play_piece_to_outport, start_interactive_performance

router = APIRouter(
    prefix="/subpieces",
    tags=["subpieces"],
    responses={404: {"description": "Not found"}},
)

@router.patch(
    "/{subpiece_id}/play",
    status_code=HTTPStatus.ACCEPTED,
    tags=["Interactive API"],
)
def play_subpiece(
    subpiece_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    db_subpiece = crud.get_subpiece(db, subpiece_id)
    background_tasks.add_task(play_piece_to_outport, piece=db_subpiece)
    return {"response": f"playing title({db_subpiece}) on the background"}

@router.get("/", response_model=List[schemas.SubPiece])
def read_subpieces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subpieces(db, skip=skip, limit=limit)


@router.get(
    "/subpieces/{subpiece_id}", response_model=schemas.SubPiece
)
def read_subpiece(subpiece_id: int, db: Session = Depends(get_db)):
    return crud.get_subpiece(db, subpiece_id=subpiece_id)

