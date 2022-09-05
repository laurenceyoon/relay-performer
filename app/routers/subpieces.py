from http import HTTPStatus

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..core.helpers import play_piece_to_outport
from ..database import get_db
from ..redis import redis_client

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
    subpiece_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db), speed: float = 1
):
    redis_client.set("speed", speed)
    db_subpiece = crud.get_subpiece(db, subpiece_id)
    background_tasks.add_task(play_piece_to_outport, piece=db_subpiece)
    return {"response": f"playing title({db_subpiece}) on the background"}

@router.get("/", response_model=list[schemas.SubPiece])
def read_subpieces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subpieces(db, skip=skip, limit=limit)


@router.get(
    "/{subpiece_id}", response_model=schemas.SubPiece
)
def read_subpiece(subpiece_id: int, db: Session = Depends(get_db)):
    return crud.get_subpiece(db, subpiece_id=subpiece_id)
