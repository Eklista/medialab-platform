"""
RolePermission model for many-to-many relationship between roles and permissions
"""
from sqlalchemy import Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class RolePermission(BaseModelWithID):
    """
    Many-to-many relationship table between roles and permissions
    Allows roles to have multiple permissions and permissions to be assigned to multiple roles
    """
    
    __tablename__ = "role_permissions"
    
    # Foreign keys
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to roles table"
    )
    
    permission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to permissions table"
    )
    
    # Status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether this role-permission assignment is active (Y/N)"
    )
    
    # Relationships
    role = relationship(
        "Role",
        back_populates="role_permissions"
    )
    
    permission = relationship(
        "Permission",
        back_populates="role_permissions"
    )
    
    # Constraints and indexes
    __table_args__ = (
        # Unique constraint to prevent duplicate role-permission pairs
        UniqueConstraint(
            "role_id", 
            "permission_id", 
            name="uq_role_permission"
        ),
        
        # Indexes for performance
        Index("idx_role_permission_role", "role_id"),
        Index("idx_role_permission_permission", "permission_id"),
        Index("idx_role_permission_active", "is_active"),
        Index("idx_role_permission_role_active", "role_id", "is_active"),
        Index("idx_role_permission_permission_active", "permission_id", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"