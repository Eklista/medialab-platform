"""
Category model
"""
from sqlalchemy import String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelWithID


class Category(BaseModelWithID):
    """
    Category model for organizing content by academic unit and type
    """
    
    __tablename__ = "categories"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Academic unit relationship for filtering
    academic_unit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("academic_units.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    # Category classification
    category_type: Mapped[str] = mapped_column(String(50), nullable=False, default="event")
    content_type_focus: Mapped[str] = mapped_column(String(50), nullable=False, default="mixed")
    
    # Status and visibility
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_featured: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    
    # SEO and frontend
    slug: Mapped[str] = mapped_column(String(120), nullable=True)
    
    # Visual identity
    color: Mapped[str] = mapped_column(String(20), nullable=True)
    icon: Mapped[str] = mapped_column(String(50), nullable=True)
    cover_image: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Content management
    auto_approve_content: Mapped[bool] = mapped_column(nullable=False, default=False)
    requires_review: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Statistics (updated by services)
    total_videos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_galleries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relationships
    academic_unit = relationship("AcademicUnit", back_populates="categories")
    videos = relationship("Video", back_populates="category", cascade="all, delete-orphan")
    galleries = relationship("Gallery", back_populates="category", cascade="all, delete-orphan")
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_category_name", "name"),
        Index("idx_category_academic_unit", "academic_unit_id"),
        Index("idx_category_active", "is_active"),
        Index("idx_category_public", "is_public"),
        Index("idx_category_slug", "slug"),
    )
    
    def __repr__(self) -> str:
        return f"<Category(name={self.name})>"