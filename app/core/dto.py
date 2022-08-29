from dataclasses import dataclass

from ..models import SubPiece

@dataclass
class Schedule:
    player: str
    subpiece: SubPiece
