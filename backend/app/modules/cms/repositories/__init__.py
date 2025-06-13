# backend/app/modules/cms/repositories/__init__.py
"""
CMS Repositories - Data access layer
"""
from .category_repository import CategoryRepository
from .video_repository import VideoRepository  
from .gallery_repository import GalleryRepository

__all__ = [
    "CategoryRepository",
    "VideoRepository",
    "GalleryRepository"
]