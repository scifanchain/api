from sqlalchemy.orm import Session
from . import models, schemas


def get_author(db: Session, author_id: int):

    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_email(db: Session, email: str):

    return db.query(models.Author).filter(models.Author.email == email).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    fake_hashed_password = author.password + "notreallyhashed"
    db_author = models.Author(
        email=author.email, hashed_password=fake_hashed_password)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_stages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stage).offset(skip).limit(limit).all()


def create_stage(db: Session, stage: schemas.StageCreate, author_id: int):
    db_stage = models.Stage(**stage.dict(), owner_id=author_id)
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage
