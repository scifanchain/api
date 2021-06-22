from datapools import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from config.dpds import get_token_header

from datapools.database import get_db

router = APIRouter(
    prefix="/stages",
    tags=["stages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},

)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_stages():
    return fake_items_db

@router.post("/create_stage", response_model=schemas.Stage)
async def create_stage(author_id: int, stage: schemas.StageCreate, db: Session = Depends(get_db)):
    return crud.create_stage(db=db, stage=stage, author_id=author_id)



