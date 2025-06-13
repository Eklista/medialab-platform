# backend/app/modules/cms/schemas/__init__.py
"""
CMS Schemas - Validation and serialization models
"""
from .category_schemas import *
from .video_schemas import *
from .gallery_schemas import *

__all__ = [
    # Category schemas
    "CategoryType",
    "ContentTypeFocus", 
    "CategoryStatus",
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "CategoryMinimal",
    "CategoryWithContent",
    "CategorySearchParams",
    "CategoryListResponse",
    "CategoryStatsResponse",
    
    # Video schemas
    "VideoStatus",
    "VideoContentType",
    "VideoQuality",
    "VideoBase",
    "VideoCreate",
    "VideoUpdate", 
    "VideoResponse",
    "VideoMinimal",
    "VideoEmbed",
    "VideoSearchParams",
    "VideoListResponse",
    "VideoStatsResponse",
    "YouTubeVideoInfo",
    
    # Gallery schemas
    "GalleryStatus",
    "GalleryContentType",
    "PhotoOrientation",
    "PhotoData",
    "PhotoUpload",
    "GalleryBase",
    "GalleryCreate",
    "GalleryUpdate",
    "GalleryResponse",
    "GalleryMinimal",
    "GalleryWithPhotos",
    "GallerySearchParams",
    "GalleryListResponse",
    "GalleryStatsResponse",
    "FileUploadResponse",
    "BulkUploadResponse",
    "PhotoReorderRequest",
    "PhotoUpdateRequest"
]