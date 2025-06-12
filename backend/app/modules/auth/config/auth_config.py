# backend/app/modules/auth/config/auth_config.py
"""
Auth Configuration - Configuración específica de autenticación
"""
from typing import Dict, Any, List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from datetime import timedelta


class AuthConfig(BaseSettings):
    """Configuración de autenticación para el módulo"""
    
    # ===================================
    # GENERAL AUTH SETTINGS
    # ===================================
    
    # Modo de desarrollo vs producción
    AUTH_DEBUG_MODE: bool = False
    AUTH_STRICT_MODE: bool = True
    
    # URLs y dominios permitidos
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3247"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # ===================================
    # LOGIN SETTINGS
    # ===================================
    
    # Métodos de identificación permitidos
    ALLOW_EMAIL_LOGIN: bool = True
    ALLOW_USERNAME_LOGIN: bool = True
    CASE_SENSITIVE_LOGIN: bool = False
    
    # Políticas de login
    REQUIRE_EMAIL_VERIFICATION: bool = True
    REQUIRE_PHONE_VERIFICATION: bool = False
    
    # ===================================
    # SESSION SETTINGS
    # ===================================
      # Configuración de cookies
    SESSION_COOKIE_NAME: str = "medialab_session"
    SESSION_COOKIE_SECURE: bool = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"
    SESSION_COOKIE_DOMAIN: Optional[str] = None  # Auto-detect
    
    # Duración de sesiones por tipo de usuario
    SESSION_DURATION_INTERNAL_HOURS: int = 8  # Staff interno
    SESSION_DURATION_INSTITUTIONAL_HOURS: int = 4  # Clientes
    SESSION_DURATION_REMEMBER_ME_DAYS: int = 30  # "Recordarme"
    
    # Extensión automática de sesiones
    SESSION_AUTO_EXTEND: bool = True
    SESSION_EXTEND_THRESHOLD_MINUTES: int = 30  # Extender si quedan menos de 30min
    
    # ===================================
    # LOGOUT SETTINGS
    # ===================================
    
    # Comportamiento de logout
    LOGOUT_REVOKE_ALL_SESSIONS: bool = False  # Solo sesión actual por defecto
    LOGOUT_CLEAR_REMEMBER_ME: bool = True
    LOGOUT_REDIRECT_URL: str = "/auth/login"
    
    # Logout automático
    AUTO_LOGOUT_INACTIVE_MINUTES: int = 60  # 1 hora de inactividad
    AUTO_LOGOUT_WARNING_MINUTES: int = 5   # Avisar 5min antes
    
    # ===================================
    # INVITATION SYSTEM
    # ===================================
    
    # Configuración de invitaciones
    INVITATION_SYSTEM_ENABLED: bool = True
    INVITATION_EXPIRE_DAYS: int = 7
    INVITATION_MAX_USES: int = 1
    INVITATION_REQUIRE_APPROVAL: bool = True
    
    # Email de invitaciones
    INVITATION_FROM_EMAIL: str = "noreply@medialab.galileo.edu"
    INVITATION_FROM_NAME: str = "MediaLab Universidad Galileo"
    
    # ===================================
    # OAUTH SETTINGS
    # ===================================
    
    # Proveedores OAuth habilitados
    OAUTH_GOOGLE_ENABLED: bool = False
    OAUTH_MICROSOFT_ENABLED: bool = False
    OAUTH_GITHUB_ENABLED: bool = False
    
    # URLs de callback OAuth
    OAUTH_CALLBACK_BASE_URL: str = "http://localhost:3247"
    
    # Configuración Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "/auth/oauth/google/callback"
    
    # Configuración Microsoft OAuth
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_REDIRECT_URI: str = "/auth/oauth/microsoft/callback"
    
    # ===================================
    # ACCOUNT MANAGEMENT
    # ===================================
    
    # Activación de cuentas
    ACCOUNT_ACTIVATION_REQUIRED: bool = True
    ACCOUNT_ACTIVATION_EXPIRE_HOURS: int = 24
    
    # Recuperación de contraseña
    PASSWORD_RESET_ENABLED: bool = True
    PASSWORD_RESET_EXPIRE_HOURS: int = 2
    PASSWORD_RESET_MAX_ATTEMPTS: int = 3
    
    # Bloqueo de cuentas
    ACCOUNT_LOCKOUT_ENABLED: bool = True
    ACCOUNT_LOCKOUT_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = 30
    
    # ===================================
    # EMAIL SETTINGS
    # ===================================
    
    # Templates de email
    EMAIL_TEMPLATE_WELCOME: str = "auth/welcome.html"
    EMAIL_TEMPLATE_ACTIVATION: str = "auth/activation.html"
    EMAIL_TEMPLATE_PASSWORD_RESET: str = "auth/password_reset.html"
    EMAIL_TEMPLATE_SECURITY_ALERT: str = "auth/security_alert.html"
    
    # Configuración de envío
    SEND_WELCOME_EMAIL: bool = True
    SEND_SECURITY_ALERTS: bool = True
    SEND_LOGIN_NOTIFICATIONS: bool = False
    
    # ===================================
    # API SETTINGS
    # ===================================
    
    # Rate limiting para API
    API_RATE_LIMIT_ENABLED: bool = True
    API_RATE_LIMIT_REQUESTS: int = 100
    API_RATE_LIMIT_WINDOW_MINUTES: int = 15
    
    # Autenticación API
    API_KEY_AUTHENTICATION: bool = False
    API_BEARER_TOKEN_REQUIRED: bool = True
    
    # ===================================
    # AUDIT SETTINGS
    # ===================================
    
    # Logging de eventos
    AUDIT_LOGIN_EVENTS: bool = True
    AUDIT_LOGOUT_EVENTS: bool = True
    AUDIT_PASSWORD_CHANGES: bool = True
    AUDIT_PERMISSION_CHANGES: bool = True
    AUDIT_FAILED_ATTEMPTS: bool = True
    
    # Retención de logs
    AUDIT_RETENTION_DAYS: int = 365
    AUDIT_EXPORT_ENABLED: bool = True
    
    # ===================================
    # DEVELOPMENT SETTINGS
    # ===================================
    
    # Configuraciones para desarrollo
    DEV_ALLOW_WEAK_PASSWORDS: bool = False
    DEV_DISABLE_EMAIL_VERIFICATION: bool = False
    DEV_MOCK_EXTERNAL_SERVICES: bool = False
    
    # Testing
    TEST_USER_AUTO_ACTIVATION: bool = False
    TEST_BYPASS_RATE_LIMITING: bool = False
    
    # ===================================
    # VALIDATORS
    # ===================================
    
    @validator('SESSION_COOKIE_SAMESITE')
    def validate_samesite(cls, v):
        allowed_values = ['strict', 'lax', 'none']
        if v.lower() not in allowed_values:
            raise ValueError(f'SESSION_COOKIE_SAMESITE must be one of: {allowed_values}')
        return v.lower()
    
    @validator('SESSION_DURATION_INTERNAL_HOURS')
    def validate_session_duration(cls, v):
        if v < 1 or v > 168:  # 1 hora a 7 días
            raise ValueError('Session duration must be between 1 and 168 hours')
        return v
    
    @validator('INVITATION_EXPIRE_DAYS')
    def validate_invitation_expiry(cls, v):
        if v < 1 or v > 30:
            raise ValueError('Invitation expiry must be between 1 and 30 days')
        return v
    
    @validator('ALLOWED_ORIGINS')
    def validate_origins(cls, v):
        if not v:
            raise ValueError('At least one allowed origin must be specified')
        return v
    
    class Config:
        env_prefix = "AUTH_"
        case_sensitive = True


class SessionConfig:
    """Configuración específica para gestión de sesiones"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_session_duration(self, user_type: str, remember_me: bool = False) -> timedelta:
        """Obtiene duración de sesión según tipo de usuario"""
        
        if remember_me:
            return timedelta(days=self.auth_config.SESSION_DURATION_REMEMBER_ME_DAYS)
        
        if user_type == "internal_user":
            return timedelta(hours=self.auth_config.SESSION_DURATION_INTERNAL_HOURS)
        elif user_type == "institutional_user":
            return timedelta(hours=self.auth_config.SESSION_DURATION_INSTITUTIONAL_HOURS)
        else:
            # Default para tipos desconocidos
            return timedelta(hours=4)
    
    def get_cookie_config(self) -> Dict[str, Any]:
        """Obtiene configuración de cookies de sesión"""
        return {
            "name": self.auth_config.SESSION_COOKIE_NAME,
            "secure": self.auth_config.SESSION_COOKIE_SECURE,
            "httponly": self.auth_config.SESSION_COOKIE_HTTPONLY,
            "samesite": self.auth_config.SESSION_COOKIE_SAMESITE,
            "domain": self.auth_config.SESSION_COOKIE_DOMAIN
        }
    
    def should_auto_extend(self, session_expires_at, current_time) -> bool:
        """Determina si se debe extender automáticamente la sesión"""
        if not self.auth_config.SESSION_AUTO_EXTEND:
            return False
        
        time_remaining = session_expires_at - current_time
        threshold = timedelta(minutes=self.auth_config.SESSION_EXTEND_THRESHOLD_MINUTES)
        
        return time_remaining <= threshold


class OAuthConfig:
    """Configuración específica para OAuth"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_enabled_providers(self) -> List[str]:
        """Obtiene lista de proveedores OAuth habilitados"""
        enabled = []
        
        if self.auth_config.OAUTH_GOOGLE_ENABLED:
            enabled.append("google")
        
        if self.auth_config.OAUTH_MICROSOFT_ENABLED:
            enabled.append("microsoft")
        
        if self.auth_config.OAUTH_GITHUB_ENABLED:
            enabled.append("github")
        
        return enabled
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Obtiene configuración específica de un proveedor OAuth"""
        
        configs = {
            "google": {
                "client_id": self.auth_config.GOOGLE_CLIENT_ID,
                "client_secret": self.auth_config.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{self.auth_config.OAUTH_CALLBACK_BASE_URL}{self.auth_config.GOOGLE_REDIRECT_URI}",
                "scopes": ["openid", "email", "profile"],
                "authorization_url": "https://accounts.google.com/o/oauth2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo"
            },
            "microsoft": {
                "client_id": self.auth_config.MICROSOFT_CLIENT_ID,
                "client_secret": self.auth_config.MICROSOFT_CLIENT_SECRET,
                "redirect_uri": f"{self.auth_config.OAUTH_CALLBACK_BASE_URL}{self.auth_config.MICROSOFT_REDIRECT_URI}",
                "scopes": ["openid", "email", "profile"],
                "authorization_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                "userinfo_url": "https://graph.microsoft.com/v1.0/me"
            }
        }
        
        return configs.get(provider, {})
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Verifica si un proveedor OAuth está habilitado"""
        return provider in self.get_enabled_providers()


class AuditConfig:
    """Configuración específica para auditoría"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_audit_events(self) -> Dict[str, bool]:
        """Obtiene configuración de eventos a auditar"""
        return {
            "login_events": self.auth_config.AUDIT_LOGIN_EVENTS,
            "logout_events": self.auth_config.AUDIT_LOGOUT_EVENTS,
            "password_changes": self.auth_config.AUDIT_PASSWORD_CHANGES,
            "permission_changes": self.auth_config.AUDIT_PERMISSION_CHANGES,
            "failed_attempts": self.auth_config.AUDIT_FAILED_ATTEMPTS
        }
    
    def should_audit_event(self, event_type: str) -> bool:
        """Determina si se debe auditar un tipo de evento específico"""
        audit_events = self.get_audit_events()
        return audit_events.get(event_type, False)
    
    def get_retention_config(self) -> Dict[str, Any]:
        """Obtiene configuración de retención de logs"""
        return {
            "retention_days": self.auth_config.AUDIT_RETENTION_DAYS,
            "export_enabled": self.auth_config.AUDIT_EXPORT_ENABLED
        }


class EmailConfig:
    """Configuración específica para emails de autenticación"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_email_templates(self) -> Dict[str, str]:
        """Obtiene rutas de templates de email"""
        return {
            "welcome": self.auth_config.EMAIL_TEMPLATE_WELCOME,
            "activation": self.auth_config.EMAIL_TEMPLATE_ACTIVATION,
            "password_reset": self.auth_config.EMAIL_TEMPLATE_PASSWORD_RESET,
            "security_alert": self.auth_config.EMAIL_TEMPLATE_SECURITY_ALERT
        }
    
    def get_sender_info(self) -> Dict[str, str]:
        """Obtiene información del remitente"""
        return {
            "email": self.auth_config.INVITATION_FROM_EMAIL,
            "name": self.auth_config.INVITATION_FROM_NAME
        }
    
    def should_send_email(self, email_type: str) -> bool:
        """Determina si se debe enviar un tipo específico de email"""
        email_settings = {
            "welcome": self.auth_config.SEND_WELCOME_EMAIL,
            "security_alerts": self.auth_config.SEND_SECURITY_ALERTS,
            "login_notifications": self.auth_config.SEND_LOGIN_NOTIFICATIONS
        }
        
        return email_settings.get(email_type, False)


class InvitationConfig:
    """Configuración específica para sistema de invitaciones"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_invitation_settings(self) -> Dict[str, Any]:
        """Obtiene configuración del sistema de invitaciones"""
        return {
            "enabled": self.auth_config.INVITATION_SYSTEM_ENABLED,
            "expire_days": self.auth_config.INVITATION_EXPIRE_DAYS,
            "max_uses": self.auth_config.INVITATION_MAX_USES,
            "require_approval": self.auth_config.INVITATION_REQUIRE_APPROVAL
        }
    
    def is_invitation_system_enabled(self) -> bool:
        """Verifica si el sistema de invitaciones está habilitado"""
        return self.auth_config.INVITATION_SYSTEM_ENABLED
    
    def get_expiration_timedelta(self) -> timedelta:
        """Obtiene timedelta para expiración de invitaciones"""
        return timedelta(days=self.auth_config.INVITATION_EXPIRE_DAYS)


class DevelopmentConfig:
    """Configuración específica para desarrollo"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    def get_dev_overrides(self) -> Dict[str, bool]:
        """Obtiene configuraciones de desarrollo que sobrescriben seguridad"""
        return {
            "allow_weak_passwords": self.auth_config.DEV_ALLOW_WEAK_PASSWORDS,
            "disable_email_verification": self.auth_config.DEV_DISABLE_EMAIL_VERIFICATION,
            "mock_external_services": self.auth_config.DEV_MOCK_EXTERNAL_SERVICES,
            "auto_activate_test_users": self.auth_config.TEST_USER_AUTO_ACTIVATION,
            "bypass_rate_limiting": self.auth_config.TEST_BYPASS_RATE_LIMITING
        }
    
    def is_development_mode(self) -> bool:
        """Verifica si estamos en modo desarrollo"""
        return self.auth_config.AUTH_DEBUG_MODE
    
    def should_apply_dev_override(self, override_type: str) -> bool:
        """Determina si se debe aplicar una configuración de desarrollo"""
        if not self.is_development_mode():
            return False
        
        overrides = self.get_dev_overrides()
        return overrides.get(override_type, False)


# Instancias globales de configuración
auth_config = AuthConfig()
session_config = SessionConfig(auth_config)
oauth_config = OAuthConfig(auth_config)
audit_config = AuditConfig(auth_config)
email_config = EmailConfig(auth_config)
invitation_config = InvitationConfig(auth_config)
development_config = DevelopmentConfig(auth_config)