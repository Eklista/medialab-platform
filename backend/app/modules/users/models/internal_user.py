"""
Internal User model
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_user import BaseUser


class InternalUser(BaseUser):
    """
    Internal User model for MediaLab staff
    """
    
    __tablename__ = "internal_users"
    
    # Employee info
    employee_id: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    position: Mapped[str] = mapped_column(String(100), nullable=True)
    banner_photo: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Activity
    last_activity: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Access
    can_access_dashboard: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Relationships
    user_roles = relationship(
        "UserRole",
        primaryjoin="and_(UserRole.user_id == InternalUser.id, UserRole.user_type == 'internal_user')",
        cascade="all, delete-orphan"
    )
    
    user_areas = relationship(
        "UserArea",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    authored_videos = relationship(
        "Video",
        back_populates="author"
    )
    
    authored_galleries = relationship(
        "Gallery",
        back_populates="author"
    )
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_internal_user_username", "username"),
        Index("idx_internal_user_email", "email"),
        Index("idx_internal_user_active", "is_active"),
        Index("idx_internal_user_employee_id", "employee_id"),
    )
    
    def __repr__(self) -> str:
        return f"<InternalUser(username={self.username})>"