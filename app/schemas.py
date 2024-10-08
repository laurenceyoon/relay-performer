from typing import Optional

from pydantic import BaseModel


class ScheduleBase(BaseModel):
    start_measure: int
    end_measure: int
    player: str
    subpiece_id: Optional[int] = None


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int
    piece_id: int

    class Config:
        orm_mode = True


class SubPieceBase(BaseModel):
    title: str
    path: str


class SubPieceCreate(SubPieceBase):
    pass


class SubPiece(SubPieceBase):
    id: int
    piece_id: int
    etr: float

    class Config:
        orm_mode = True


class PieceBase(BaseModel):
    title: str
    path: str


class PieceCreate(PieceBase):
    pass


class Piece(PieceBase):
    id: int
    subpieces: list[SubPiece] = []
    schedules: list[Schedule] = []

    class Config:
        orm_mode = True
