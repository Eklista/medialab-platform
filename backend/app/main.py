"""
Universidad Galileo MediaLab Platform - Main Application
FastAPI application setup - Con registro elegante de modelos
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.config_utils import (
    setup_logging,
    ensure_directories,
    get_cors_config,
    get_api_config,
    get_environment_info,
    validate_production_config
)

# Registra todos los modelos automáticamente
import app.models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan events
    """
    # Startup
    logging.info("🚀 Starting Universidad Galileo MediaLab Platform...")
    
    settings = get_settings()
    
    # Setup logging
    setup_logging()
    
    # Ensure directories exist
    ensure_directories()
    
    # Log model registration info
    if settings.is_development:
        from app.models import get_registry_info
        registry_info = get_registry_info()
        logging.info(f"📊 Models registered: {registry_info['total_tables']} tables")
    
    # Validate production config
    if settings.is_production:
        if not validate_production_config():
            raise RuntimeError("Production configuration validation failed!")
    
    # Log environment info
    env_info = get_environment_info()
    logging.info(f"Environment: {env_info}")
    
    logging.info("✅ Application startup completed")
    
    yield
    
    # Shutdown
    logging.info("🛑 Shutting down MediaLab Platform...")
    logging.info("✅ Application shutdown completed")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    settings = get_settings()
    
    # Get API configuration
    api_config = get_api_config()
    
    # Create FastAPI app with lifespan
    app = FastAPI(
        lifespan=lifespan,
        **api_config
    )
    
    # Add middleware
    setup_middleware(app)
    
    # Add routes
    setup_routes(app)
    
    # Add exception handlers
    setup_exception_handlers(app)
    
    return app


def setup_middleware(app: FastAPI) -> None:
    """
    Setup application middleware
    """
    settings = get_settings()
    
    # CORS Middleware
    if settings.features.ENABLE_CORS:
        cors_config = get_cors_config()
        app.add_middleware(CORSMiddleware, **cors_config)
        logging.info("✅ CORS middleware enabled")
    
    # Trusted Host Middleware (for production)
    if settings.is_production:
        allowed_hosts = [str(settings.BASE_URL).replace("http://", "").replace("https://", "")]
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=allowed_hosts
        )
        logging.info(f"✅ Trusted host middleware enabled for: {allowed_hosts}")


def setup_routes(app: FastAPI) -> None:
    """
    Setup application routes and static files
    """
    settings = get_settings()
    
    # Mount static files (if directory exists)
    try:
        app.mount(
            "/static", 
            StaticFiles(directory=settings.storage.STATIC_DIR), 
            name="static"
        )
        logging.info("✅ Static files mounted at /static")
    except RuntimeError:
        logging.warning("⚠️ Static directory not found, skipping static files mounting")
    
    # Mount uploads (if directory exists)
    try:
        app.mount(
            "/uploads", 
            StaticFiles(directory=settings.storage.UPLOAD_DIR), 
            name="uploads"
        )
        logging.info("✅ Upload files mounted at /uploads")
    except RuntimeError:
        logging.warning("⚠️ Upload directory not found, skipping uploads mounting")
    
    # Health check endpoint
    @app.get("/health", tags=["System"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG
        }
    
    # Environment info endpoint (dev only)
    if settings.is_development:
        @app.get("/debug/env", tags=["Debug"])
        async def debug_environment():
            """Get environment information (development only)"""
            return get_environment_info()
        
        @app.get("/debug/models", tags=["Debug"])
        async def debug_models():
            """Check registered SQLAlchemy models"""
            from app.models import get_registry_info
            return get_registry_info()
    
    # API routes
    from app.modules.users.router import router as users_router
    
    app.include_router(users_router, prefix=settings.API_V1_PREFIX, tags=["Users"])
    
    # Root endpoint
    @app.get("/", tags=["System"])
    async def root():
        """Root endpoint"""
        return {
            "message": "Universidad Galileo MediaLab Platform API",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "docs_url": "/docs" if settings.features.ENABLE_API_DOCS else None
        }


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Setup global exception handlers
    """
    
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """Handle 404 errors"""
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Not Found",
                "message": "The requested resource was not found",
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        """Handle 500 errors"""
        logging.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }
        )
    
    # Maintenance mode check
    settings = get_settings()
    if settings.features.ENABLE_MAINTENANCE_MODE:
        @app.middleware("http")
        async def maintenance_mode(request: Request, call_next):
            """Maintenance mode middleware"""
            if request.url.path not in ["/health", "/docs", "/redoc", "/openapi.json"]:
                return JSONResponse(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content={
                        "error": "Service Unavailable",
                        "message": "System is currently under maintenance"
                    }
                )
            return await call_next(request)


# Create the app instance
app = create_application()


# For debugging
if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )