"""
Internal User model for MediaLab staff
"""
from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_user import BaseUser


class InternalUser(BaseUser):
    """
    Internal User model for MediaLab staff
    """
    
    __tablename__ = "internal_users"
    
    # Info básica de empleado
    employee_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        comment="ID de empleado"
    )
    
    position: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Puesto de trabajo"
    )
    
    # Banner para perfil (simple)
    banner_photo: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Foto de banner"
    )
    
    # Online tracking simple
    last_activity: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="Última actividad"
    )
    
    # Permisos básicos
    can_access_dashboard: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Puede acceder al dashboard (Y/N)"
    )
    
    # Relaciones
    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    user_areas = relationship(
        "UserArea",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Índices básicos
    __table_args__ = (
        Index("idx_internal_user_employee_id", "employee_id"),
        Index("idx_internal_user_position", "position"),
        Index("idx_internal_user_dashboard_access", "can_access_dashboard"),
        Index("idx_internal_user_last_activity", "last_activity"),
        # Base user indexes
        Index("idx_internal_users_username", "username"),
        Index("idx_internal_users_email", "email"),
        Index("idx_internal_users_uuid", "uuid"),
        Index("idx_internal_users_active", "is_active"),
        Index("idx_internal_users_last_login", "last_login"),
    )
    
    def __repr__(self) -> str:
        return f"<InternalUser(username={self.username}, position={self.position})>"