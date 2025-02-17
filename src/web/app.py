from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    load_dotenv()  # Add this at the top of your app initialization
    app = FastAPI(
        title="Top 10 Analytics Dashboard",
        description="Web interface for generating and viewing Top 10 rankings",
        version="0.1.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Should be restricted in production environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Get absolute path of static files directory
    static_dir = Path(__file__).parent / "static"
    
    # Mount static files directory
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
    
    # Import and register routes
    from .routes import api
    app.include_router(api.router, prefix="/api")
    
    # Add this error handler
    @app.exception_handler(Exception)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "detail": str(exc)}
        )
    
    return app 