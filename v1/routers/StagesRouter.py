from datapools import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datapools.database import get_db

router = APIRouter(
    prefix="/stages",
    tags=["stages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},

)

@router.post("/create_stage/", response_model=schemas.Stage)
async def create_stage(stage: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), author: schemas.Author = Depends(crud.get_current_user)):
    return crud.create_stage(stage=stage, db=db, author=author)


@router.post("/test/", response_model=schemas.Test)
def create_test(form_data: schemas.TestCreate, db: Session = Depends(get_db)):
    test = crud.create_test(db=db, title=form_data.title)
    return {"id":test.id, "title": test.title}

@router.get("/")
async def read_stages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stages = crud.get_stages(db, skip=skip, limit=limit)
    return stages


@router.get("/{stage_id}")
async def read_stages(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.get_stage(stage_id, db)
    return stage



