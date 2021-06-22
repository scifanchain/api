from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from routers import AuthorsRouter, StagesRouter

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    title="赛凡链应用层API",
    description="Scifanchain的数据API接口。",
    version="0.1.0",
    docs_url="/docs", 
    redoc_url="/docs2",
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.include_router(AuthorsRouter.router)
app.include_router(StagesRouter.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
