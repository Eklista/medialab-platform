# backend/app/modules/auth/models/auth_session.py
"""
Auth Session model - Tracks active user sessions
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class AuthSession(BaseModelWithID):
    """
    Auth Session model for tracking active user sessions
    """
    
    __tablename__ = "auth_sessions"
    
    # User relationship (polymorphic)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'internal_user' or 'institutional_user'
    
    # Session identification
    session_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    refresh_token_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    
    # Device and location info
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)  # IPv6 compatible
    device_fingerprint: Mapped[str] = mapped_column(String(128), nullable=True)
    device_name: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Session status and timing
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_activity: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Security flags
    is_2fa_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_oauth_session: Mapped[bool] = mapped_column(nullable=False, default=False)
    oauth_provider: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Session metadata
    login_method: Mapped[str] = mapped_column(String(50), nullable=False, default="password")  # password, oauth, 2fa
    session_type: Mapped[str] = mapped_column(String(20), nullable=False, default="web")  # web, mobile, api
    
    # Logout info
    logout_reason: Mapped[str] = mapped_column(String(100), nullable=True)  # manual, expired, forced, security
    logout_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Critical indexes
    __table_args__ = (
        Index("idx_auth_session_user", "user_id", "user_type"),
        Index("idx_auth_session_active", "is_active"),
        Index("idx_auth_session_expires", "expires_at"),
        Index("idx_auth_session_activity", "last_activity"),
        Index("idx_auth_session_session_id", "session_id"),
        Index("idx_auth_session_refresh_token", "refresh_token_id"),
        Index("idx_auth_session_user_active", "user_id", "user_type", "is_active"),
        Index("idx_auth_session_ip", "ip_address"),
    )
    
    def __repr__(self) -> str:
        return f"<AuthSession(user_id={self.user_id}, user_type={self.user_type}, active={self.is_active})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def extend_session(self, hours: int = 24) -> None:
        """Extend session expiration"""
        from datetime import timedelta
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        self.last_activity = datetime.utcnow()
    
    def terminate_session(self, reason: str = "manual") -> None:
        """Terminate the session"""
        self.is_active = False
        self.logout_at = datetime.utcnow()
        self.logout_reason = reason