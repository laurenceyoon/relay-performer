from http import HTTPStatus

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..config import ADJUST_TEMPO
from ..core.helpers import play_piece_to_outport, start_relay_performance
from ..database import get_db
from ..redis import redis_client

router = APIRouter(
    prefix="/pieces",
    responses={404: {"description": "Not found"}},
)


@router.patch(
    "/{piece_id}/play", status_code=HTTPStatus.ACCEPTED, tags=["Interactive API"]
)
def play_piece(
    piece_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    speed: float = 1,
):
    if ADJUST_TEMPO:
        redis_client.set("speed", speed)
        print(f"~~~~~~~~~~~~~~~~~~~redis set speed to {speed}~~~~~~~~~~~~~~~~~~~")
    background_tasks.add_task(play_piece_to_outport, piece_id=piece_id, db=db)
    return {"response": f"playing title({piece_id}) on the background"}


@router.patch(
    "/{piece_id}/relay-perform",
    status_code=HTTPStatus.ACCEPTED,
    tags=["Interactive API"],
)
def relay_perform_piece(
    piece_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    start_from=1,
    force=True,
):
    background_tasks.add_task(
        start_relay_performance,
        piece_id=piece_id,
        db=db,
        start_from=int(start_from),
        force=force,
    )
    return {"response": f"following title({piece_id})"}


@router.post("/{piece_id}/subpieces/", response_model=schemas.SubPiece, tags=["pieces"])
def create_subpiece_by_piece(
    piece_id: int, subpiece: schemas.SubPieceCreate, db: Session = Depends(get_db)
):
    return crud.create_subpiece(db=db, subpiece=subpiece, piece_id=piece_id)


@router.post("/pieces", response_model=schemas.Piece, tags=["pieces"])
def create_piece(piece: schemas.PieceCreate, db: Session = Depends(get_db)):
    return crud.create_piece(db=db, piece=piece)


@router.get(
    "/{piece_id}/schedules/", response_model=list[schemas.Schedule], tags=["pieces"]
)
def read_schedules_by_piece(piece_id, db: Session = Depends(get_db)):
    return crud.get_schedules_by_piece(db, piece_id)


@router.get(
    "/{piece_id}/subpieces/", response_model=list[schemas.SubPiece], tags=["pieces"]
)
def read_subpieces_by_piece(piece_id, db: Session = Depends(get_db)):
    return crud.get_subpieces_by_piece(db, piece_id)


@router.get("/", response_model=list[schemas.Piece], tags=["pieces"])
def read_pieces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pieces(db, skip=skip, limit=limit)
