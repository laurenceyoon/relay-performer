from sqlalchemy.orm import Session

from . import models, schemas


def get_pieces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Piece).offset(skip).limit(limit).all()


def get_piece_by_id(db: Session, piece_id: int):
    return db.query(models.Piece).filter(models.Piece.id == piece_id).first()


def get_piece_by_title(db: Session, title: str):
    return db.query(models.Piece).filter(models.Piece.title.like(title)).first()


def create_piece(db: Session, piece: schemas.PieceCreate):
    db_piece = models.Piece(**piece.dict())
    db.add(db_piece)
    db.commit()
    db.refresh(db_piece)
    return db_piece


def get_schedules_by_piece(db: Session, piece_id: int):
    return db.query(models.Schedule).filter(models.Schedule.piece_id == piece_id).all()


def get_subpieces_by_piece(db: Session, piece_id: int):
    return db.query(models.SubPiece).filter(models.SubPiece.piece_id == piece_id).all()


def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()


def create_schedule(db: Session, schedule: schemas.Schedule, piece_id: int):
    db_schedule = models.Schedule(**schedule.dict(), piece_id=piece_id)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_subpieces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SubPiece).offset(skip).limit(limit).all()


def get_subpiece(db: Session, subpiece_id: int):
    return db.query(models.SubPiece).filter(models.SubPiece.id == subpiece_id).first()


def create_subpiece(db: Session, subpiece: schemas.SubPiece, piece_id: int):
    db_subpiece = models.SubPiece(**subpiece.dict(), piece_id=piece_id)
    db.add(db_subpiece)
    db.commit()
    db.refresh(db_subpiece)
    return db_subpiece
