"""
Base User model
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base.base_model import BaseModelHybrid


class BaseUser(BaseModelHybrid):
    """
    Base class for all user types
    """
    
    __abstract__ = True
    
    # Authentication
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Personal info
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Profile
    profile_photo: Mapped[str] = mapped_column(String(500), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Settings
    preferred_language: Mapped[str] = mapped_column(String(10), nullable=False, default="es")
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="America/Guatemala")
    
    # Status (using booleans)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Activity tracking
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    login_count: Mapped[int] = mapped_column(nullable=False, default=0)
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    locked_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    password_changed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Notifications
    email_notifications: Mapped[bool] = mapped_column(nullable=False, default=True)
    sms_notifications: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    def __repr__(self) -> str:
        return f"<BaseUser(username={self.username})>"