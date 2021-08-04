from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import AuthorsRouter, StagesRouter, TestRouter
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

import uvicorn


app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    title="赛凡链应用层API",
    description="Scifanchain的数据API接口，为Client端提供数据和应用逻辑， 并且提供Websocket服务。本接口开源并面向公众开放，任何第三方客户端皆可使用本接口获取Scifanchain的内容数据。",
    version="0.1.0",
    docs_url="/docs", 
    redoc_url="/",
)

origins = [
    "*"
    # "http://scifanchain.com",
    # "http://www.scifanchain.com",
    # "http://api.scifanchain.com",
    # "https://scifanchain.com",
    # "https://www.scifanchain.com",
    # "https://api.scifanchain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Settings(BaseModel):
    authjwt_secret_key: str = "569bbbbce875a614e0d8c471e63891a4308331b99fc8731b2238dcdb3468dc22"
    authjwt_access_token_expires: int = 60

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(StagesRouter.router)
app.include_router(AuthorsRouter.router)
app.include_router(TestRouter.router)

@app.get("/")
async def root():
    return {"message": "Welcome!"}

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', 
        host="127.0.0.1",
        port=7000, 
        reload=True,
        debug=True,
    )
