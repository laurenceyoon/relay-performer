from http import HTTPStatus
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..core.helpers import play_piece_to_outport, start_interactive_performance

router = APIRouter(
    prefix="/pieces",
    responses={404: {"description": "Not found"}},
)

@router.patch(
    "/{piece_id}/play", status_code=HTTPStatus.ACCEPTED, tags=["Interactive API"]
)
def play_piece(
    piece_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    db_piece = crud.get_piece_by_id(db, piece_id=piece_id)
    background_tasks.add_task(play_piece_to_outport, piece=db_piece)
    return {"response": f"playing title({db_piece.title}) on the background"}


@router.patch(
    "/{piece_id}/perform",
    status_code=HTTPStatus.ACCEPTED,
    tags=["Interactive API"],
)
def perform_piece(
    piece_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    start_from=1,
):
    piece = crud.get_piece_by_id(db, piece_id=piece_id)
    background_tasks.add_task(
        start_interactive_performance, piece=piece, start_from=int(start_from)
    )
    return {"response": f"following title({piece.title})"}


@router.post(
    "/{piece_id}/subpieces/", response_model=schemas.SubPiece, tags=["pieces"]
)
def create_subpiece_by_piece(
    piece_id: int, subpiece: schemas.SubPieceCreate, db: Session = Depends(get_db)
):
    return crud.create_subpiece(db=db, subpiece=subpiece, piece_id=piece_id)

@router.post("/pieces", response_model=schemas.Piece, tags=["pieces"])
def create_piece(piece: schemas.PieceCreate, db: Session = Depends(get_db)):
    return crud.create_piece(db=db, piece=piece)


@router.get("/pieces/", response_model=List[schemas.Piece], tags=["pieces"])
def read_pieces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pieces(db, skip=skip, limit=limit)
