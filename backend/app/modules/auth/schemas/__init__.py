# backend/app/modules/auth/schemas/__init__.py
"""
Auth schemas for API validation and serialization
"""
from .auth_schemas import *

__all__ = [
    # Login schemas
    "LoginRequest",
    "LoginResponse",
    
    # 2FA schemas
    "TwoFactorRequest", 
    "TwoFactorResponse",
    
    # Session schemas
    "SessionResponse",
    "ActiveSessionInfo",
    "ActiveSessionsResponse",
    
    # Logout schemas
    "LogoutRequest",
    "LogoutAllRequest",
    "LogoutResponse",
    
    # Security monitoring schemas
    "SecurityStatsResponse",
    "LoginHistoryItem",
    "LoginHistoryResponse",
    "RateLimitInfo",
    "RateLimitResponse",
    
    # Device management schemas
    "DeviceInfo",
    "TrustedDevicesResponse", 
    "TrustDeviceRequest",
    
    # Password schemas
    "PasswordChangeRequest",
    "PasswordChangeResponse",
    
    # Security overview schemas
    "SecurityEventItem",
    "SecurityEventsResponse",
    "AccountSecurityOverview",
    
    # Admin schemas
    "BulkSessionAction",
    "BulkSessionResponse",
    "SystemSecurityConfig",
    
    # Invitation schemas
    "InvitationRequest",
    "InvitationResponse"
]