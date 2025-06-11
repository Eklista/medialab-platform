"""
Gallery model
"""
from datetime import date
from sqlalchemy import String, Text, Integer, Date, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, Any

from app.shared.base.base_model import BaseModelWithUUID


class Gallery(BaseModelWithUUID):
    """
    Gallery model for MediaLab photo collections
    """
    
    __tablename__ = "galleries"
    
    # Content fields
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(300), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Photos storage
    photos: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=True)
    cover_photo: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Date and classification
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, default="event")
    
    # Photo statistics
    photo_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_size_mb: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Technical information
    camera_info: Mapped[str] = mapped_column(String(200), nullable=True)
    photographer: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Relationships
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("internal_users.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    # Status and visibility
    is_published: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_featured: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Publishing workflow
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    approval_required: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # SEO
    slug: Mapped[str] = mapped_column(String(250), nullable=True, unique=True)
    seo_title: Mapped[str] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Analytics
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    like_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    share_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    download_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Settings
    allow_download: Mapped[bool] = mapped_column(nullable=False, default=True)
    allow_comments: Mapped[bool] = mapped_column(nullable=False, default=True)
    watermark_enabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    # Relationships
    category = relationship("Category", back_populates="galleries")
    author = relationship("InternalUser", back_populates="authored_galleries")
    
    # Critical indexes only
    __table_args__ = (
        Index("idx_gallery_title", "title"),
        Index("idx_gallery_category", "category_id"),
        Index("idx_gallery_author", "author_id"),
        Index("idx_gallery_published", "is_published"),
        Index("idx_gallery_public", "is_public"),
        Index("idx_gallery_status", "status"),
        Index("idx_gallery_slug", "slug"),
        Index("idx_gallery_event_date", "event_date"),
    )
    
    def __repr__(self) -> str:
        return f"<Gallery(title={self.title})>"