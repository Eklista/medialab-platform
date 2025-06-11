"""
Gallery model for MediaLab photo collections
"""
from datetime import date
from sqlalchemy import String, Text, Integer, Date, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from app.shared.base.base_model import BaseModelWithUUID


class Gallery(BaseModelWithUUID):
    """
    Gallery model for MediaLab photo collections
    Uses UUID for public URLs and security
    """
    
    __tablename__ = "galleries"
    
    # Content fields
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Gallery title"
    )
    
    subtitle: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
        comment="Gallery subtitle"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Gallery description"
    )
    
    # Photos - JSON array for bulk photos
    photos: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        comment="JSON array of photo URLs/paths"
    )
    
    # Thumbnail
    thumbnail_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Thumbnail for gallery cards"
    )
    
    # Date management
    event_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Date of the event"
    )
    
    # Tags - simple string for now, JSON array in future
    tags: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Comma-separated tags (evento, fisicc, 2024)"
    )
    
    # Photo count for quick reference
    photo_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Total number of photos in gallery"
    )
    
    # Relationships
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to categories"
    )
    
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("internal_users.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to internal users (author)"
    )
    
    # Status and visibility
    is_published: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether gallery is published (Y/N)"
    )
    
    is_featured: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether gallery is featured (Y/N)"
    )
    
    # SEO and frontend
    slug: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
        unique=True,
        comment="URL-friendly version of title"
    )
    
    # Analytics (simple)
    view_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of views"
    )
    
    # Download settings
    allow_download: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="Y",
        comment="Whether photos can be downloaded (Y/N)"
    )
    
    # Relationships
    category = relationship(
        "Category",
        back_populates="galleries"
    )
    
    author = relationship(
        "InternalUser",
        back_populates="authored_galleries"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_gallery_title", "title"),
        Index("idx_gallery_category", "category_id"),
        Index("idx_gallery_author", "author_id"),
        Index("idx_gallery_event_date", "event_date"),
        Index("idx_gallery_published", "is_published"),
        Index("idx_gallery_featured", "is_featured"),
        Index("idx_gallery_slug", "slug"),
        Index("idx_gallery_views", "view_count"),
        Index("idx_gallery_photo_count", "photo_count"),
        Index("idx_gallery_category_published", "category_id", "is_published"),
        Index("idx_gallery_category_date", "category_id", "event_date"),
        Index("idx_gallery_published_date", "is_published", "event_date"),
        Index("idx_gallery_published_featured", "is_published", "is_featured"),
        Index("idx_gallery_category_published_date", "category_id", "is_published", "event_date"),
    )
    
    def __repr__(self) -> str:
        return f"<Gallery(title={self.title}, photo_count={self.photo_count})>"