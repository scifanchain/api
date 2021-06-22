from typing import List, Optional, Text
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import SMALLINT


class StageBase(BaseModel):
    title: str
    content: Optional[Text] = None
    type: int

class StageCreate(StageBase):
    pass

class Stage(StageBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    username: str
    nickname: str
    email: str

class AuthorCreate(AuthorBase):
    password: str

class Author(AuthorBase):
    id: int
    is_active: bool
    stages: List[Stage] = []

    class Config: 
        orm_mode = True