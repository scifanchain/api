from datapools import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datapools.database import get_db

router = APIRouter()


@router.post("/stages/create_stage/", response_model=schemas.Stage, tags=["authors"])
async def create_stage(stage: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), author: schemas.Author = Depends(crud.get_current_user)):
    return crud.create_stage(stage=stage, db=db, author=author)


@router.post("/stages/test/", response_model=schemas.Test, tags=["authors"])
def create_test(form_data: schemas.TestCreate, db: Session = Depends(get_db)):
    test = crud.create_test(db=db, title=form_data.title)
    return {"id":test.id, "title": test.title}


@router.get("/stages/", tags=["authors"])
async def read_stages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stages = crud.get_stages(db, skip=skip, limit=limit)
    return stages


@router.get("/stages/{stage_id}", tags=["authors"])
async def read_stages(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.get_stage(stage_id, db)
    return stage



