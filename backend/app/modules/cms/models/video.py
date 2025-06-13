# backend/app/modules/cms/models/video.py
"""
Video model - Usando BaseModelHybrid para tener ID interno y UUID público
"""
from datetime import date
from sqlalchemy import String, Text, Integer, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base.base_model import BaseModelHybrid


class Video(BaseModelHybrid):
    """
    Video model for MediaLab content
    """
    
    __tablename__ = "videos"
    
    # Content fields
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(300), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Video source
    embed_url: Mapped[str] = mapped_column(String(500), nullable=False)
    original_url: Mapped[str] = mapped_column(String(500), nullable=True)
    video_id: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Visual and metadata
    thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Date and classification
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, default="event")
    
    # Technical info
    video_quality: Mapped[str] = mapped_column(String(20), nullable=True)
    aspect_ratio: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Relationships - usando INTEGER IDs para foreign keys
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
    
    # Settings
    allow_comments: Mapped[bool] = mapped_column(nullable=False, default=True)
    allow_embedding: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    # Relationships
    category = relationship("Category", back_populates="videos")
    author = relationship("InternalUser", back_populates="authored_videos")
    
    # Indexes
    __table_args__ = (
        Index("idx_video_title", "title"),
        Index("idx_video_category", "category_id"),
        Index("idx_video_author", "author_id"),
        Index("idx_video_published", "is_published"),
        Index("idx_video_public", "is_public"),
        Index("idx_video_status", "status"),
        Index("idx_video_slug", "slug"),
        Index("idx_video_event_date", "event_date"),
        Index("idx_video_uuid", "uuid"),
    )
    
    def __repr__(self) -> str:
        return f"<Video(title={self.title})>"