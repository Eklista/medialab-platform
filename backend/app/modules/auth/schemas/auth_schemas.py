# backend/app/modules/auth/schemas/auth_schemas.py
"""
Auth schemas para validación de endpoints
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


# ===================================
# LOGIN SCHEMAS
# ===================================

class LoginRequest(BaseModel):
    """Schema para request de login"""
    identifier: str = Field(..., min_length=3, max_length=150, description="Username o email")
    password: str = Field(..., min_length=1, max_length=128, description="Password")
    remember_me: bool = Field(default=False, description="Mantener sesión por más tiempo")
    device_name: Optional[str] = Field(None, max_length=100, description="Nombre del dispositivo")


class LoginResponse(BaseModel):
    """Schema para response de login"""
    success: bool
    message: str
    
    # En caso de login exitoso
    user_id: Optional[int] = None
    user_type: Optional[str] = None
    session_id: Optional[str] = None
    expires_at: Optional[str] = None
    
    # En caso de requerir 2FA
    temp_session_id: Optional[str] = None
    requires_2fa: bool = False
    expires_in: Optional[int] = None  # segundos
    
    # Métricas
    response_time_ms: Optional[int] = None


# ===================================
# 2FA SCHEMAS
# ===================================

class TwoFactorRequest(BaseModel):
    """Schema para request de 2FA"""
    temp_session_id: str = Field(..., description="ID de sesión temporal")
    code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$', description="Código TOTP de 6 dígitos")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError('El código debe contener solo dígitos')
        return v


class TwoFactorResponse(BaseModel):
    """Schema para response de 2FA"""
    success: bool
    message: str
    
    # En caso exitoso
    user_id: Optional[int] = None
    user_type: Optional[str] = None
    session_id: Optional[str] = None
    expires_at: Optional[str] = None


# ===================================
# SESSION SCHEMAS
# ===================================

class SessionResponse(BaseModel):
    """Schema para response de validación de sesión"""
    valid: bool
    message: Optional[str] = None
    
    # Si la sesión es válida
    user_id: Optional[int] = None
    user_type: Optional[str] = None
    expires_at: Optional[str] = None
    is_2fa_verified: Optional[bool] = None


class ActiveSessionInfo(BaseModel):
    """Información de una sesión activa"""
    session_id: str
    ip_address: str
    device_name: Optional[str]
    location: Optional[str]
    created_at: str
    last_activity: str
    expires_at: str
    is_current: bool = False


class ActiveSessionsResponse(BaseModel):
    """Lista de sesiones activas del usuario"""
    sessions: List[ActiveSessionInfo]
    total_count: int


# ===================================
# LOGOUT SCHEMAS
# ===================================

class LogoutRequest(BaseModel):
    """Schema para request de logout"""
    session_id: str = Field(..., description="ID de la sesión a cerrar")


class LogoutAllRequest(BaseModel):
    """Schema para logout de todas las sesiones"""
    user_id: int = Field(..., ge=1)
    user_type: str = Field(..., pattern=r'^(internal_user|institutional_user)$')
    keep_current: bool = Field(default=True, description="Mantener sesión actual activa")


class LogoutResponse(BaseModel):
    """Schema para response de logout"""
    success: bool
    message: str


# ===================================
# SECURITY MONITORING SCHEMAS
# ===================================

class SecurityStatsResponse(BaseModel):
    """Estadísticas de seguridad en tiempo real"""
    # Redis stats (tiempo real)
    blocked_ips: int
    blocked_users: int
    active_sessions_redis: int
    
    # MySQL stats (histórico últimas 24h)
    total_attempts_24h: int
    successful_attempts_24h: int
    suspicious_attempts_24h: int
    high_risk_attempts_24h: int
    active_sessions_mysql: int
    
    # Métricas calculadas
    success_rate_24h: float
    suspicious_rate_24h: float
    
    timestamp: str


class LoginHistoryItem(BaseModel):
    """Item del historial de login"""
    timestamp: str
    ip_address: str
    location: Optional[str]
    device: Optional[str]
    success: bool
    method: str
    risk_score: int
    suspicious: bool
    failure_reason: Optional[str]


class LoginHistoryResponse(BaseModel):
    """Historial de logins del usuario"""
    login_history: List[LoginHistoryItem]
    recent_failures_count: int
    total_records: int


class RateLimitInfo(BaseModel):
    """Información de rate limiting"""
    allowed: bool
    attempts: int
    max_attempts: int
    reset_time: str
    blocked_until: Optional[str] = None


class RateLimitResponse(BaseModel):
    """Estado de rate limiting"""
    ip_rate_limit: RateLimitInfo
    user_rate_limit: RateLimitInfo


# ===================================
# DEVICE MANAGEMENT SCHEMAS
# ===================================

class DeviceInfo(BaseModel):
    """Información de dispositivo"""
    device_fingerprint: str
    device_name: str
    first_seen: str
    last_seen: str
    login_count: int
    is_trusted: bool = False


class TrustedDevicesResponse(BaseModel):
    """Lista de dispositivos de confianza"""
    devices: List[DeviceInfo]
    total_count: int


class TrustDeviceRequest(BaseModel):
    """Request para marcar dispositivo como confiable"""
    device_fingerprint: str = Field(..., description="Fingerprint del dispositivo")
    device_name: Optional[str] = Field(None, max_length=100, description="Nombre personalizado")


# ===================================
# PASSWORD CHANGE SCHEMAS
# ===================================

class PasswordChangeRequest(BaseModel):
    """Request para cambio de contraseña"""
    current_password: str = Field(..., min_length=1, description="Contraseña actual")
    new_password: str = Field(..., min_length=8, max_length=128, description="Nueva contraseña")
    confirm_password: str = Field(..., description="Confirmación de nueva contraseña")
    logout_all_sessions: bool = Field(default=True, description="Cerrar todas las demás sesiones")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('La contraseña debe contener mayúsculas, minúsculas y números')
        
        return v


class PasswordChangeResponse(BaseModel):
    """Response para cambio de contraseña"""
    success: bool
    message: str
    sessions_terminated: Optional[int] = None


# ===================================
# ACCOUNT SECURITY SCHEMAS
# ===================================

class SecurityEventItem(BaseModel):
    """Evento de seguridad"""
    timestamp: str
    event_type: str
    description: str
    ip_address: str
    location: Optional[str]
    risk_level: str  # low, medium, high
    resolved: bool = False


class SecurityEventsResponse(BaseModel):
    """Lista de eventos de seguridad"""
    events: List[SecurityEventItem]
    total_count: int
    unresolved_count: int


class AccountSecurityOverview(BaseModel):
    """Resumen de seguridad de la cuenta"""
    user_id: int
    user_type: str
    account_status: str
    has_2fa_enabled: bool
    trusted_devices_count: int
    active_sessions_count: int
    recent_login_attempts: int
    security_score: int  # 0-100
    last_security_event: Optional[str]
    recommendations: List[str]


# ===================================
# ADMIN SCHEMAS
# ===================================

class BulkSessionAction(BaseModel):
    """Acción en lote sobre sesiones"""
    action: str = Field(..., pattern=r'^(terminate|extend|trust)$')
    session_ids: List[str] = Field(..., min_items=1, max_items=100)
    reason: Optional[str] = Field(None, max_length=200)


class BulkSessionResponse(BaseModel):
    """Response de acción en lote"""
    success: bool
    processed_count: int
    failed_count: int
    errors: List[str] = []


class SystemSecurityConfig(BaseModel):
    """Configuración de seguridad del sistema"""
    max_login_attempts: int = Field(default=5, ge=1, le=20)
    lockout_duration_minutes: int = Field(default=30, ge=1, le=1440)
    session_timeout_hours: int = Field(default=24, ge=1, le=168)
    require_2fa_for_admin: bool = Field(default=True)
    password_min_length: int = Field(default=8, ge=6, le=50)
    password_require_special_chars: bool = Field(default=False)


# ===================================
# INVITATION SCHEMAS (para futuro)
# ===================================

class InvitationRequest(BaseModel):
    """Request para crear invitación"""
    email: str = Field(..., description="Email del invitado")
    target_user_type: str = Field(..., pattern=r'^(internal_user|institutional_user)$')
    expires_in_days: int = Field(default=7, ge=1, le=30)
    max_uses: int = Field(default=1, ge=1, le=10)
    message: Optional[str] = Field(None, max_length=500)
    suggested_roles: Optional[List[int]] = Field(default=[])


class InvitationResponse(BaseModel):
    """Response de invitación creada"""
    success: bool
    invitation_id: Optional[int] = None
    invitation_token: Optional[str] = None
    expires_at: Optional[str] = None
    invitation_url: Optional[str] = None