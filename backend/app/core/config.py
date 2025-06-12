# backend/app/core/config.py
"""
Core configuration settings for the MediaLab Platform
"""
import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Main configuration class for the application"""
    
    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "env_prefix": ""
    }
    
    # ===================================
    # APPLICATION SETTINGS
    # ===================================
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "Universidad Galileo MediaLab Platform"
    APP_VERSION: str = "1.1.0"
    APP_DESCRIPTION: str = "MediaLab content management and project platform"
    BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3247"
    IS_DOCKER: bool = False
    
    # ===================================
    # DATABASE CONFIGURATION
    # ===================================
    
    DB_URL: str = "mysql+pymysql://root:root@localhost:3306/medialab_db"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # ===================================
    # REDIS CONFIGURATION
    # ===================================
    
    REDIS_URL: str = "redis://:medialab2025@localhost:6479"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6479
    REDIS_PASSWORD: str = "medialab2025"
    REDIS_DB: int = 0
    REDIS_AUTH_DB: int = 1
    REDIS_TIMEOUT: int = 5
    REDIS_KEY_PREFIX: str = "medialab:"
    REDIS_TTL: int = 3600
    REDIS_MAX_CONNECTIONS: int = 50
    
    # ===================================
    # SECURITY CONFIGURATION (LEGACY)
    # ===================================
    
    SECURITY_SECRET_KEY: str = "dev-secret-key-change-in-production-2025"
    SECURITY_JWT_SECRET_KEY: str = "jwt-secret-key-change-in-production-2025"
    SECURITY_JWT_ALGORITHM: str = "HS256"
    SECURITY_JWT_EXPIRE_MINUTES: int = 30
    SECURITY_JWT_REFRESH_EXPIRE_DAYS: int = 7
    SECURITY_JWE_SECRET_KEY: str = "jwe-secret-key-for-cookies-must-be-32-chars-minimum-2025"
    SECURITY_JWE_ALGORITHM: str = "A256GCM"
    SECURITY_COOKIE_SECURE: bool = False
    SECURITY_COOKIE_SAMESITE: str = "lax"
    SECURITY_COOKIE_HTTPONLY: bool = True
    SECURITY_COOKIE_MAX_AGE: int = 1800
    SECURITY_BCRYPT_ROUNDS: int = 12
    SECURITY_RATE_LIMIT_ENABLED: bool = True
    SECURITY_RATE_LIMIT_REQUESTS: int = 100
    SECURITY_RATE_LIMIT_WINDOW: int = 60
    
    # ===================================
    # AUTH MODULE CONFIGURATION
    # ===================================
    
    # Encryption settings
    SESSION_MASTER_KEY: str = "dev-session-encryption-key-32-chars-minimum-change-in-prod-2025"
    TOKEN_MASTER_KEY: str = "dev-token-encryption-key-32-chars-minimum-change-in-prod-2025"
    SESSION_ENCRYPTION_SALT: str = "medialab_session_encryption_salt_v1"
    TOKEN_ENCRYPTION_SALT: str = "medialab_token_encryption_salt_v1"
    ENCRYPTION_ENABLED: bool = True
    KEY_ROTATION_ENABLED: bool = False
    KEY_ROTATION_DAYS: int = 90
    
    # Rate limiting settings
    IP_MAX_ATTEMPTS: int = 10
    IP_WINDOW_MINUTES: int = 15
    IP_BLOCK_ESCALATION: bool = True
    USER_MAX_ATTEMPTS: int = 5
    USER_WINDOW_MINUTES: int = 30
    USER_BLOCK_ESCALATION: bool = True
    GLOBAL_MAX_ATTEMPTS: int = 1000
    GLOBAL_WINDOW_MINUTES: int = 5
    
    # Block escalation settings
    BLOCK_DURATIONS: List[int] = Field(
        default=[15, 30, 60, 120, 240, 480],
        description="Block duration escalation (minutes)"
    )
    MAX_BLOCK_DURATION: int = 480
    BLOCK_RESET_HOURS: int = 24
    
    # Risk analysis settings
    RISK_THRESHOLD_LOW: int = 30
    RISK_THRESHOLD_MEDIUM: int = 60
    RISK_THRESHOLD_HIGH: int = 80
    RISK_WEIGHT_FAILED_ATTEMPTS: int = 30
    RISK_WEIGHT_NEW_LOCATION: int = 25
    RISK_WEIGHT_NEW_DEVICE: int = 20
    RISK_WEIGHT_UNUSUAL_TIME: int = 15
    RISK_WEIGHT_SUSPICIOUS_IP: int = 35
    RISK_WEIGHT_BOT_BEHAVIOR: int = 25
    LOCATION_CHANGE_DETECTION: bool = True
    LOCATION_RADIUS_KM: int = 50
    
    # Session management
    SESSION_DURATION_HOURS: int = 24
    SESSION_DURATION_INTERNAL_HOURS: int = 8
    SESSION_DURATION_INSTITUTIONAL_HOURS: int = 4
    SESSION_DURATION_REMEMBER_ME_DAYS: int = 30
    SESSION_EXTENSION_MAX_HOURS: int = 72
    SESSION_CLEANUP_INTERVAL_HOURS: int = 6
    SESSION_AUTO_EXTEND: bool = True
    SESSION_EXTEND_THRESHOLD_MINUTES: int = 30
    MAX_CONCURRENT_SESSIONS_INTERNAL: int = 5
    MAX_CONCURRENT_SESSIONS_INSTITUTIONAL: int = 3
    
    # Token settings
    ACCESS_TOKEN_DURATION_MINUTES: int = 15
    ACCESS_TOKEN_ALGORITHM: str = "A256KW"
    ACCESS_TOKEN_ENCRYPTION: str = "A256GCM"
    REFRESH_TOKEN_DURATION_DAYS: int = 30
    REFRESH_TOKEN_ROTATION: bool = True
    REFRESH_TOKEN_ROTATION_THRESHOLD_DAYS: int = 7
    
    # Two factor authentication
    FORCE_2FA_FOR_ADMIN: bool = True
    FORCE_2FA_HIGH_RISK: bool = True
    TOTP_WINDOW_SECONDS: int = 30
    TOTP_DIGITS: int = 6
    TOTP_ALGORITHM: str = "SHA1"
    BACKUP_CODES_COUNT: int = 10
    BACKUP_CODES_LENGTH: int = 8
    BACKUP_CODES_EXPIRY_DAYS: int = 365
    TEMP_SESSION_DURATION_MINUTES: int = 10
    TEMP_SESSION_MAX_ATTEMPTS: int = 3
    
    # Legacy 2FA settings (compatibility)
    SECURITY_TOTP_ISSUER: str = "Universidad Galileo MediaLab"
    SECURITY_TOTP_VALID_WINDOW: int = 1
    SECURITY_BACKUP_CODES_COUNT: int = 10
    
    # Security monitoring
    LOG_ALL_LOGIN_ATTEMPTS: bool = True
    LOG_SECURITY_EVENTS: bool = True
    LOG_SENSITIVE_DATA: bool = False
    ALERT_ON_SUSPICIOUS_ACTIVITY: bool = True
    ALERT_ON_MULTIPLE_FAILURES: bool = True
    ALERT_THRESHOLD_FAILURES: int = 5
    LOGIN_HISTORY_RETENTION_DAYS: int = 90
    SECURITY_EVENTS_RETENTION_DAYS: int = 365
    FAILED_ATTEMPTS_RETENTION_HOURS: int = 24
    
    # Device trust
    DEVICE_TRUST_ENABLED: bool = True
    DEVICE_TRUST_DURATION_DAYS: int = 30
    DEVICE_FINGERPRINT_REQUIRED: bool = True
    
    # Password policy
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 128
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = False
    PASSWORD_HISTORY_COUNT: int = 5
    PASSWORD_MAX_AGE_DAYS: int = 90
    
    # OAuth configuration
    OAUTH_GOOGLE_ENABLED: bool = False
    OAUTH_MICROSOFT_ENABLED: bool = False
    OAUTH_GITHUB_ENABLED: bool = False
    OAUTH_CALLBACK_BASE_URL: str = "http://localhost:8000"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "/api/v1/auth/oauth/google/callback"
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_REDIRECT_URI: str = "/api/v1/auth/oauth/microsoft/callback"
    
    # Legacy OAuth settings (compatibility)
    OAUTH_GOOGLE_CLIENT_ID: Optional[str] = None
    OAUTH_GOOGLE_CLIENT_SECRET: Optional[str] = None
    OAUTH_GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/google/callback"
    
    # ===================================
    # STORAGE CONFIGURATION
    # ===================================
    
    STORAGE_UPLOAD_DIR: str = "../uploads"
    STORAGE_STATIC_DIR: str = "./static"
    STORAGE_ORIGINAL_DIR: str = "original"
    STORAGE_PROCESSED_DIR: str = "processed"
    STORAGE_THUMBNAILS_DIR: str = "thumbnails"
    STORAGE_TEMP_DIR: str = "temp"
    STORAGE_MAX_UPLOAD_SIZE: int = 104857600
    STORAGE_MAX_IMAGE_SIZE: int = 20971520
    STORAGE_MAX_VIDEO_SIZE: int = 524288000
    STORAGE_IMAGE_QUALITY: int = 85
    STORAGE_WATERMARK_ENABLED: bool = False
    
    # ===================================
    # EMAIL CONFIGURATION
    # ===================================
    
    EMAIL_FALLBACK_SMTP_HOST: str = "smtp.gmail.com"
    EMAIL_FALLBACK_SMTP_PORT: int = 587
    EMAIL_FALLBACK_SMTP_TLS: bool = True
    EMAIL_FALLBACK_FROM_EMAIL: str = "noreply@medialab.edu.gt"
    EMAIL_TEMPLATE_DIR: str = "./static/email_templates"
    EMAIL_TEMPLATE_WELCOME: str = "auth/welcome.html"
    EMAIL_TEMPLATE_ACTIVATION: str = "auth/activation.html"
    EMAIL_TEMPLATE_PASSWORD_RESET: str = "auth/password_reset.html"
    EMAIL_TEMPLATE_SECURITY_ALERT: str = "auth/security_alert.html"
    SEND_WELCOME_EMAIL: bool = True
    SEND_SECURITY_ALERTS: bool = True
    SEND_LOGIN_NOTIFICATIONS: bool = False
    INVITATION_FROM_EMAIL: str = "noreply@medialab.galileo.edu"
    INVITATION_FROM_NAME: str = "MediaLab Universidad Galileo"
    
    # ===================================
    # FEATURE FLAGS
    # ===================================
    
    FEATURE_ENABLE_REGISTRATION: bool = False
    FEATURE_ENABLE_EMAIL_VERIFICATION: bool = True
    FEATURE_ENABLE_PASSWORD_RESET: bool = True
    FEATURE_ENABLE_MAINTENANCE_MODE: bool = False
    FEATURE_ENABLE_API_DOCS: bool = True
    FEATURE_ENABLE_CORS: bool = True
    FEATURE_ENABLE_RATE_LIMITING: bool = True
    
    # ===================================
    # API CONFIGURATION
    # ===================================
    
    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    OPENAPI_URL: Optional[str] = "/openapi.json"
    
    # ===================================
    # CORS CONFIGURATION
    # ===================================
    
    CORS_ORIGINS: List[str] = ["http://localhost:3247", "http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # ===================================
    # LOGGING CONFIGURATION
    # ===================================
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    LOG_ROTATION: bool = True
    LOG_MAX_SIZE: str = "10MB"
    LOG_BACKUP_COUNT: int = 5
    
    # ===================================
    # LEGACY COMPATIBILITY
    # ===================================
    
    ALLOWED_EMAIL_DOMAINS: List[str] = ["galileo.edu"]
    ADMIN_EMAIL_DOMAINS: List[str] = ["galileo.edu"]
    INVITATION_TOKEN_EXPIRE_HOURS: int = 72
    INVITATION_MAX_USES: int = 1
    SESSION_MAX_CONCURRENT: int = 5
    SESSION_EXTEND_ON_ACTIVITY: bool = True
    AUTH_RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    AUTH_RATE_LIMIT_LOGIN_WINDOW: int = 300
    AUTH_RATE_LIMIT_PASSWORD_RESET: int = 3
    AUTH_RATE_LIMIT_PASSWORD_RESET_WINDOW: int = 3600
    ACCOUNT_LOCKOUT_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION: int = 1800
    ACCOUNT_LOCKOUT_RESET_TIME: int = 3600
    
    # Additional auth settings for compatibility
    INVITATION_SYSTEM_ENABLED: bool = True
    INVITATION_EXPIRE_DAYS: int = 7
    INVITATION_REQUIRE_APPROVAL: bool = True
    ACCOUNT_ACTIVATION_REQUIRED: bool = True
    ACCOUNT_ACTIVATION_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_ENABLED: bool = True
    PASSWORD_RESET_EXPIRE_HOURS: int = 2
    PASSWORD_RESET_MAX_ATTEMPTS: int = 3
    ACCOUNT_LOCKOUT_ENABLED: bool = True
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = 30
    
    # Development settings
    AUTH_DEBUG_MODE: bool = True
    AUTH_STRICT_MODE: bool = False
    DEV_ALLOW_WEAK_PASSWORDS: bool = False
    DEV_DISABLE_EMAIL_VERIFICATION: bool = False
    DEV_MOCK_EXTERNAL_SERVICES: bool = False
    TEST_USER_AUTO_ACTIVATION: bool = False
    TEST_BYPASS_RATE_LIMITING: bool = False
    
    # Cookie settings
    SESSION_COOKIE_NAME: str = "medialab_session"
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"
    SESSION_COOKIE_DOMAIN: Optional[str] = None
    
    # Audit settings
    AUDIT_LOGIN_EVENTS: bool = True
    AUDIT_LOGOUT_EVENTS: bool = True
    AUDIT_PASSWORD_CHANGES: bool = True
    AUDIT_PERMISSION_CHANGES: bool = True
    AUDIT_FAILED_ATTEMPTS: bool = True
    AUDIT_RETENTION_DAYS: int = 365
    AUDIT_EXPORT_ENABLED: bool = True
    
    # API settings
    API_RATE_LIMIT_ENABLED: bool = True
    API_RATE_LIMIT_REQUESTS: int = 100
    API_RATE_LIMIT_WINDOW_MINUTES: int = 15
    API_KEY_AUTHENTICATION: bool = False
    API_BEARER_TOKEN_REQUIRED: bool = True
    
    # Logout settings
    LOGOUT_REVOKE_ALL_SESSIONS: bool = False
    LOGOUT_CLEAR_REMEMBER_ME: bool = True
    LOGOUT_REDIRECT_URL: str = "/auth/login"
    AUTO_LOGOUT_INACTIVE_MINUTES: int = 60
    AUTO_LOGOUT_WARNING_MINUTES: int = 5
    
    # CORS settings (additional)
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3247"]
    
    # ===================================
    # VALIDATORS
    # ===================================
    
    @validator('SECURITY_JWE_SECRET_KEY')
    def validate_jwe_key_length(cls, v):
        if len(v) < 32:
            raise ValueError('JWE_SECRET_KEY must be at least 32 characters long')
        return v
    
    @validator('SESSION_MASTER_KEY')
    def validate_session_master_key(cls, v):
        if len(v) < 32:
            raise ValueError('SESSION_MASTER_KEY must be at least 32 characters long')
        return v
        
    @validator('TOKEN_MASTER_KEY')
    def validate_token_master_key(cls, v):
        if len(v) < 32:
            raise ValueError('TOKEN_MASTER_KEY must be at least 32 characters long')
        return v
    
    @validator('BLOCK_DURATIONS')
    def validate_block_durations(cls, v):
        if not v or len(v) == 0:
            raise ValueError('BLOCK_DURATIONS cannot be empty')
        if not all(isinstance(duration, int) and duration > 0 for duration in v):
            raise ValueError('All block durations must be positive integers')
        if sorted(v) != v:
            raise ValueError('Block durations must be in ascending order')
        return v
    
    @validator('RISK_THRESHOLD_HIGH')
    def validate_risk_thresholds(cls, v, values):
        if 'RISK_THRESHOLD_MEDIUM' in values:
            if v <= values['RISK_THRESHOLD_MEDIUM']:
                raise ValueError('RISK_THRESHOLD_HIGH must be greater than RISK_THRESHOLD_MEDIUM')
        return v
    
    @validator('ALLOWED_ORIGINS', pre=True)
    def validate_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    @validator('CORS_ORIGINS', pre=True)
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    @validator('SESSION_COOKIE_SAMESITE')
    def validate_samesite(cls, v):
        allowed_values = ['strict', 'lax', 'none']
        if v.lower() not in allowed_values:
            raise ValueError(f'SESSION_COOKIE_SAMESITE must be one of: {allowed_values}')
        return v.lower()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_redis_urls()
        self._apply_environment_overrides()
        if self.ENVIRONMENT == "development":
            print(f"[DEBUG] DB URL: {self.DB_URL}")
            print(f"[DEBUG] Redis URL: {self.redis_url}")
            print(f"[DEBUG] Redis Auth URL: {self.redis_auth_url}")
            print(f"[DEBUG] Encryption Enabled: {self.ENCRYPTION_ENABLED}")
        self._validate_environment_config()
    
    def _build_redis_urls(self):
        """Construir URLs de Redis dinámicamente"""
        if self.REDIS_PASSWORD:
            self.redis_url = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            self.redis_auth_url = f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_AUTH_DB}"
        else:
            self.redis_url = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            self.redis_auth_url = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_AUTH_DB}"
        
        self.REDIS_URL = self.redis_url
    
    def _apply_environment_overrides(self):
        """Apply environment-specific configuration overrides"""
        if self.ENVIRONMENT == "production":
            self.DEBUG = False
            self.FEATURE_ENABLE_API_DOCS = False
            self.SECURITY_COOKIE_SECURE = True
            self.SECURITY_COOKIE_SAMESITE = "strict"
            self.LOG_SENSITIVE_DATA = False
            self.RISK_THRESHOLD_HIGH = 60
            self.FORCE_2FA_HIGH_RISK = True
            
        elif self.ENVIRONMENT == "staging":
            self.DEBUG = False
            self.FEATURE_ENABLE_API_DOCS = True
            self.LOG_SENSITIVE_DATA = False
            
        elif self.ENVIRONMENT == "testing":
            self.DB_ECHO = False
            self.FEATURE_ENABLE_EMAIL_VERIFICATION = False
            self.IP_MAX_ATTEMPTS = 50
            self.USER_MAX_ATTEMPTS = 20
            self.LOG_SENSITIVE_DATA = True
    
    def _validate_environment_config(self):
        """Validate configuration based on environment"""
        if self.ENVIRONMENT == "production":
            required_vars = [
                ("DB_URL", self.DB_URL),
                ("REDIS_HOST", self.REDIS_HOST),
                ("SECURITY_SECRET_KEY", self.SECURITY_SECRET_KEY),
                ("SECURITY_JWT_SECRET_KEY", self.SECURITY_JWT_SECRET_KEY),
                ("SECURITY_JWE_SECRET_KEY", self.SECURITY_JWE_SECRET_KEY),
                ("SESSION_MASTER_KEY", self.SESSION_MASTER_KEY),
                ("TOKEN_MASTER_KEY", self.TOKEN_MASTER_KEY),
            ]
            
            missing_vars = []
            for var_name, var_value in required_vars:
                if not var_value:
                    missing_vars.append(var_name)
            
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # ===================================
    # COMPATIBILITY PROPERTIES
    # ===================================
    
    @property
    def database(self):
        """Compatibility property for database settings"""
        return type('DatabaseSettings', (), {
            'URL': self.DB_URL,
            'ECHO': self.DB_ECHO,
            'POOL_SIZE': self.DB_POOL_SIZE,
            'MAX_OVERFLOW': self.DB_MAX_OVERFLOW,
            'POOL_TIMEOUT': self.DB_POOL_TIMEOUT,
            'POOL_RECYCLE': self.DB_POOL_RECYCLE,
        })()
    
    @property
    def redis(self):
        """Compatibility property for redis settings"""
        return type('RedisSettings', (), {
            'URL': self.REDIS_URL,
            'KEY_PREFIX': self.REDIS_KEY_PREFIX,
            'TTL': self.REDIS_TTL,
            'MAX_CONNECTIONS': self.REDIS_MAX_CONNECTIONS,
        })()
    
    @property
    def security(self):
        """Compatibility property for security settings"""
        return type('SecuritySettings', (), {
            'SECRET_KEY': self.SECURITY_SECRET_KEY,
            'JWT_SECRET_KEY': self.SECURITY_JWT_SECRET_KEY,
            'JWT_ALGORITHM': self.SECURITY_JWT_ALGORITHM,
            'JWT_EXPIRE_MINUTES': self.SECURITY_JWT_EXPIRE_MINUTES,
            'JWT_REFRESH_EXPIRE_DAYS': self.SECURITY_JWT_REFRESH_EXPIRE_DAYS,
            'JWE_SECRET_KEY': self.SECURITY_JWE_SECRET_KEY,
            'JWE_ALGORITHM': self.SECURITY_JWE_ALGORITHM,
            'COOKIE_SECURE': self.SECURITY_COOKIE_SECURE,
            'COOKIE_SAMESITE': self.SECURITY_COOKIE_SAMESITE,
            'COOKIE_HTTPONLY': self.SECURITY_COOKIE_HTTPONLY,
            'COOKIE_MAX_AGE': self.SECURITY_COOKIE_MAX_AGE,
            'BCRYPT_ROUNDS': self.SECURITY_BCRYPT_ROUNDS,
            'RATE_LIMIT_ENABLED': self.SECURITY_RATE_LIMIT_ENABLED,
            'RATE_LIMIT_REQUESTS': self.SECURITY_RATE_LIMIT_REQUESTS,
            'RATE_LIMIT_WINDOW': self.SECURITY_RATE_LIMIT_WINDOW,
        })()
    
    @property
    def storage(self):
        """Compatibility property for storage settings"""
        return type('StorageSettings', (), {
            'UPLOAD_DIR': self.STORAGE_UPLOAD_DIR,
            'STATIC_DIR': self.STORAGE_STATIC_DIR,
            'ORIGINAL_DIR': self.STORAGE_ORIGINAL_DIR,
            'PROCESSED_DIR': self.STORAGE_PROCESSED_DIR,
            'THUMBNAILS_DIR': self.STORAGE_THUMBNAILS_DIR,
            'TEMP_DIR': self.STORAGE_TEMP_DIR,
            'MAX_UPLOAD_SIZE': self.STORAGE_MAX_UPLOAD_SIZE,
            'MAX_IMAGE_SIZE': self.STORAGE_MAX_IMAGE_SIZE,
            'MAX_VIDEO_SIZE': self.STORAGE_MAX_VIDEO_SIZE,
            'IMAGE_QUALITY': self.STORAGE_IMAGE_QUALITY,
            'WATERMARK_ENABLED': self.STORAGE_WATERMARK_ENABLED,
            'ALLOWED_IMAGE_EXTENSIONS': ["jpg", "jpeg", "png", "webp", "gif", "avif", "heic"],
            'ALLOWED_VIDEO_EXTENSIONS': ["mp4", "mov", "avi", "mkv", "webm"],
            'ALLOWED_DOCUMENT_EXTENSIONS': ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
            'THUMBNAIL_SIZE': (300, 300),
        })()
    
    @property
    def email(self):
        """Compatibility property for email settings"""
        return type('EmailSettings', (), {
            'FALLBACK_SMTP_HOST': self.EMAIL_FALLBACK_SMTP_HOST,
            'FALLBACK_SMTP_PORT': self.EMAIL_FALLBACK_SMTP_PORT,
            'FALLBACK_SMTP_TLS': self.EMAIL_FALLBACK_SMTP_TLS,
            'FALLBACK_FROM_EMAIL': self.EMAIL_FALLBACK_FROM_EMAIL,
            'TEMPLATE_DIR': self.EMAIL_TEMPLATE_DIR,
        })()
    
    @property
    def features(self):
        """Compatibility property for features settings"""
        return type('FeatureFlagsSettings', (), {
            'ENABLE_REGISTRATION': self.FEATURE_ENABLE_REGISTRATION,
            'ENABLE_EMAIL_VERIFICATION': self.FEATURE_ENABLE_EMAIL_VERIFICATION,
            'ENABLE_PASSWORD_RESET': self.FEATURE_ENABLE_PASSWORD_RESET,
            'ENABLE_MAINTENANCE_MODE': self.FEATURE_ENABLE_MAINTENANCE_MODE,
            'ENABLE_API_DOCS': self.FEATURE_ENABLE_API_DOCS,
            'ENABLE_CORS': self.FEATURE_ENABLE_CORS,
            'ENABLE_RATE_LIMITING': self.FEATURE_ENABLE_RATE_LIMITING,
        })()
    
    @property
    def external(self):
        """Compatibility property for external services settings"""
        return type('ExternalServicesSettings', (), {
            'YOUTUBE_API_KEY': None,
            'AWS_ACCESS_KEY_ID': None,
            'AWS_SECRET_ACCESS_KEY': None,
            'AWS_REGION': "us-east-1",
            'AWS_S3_BUCKET': None,
            'GOOGLE_ANALYTICS_ID': None,
        })()
    
    # ===================================
    # AUTH PROPERTIES
    # ===================================
    
    @property
    def auth_encryption(self):
        """Auth encryption configuration"""
        return type('AuthEncryptionSettings', (), {
            'SESSION_MASTER_KEY': self.SESSION_MASTER_KEY,
            'TOKEN_MASTER_KEY': self.TOKEN_MASTER_KEY,
            'SESSION_ENCRYPTION_SALT': self.SESSION_ENCRYPTION_SALT,
            'TOKEN_ENCRYPTION_SALT': self.TOKEN_ENCRYPTION_SALT,
            'ENCRYPTION_ENABLED': self.ENCRYPTION_ENABLED,
            'KEY_ROTATION_ENABLED': self.KEY_ROTATION_ENABLED,
            'KEY_ROTATION_DAYS': self.KEY_ROTATION_DAYS,
        })()
    
    @property
    def auth_rate_limiting(self):
        """Auth rate limiting configuration"""
        return type('AuthRateLimitSettings', (), {
            'IP_MAX_ATTEMPTS': self.IP_MAX_ATTEMPTS,
            'IP_WINDOW_MINUTES': self.IP_WINDOW_MINUTES,
            'IP_BLOCK_ESCALATION': self.IP_BLOCK_ESCALATION,
            'USER_MAX_ATTEMPTS': self.USER_MAX_ATTEMPTS,
            'USER_WINDOW_MINUTES': self.USER_WINDOW_MINUTES,
            'USER_BLOCK_ESCALATION': self.USER_BLOCK_ESCALATION,
            'GLOBAL_MAX_ATTEMPTS': self.GLOBAL_MAX_ATTEMPTS,
            'GLOBAL_WINDOW_MINUTES': self.GLOBAL_WINDOW_MINUTES,
            'BLOCK_DURATIONS': self.BLOCK_DURATIONS,
            'MAX_BLOCK_DURATION': self.MAX_BLOCK_DURATION,
            'BLOCK_RESET_HOURS': self.BLOCK_RESET_HOURS,
        })()
    
    @property
    def auth_risk_analysis(self):
        """Auth risk analysis configuration"""
        return type('AuthRiskAnalysisSettings', (), {
            'RISK_THRESHOLD_LOW': self.RISK_THRESHOLD_LOW,
            'RISK_THRESHOLD_MEDIUM': self.RISK_THRESHOLD_MEDIUM,
            'RISK_THRESHOLD_HIGH': self.RISK_THRESHOLD_HIGH,
            'RISK_WEIGHT_FAILED_ATTEMPTS': self.RISK_WEIGHT_FAILED_ATTEMPTS,
            'RISK_WEIGHT_NEW_LOCATION': self.RISK_WEIGHT_NEW_LOCATION,
            'RISK_WEIGHT_NEW_DEVICE': self.RISK_WEIGHT_NEW_DEVICE,
            'RISK_WEIGHT_UNUSUAL_TIME': self.RISK_WEIGHT_UNUSUAL_TIME,
            'RISK_WEIGHT_SUSPICIOUS_IP': self.RISK_WEIGHT_SUSPICIOUS_IP,
            'RISK_WEIGHT_BOT_BEHAVIOR': self.RISK_WEIGHT_BOT_BEHAVIOR,
            'LOCATION_CHANGE_DETECTION': self.LOCATION_CHANGE_DETECTION,
            'LOCATION_RADIUS_KM': self.LOCATION_RADIUS_KM,
        })()
    
    @property
    def auth_sessions(self):
        """Auth session management configuration"""
        return type('AuthSessionSettings', (), {
            'SESSION_DURATION_HOURS': self.SESSION_DURATION_HOURS,
            'SESSION_DURATION_INTERNAL_HOURS': self.SESSION_DURATION_INTERNAL_HOURS,
            'SESSION_DURATION_INSTITUTIONAL_HOURS': self.SESSION_DURATION_INSTITUTIONAL_HOURS,
            'SESSION_DURATION_REMEMBER_ME_DAYS': self.SESSION_DURATION_REMEMBER_ME_DAYS,
            'SESSION_EXTENSION_MAX_HOURS': self.SESSION_EXTENSION_MAX_HOURS,
            'SESSION_CLEANUP_INTERVAL_HOURS': self.SESSION_CLEANUP_INTERVAL_HOURS,
            'SESSION_AUTO_EXTEND': self.SESSION_AUTO_EXTEND,
            'SESSION_EXTEND_THRESHOLD_MINUTES': self.SESSION_EXTEND_THRESHOLD_MINUTES,
            'MAX_CONCURRENT_SESSIONS_INTERNAL': self.MAX_CONCURRENT_SESSIONS_INTERNAL,
            'MAX_CONCURRENT_SESSIONS_INSTITUTIONAL': self.MAX_CONCURRENT_SESSIONS_INSTITUTIONAL,
            'TEMP_SESSION_DURATION_MINUTES': self.TEMP_SESSION_DURATION_MINUTES,
            'TEMP_SESSION_MAX_ATTEMPTS': self.TEMP_SESSION_MAX_ATTEMPTS,
        })()
    
    @property
    def auth_tokens(self):
        """Auth token configuration"""
        return type('AuthTokenSettings', (), {
            'ACCESS_TOKEN_DURATION_MINUTES': self.ACCESS_TOKEN_DURATION_MINUTES,
            'ACCESS_TOKEN_ALGORITHM': self.ACCESS_TOKEN_ALGORITHM,
            'ACCESS_TOKEN_ENCRYPTION': self.ACCESS_TOKEN_ENCRYPTION,
            'REFRESH_TOKEN_DURATION_DAYS': self.REFRESH_TOKEN_DURATION_DAYS,
            'REFRESH_TOKEN_ROTATION': self.REFRESH_TOKEN_ROTATION,
            'REFRESH_TOKEN_ROTATION_THRESHOLD_DAYS': self.REFRESH_TOKEN_ROTATION_THRESHOLD_DAYS,
        })()
    
    @property
    def auth_2fa(self):
        """Auth 2FA configuration"""
        return type('Auth2FASettings', (), {
            'FORCE_2FA_FOR_ADMIN': self.FORCE_2FA_FOR_ADMIN,
            'FORCE_2FA_HIGH_RISK': self.FORCE_2FA_HIGH_RISK,
            'TOTP_WINDOW_SECONDS': self.TOTP_WINDOW_SECONDS,
            'TOTP_DIGITS': self.TOTP_DIGITS,
            'TOTP_ALGORITHM': self.TOTP_ALGORITHM,
            'BACKUP_CODES_COUNT': self.BACKUP_CODES_COUNT,
            'BACKUP_CODES_LENGTH': self.BACKUP_CODES_LENGTH,
            'BACKUP_CODES_EXPIRY_DAYS': self.BACKUP_CODES_EXPIRY_DAYS,
        })()
    
    @property
    def auth_monitoring(self):
        """Auth security monitoring configuration"""
        return type('AuthMonitoringSettings', (), {
            'LOG_ALL_LOGIN_ATTEMPTS': self.LOG_ALL_LOGIN_ATTEMPTS,
            'LOG_SECURITY_EVENTS': self.LOG_SECURITY_EVENTS,
            'LOG_SENSITIVE_DATA': self.LOG_SENSITIVE_DATA,
            'ALERT_ON_SUSPICIOUS_ACTIVITY': self.ALERT_ON_SUSPICIOUS_ACTIVITY,
            'ALERT_ON_MULTIPLE_FAILURES': self.ALERT_ON_MULTIPLE_FAILURES,
            'ALERT_THRESHOLD_FAILURES': self.ALERT_THRESHOLD_FAILURES,
            'LOGIN_HISTORY_RETENTION_DAYS': self.LOGIN_HISTORY_RETENTION_DAYS,
            'SECURITY_EVENTS_RETENTION_DAYS': self.SECURITY_EVENTS_RETENTION_DAYS,
            'FAILED_ATTEMPTS_RETENTION_HOURS': self.FAILED_ATTEMPTS_RETENTION_HOURS,
        })()
    
    @property
    def auth_devices(self):
        """Auth device trust configuration"""
        return type('AuthDeviceSettings', (), {
            'DEVICE_TRUST_ENABLED': self.DEVICE_TRUST_ENABLED,
            'DEVICE_TRUST_DURATION_DAYS': self.DEVICE_TRUST_DURATION_DAYS,
            'DEVICE_FINGERPRINT_REQUIRED': self.DEVICE_FINGERPRINT_REQUIRED,
        })()
    
    @property
    def auth_passwords(self):
        """Auth password policy configuration"""
        return type('AuthPasswordSettings', (), {
            'PASSWORD_MIN_LENGTH': self.PASSWORD_MIN_LENGTH,
            'PASSWORD_MAX_LENGTH': self.PASSWORD_MAX_LENGTH,
            'PASSWORD_REQUIRE_UPPERCASE': self.PASSWORD_REQUIRE_UPPERCASE,
            'PASSWORD_REQUIRE_LOWERCASE': self.PASSWORD_REQUIRE_LOWERCASE,
            'PASSWORD_REQUIRE_DIGITS': self.PASSWORD_REQUIRE_DIGITS,
            'PASSWORD_REQUIRE_SPECIAL_CHARS': self.PASSWORD_REQUIRE_SPECIAL_CHARS,
            'PASSWORD_HISTORY_COUNT': self.PASSWORD_HISTORY_COUNT,
            'PASSWORD_MAX_AGE_DAYS': self.PASSWORD_MAX_AGE_DAYS,
        })()
    
    @property
    def auth_oauth(self):
        """Auth OAuth configuration"""
        return type('AuthOAuthSettings', (), {
            'OAUTH_GOOGLE_ENABLED': self.OAUTH_GOOGLE_ENABLED,
            'OAUTH_MICROSOFT_ENABLED': self.OAUTH_MICROSOFT_ENABLED,
            'OAUTH_GITHUB_ENABLED': self.OAUTH_GITHUB_ENABLED,
            'OAUTH_CALLBACK_BASE_URL': self.OAUTH_CALLBACK_BASE_URL,
            'GOOGLE_CLIENT_ID': self.GOOGLE_CLIENT_ID,
            'GOOGLE_CLIENT_SECRET': self.GOOGLE_CLIENT_SECRET,
            'GOOGLE_REDIRECT_URI': self.GOOGLE_REDIRECT_URI,
            'MICROSOFT_CLIENT_ID': self.MICROSOFT_CLIENT_ID,
            'MICROSOFT_CLIENT_SECRET': self.MICROSOFT_CLIENT_SECRET,
            'MICROSOFT_REDIRECT_URI': self.MICROSOFT_REDIRECT_URI,
        })()
    
    # ===================================
    # LEGACY AUTH PROPERTIES (COMPATIBILITY)
    # ===================================
    
    @property
    def auth(self):
        """Legacy auth configuration settings for backward compatibility"""
        return type('AuthSettings', (), {
            # Rate limiting (legacy names)
            'MAX_LOGIN_ATTEMPTS_PER_IP': self.IP_MAX_ATTEMPTS,
            'MAX_LOGIN_ATTEMPTS_PER_USER': self.USER_MAX_ATTEMPTS,
            'RATE_LIMIT_WINDOW_MINUTES': self.IP_WINDOW_MINUTES,
            
            # Session management (legacy names)
            'SESSION_TIMEOUT_HOURS': self.SESSION_DURATION_HOURS,
            'MAX_CONCURRENT_SESSIONS': self.MAX_CONCURRENT_SESSIONS_INTERNAL,
            'TEMP_2FA_SESSION_MINUTES': self.TEMP_SESSION_DURATION_MINUTES,
            
            # Security thresholds (legacy names)
            'HIGH_RISK_THRESHOLD': self.RISK_THRESHOLD_HIGH,
            'REQUIRE_2FA_THRESHOLD': self.RISK_THRESHOLD_MEDIUM,
            'SUSPICIOUS_THRESHOLD': self.RISK_THRESHOLD_HIGH,
            
            # Password policies (legacy names)
            'PASSWORD_MIN_LENGTH': self.PASSWORD_MIN_LENGTH,
            'PASSWORD_REQUIRE_UPPERCASE': self.PASSWORD_REQUIRE_UPPERCASE,
            'PASSWORD_REQUIRE_LOWERCASE': self.PASSWORD_REQUIRE_LOWERCASE,
            'PASSWORD_REQUIRE_NUMBERS': self.PASSWORD_REQUIRE_DIGITS,
            'PASSWORD_REQUIRE_SPECIAL': self.PASSWORD_REQUIRE_SPECIAL_CHARS,
            
            # 2FA configuration (legacy names)
            '2FA_ISSUER_NAME': self.SECURITY_TOTP_ISSUER,
            '2FA_CODE_VALIDITY_SECONDS': self.TOTP_WINDOW_SECONDS,
            'BACKUP_CODES_COUNT': self.BACKUP_CODES_COUNT,
            
            # Device trust (legacy names)
            'DEVICE_TRUST_DAYS': self.DEVICE_TRUST_DURATION_DAYS,
            'NEW_DEVICE_REQUIRES_2FA': True,
            'NEW_LOCATION_REQUIRES_2FA': True,
        })()
    
    # ===================================
    # CONVENIENCE PROPERTIES
    # ===================================
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"
    
    @property
    def is_staging(self) -> bool:
        return self.ENVIRONMENT == "staging"
    
    @property
    def auth_encryption_enabled(self) -> bool:
        """Check if auth encryption is enabled"""
        return self.ENCRYPTION_ENABLED and len(self.SESSION_MASTER_KEY) >= 32
    
    @property
    def redis_auth_config(self) -> dict:
        """Redis configuration for auth module"""
        return {
            'host': self.REDIS_HOST,
            'port': self.REDIS_PORT,
            'password': self.REDIS_PASSWORD,
            'db': self.REDIS_AUTH_DB,
            'timeout': self.REDIS_TIMEOUT,
            'max_connections': self.REDIS_MAX_CONNECTIONS,
            'url': self.redis_auth_url
        }


# Instancia global de configuración
_settings = None

def get_settings() -> Settings:
    """Get cached settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


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