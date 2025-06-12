# backend/app/modules/auth/exceptions/security_exceptions.py
"""
Security Exceptions - Excepciones específicas para operaciones de seguridad
"""
from typing import Optional, Dict, Any


class AuthSecurityException(Exception):
    """Excepción base para errores de seguridad en autenticación"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class EncryptionError(AuthSecurityException):
    """Error en proceso de encriptación"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="ENCRYPTION_ERROR",
            details=details
        )


class DecryptionError(AuthSecurityException):
    """Error en proceso de desencriptación"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DECRYPTION_ERROR", 
            details=details
        )


class RateLimitExceeded(AuthSecurityException):
    """Rate limit excedido"""
    
    def __init__(
        self, 
        message: str, 
        retry_after: int,
        limit_type: str = "general",
        details: Optional[Dict[str, Any]] = None
    ):
        self.retry_after = retry_after
        self.limit_type = limit_type
        
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            details={
                "retry_after": retry_after,
                "limit_type": limit_type,
                **(details or {})
            }
        )


class SuspiciousActivity(AuthSecurityException):
    """Actividad sospechosa detectada"""
    
    def __init__(
        self, 
        message: str,
        risk_score: int,
        risk_factors: list,
        details: Optional[Dict[str, Any]] = None
    ):
        self.risk_score = risk_score
        self.risk_factors = risk_factors
        
        super().__init__(
            message=message,
            error_code="SUSPICIOUS_ACTIVITY",
            details={
                "risk_score": risk_score,
                "risk_factors": risk_factors,
                **(details or {})
            }
        )


class InvalidTokenError(AuthSecurityException):
    """Token inválido o corrupto"""
    
    def __init__(self, message: str, token_type: str = "unknown"):
        self.token_type = token_type
        
        super().__init__(
            message=message,
            error_code="INVALID_TOKEN",
            details={"token_type": token_type}
        )


class TokenExpiredError(AuthSecurityException):
    """Token expirado"""
    
    def __init__(self, message: str, token_type: str = "unknown", expired_at: Optional[str] = None):
        self.token_type = token_type
        self.expired_at = expired_at
        
        super().__init__(
            message=message,
            error_code="TOKEN_EXPIRED",
            details={
                "token_type": token_type,
                "expired_at": expired_at
            }
        )


class SessionNotFoundError(AuthSecurityException):
    """Sesión no encontrada o inválida"""
    
    def __init__(self, message: str, session_id: Optional[str] = None):
        self.session_id = session_id
        
        super().__init__(
            message=message,
            error_code="SESSION_NOT_FOUND",
            details={"session_id": session_id}
        )


class AccountLockedException(AuthSecurityException):
    """Cuenta bloqueada por seguridad"""
    
    def __init__(
        self, 
        message: str, 
        locked_until: Optional[str] = None,
        lock_reason: Optional[str] = None
    ):
        self.locked_until = locked_until
        self.lock_reason = lock_reason
        
        super().__init__(
            message=message,
            error_code="ACCOUNT_LOCKED",
            details={
                "locked_until": locked_until,
                "lock_reason": lock_reason
            }
        )


class TwoFactorRequired(AuthSecurityException):
    """Autenticación de dos factores requerida"""
    
    def __init__(
        self, 
        message: str, 
        temp_session_id: str,
        expires_in: int
    ):
        self.temp_session_id = temp_session_id
        self.expires_in = expires_in
        
        super().__init__(
            message=message,
            error_code="TWO_FACTOR_REQUIRED",
            details={
                "temp_session_id": temp_session_id,
                "expires_in": expires_in
            }
        )


class InvalidTwoFactorCode(AuthSecurityException):
    """Código 2FA inválido"""
    
    def __init__(self, message: str, attempts_remaining: Optional[int] = None):
        self.attempts_remaining = attempts_remaining
        
        super().__init__(
            message=message,
            error_code="INVALID_2FA_CODE",
            details={"attempts_remaining": attempts_remaining}
        )


class SecurityConfigurationError(AuthSecurityException):
    """Error en configuración de seguridad"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        self.config_key = config_key
        
        super().__init__(
            message=message,
            error_code="SECURITY_CONFIG_ERROR",
            details={"config_key": config_key}
        )