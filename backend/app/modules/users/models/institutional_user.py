"""
Institutional User model - Base unificado
"""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelHybrid


class InstitutionalUser(BaseModelHybrid):
    """
    Institutional User model for university faculty, students, and external clients
    """
    
    __tablename__ = "institutional_users"
    
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
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    account_locked: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Institution info
    institution: Mapped[str] = mapped_column(String(200), nullable=False, default="Universidad Galileo")
    faculty_id: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Academic info
    academic_title: Mapped[str] = mapped_column(String(100), nullable=True)
    position_title: Mapped[str] = mapped_column(String(150), nullable=True)
    
    # Contact info
    office_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    office_location: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # User type flags
    is_faculty: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_student: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_external_client: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Permissions
    can_request_projects: Mapped[bool] = mapped_column(nullable=False, default=True)
    
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
    
    # Relationships
    user_academic_units = relationship("UserAcademicUnit", back_populates="user", cascade="all, delete-orphan")
    
    # UserRole específico para institutional users
    user_roles = relationship(
        "UserRole",
        primaryjoin="and_(InstitutionalUser.id==UserRole.user_id, UserRole.user_type=='institutional_user')",
        foreign_keys="[UserRole.user_id]",
        cascade="all, delete-orphan",
        overlaps="user_roles"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_institutional_user_username", "username"),
        Index("idx_institutional_user_email", "email"),
        Index("idx_institutional_user_active", "is_active"),
        Index("idx_institutional_user_faculty_id", "faculty_id"),
        Index("idx_institutional_user_active_created", "is_active", "created_at"),
        Index("idx_institutional_user_types", "is_faculty", "is_student", "is_external_client"),
        Index("idx_institutional_user_search", "first_name", "last_name", "username"),
        Index("idx_institutional_user_uuid", "uuid"),
        Index("idx_institutional_user_institution", "institution"),
    )
    
    def __repr__(self) -> str:
        return f"<InstitutionalUser(username={self.username})>"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"