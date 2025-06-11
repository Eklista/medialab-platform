"""
UserRole model - CORREGIDO usando strings en relationships
"""
from sqlalchemy import Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class UserRole(BaseModelWithID):
    """
    Many-to-many relationship between users and roles
    """
    
    __tablename__ = "user_roles"
    
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    
    user_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    assigned_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationships - USANDO STRINGS
    role = relationship("Role", back_populates="user_roles")
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "user_type", name="uq_user_role_type"),
        Index("idx_user_role_user", "user_id"),
        Index("idx_user_role_role", "role_id"),
        Index("idx_user_role_active", "is_active"),
        Index("idx_user_role_user_type", "user_id", "user_type"),
        Index("idx_user_role_user_type_active", "user_id", "user_type", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"