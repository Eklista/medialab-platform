"""
Institutional User model
"""
from typing import Optional
from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_user import BaseUser


class InstitutionalUser(BaseUser):
    """
    Institutional User model
    """
    
    __tablename__ = "institutional_users"
    
    # Info básica institucional
    institution: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="Universidad Galileo",
        comment="Institución"
    )
    
    faculty_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="ID de facultad/empleado"
    )
    
    # Info académica básica
    academic_title: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Título académico (Dr., Lic., Ing.)"
    )
    
    position_title: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        comment="Puesto en la institución"
    )
    
    # Contacto institucional
    office_phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Teléfono de oficina"
    )
    
    office_location: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Ubicación de oficina"
    )
    
    # Tipo de usuario
    is_faculty: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Es faculty (Y/N)"
    )
    
    is_student: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Es estudiante (Y/N)"
    )
    
    is_external_client: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Es cliente externo (Y/N)"
    )
    
    # Permisos
    can_request_projects: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Puede solicitar proyectos (Y/N)"
    )
    
    # Relaciones
    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    user_academic_units = relationship(
        "UserAcademicUnit",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Índices básicos
    __table_args__ = (
        Index("idx_institutional_user_faculty_id", "faculty_id"),
        Index("idx_institutional_user_institution", "institution"),
        Index("idx_institutional_user_is_faculty", "is_faculty"),
        Index("idx_institutional_user_is_student", "is_student"),
        Index("idx_institutional_user_is_external", "is_external_client"),
        Index("idx_institutional_user_can_request", "can_request_projects"),
        # Base user indexes
        Index("idx_institutional_users_username", "username"),
        Index("idx_institutional_users_email", "email"),
        Index("idx_institutional_users_uuid", "uuid"),
        Index("idx_institutional_users_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        user_type = "Faculty" if self.is_faculty == "Y" else "Student" if self.is_student == "Y" else "External" if self.is_external_client == "Y" else "Institutional"
        return f"<InstitutionalUser(username={self.username}, type={user_type})>"