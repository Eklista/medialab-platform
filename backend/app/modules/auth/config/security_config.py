# backend/app/modules/auth/config/security_config.py
"""
Security Configuration - Configuración centralizada de seguridad
"""
from typing import Dict, Any
from pydantic import validator
from pydantic_settings import BaseSettings
from datetime import timedelta


class SecurityConfig(BaseSettings):
    """Configuración de seguridad para el módulo de autenticación"""
    
    # ===================================
    # ENCRYPTION SETTINGS
    # ===================================
    
    # Claves maestras (deben venir de variables de entorno)
    SESSION_MASTER_KEY: str = "dev-session-key-change-in-production"
    TOKEN_MASTER_KEY: str = "dev-token-key-change-in-production"
    
    # Sales para derivación de claves
    SESSION_ENCRYPTION_SALT: str = "medialab_session_encryption_salt_v1"
    TOKEN_ENCRYPTION_SALT: str = "medialab_token_encryption_salt_v1"
    
    # Configuración de encriptación
    ENCRYPTION_ENABLED: bool = True
    ENCRYPTION_ALGORITHM: str = "Fernet"
    KEY_ROTATION_ENABLED: bool = False
    KEY_ROTATION_DAYS: int = 90
    
    # ===================================
    # RATE LIMITING SETTINGS
    # ===================================
    
    # Rate limits por IP
    IP_MAX_ATTEMPTS: int = 10
    IP_WINDOW_MINUTES: int = 15
    IP_BLOCK_ESCALATION: bool = True
    
    # Rate limits por usuario
    USER_MAX_ATTEMPTS: int = 5
    USER_WINDOW_MINUTES: int = 30
    USER_BLOCK_ESCALATION: bool = True
    
    # Rate limits globales
    GLOBAL_MAX_ATTEMPTS: int = 1000
    GLOBAL_WINDOW_MINUTES: int = 5
    
    # Duración de bloqueos (en minutos)
    BLOCK_DURATIONS: list = [15, 30, 60, 120, 240, 480]  # Escalamiento: 15min -> 8h
    MAX_BLOCK_DURATION: int = 480  # 8 horas máximo
    BLOCK_RESET_HOURS: int = 24  # Reset contador después de 24h
    
    # ===================================
    # SESSION MANAGEMENT SETTINGS
    # ===================================
    
    # Duración de sesiones
    SESSION_DURATION_HOURS: int = 24
    SESSION_EXTENSION_MAX_HOURS: int = 72
    SESSION_CLEANUP_INTERVAL_HOURS: int = 6
    
    # Sesiones temporales (2FA)
    TEMP_SESSION_DURATION_MINUTES: int = 10
    TEMP_SESSION_MAX_ATTEMPTS: int = 3
    
    # Límites de sesiones concurrentes
    MAX_CONCURRENT_SESSIONS_INTERNAL: int = 5
    MAX_CONCURRENT_SESSIONS_INSTITUTIONAL: int = 3
    
    # ===================================
    # RISK ANALYSIS SETTINGS
    # ===================================
    
    # Umbrales de riesgo
    RISK_THRESHOLD_LOW: int = 30
    RISK_THRESHOLD_MEDIUM: int = 60
    RISK_THRESHOLD_HIGH: int = 80
    
    # Factores de riesgo (pesos)
    RISK_WEIGHT_FAILED_ATTEMPTS: int = 30
    RISK_WEIGHT_NEW_LOCATION: int = 25
    RISK_WEIGHT_NEW_DEVICE: int = 20
    RISK_WEIGHT_UNUSUAL_TIME: int = 15
    RISK_WEIGHT_SUSPICIOUS_IP: int = 35
    RISK_WEIGHT_BOT_BEHAVIOR: int = 25
    
    # Configuración de ubicación
    LOCATION_CHANGE_DETECTION: bool = True
    LOCATION_RADIUS_KM: int = 50  # Radio para considerar "misma ubicación"
    
    # ===================================
    # TWO FACTOR AUTHENTICATION SETTINGS
    # ===================================
    
    # Configuración 2FA
    FORCE_2FA_FOR_ADMIN: bool = True
    FORCE_2FA_HIGH_RISK: bool = True
    TOTP_WINDOW_SECONDS: int = 30
    TOTP_DIGITS: int = 6
    TOTP_ALGORITHM: str = "SHA1"
    
    # Backup codes
    BACKUP_CODES_COUNT: int = 10
    BACKUP_CODES_LENGTH: int = 8
    BACKUP_CODES_EXPIRY_DAYS: int = 365
    
    # ===================================
    # TOKEN SETTINGS (JWE)
    # ===================================
    
    # Access tokens
    ACCESS_TOKEN_DURATION_MINUTES: int = 15
    ACCESS_TOKEN_ALGORITHM: str = "A256KW"
    ACCESS_TOKEN_ENCRYPTION: str = "A256GCM"
    
    # Refresh tokens
    REFRESH_TOKEN_DURATION_DAYS: int = 30
    REFRESH_TOKEN_ROTATION: bool = True
    REFRESH_TOKEN_ROTATION_THRESHOLD_DAYS: int = 7
    
    # ===================================
    # SECURITY MONITORING SETTINGS
    # ===================================
    
    # Logging y auditoría
    LOG_ALL_LOGIN_ATTEMPTS: bool = True
    LOG_SECURITY_EVENTS: bool = True
    LOG_SENSITIVE_DATA: bool = False  # Para desarrollo
    
    # Alertas de seguridad
    ALERT_ON_SUSPICIOUS_ACTIVITY: bool = True
    ALERT_ON_MULTIPLE_FAILURES: bool = True
    ALERT_THRESHOLD_FAILURES: int = 5
    
    # Retención de datos
    LOGIN_HISTORY_RETENTION_DAYS: int = 90
    SECURITY_EVENTS_RETENTION_DAYS: int = 365
    FAILED_ATTEMPTS_RETENTION_HOURS: int = 24
    
    # ===================================
    # DEVICE TRUST SETTINGS
    # ===================================
    
    # Dispositivos de confianza
    DEVICE_TRUST_ENABLED: bool = True
    DEVICE_TRUST_DURATION_DAYS: int = 30
    DEVICE_FINGERPRINT_REQUIRED: bool = True
    
    # ===================================
    # PASSWORD POLICY SETTINGS
    # ===================================
    
    # Políticas de contraseña
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 128
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = False
    PASSWORD_HISTORY_COUNT: int = 5  # No reutilizar últimas 5 contraseñas
    
    # ===================================
    # VALIDATORS
    # ===================================
    
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
    
    @validator('ACCESS_TOKEN_DURATION_MINUTES')
    def validate_token_duration(cls, v):
        if v < 5 or v > 60:
            raise ValueError('ACCESS_TOKEN_DURATION_MINUTES must be between 5 and 60')
        return v
    
    class Config:
        env_prefix = "AUTH_"
        case_sensitive = True


