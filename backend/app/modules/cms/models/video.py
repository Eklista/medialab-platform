"""
Video model for MediaLab content management
"""
from datetime import date
from sqlalchemy import String, Text, Integer, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.shared.base.base_model import BaseModelWithUUID


class Video(BaseModelWithUUID):
    """
    Video model for MediaLab content
    Uses UUID for public URLs and embed security
    """
    
    __tablename__ = "videos"
    
    # Content fields
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Video title"
    )
    
    subtitle: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
        comment="Video subtitle"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Video description"
    )
    
    # Video source - flexible for future
    embed_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="YouTube embed URL or future AWS/external service URL"
    )
    
    # Visual
    thumbnail_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Thumbnail image URL"
    )
    
    # Date management
    event_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Date of the event (NOT publication date)"
    )
    
    # Tags - simple string for now, JSON array in future
    tags: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Comma-separated tags (evento, fisicc, 2024)"
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
        comment="Whether video is published (Y/N)"
    )
    
    is_featured: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        comment="Whether video is featured (Y/N)"
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
    
    # Relationships
    category = relationship(
        "Category",
        back_populates="videos"
    )
    
    author = relationship(
        "InternalUser",
        back_populates="authored_videos"  # Need to add this to InternalUser
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_video_title", "title"),
        Index("idx_video_category", "category_id"),
        Index("idx_video_author", "author_id"),
        Index("idx_video_event_date", "event_date"),
        Index("idx_video_published", "is_published"),
        Index("idx_video_featured", "is_featured"),
        Index("idx_video_slug", "slug"),
        Index("idx_video_views", "view_count"),
        Index("idx_video_category_published", "category_id", "is_published"),
        Index("idx_video_category_date", "category_id", "event_date"),
        Index("idx_video_published_date", "is_published", "event_date"),
        Index("idx_video_published_featured", "is_published", "is_featured"),
        Index("idx_video_category_published_date", "category_id", "is_published", "event_date"),
    )
    
    def __repr__(self) -> str:
        return f"<Video(title={self.title}, category_id={self.category_id})>"