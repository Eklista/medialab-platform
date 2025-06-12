# backend/app/modules/auth/exceptions/auth_exceptions.py
"""
Auth Exceptions - Excepciones específicas para operaciones de autenticación
"""
from typing import Optional, Dict, Any


class AuthException(Exception):
    """Excepción base para errores de autenticación"""
    
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


class InvalidCredentialsError(AuthException):
    """Credenciales inválidas"""
    
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(
            message=message,
            error_code="INVALID_CREDENTIALS"
        )


class UserNotFoundError(AuthException):
    """Usuario no encontrado"""
    
    def __init__(self, identifier: str):
        super().__init__(
            message=f"User not found: {identifier}",
            error_code="USER_NOT_FOUND",
            details={"identifier": identifier}
        )


class AccountInactiveError(AuthException):
    """Cuenta inactiva"""
    
    def __init__(self, user_id: int, user_type: str):
        super().__init__(
            message="Account is not active",
            error_code="ACCOUNT_INACTIVE",
            details={
                "user_id": user_id,
                "user_type": user_type
            }
        )


class LoginAttemptError(AuthException):
    """Error en intento de login"""
    
    def __init__(
        self, 
        message: str, 
        failure_reason: str,
        user_id: Optional[int] = None
    ):
        self.failure_reason = failure_reason
        
        super().__init__(
            message=message,
            error_code="LOGIN_ATTEMPT_FAILED",
            details={
                "failure_reason": failure_reason,
                "user_id": user_id
            }
        )


class SessionCreationError(AuthException):
    """Error al crear sesión"""
    
    def __init__(self, message: str, user_id: int):
        super().__init__(
            message=message,
            error_code="SESSION_CREATION_ERROR",
            details={"user_id": user_id}
        )


class PasswordValidationError(AuthException):
    """Error en validación de contraseña"""
    
    def __init__(self, message: str, validation_errors: list):
        self.validation_errors = validation_errors
        
        super().__init__(
            message=message,
            error_code="PASSWORD_VALIDATION_ERROR",
            details={"validation_errors": validation_errors}
        )


class InvitationError(AuthException):
    """Error relacionado con invitaciones"""
    
    def __init__(
        self, 
        message: str, 
        invitation_token: Optional[str] = None,
        reason: Optional[str] = None
    ):
        self.invitation_token = invitation_token
        self.reason = reason
        
        super().__init__(
            message=message,
            error_code="INVITATION_ERROR",
            details={
                "invitation_token": invitation_token,
                "reason": reason
            }
        )


class OAuthError(AuthException):
    """Error en autenticación OAuth"""
    
    def __init__(
        self, 
        message: str, 
        provider: str,
        oauth_error: Optional[str] = None
    ):
        self.provider = provider
        self.oauth_error = oauth_error
        
        super().__init__(
            message=message,
            error_code="OAUTH_ERROR",
            details={
                "provider": provider,
                "oauth_error": oauth_error
            }
        )