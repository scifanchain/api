from typing import List, Optional, Text
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Integer, SMALLINT
from enum import Enum, IntEnum


class StageTypeEnum(IntEnum):
    人物 = 1
    地点 = 2
    事件 = 3
    故事 = 4

class MaturityEnum(IntEnum):
    构思 = 1
    草稿 = 2
    编写 = 3
    审校 = 4
    成稿 = 3

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# Stage

class StageBase(BaseModel):
    title: str
    content: Optional[Text] = None
    type: StageTypeEnum.人物


class StageCreate(StageBase):
    pass


class Stage(StageBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Author

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



