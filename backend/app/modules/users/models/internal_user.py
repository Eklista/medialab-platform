"""
Internal User model - Completely independent
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelHybrid


class InternalUser(BaseModelHybrid):
    """
    Internal User model for MediaLab staff - Completely independent
    """
    
    __tablename__ = "internal_users"
    
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
    banner_photo: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Settings
    preferred_language: Mapped[str] = mapped_column(String(10), nullable=False, default="es")
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="America/Guatemala")
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    account_locked: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Employee info
    employee_id: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    position: Mapped[str] = mapped_column(String(100), nullable=True)
    can_access_dashboard: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Activity tracking
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_activity: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    login_count: Mapped[int] = mapped_column(nullable=False, default=0)
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    locked_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    password_changed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Notifications
    email_notifications: Mapped[bool] = mapped_column(nullable=False, default=True)
    sms_notifications: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Relationships
    user_areas = relationship("UserArea", back_populates="user")
    authored_videos = relationship("Video", back_populates="author")
    authored_galleries = relationship("Gallery", back_populates="author")
    
    # Indexes
    __table_args__ = (
        Index("idx_internal_user_username", "username"),
        Index("idx_internal_user_email", "email"),
        Index("idx_internal_user_active", "is_active"),
        Index("idx_internal_user_employee_id", "employee_id"),
        Index("idx_internal_user_active_created", "is_active", "created_at"),
        Index("idx_internal_user_dashboard_access", "can_access_dashboard"),
        Index("idx_internal_user_search", "first_name", "last_name", "username"),
        Index("idx_internal_user_uuid", "uuid"),
    )
    
    def __repr__(self) -> str:
        return f"<InternalUser(username={self.username})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"