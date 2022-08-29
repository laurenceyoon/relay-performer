from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={404: {"description": "Not found"}},
)


@router.get("/schedules/", response_model=list[schemas.Schedule])
def read_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_schedules_by_piece(db, skip=skip, limit=limit)

@router.get(
    "/schedules/{schedule_id}", response_model=schemas.Schedule
)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    return crud.get_schedule(db, schedule_id=schedule_id)
