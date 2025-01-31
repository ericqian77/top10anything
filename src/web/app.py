from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Top 10 Analytics Dashboard",
        description="Web interface for generating and viewing Top 10 rankings",
        version="0.1.0"
    )
    
    @app.get("/")
    async def root():
        return JSONResponse({
            "status": "ok",
            "service": "Top 10 Analytics API",
            "version": "0.1.0"
        })
    
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 在生产环境中应该限制来源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 挂载静态文件目录
    app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
    
    # 导入和注册路由
    from .routes import api
    app.include_router(api.router, prefix="/api")
    
    return app 