# backend/app/modules/auth/exceptions/__init__.py
"""
Auth exceptions module - Centralized exception handling for authentication
"""

# Security exceptions
from .security_exceptions import (
    AuthSecurityException,
    EncryptionError,
    DecryptionError,
    RateLimitExceeded,
    SuspiciousActivity,
    InvalidTokenError,
    TokenExpiredError,
    SessionNotFoundError,
    AccountLockedException,
    TwoFactorRequired,
    InvalidTwoFactorCode,
    SecurityConfigurationError
)

# Auth exceptions
from .auth_exceptions import (
    AuthException,
    InvalidCredentialsError,
    UserNotFoundError,
    AccountInactiveError,
    LoginAttemptError,
    SessionCreationError,
    PasswordValidationError,
    InvitationError,
    OAuthError
)

__all__ = [
    # Security exceptions
    "AuthSecurityException",
    "EncryptionError",
    "DecryptionError", 
    "RateLimitExceeded",
    "SuspiciousActivity",
    "InvalidTokenError",
    "TokenExpiredError",
    "SessionNotFoundError",
    "AccountLockedException",
    "TwoFactorRequired",
    "InvalidTwoFactorCode",
    "SecurityConfigurationError",
    
    # Auth exceptions
    "AuthException",
    "InvalidCredentialsError",
    "UserNotFoundError",
    "AccountInactiveError",
    "LoginAttemptError",
    "SessionCreationError",
    "PasswordValidationError",
    "InvitationError",
    "OAuthError"
]