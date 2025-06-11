# backend/app/modules/auth/models/login_attempt.py
"""
Login Attempt model - Tracks login attempts for security
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelWithID


class LoginAttempt(BaseModelWithID):
    """
    Login Attempt model for tracking authentication attempts
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
    
    # User info (if login was successful)
    user_id: Mapped[int] = mapped_column(nullable=True)
    user_type: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Geolocation (optional)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Security flags
    is_suspicious: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_blocked: Mapped[bool] = mapped_column(nullable=False, default=False)
    risk_score: Mapped[int] = mapped_column(nullable=False, default=0)  # 0-100
    
    # Session info (if successful)
    session_id: Mapped[str] = mapped_column(String(128), nullable=True)
    
    # Critical indexes for security queries
    __table_args__ = (
        Index("idx_login_attempt_identifier", "identifier"),
        Index("idx_login_attempt_ip", "ip_address"),
        Index("idx_login_attempt_successful", "is_successful"),
        Index("idx_login_attempt_time", "created_at"),
        Index("idx_login_attempt_ip_time", "ip_address", "created_at"),
        Index("idx_login_attempt_identifier_time", "identifier", "created_at"),
        Index("idx_login_attempt_suspicious", "is_suspicious"),
        Index("idx_login_attempt_blocked", "is_blocked"),
        Index("idx_login_attempt_user", "user_id", "user_type"),
    )
    
    def __repr__(self) -> str:
        return f"<LoginAttempt(identifier={self.identifier}, success={self.is_successful})>"