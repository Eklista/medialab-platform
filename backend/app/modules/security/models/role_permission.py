"""
RolePermission model
"""
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Index, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class RolePermission(BaseModelWithID):
    """
    Many-to-many relationship between roles and permissions
    """
    
    __tablename__ = "role_permissions"
    
    # Foreign keys
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Grant details
    grant_type: Mapped[str] = mapped_column(String(20), nullable=False, default="direct")
    assigned_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Time-based access
    valid_from: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Context restrictions
    context_restrictions: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationships
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
    
    # Critical indexes and constraints
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
        Index("idx_role_permission_role", "role_id"),
        Index("idx_role_permission_permission", "permission_id"),
        Index("idx_role_permission_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"