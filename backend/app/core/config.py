"""
Core configuration settings for Universidad Galileo MediaLab Platform v1.1
Complete restructure for scalability and modularity
"""
import os
from functools import lru_cache
from typing import Optional, List, Union
from pydantic import Field, validator, AnyHttpUrl
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    URL: str = Field(description="Database connection URL")
    ECHO: bool = Field(default=False, description="Enable SQLAlchemy query logging")
    POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    MAX_OVERFLOW: int = Field(default=30, description="Database connection pool overflow")
    POOL_TIMEOUT: int = Field(default=30, description="Pool connection timeout")
    POOL_RECYCLE: int = Field(default=3600, description="Pool connection recycle time")

    class Config:
        env_prefix = "DB_"
        extra = "allow"


class RedisSettings(BaseSettings):
    """Redis configuration"""
    URL: str = Field(description="Redis connection URL")
    KEY_PREFIX: str = Field(default="medialab:", description="Redis key prefix")
    TTL: int = Field(default=3600, description="Default Redis TTL in seconds")
    MAX_CONNECTIONS: int = Field(default=50, description="Redis connection pool size")

    class Config:
        env_prefix = "REDIS_"
        extra = "allow"


class SecuritySettings(BaseSettings):
    """Security and encryption configuration"""
    SECRET_KEY: str = Field(description="Main application secret key")
    
    JWT_SECRET_KEY: str = Field(description="JWT token secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiration")
    JWT_REFRESH_EXPIRE_DAYS: int = Field(default=7, description="JWT refresh token expiration")
    
    JWE_SECRET_KEY: str = Field(description="JWE encryption key for cookies (must be 32+ chars)")
    JWE_ALGORITHM: str = Field(default="A256GCM", description="JWE encryption algorithm")
    
    COOKIE_SECURE: bool = Field(default=False, description="Use secure cookies (HTTPS only)")
    COOKIE_SAMESITE: str = Field(default="lax", description="Cookie SameSite policy")
    COOKIE_HTTPONLY: bool = Field(default=True, description="HTTP only cookies")
    COOKIE_MAX_AGE: int = Field(default=1800, description="Cookie max age in seconds")
    
    BCRYPT_ROUNDS: int = Field(default=12, description="Bcrypt hashing rounds")
    
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")

    @validator('JWE_SECRET_KEY')
    def validate_jwe_key_length(cls, v):
        if len(v) < 32:
            raise ValueError('JWE_SECRET_KEY must be at least 32 characters long')
        return v

    class Config:
        env_prefix = "SECURITY_"
        extra = "allow"


class StorageSettings(BaseSettings):
    """File storage and upload configuration"""
    UPLOAD_DIR: str = Field(default="../uploads", description="Main upload directory (outside backend)")
    STATIC_DIR: str = Field(default="./static", description="Static files directory (inside backend)")
    
    ORIGINAL_DIR: str = Field(default="original", description="Original files subdirectory")
    PROCESSED_DIR: str = Field(default="processed", description="Processed files subdirectory")
    THUMBNAILS_DIR: str = Field(default="thumbnails", description="Thumbnails subdirectory")
    TEMP_DIR: str = Field(default="temp", description="Temporary files subdirectory")
    
    MAX_UPLOAD_SIZE: int = Field(default=100 * 1024 * 1024, description="Max upload size (100MB)")
    MAX_IMAGE_SIZE: int = Field(default=20 * 1024 * 1024, description="Max image size (20MB)")
    MAX_VIDEO_SIZE: int = Field(default=500 * 1024 * 1024, description="Max video size (500MB)")
    
    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default=["jpg", "jpeg", "png", "webp", "gif", "avif", "heic"],
        description="Allowed image extensions"
    )
    ALLOWED_VIDEO_EXTENSIONS: List[str] = Field(
        default=["mp4", "mov", "avi", "mkv", "webm"],
        description="Allowed video extensions"
    )
    ALLOWED_DOCUMENT_EXTENSIONS: List[str] = Field(
        default=["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
        description="Allowed document extensions"
    )
    
    IMAGE_QUALITY: int = Field(default=85, description="Image compression quality")
    THUMBNAIL_SIZE: tuple = Field(default=(300, 300), description="Thumbnail dimensions")
    WATERMARK_ENABLED: bool = Field(default=False, description="Enable watermarking")

    class Config:
        env_prefix = "STORAGE_"
        extra = "allow"


class EmailSettings(BaseSettings):
    """Email configuration - managed from database"""
    FALLBACK_SMTP_HOST: str = Field(default="smtp.gmail.com")
    FALLBACK_SMTP_PORT: int = Field(default=587)
    FALLBACK_SMTP_TLS: bool = Field(default=True)
    FALLBACK_FROM_EMAIL: str = Field(default="noreply@medialab.edu.gt")
    
    TEMPLATE_DIR: str = Field(default="./static/email_templates", description="Email template directory (inside backend/static)")

    class Config:
        env_prefix = "EMAIL_"
        extra = "allow"


class ExternalServicesSettings(BaseSettings):
    """External services configuration"""
    YOUTUBE_API_KEY: Optional[str] = Field(default=None, description="YouTube API key")
    
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None)
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None)
    AWS_REGION: str = Field(default="us-east-1")
    AWS_S3_BUCKET: Optional[str] = Field(default=None)
    
    GOOGLE_ANALYTICS_ID: Optional[str] = Field(default=None)

    class Config:
        env_prefix = "EXTERNAL_"
        extra = "allow"


