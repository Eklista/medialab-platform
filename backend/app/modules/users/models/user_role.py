"""
UserRole model for many-to-many relationship between users and roles
"""
from sqlalchemy import Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class UserRole(BaseModelWithID):
    """
    Many-to-many relationship table between users and roles
    Works with both InternalUser and InstitutionalUser through polymorphic approach
    """
    
    __tablename__ = "user_roles"
    
    # Foreign keys - using Integer to reference the internal ID from hybrid model
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Foreign key to users table (internal ID)"
    )
    
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to roles table"
    )
    
    # User type to handle polymorphic relationship
    user_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Type of user (internal_user, institutional_user)"
    )
    
    # Status and metadata
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether this role assignment is active (Y/N)"
    )
    
    is_primary: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether this is the user's primary role (Y/N)"
    )
    
    # Assignment metadata
    assigned_reason: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Reason for role assignment"
    )
    
    # Relationships
    role = relationship(
        "Role",
        back_populates="user_roles"
    )
    
    # Polymorphic relationships to both user types
    # Note: These will be configured differently based on user_type
    
    # Constraints and indexes
    __table_args__ = (
        # Unique constraint to prevent duplicate user-role pairs
        UniqueConstraint(
            "user_id", 
            "role_id", 
            "user_type",
            name="uq_user_role_type"
        ),
        
        # Indexes for performance
        Index("idx_user_role_user", "user_id"),
        Index("idx_user_role_role", "role_id"),
        Index("idx_user_role_type", "user_type"),
        Index("idx_user_role_active", "is_active"),
        Index("idx_user_role_primary", "is_primary"),
        Index("idx_user_role_user_type", "user_id", "user_type"),
        Index("idx_user_role_user_active", "user_id", "is_active"),
        Index("idx_user_role_role_active", "role_id", "is_active"),
        Index("idx_user_role_type_active", "user_type", "is_active"),
        Index("idx_user_role_user_primary", "user_id", "is_primary"),
    )
    
    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id}, type={self.user_type})>"