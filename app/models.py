from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Piece(Base):
    __tablename__ = "pieces"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    path = Column(String)

    schedules = relationship("Schedule", back_populates="piece")
    subpieces = relationship("SubPiece", back_populates="piece")


class SubPiece(Base):
    __tablename__ = "subpieces"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    path = Column(String)
    piece_id = Column(Integer, ForeignKey("pieces.id"))
    etr = Column(Float, default=0)  # estimated time remaining (sec.)

    piece = relationship("Piece", back_populates="subpieces")
    schedules = relationship("Schedule", back_populates="subpiece")

    def __str__(self) -> str:
        return f"{self.title}"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    start_measure = Column(
        Integer, index=True, comment="measure number of starting point of a piece"
    )
    end_measure = Column(
        Integer, index=True, comment="measure number of ending point of a piece"
    )
    player = Column(String, comment="scheduled player's name")
    piece_id = Column(Integer, ForeignKey("pieces.id"))
    subpiece_id = Column(Integer, ForeignKey("subpieces.id"))

    piece = relationship("Piece", back_populates="schedules")
    subpiece = relationship("SubPiece", back_populates="schedules")

    def __str__(self) -> str:
        return f"{self.player}, {self.subpiece.title}, {self.start_measure}-{self.end_measure}"
