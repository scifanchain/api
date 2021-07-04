from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datapools import crud, models, schemas
from sqlalchemy.orm import Session
from datapools.database import get_db
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.post("/stages/create_stage/", response_model=schemas.Stage, tags=["stages"])
async def create_stage(stage: schemas.StageCreate, db: Session = Depends(get_db), author: schemas.Author = Depends(crud.get_current_user)):
    return crud.create_stage(stage=stage, db=db, author=author)


@router.get("/stages/", tags=["stages"])
async def read_stages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stages = crud.get_stages(db, skip=skip, limit=limit)
    return stages


@router.get("/stages/{stage_id}", tags=["stages"])
async def read_stages(stage_id: int, db: Session = Depends(get_db)):
    stage = crud.get_stage(stage_id, db)
    return stage


@router.put("/stages/{stage_id}", response_model=schemas.Stage, tags=["stages"])
def update_item(stage_id: int, author: schemas.Author = Depends(crud.get_current_user), stage_update: schemas.StageUpdate, db: Session = Depends(get_db)):
    update_stage = crud.update_stage(stage_id, stage_update, db)
    if update_stage is None:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    # 写入关联数据
    add_stage_author = crud.create_state_author(stage_id, author.id, db)
    if add_stage_author is None:
      raise HTTPException(status_code=404, detail="关联数据未能插入")
    
    return update_stage
