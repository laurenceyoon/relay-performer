from fastapi.responses import RedirectResponse
from sqladmin import BaseView, ModelView, expose

from ..models import Piece, Schedule, SubPiece


class DocsView(BaseView):
    name = "API Document Page"
    icon = "fa-solid fa-book"

    @expose("/docs", methods=["GET"])
    def docs_page(self, request):
        return RedirectResponse("/docs")


class PieceAdmin(ModelView, model=Piece):
    icon = "fa-solid fa-compact-disc"
    column_list = [Piece.id, Piece.title]
    form_excluded_columns = ["subpieces", "schedules"]


class SubPieceAdmin(ModelView, model=SubPiece):
    icon = "fa-solid fa-music"
    column_list = [SubPiece.id, SubPiece.title, SubPiece.path]
    form_excluded_columns = ["schedules"]
    page_size = 100


class ScheduleAdmin(ModelView, model=Schedule):
    icon = "fa-solid fa-align-justify"
    column_list = [
        Schedule.id,
        Schedule.piece_id,
        Schedule.subpiece_id,
        Schedule.player,
        Schedule.subpiece,
    ]
    page_size = 100
