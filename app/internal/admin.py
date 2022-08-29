from sqladmin import ModelView
from ..models import Piece, SubPiece, Schedule


class PieceAdmin(ModelView, model=Piece):
    column_list = [Piece.id, Piece.title]

class SubPieceAdmin(ModelView, model=SubPiece):
    column_list = [SubPiece.id, SubPiece.title]

class ScheduleAdmin(ModelView, model=Schedule):
    column_list = [Schedule.id, Schedule.subpiece_id, Schedule.player]
