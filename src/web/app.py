from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pathlib import Path

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Top 10 Analytics Dashboard",
        description="Web interface for generating and viewing Top 10 rankings",
        version="0.1.0"
    )
    
    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 在生产环境中应该限制来源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 获取静态文件目录的绝对路径
    static_dir = Path(__file__).parent / "static"
    
    # 挂载静态文件目录
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    @app.get("/")
    async def root():
        """Serve the main HTML page"""
        return FileResponse(str(static_dir / "index.html"))
    
    @app.get("/api")
    async def api_root():
        """API status endpoint"""
        return JSONResponse({
            "status": "ok",
            "service": "Top 10 Analytics API",
            "version": "0.1.0"
        })
    
    # 导入和注册路由
    from .routes import api
    app.include_router(api.router, prefix="/api")
    
    return app 