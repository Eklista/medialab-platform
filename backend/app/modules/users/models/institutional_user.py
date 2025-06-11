"""
Institutional User model
"""
from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_user import BaseUser


class InstitutionalUser(BaseUser):
    """
    Institutional User model for university faculty, students, and external clients
    """
    
    __tablename__ = "institutional_users"
    
    # Institution info
    institution: Mapped[str] = mapped_column(String(200), nullable=False, default="Universidad Galileo")
    faculty_id: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Academic info
    academic_title: Mapped[str] = mapped_column(String(100), nullable=True)
    position_title: Mapped[str] = mapped_column(String(150), nullable=True)
    
    # Contact info
    office_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    office_location: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # User type (using booleans)
    is_faculty: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_student: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_external_client: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Permissions
    can_request_projects: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Relationships
    user_roles = relationship(
        "UserRole",
        primaryjoin="and_(UserRole.user_id == InstitutionalUser.id, UserRole.user_type == 'institutional_user')",
        cascade="all, delete-orphan"
    )
    
    user_academic_units = relationship(
        "UserAcademicUnit",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_institutional_user_username", "username"),
        Index("idx_institutional_user_email", "email"),
        Index("idx_institutional_user_active", "is_active"),
        Index("idx_institutional_user_faculty_id", "faculty_id"),
    )
    
    def __repr__(self) -> str:
        return f"<InstitutionalUser(username={self.username})>"