"""
AcademicUnitType model - Base unificado
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class AcademicUnitType(BaseModelWithID):
    """
    Academic Unit Type model for categorizing academic units
    """
    
    __tablename__ = "academic_unit_types"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Hierarchy and classification
    hierarchy_level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    abbreviation: Mapped[str] = mapped_column(String(10), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="academic")
    
    # Status
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    
    # Configuration
    allows_students: Mapped[bool] = mapped_column(nullable=False, default=True)
    allows_faculty: Mapped[bool] = mapped_column(nullable=False, default=True)
    requires_approval: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Relationships
    academic_units = relationship("AcademicUnit", back_populates="academic_unit_type", cascade="all, delete-orphan")
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_academic_unit_type_name", "name"),
        Index("idx_academic_unit_type_active", "is_active"),
        Index("idx_academic_unit_type_hierarchy", "hierarchy_level"),
    )
    
    def __repr__(self) -> str:
        return f"<AcademicUnitType(name={self.name})>"