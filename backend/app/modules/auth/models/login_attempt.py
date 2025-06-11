# backend/app/modules/auth/models/login_attempt.py
"""
Login Attempt model - OPTIMIZADO para eventos importantes únicamente
Solo guarda en MySQL: logins exitosos, eventos sospechosos, y cambios críticos
Los intentos fallidos van a Redis con TTL
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Index, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class LoginAttempt(BaseModelWithID):
    """
    Login Attempt model - Solo para eventos de seguridad importantes
    
    SE GUARDA EN MYSQL:
    - Logins exitosos (auditoría)
    - Intentos con risk_score > 70 (sospechosos)
    - Cambios de ubicación geográfica
    - Bloqueos de seguridad
    - Eventos de 2FA
    
    NO SE GUARDA (va a Redis):
    - Intentos fallidos normales (risk_score < 70)
    - Rate limiting básico
    - Contadores temporales
    """
    
    __tablename__ = "login_attempts"
    
    # Attempt identification
    identifier: Mapped[str] = mapped_column(String(150), nullable=False)  # email or username
    identifier_type: Mapped[str] = mapped_column(String(20), nullable=False)  # email, username
    
    # Network information
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)
    device_fingerprint: Mapped[str] = mapped_column(String(128), nullable=True)
    
    # Attempt details
    attempt_type: Mapped[str] = mapped_column(String(30), nullable=False)  # password, 2fa, oauth
    is_successful: Mapped[bool] = mapped_column(nullable=False, default=False)
    failure_reason: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # User info (si login fue exitoso o es evento importante)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_type: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Geolocation
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Security analysis
    risk_score: Mapped[int] = mapped_column(nullable=False, default=0)  # 0-100
    risk_factors: Mapped[str] = mapped_column(Text, nullable=True)  # JSON de factores de riesgo
    is_suspicious: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Flags de eventos importantes
    is_location_change: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_new_device: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_security_event: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Session info (if successful)
    session_id: Mapped[str] = mapped_column(String(128), nullable=True)
    
    # Response time (para detectar ataques automatizados)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Critical indexes for security queries
    __table_args__ = (
        Index("idx_login_attempt_identifier", "identifier"),
        Index("idx_login_attempt_ip", "ip_address"),
        Index("idx_login_attempt_successful", "is_successful"),
        Index("idx_login_attempt_time", "created_at"),
        Index("idx_login_attempt_user", "user_id", "user_type"),
        Index("idx_login_attempt_risk", "risk_score"),
        Index("idx_login_attempt_suspicious", "is_suspicious"),
        Index("idx_login_attempt_security", "is_security_event"),
        Index("idx_login_attempt_location", "is_location_change"),
        Index("idx_login_attempt_device", "is_new_device"),
        Index("idx_login_attempt_user_time", "user_id", "user_type", "created_at"),
        Index("idx_login_attempt_ip_time", "ip_address", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<LoginAttempt(identifier={self.identifier}, success={self.is_successful}, risk={self.risk_score})>"
    
    @property
    def should_save_to_mysql(self) -> bool:
        """Determina si este intento debe guardarse en MySQL"""
        return (
            self.is_successful or  # Todos los logins exitosos
            self.risk_score >= 70 or  # Intentos sospechosos
            self.is_security_event or  # Eventos de seguridad
            self.is_location_change or  # Cambios de ubicación
            self.is_new_device  # Nuevos dispositivos
        )