class FeatureFlagsSettings(BaseSettings):
    """Feature flags for enabling/disabling features"""
    ENABLE_REGISTRATION: bool = Field(default=False, description="Enable user registration")
    ENABLE_EMAIL_VERIFICATION: bool = Field(default=True, description="Enable email verification")
    ENABLE_PASSWORD_RESET: bool = Field(default=True, description="Enable password reset")
    ENABLE_MAINTENANCE_MODE: bool = Field(default=False, description="Enable maintenance mode")
    ENABLE_API_DOCS: bool = Field(default=True, description="Enable API documentation")
    ENABLE_CORS: bool = Field(default=True, description="Enable CORS")
    ENABLE_RATE_LIMITING: bool = Field(default=True, description="Enable rate limiting")

    class Config:
        env_prefix = "FEATURE_"
        extra = "allow"


class Settings(BaseSettings):
    """
    Main application settings
    """
    
    APP_NAME: str = Field(default="Universidad Galileo MediaLab Platform")
    APP_VERSION: str = Field(default="1.1.0")
    APP_DESCRIPTION: str = Field(default="MediaLab content management and project platform")
    
    ENVIRONMENT: str = Field(default="development", description="Runtime environment")
    DEBUG: bool = Field(default=True, description="Debug mode")
    IS_DOCKER: bool = Field(default=False, description="Running in Docker container")
    
    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL for the application"
    )
    FRONTEND_URL: str = Field(
        default="http://localhost:3247",
        description="Frontend application URL"
    )
    
    API_V1_PREFIX: str = Field(default="/api/v1")
    DOCS_URL: Optional[str] = Field(default="/docs")
    REDOC_URL: Optional[str] = Field(default="/redoc")
    OPENAPI_URL: Optional[str] = Field(default="/openapi.json")
    
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3247", "http://localhost:3000"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "PATCH"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])
    
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    LOG_ROTATION: bool = Field(default=True, description="Enable log rotation")
    LOG_MAX_SIZE: str = Field(default="10MB", description="Max log file size")
    LOG_BACKUP_COUNT: int = Field(default=5, description="Number of backup log files")
    
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    email: EmailSettings = Field(default_factory=EmailSettings)
    external: ExternalServicesSettings = Field(default_factory=ExternalServicesSettings)
    features: FeatureFlagsSettings = Field(default_factory=FeatureFlagsSettings)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._apply_environment_overrides()
        if self.ENVIRONMENT == "development":
            print(f"[DEBUG] DB URL: {self.database.URL}")
            print(f"[DEBUG] Redis URL: {self.redis.URL}")
            print(f"[DEBUG] Secret Key: {self.security.SECRET_KEY[:20]}...")
        self._validate_environment_config()
    
    def _apply_environment_overrides(self):
        """Apply environment-specific configuration overrides"""
        if self.ENVIRONMENT == "production":
            self.DEBUG = False
            self.features.ENABLE_API_DOCS = False
            self.security.COOKIE_SECURE = True
            self.security.COOKIE_SAMESITE = "strict"
            
        elif self.ENVIRONMENT == "staging":
            self.DEBUG = False
            self.features.ENABLE_API_DOCS = True
            
        elif self.ENVIRONMENT == "testing":
            self.database.ECHO = False
            self.features.ENABLE_EMAIL_VERIFICATION = False
    
    def _validate_environment_config(self):
        """Validate configuration based on environment"""
        if self.ENVIRONMENT == "production":
            required_vars = [
                ("DB_URL", self.database.URL),
                ("REDIS_URL", self.redis.URL),
                ("SECURITY_SECRET_KEY", self.security.SECRET_KEY),
                ("SECURITY_JWT_SECRET_KEY", self.security.JWT_SECRET_KEY),
                ("SECURITY_JWE_SECRET_KEY", self.security.JWE_SECRET_KEY),
            ]
            
            missing_vars = []
            for var_name, var_value in required_vars:
                if not var_value:
                    missing_vars.append(var_name)
            
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        env_nested_delimiter = "_"
        extra = "allow"
        
    def __post_init__(self):
        """Debug configuration loading"""
        if self.ENVIRONMENT == "development":
            print(f"DB URL loaded: {getattr(self.database, 'URL', 'NOT_LOADED')}")
            print(f"Redis URL loaded: {getattr(self.redis, 'URL', 'NOT_LOADED')}")
            print(f"Environment vars with DB: {[k for k in os.environ.keys() if 'DB' in k]}")
            print(f"Environment vars with REDIS: {[k for k in os.environ.keys() if 'REDIS' in k]}")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


def get_upload_path(subdir: str = "") -> str:
    """Get absolute upload path"""
    settings = get_settings()
    base_path = os.path.abspath(settings.storage.UPLOAD_DIR)
    if subdir:
        return os.path.join(base_path, subdir)
    return base_path


def get_static_path(subdir: str = "") -> str:
    """Get absolute static path"""
    settings = get_settings()
    base_path = os.path.abspath(settings.storage.STATIC_DIR)
    if subdir:
        return os.path.join(base_path, subdir)
    return base_path


def is_allowed_file_extension(filename: str, file_type: str = "image") -> bool:
    """Check if file extension is allowed"""
    settings = get_settings()
    extension = filename.lower().split('.')[-1] if '.' in filename else ''
    
    if file_type == "image":
        return extension in settings.storage.ALLOWED_IMAGE_EXTENSIONS
    elif file_type == "video":
        return extension in settings.storage.ALLOWED_VIDEO_EXTENSIONS
    elif file_type == "document":
        return extension in settings.storage.ALLOWED_DOCUMENT_EXTENSIONS
    
    return False