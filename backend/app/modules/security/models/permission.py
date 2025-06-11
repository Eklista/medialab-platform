"""
Permission model
"""
from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class Permission(BaseModelWithID):
    """
    Permission model for defining specific actions users can perform
    """
    
    __tablename__ = "permissions"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Classification
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="general")
    resource: Mapped[str] = mapped_column(String(50), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_system: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Display
    sort_order: Mapped[int] = mapped_column(nullable=False, default=100)
    
    # Relationships
    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_permission_name", "name"),
        Index("idx_permission_category", "category"),
        Index("idx_permission_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<Permission(name={self.name})>"