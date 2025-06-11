"""
AcademicUnitType model for categorizing different types of academic units
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class AcademicUnitType(BaseModelWithID):
    """
    Academic Unit Type model for defining different categories of academic units
    
    Examples:
    - Facultad (Faculty)
    - Escuela (School)
    - Instituto (Institute)
    - Departamento (Department)
    - Centro (Center)
    - Laboratorio (Laboratory)
    """
    
    __tablename__ = "academic_unit_types"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Unique type name"
    )
    
    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Human-readable type name"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed description of this academic unit type"
    )
    
    # Hierarchy information
    hierarchy_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="Level in academic hierarchy (1=top level, higher=sub levels)"
    )
    
    # Status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether type is active (Y/N)"
    )
    
    # Display order for UI
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        comment="Display order in lists (lower = appears first)"
    )
    
    # Relationships
    academic_units = relationship(
        "AcademicUnit",
        back_populates="unit_type",
        cascade="all, delete-orphan"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_academic_unit_type_name", "name"),
        Index("idx_academic_unit_type_active", "is_active"),
        Index("idx_academic_unit_type_hierarchy", "hierarchy_level"),
        Index("idx_academic_unit_type_sort", "sort_order"),
        Index("idx_academic_unit_type_active_sort", "is_active", "sort_order"),
    )
    
    def __repr__(self) -> str:
        return f"<AcademicUnitType(name={self.name}, level={self.hierarchy_level})>"