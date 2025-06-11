"""
Role model for role-based access control
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class Role(BaseModelWithID):
    """
    Role model for grouping permissions and assigning to users
    
    Examples:
    - super_admin
    - admin
    - editor
    - client
    - viewer
    """
    
    __tablename__ = "roles"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Unique role name (snake_case)"
    )
    
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Human-readable role name"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed description of role responsibilities"
    )
    
    # Role level for hierarchy (lower number = higher privilege)
    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        comment="Role hierarchy level (1=highest, 100=lowest)"
    )
    
    # Role type for categorization
    role_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="standard",
        comment="Role type (system, admin, standard, client)"
    )
    
    # Status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether role is active (Y/N)"
    )
    
    is_system: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether role is system-defined (Y/N)"
    )
    
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
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_role_name", "name"),
        Index("idx_role_type", "role_type"),
        Index("idx_role_level", "level"),
        Index("idx_role_active", "is_active"),
        Index("idx_role_system", "is_system"),
        Index("idx_role_type_active", "role_type", "is_active"),
        Index("idx_role_level_active", "level", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<Role(name={self.name}, level={self.level}, type={self.role_type})>"