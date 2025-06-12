# backend/app/modules/auth/config/__init__.py
"""
Auth config module - Configuraciones para autenticación
"""

from .security_config import (
    security_config,
    rate_limit_config, 
    risk_analysis_config,
    two_factor_config,
    SecurityConfig,
    RateLimitConfig,
    RiskAnalysisConfig,
    TwoFactorConfig
)

from .auth_config import (
    auth_config,
    session_config,
    oauth_config,
    audit_config,
    email_config,
    invitation_config,
    development_config,
    AuthConfig,
    SessionConfig,
    OAuthConfig,
    AuditConfig,
    EmailConfig,
    InvitationConfig,
    DevelopmentConfig
)

__all__ = [
    # Security config instances
    "security_config",
    "rate_limit_config",
    "risk_analysis_config", 
    "two_factor_config",
    
    # Auth config instances  
    "auth_config",
    "session_config",
    "oauth_config",
    "audit_config",
    "email_config",
    "invitation_config",
    "development_config",
    
    # Security config classes
    "SecurityConfig",
    "RateLimitConfig",
    "RiskAnalysisConfig",
    "TwoFactorConfig",
    
    # Auth config classes
    "AuthConfig",
    "SessionConfig", 
    "OAuthConfig",
    "AuditConfig",
    "EmailConfig",
    "InvitationConfig",
    "DevelopmentConfig"
]