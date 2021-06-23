from fastapi import FastAPI
import uvicorn
from routers import AuthorsRouter, StagesRouter


app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    title="赛凡链应用层API",
    description="Scifanchain的数据API接口，为Client端提供数据和应用逻辑， 并且提供Websocket服务。本接口开源并面向公众开放，任何第三方客户端皆可使用本接口获取Scifanchain的内容数据。",
    version="0.1.0",
    docs_url="/docs", 
    redoc_url="/redoc",
)

app.include_router(AuthorsRouter.router)
app.include_router(StagesRouter.router)

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', 
        host="127.0.0.1",
        port=7000, 
        reload=True,
        debug=True,
    )
