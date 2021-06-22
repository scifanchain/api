from typing import List
from fastapi import APIRouter, Depends, HTTPException
from datapools import crud, models, schemas
from sqlalchemy.orm import Session
from datapools.database import get_db

router = APIRouter()

@router.get("/authors/", response_model=List[schemas.Author], tags=["authors"])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors
