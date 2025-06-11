"""
AcademicUnit model - Simple version for university faculties
"""
from sqlalchemy import String, Text, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class AcademicUnit(BaseModelWithID):
    """
    Simple Academic Unit model for university faculties
    Used to identify where institutional users come from
    
    Examples:
    - FISICC 
    - FING
    - FACTI
    """
    
    __tablename__ = "academic_units"
    
    # Core fields only
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Faculty name"
    )
    
    abbreviation: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        comment="Faculty abbreviation (FISICC, FING)"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Faculty description"
    )
    
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Active status"
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        comment="Display order"
    )
    
    # relationship with institutional users
    user_academic_units = relationship(
        "UserAcademicUnit",
        back_populates="academic_unit",
        cascade="all, delete-orphan"
    )
    
    # Simple indexes
    __table_args__ = (
        Index("idx_academic_unit_name", "name"),
        Index("idx_academic_unit_abbreviation", "abbreviation"),
        Index("idx_academic_unit_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<AcademicUnit(name={self.name})>"