class RateLimitConfig:
    """Configuración específica para rate limiting"""
    
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config
    
    def get_rate_limits(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene configuración de rate limits"""
        return {
            'ip': {
                'max_attempts': self.security_config.IP_MAX_ATTEMPTS,
                'window_minutes': self.security_config.IP_WINDOW_MINUTES,
                'escalation_enabled': self.security_config.IP_BLOCK_ESCALATION
            },
            'user': {
                'max_attempts': self.security_config.USER_MAX_ATTEMPTS,
                'window_minutes': self.security_config.USER_WINDOW_MINUTES,
                'escalation_enabled': self.security_config.USER_BLOCK_ESCALATION
            },
            'global': {
                'max_attempts': self.security_config.GLOBAL_MAX_ATTEMPTS,
                'window_minutes': self.security_config.GLOBAL_WINDOW_MINUTES,
                'escalation_enabled': False
            }
        }
    
    def get_block_durations(self) -> list:
        """Obtiene duraciones de bloqueo escalables"""
        return self.security_config.BLOCK_DURATIONS


class RiskAnalysisConfig:
    """Configuración específica para análisis de riesgo"""
    
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config
    
    def get_risk_weights(self) -> Dict[str, int]:
        """Obtiene pesos para factores de riesgo"""
        return {
            'failed_attempts': self.security_config.RISK_WEIGHT_FAILED_ATTEMPTS,
            'new_location': self.security_config.RISK_WEIGHT_NEW_LOCATION,
            'new_device': self.security_config.RISK_WEIGHT_NEW_DEVICE,
            'unusual_time': self.security_config.RISK_WEIGHT_UNUSUAL_TIME,
            'suspicious_ip': self.security_config.RISK_WEIGHT_SUSPICIOUS_IP,
            'bot_behavior': self.security_config.RISK_WEIGHT_BOT_BEHAVIOR
        }
    
    def get_risk_thresholds(self) -> Dict[str, int]:
        """Obtiene umbrales de riesgo"""
        return {
            'low': self.security_config.RISK_THRESHOLD_LOW,
            'medium': self.security_config.RISK_THRESHOLD_MEDIUM,
            'high': self.security_config.RISK_THRESHOLD_HIGH
        }


class TwoFactorConfig:
    """Configuración específica para 2FA"""
    
    def __init__(self, security_config: SecurityConfig):
        self.security_config = security_config
    
    def get_totp_config(self) -> Dict[str, Any]:
        """Obtiene configuración TOTP"""
        return {
            'window_seconds': self.security_config.TOTP_WINDOW_SECONDS,
            'digits': self.security_config.TOTP_DIGITS,
            'algorithm': self.security_config.TOTP_ALGORITHM
        }
    
    def get_backup_codes_config(self) -> Dict[str, Any]:
        """Obtiene configuración de backup codes"""
        return {
            'count': self.security_config.BACKUP_CODES_COUNT,
            'length': self.security_config.BACKUP_CODES_LENGTH,
            'expiry_days': self.security_config.BACKUP_CODES_EXPIRY_DAYS
        }
    
    def should_require_2fa(
        self, 
        user_type: str, 
        risk_score: int, 
        is_new_location: bool = False, 
        is_new_device: bool = False
    ) -> bool:
        """Determina si se requiere 2FA basado en configuración"""
        
        # Admin siempre requiere 2FA
        if user_type == 'internal_user' and self.security_config.FORCE_2FA_FOR_ADMIN:
            return True
        
        # Alto riesgo requiere 2FA
        if risk_score >= self.security_config.RISK_THRESHOLD_HIGH and self.security_config.FORCE_2FA_HIGH_RISK:
            return True
        
        # Nueva ubicación o dispositivo
        if is_new_location or is_new_device:
            return True
        
        return False


# Instancia global de configuración
security_config = SecurityConfig()
rate_limit_config = RateLimitConfig(security_config)
risk_analysis_config = RiskAnalysisConfig(security_config)
two_factor_config = TwoFactorConfig(security_config)