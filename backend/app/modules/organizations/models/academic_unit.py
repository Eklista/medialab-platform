"""
AcademicUnit model - CON relaciones Category restauradas
"""
from sqlalchemy import String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class AcademicUnit(BaseModelWithID):
    """
    Academic Unit model for university faculties, schools, institutes
    """
    
    __tablename__ = "academic_units"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[str] = mapped_column(String(100), nullable=True)
    abbreviation: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Type relationship
    academic_unit_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("academic_unit_types.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    # Contact information
    website: Mapped[str] = mapped_column(String(500), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    building: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Visual identity
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    color_primary: Mapped[str] = mapped_column(String(20), nullable=True)
    color_secondary: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Status and configuration
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    allows_public_content: Mapped[bool] = mapped_column(nullable=False, default=True)
    requires_approval: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Statistics (updated by services)
    total_students: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_faculty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_projects: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relationships - TODAS RESTAURADAS
    academic_unit_type = relationship("AcademicUnitType", back_populates="academic_units")
    user_academic_units = relationship("UserAcademicUnit", back_populates="academic_unit", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="academic_unit", cascade="all, delete-orphan")
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_academic_unit_name", "name"),
        Index("idx_academic_unit_abbreviation", "abbreviation"),
        Index("idx_academic_unit_type", "academic_unit_type_id"),
        Index("idx_academic_unit_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<AcademicUnit(name={self.abbreviation or self.name})>"