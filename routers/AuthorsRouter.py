from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datapools import crud, models, schemas
from sqlalchemy.orm import Session
from datapools.database import get_db
from datetime import datetime, timedelta

from fastapi_jwt_auth import AuthJWT

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# 用户注册
# 同时生成access_token和refresh_token
@router.post("/authors/login/",  response_model=schemas.Token,  tags=["authors"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    # access_expires = timedelta(days=1)
    # refresh_expires = timedelta(days=30)
    # access_token = Authorize.create_access_token(subject=user.username, expires_time=access_expires)
    access_token = Authorize.create_access_token(subject=user.username)
    # refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=refresh_expires)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    
    return {"access_token": access_token, "refresh_token": refresh_token,  "token_type": "bearer"}

# 获取令牌
@router.post("/authors/token/", tags=["authors"])
async def get_access_token(Authorize: AuthJWT = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 刷新令牌
@router.post('/authors/refresh/')
def refresh( Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token}

# 获取当前登录用户
@router.get('/authors/current/')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()

    # if(current_user == ''){
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="用户名或密码错误",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # }

    return {"current_user": current_user}


@router.get("/authors/", response_model=List[schemas.Author], tags=["authors"])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@router.get("/authors/me/", tags=["authors"])
def read_authors_me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_author = Authorize.get_jwt_subject()

    return {"author": current_author}


@router.post("/authors/create_author/", response_model=schemas.Token, tags=["authors"])
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author = crud.create_author(db=db, author=author)

    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": author.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/authors/{username}/", response_model=schemas.Author, tags=["authors"])
def read_author(username, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_username(db, username=username)
    if db_author is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_author






