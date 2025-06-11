"""
Core configuration settings for Universidad Galileo MediaLab Platform
"""
import os
from functools import lru_cache
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # =================================
    # APPLICATION SETTINGS
    # =================================
    APP_NAME: str = Field(default="Universidad Galileo MediaLab Platform")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # =================================
    # DATABASE SETTINGS
    # =================================
    DATABASE_URL: str = Field(
        default="mysql+pymysql://medialab:password@localhost:3306/medialab_db",
        description="Database connection URL"
    )
    DB_ECHO: bool = Field(default=False, description="Enable SQLAlchemy query logging")
    DB_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=30, description="Database connection pool overflow")
    
    # =================================
    # REDIS SETTINGS
    # =================================
    REDIS_URL: str = Field(
        default="redis://:medialab2025@localhost:6479",
        description="Redis connection URL"
    )
    REDIS_KEY_PREFIX: str = Field(default="medialab:", description="Redis key prefix")
    REDIS_TTL: int = Field(default=3600, description="Default Redis TTL in seconds")
    
    # =================================
    # SECURITY SETTINGS
    # =================================
    SECRET_KEY: str = Field(
        default="your-super-secret-key-here-change-in-production",
        description="Secret key for cryptographic operations"
    )
    JWT_SECRET_KEY: str = Field(
        default="another-secret-key-for-jwt",
        description="Secret key for JWT tokens"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiration in minutes")
    JWT_REFRESH_EXPIRE_DAYS: int = Field(default=7, description="JWT refresh token expiration in days")
    
    # Password hashing
    BCRYPT_ROUNDS: int = Field(default=12, description="Bcrypt hashing rounds")
    
    # =================================
    # CORS SETTINGS
    # =================================
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3247", "http://localhost:3000"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])
    
    # =================================
    # FILE UPLOAD SETTINGS
    # =================================
    UPLOAD_DIR: str = Field(default="./uploads", description="Upload directory path")
    MAX_UPLOAD_SIZE: int = Field(default=50 * 1024 * 1024, description="Max upload size in bytes (50MB)")
    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default=["jpg", "jpeg", "png", "webp", "gif"],
        description="Allowed image file extensions"
    )
    ALLOWED_VIDEO_EXTENSIONS: List[str] = Field(
        default=["mp4", "mov", "avi", "mkv", "webm"],
        description="Allowed video file extensions"
    )
    
    # Storage paths
    STORAGE_ORIGINAL_DIR: str = Field(default="./storage/original")
    STORAGE_PROCESSED_DIR: str = Field(default="./storage/processed")
    STORAGE_THUMBNAILS_DIR: str = Field(default="./storage/thumbnails")
    
    # =================================
    # EMAIL SETTINGS
    # =================================
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP server host")
    SMTP_PORT: int = Field(default=587, description="SMTP server port")
    SMTP_USER: str = Field(default="", description="SMTP username")
    SMTP_PASSWORD: str = Field(default="", description="SMTP password")
    SMTP_TLS: bool = Field(default=True, description="Use TLS for SMTP")
    FROM_EMAIL: str = Field(default="noreply@medialab.edu.gt", description="Default from email")
    
    # =================================
    # API SETTINGS
    # =================================
    API_V1_PREFIX: str = Field(default="/api/v1", description="API version 1 prefix")
    DOCS_URL: str = Field(default="/docs", description="API documentation URL")
    REDOC_URL: str = Field(default="/redoc", description="ReDoc documentation URL")
    OPENAPI_URL: str = Field(default="/openapi.json", description="OpenAPI schema URL")
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # =================================
    # LOGGING SETTINGS
    # =================================
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    
    # =================================
    # FEATURE FLAGS
    # =================================
    ENABLE_REGISTRATION: bool = Field(default=False, description="Enable user registration")
    ENABLE_EMAIL_VERIFICATION: bool = Field(default=True, description="Enable email verification")
    ENABLE_PASSWORD_RESET: bool = Field(default=True, description="Enable password reset")
    ENABLE_MAINTENANCE_MODE: bool = Field(default=False, description="Enable maintenance mode")
    
    # =================================
    # EXTERNAL SERVICES
    # =================================
    # YouTube API (for video embeds)
    YOUTUBE_API_KEY: Optional[str] = Field(default=None, description="YouTube API key")
    
    # Image processing
    IMAGE_QUALITY: int = Field(default=85, description="Image compression quality (1-100)")
    THUMBNAIL_SIZE: tuple = Field(default=(300, 300), description="Thumbnail size (width, height)")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()