from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{schedule_id}", response_model=schemas.Schedule
)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    return crud.get_schedule(db, schedule_id=schedule_id)
