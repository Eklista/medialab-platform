"""
Permission model for role-based access control
"""
from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class Permission(BaseModelWithID):
    """
    Permission model for defining specific actions users can perform
    
    Examples:
    - create_video
    - edit_gallery  
    - manage_users
    - view_analytics
    """
    
    __tablename__ = "permissions"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Unique permission name (snake_case)"
    )
    
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Human-readable permission name"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed description of what this permission allows"
    )
    
    # Categorization
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="general",
        comment="Permission category (cms, users, analytics, etc.)"
    )
    
    # Status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether permission is active (Y/N)"
    )
    
    # Relationships
    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_permission_name", "name"),
        Index("idx_permission_category", "category"),
        Index("idx_permission_active", "is_active"),
        Index("idx_permission_category_active", "category", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<Permission(name={self.name}, category={self.category})>"