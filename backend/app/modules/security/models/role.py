"""
Role model
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class Role(BaseModelWithID):
    """
    Role model for grouping permissions and assigning to users
    """
    
    __tablename__ = "roles"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Hierarchy and classification
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    role_type: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    target_user_type: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_system: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_default: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Display
    color: Mapped[str] = mapped_column(String(20), nullable=True)
    icon: Mapped[str] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    
    # Limits
    max_assignments: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Relationships
    role_permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan"
    )
    
    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan"
    )
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_role_name", "name"),
        Index("idx_role_type", "role_type"),
        Index("idx_role_level", "level"),
        Index("idx_role_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<Role(name={self.name})>"