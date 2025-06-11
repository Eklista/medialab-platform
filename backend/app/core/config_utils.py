"""
Configuration utilities and helpers
"""
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .config import get_settings


def setup_logging() -> None:
    """Setup application logging based on configuration"""
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        filename=settings.LOG_FILE if settings.LOG_FILE else None
    )
    
    # Disable some noisy loggers in development
    if settings.is_development:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def ensure_directories() -> None:
    """Ensure all required directories exist"""
    settings = get_settings()
    
    # Create upload directories (outside backend)
    upload_base = Path(settings.storage.UPLOAD_DIR)
    for subdir in [
        settings.storage.ORIGINAL_DIR,
        settings.storage.PROCESSED_DIR,
        settings.storage.THUMBNAILS_DIR,
        settings.storage.TEMP_DIR
    ]:
        (upload_base / subdir).mkdir(parents=True, exist_ok=True)
    
    # Create static directory (inside backend)
    static_base = Path(settings.storage.STATIC_DIR)
    static_base.mkdir(parents=True, exist_ok=True)
    
    # Create email templates directory (inside backend/static)
    email_templates = Path(settings.email.TEMPLATE_DIR)
    email_templates.mkdir(parents=True, exist_ok=True)


def get_cors_config() -> Dict[str, Any]:
    """Get CORS configuration for FastAPI"""
    settings = get_settings()
    
    if not settings.features.ENABLE_CORS:
        return {}
    
    return {
        "allow_origins": settings.CORS_ORIGINS,
        "allow_credentials": settings.CORS_ALLOW_CREDENTIALS,
        "allow_methods": settings.CORS_ALLOW_METHODS,
        "allow_headers": settings.CORS_ALLOW_HEADERS,
    }


def get_database_url() -> str:
    """Get database URL with environment-specific overrides"""
    settings = get_settings()
    return settings.database.URL


def get_redis_url() -> str:
    """Get Redis URL with environment-specific overrides"""
    settings = get_settings()
    return settings.redis.URL


def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature flag is enabled"""
    settings = get_settings()
    return getattr(settings.features, f"ENABLE_{feature_name.upper()}", False)


def get_api_config() -> Dict[str, Optional[str]]:
    """Get API configuration for FastAPI app"""
    settings = get_settings()
    
    config = {
        "title": settings.APP_NAME,
        "description": settings.APP_DESCRIPTION,
        "version": settings.APP_VERSION,
        "openapi_url": settings.OPENAPI_URL,
    }
    
    # Conditionally add docs URLs based on feature flags
    if settings.features.ENABLE_API_DOCS:
        config["docs_url"] = settings.DOCS_URL
        config["redoc_url"] = settings.REDOC_URL
    else:
        config["docs_url"] = None
        config["redoc_url"] = None
    
    return config


def get_cookie_config() -> Dict[str, Any]:
    """Get cookie configuration for JWE encrypted cookies"""
    settings = get_settings()
    
    return {
        "max_age": settings.security.COOKIE_MAX_AGE,
        "secure": settings.security.COOKIE_SECURE,
        "httponly": settings.security.COOKIE_HTTPONLY,
        "samesite": settings.security.COOKIE_SAMESITE,
    }


def get_environment_info() -> Dict[str, Any]:
    """Get current environment information for debugging"""
    settings = get_settings()
    
    return {
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "is_docker": settings.IS_DOCKER,
        "base_url": str(settings.BASE_URL),
        "frontend_url": str(settings.FRONTEND_URL),
        "api_docs_enabled": settings.features.ENABLE_API_DOCS,
        "version": settings.APP_VERSION,
    }


def validate_production_config() -> bool:
    """Validate configuration for production deployment"""
    settings = get_settings()
    
    if not settings.is_production:
        return True
    
    errors = []
    
    # Check for default secrets
    if "change-in-production" in settings.security.SECRET_KEY.lower():
        errors.append("SECRET_KEY is using default value")
    
    if "change-in-production" in settings.security.JWT_SECRET_KEY.lower():
        errors.append("JWT_SECRET_KEY is using default value")
    
    # Check security settings
    if not settings.security.COOKIE_SECURE:
        errors.append("COOKIE_SECURE should be True in production")
    
    if settings.DEBUG:
        errors.append("DEBUG should be False in production")
    
    if settings.features.ENABLE_API_DOCS:
        errors.append("API docs should be disabled in production")
    
    if errors:
        logging.error("Production configuration errors:")
        for error in errors:
            logging.error(f"  - {error}")
        return False
    
    return True


# Environment detection helpers
def detect_docker_environment() -> bool:
    """Detect if running inside Docker container"""
    return (
        os.path.exists("/.dockerenv") or
        os.path.exists("/proc/1/cgroup") and "docker" in open("/proc/1/cgroup").read()
    )


def get_effective_environment() -> str:
    """Get the effective environment considering auto-detection"""
    settings = get_settings()
    
    # Auto-detect Docker if not explicitly set
    if not settings.IS_DOCKER and detect_docker_environment():
        os.environ["IS_DOCKER"] = "true"
    
    return settings.ENVIRONMENT