"""
Category model for content organization and filtering
"""
from sqlalchemy import String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithID


class Category(BaseModelWithID):
    """
    Category model for organizing content by academic unit and type
    Enables smart filtering: Academic Unit → Category → Content
    
    Examples:
    - FISICC → Graduación
    - FISICC → Conferencia  
    - FISICC → Evento
    - FING → Fotografías
    """
    
    __tablename__ = "categories"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Category name (graduación, conferencia, evento, fotografías)"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Category description"
    )
    
    # Academic unit relationship for filtering
    academic_unit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("academic_units.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to academic units for filtering"
    )
    
    # Display and status
    is_active: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether category is active (Y/N)"
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
        comment="Display order within academic unit"
    )
    
    # SEO and frontend
    slug: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        comment="URL-friendly version of name"
    )
    
    # Relationships
    academic_unit = relationship(
        "AcademicUnit",
        back_populates="categories"
    )
    
    videos = relationship(
        "Video",
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    galleries = relationship(
        "Gallery", 
        back_populates="category",
        cascade="all, delete-orphan"
    )
    
    # Indexes for filtering performance
    __table_args__ = (
        Index("idx_category_name", "name"),
        Index("idx_category_academic_unit", "academic_unit_id"),
        Index("idx_category_active", "is_active"),
        Index("idx_category_sort", "sort_order"),
        Index("idx_category_slug", "slug"),
        Index("idx_category_unit_active", "academic_unit_id", "is_active"),
        Index("idx_category_unit_sort", "academic_unit_id", "sort_order"),
        Index("idx_category_name_unit", "name", "academic_unit_id"),  # For filtering
    )
    
    def __repr__(self) -> str:
        return f"<Category(name={self.name}, academic_unit_id={self.academic_unit_id})>"