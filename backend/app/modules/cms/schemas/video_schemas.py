"""
CMS Video Schemas - Validation and serialization
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum
import re


class VideoStatus(str, Enum):
    """Video status options"""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class VideoContentType(str, Enum):
    """Video content type options"""
    EVENT = "event"
    LECTURE = "lecture"
    GRADUATION = "graduation"
    CEREMONY = "ceremony"
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    PROMOTIONAL = "promotional"
    DOCUMENTARY = "documentary"
    TUTORIAL = "tutorial"
    GENERAL = "general"


class VideoQuality(str, Enum):
    """Video quality options"""
    HD_720P = "720p"
    FULL_HD_1080P = "1080p"
    UHD_4K = "4k"
    AUTO = "auto"


# ===================================
# BASE VIDEO SCHEMAS
# ===================================

class VideoBase(BaseModel):
    """Base video schema"""
    title: str = Field(..., min_length=3, max_length=200, description="Título del video")
    subtitle: Optional[str] = Field(None, max_length=300, description="Subtítulo")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción del video")
    
    # YouTube data
    original_url: str = Field(..., description="URL original de YouTube")
    
    # Classification
    event_date: date = Field(..., description="Fecha del evento")
    content_type: VideoContentType = Field(default=VideoContentType.EVENT, description="Tipo de contenido")
    tags: Optional[str] = Field(None, max_length=500, description="Tags separados por comas")
    
    # Technical
    video_quality: Optional[VideoQuality] = Field(None, description="Calidad del video")
    aspect_ratio: Optional[str] = Field(None, max_length=20, description="Relación de aspecto")
    
    # Visibility
    is_featured: bool = Field(default=False, description="Video destacado")
    is_public: bool = Field(default=True, description="Visible públicamente")
    
    # Publishing
    approval_required: bool = Field(default=True, description="Requiere aprobación")
    
    # SEO
    seo_title: Optional[str] = Field(None, max_length=200, description="Título SEO")
    seo_description: Optional[str] = Field(None, max_length=300, description="Descripción SEO")
    
    # Settings
    allow_comments: bool = Field(default=True, description="Permitir comentarios")
    allow_embedding: bool = Field(default=True, description="Permitir embed")
    
    @validator('original_url')
    def validate_youtube_url(cls, v):
        """Validate YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, v):
                return v
        
        raise ValueError('URL debe ser de YouTube válida')


class VideoCreate(VideoBase):
    """Video creation schema"""
    category_id: int = Field(..., description="ID de la categoría")
    author_id: Optional[int] = Field(None, description="ID del autor (opcional)")


class VideoUpdate(BaseModel):
    """Video update schema"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=300)
    description: Optional[str] = Field(None, max_length=2000)
    
    original_url: Optional[str] = None
    
    event_date: Optional[date] = None
    content_type: Optional[VideoContentType] = None
    tags: Optional[str] = Field(None, max_length=500)
    
    video_quality: Optional[VideoQuality] = None
    aspect_ratio: Optional[str] = Field(None, max_length=20)
    
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    
    status: Optional[VideoStatus] = None
    approval_required: Optional[bool] = None
    
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = Field(None, max_length=300)
    
    allow_comments: Optional[bool] = None
    allow_embedding: Optional[bool] = None
    
    @validator('original_url')
    def validate_youtube_url(cls, v):
        if v is None:
            return v
        
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, v):
                return v
        
        raise ValueError('URL debe ser de YouTube válida')


class VideoResponse(VideoBase):
    """Video response schema"""
    id: int
    uuid: str
    slug: Optional[str]
    
    # YouTube processed data
    embed_url: str
    video_id: Optional[str]
    thumbnail_url: Optional[str]
    duration: Optional[int]  # en segundos
    
    # Status
    is_published: bool
    status: VideoStatus
    
    # Analytics
    view_count: int
    like_count: int
    share_count: int
    
    # Relationships
    category_id: int
    author_id: int
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Related data
    category: Optional[dict] = None
    author: Optional[dict] = None
    
    class Config:
        from_attributes = True


class VideoMinimal(BaseModel):
    """Minimal video for lists/cards"""
    id: int
    uuid: str
    title: str
    slug: Optional[str]
    thumbnail_url: Optional[str]
    duration: Optional[int]
    embed_url: str
    is_published: bool
    view_count: int
    event_date: date
    created_at: datetime
    
    class Config:
        from_attributes = True


class VideoEmbed(BaseModel):
    """Video embed data for frontend player"""
    id: int
    uuid: str
    title: str
    embed_url: str
    thumbnail_url: Optional[str]
    duration: Optional[int]
    allow_embedding: bool
    
    class Config:
        from_attributes = True


# ===================================
# SEARCH AND FILTERING
# ===================================

class VideoSearchParams(BaseModel):
    """Video search parameters"""
    q: Optional[str] = Field(None, description="Búsqueda en título/descripción")
    category_id: Optional[int] = Field(None, description="Filtrar por categoría")
    author_id: Optional[int] = Field(None, description="Filtrar por autor")
    content_type: Optional[VideoContentType] = Field(None, description="Filtrar por tipo")
    status: Optional[VideoStatus] = Field(None, description="Filtrar por estado")
    is_published: Optional[bool] = Field(None, description="Filtrar publicados")
    is_featured: Optional[bool] = Field(None, description="Filtrar destacados")
    is_public: Optional[bool] = Field(None, description="Filtrar públicos")
    
    # Date filters
    event_date_from: Optional[date] = Field(None, description="Fecha evento desde")
    event_date_to: Optional[date] = Field(None, description="Fecha evento hasta")
    created_from: Optional[datetime] = Field(None, description="Creado desde")
    created_to: Optional[datetime] = Field(None, description="Creado hasta")
    
    # Pagination
    page: int = Field(default=1, ge=1, description="Número de página")
    per_page: int = Field(default=20, ge=1, le=100, description="Items por página")
    
    # Sorting
    sort_by: str = Field(default="created_at", description="Campo para ordenar")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="Dirección")
    
    # Response options
    minimal: bool = Field(default=False, description="Respuesta mínima")
    include_author: bool = Field(default=True, description="Incluir datos del autor")
    include_category: bool = Field(default=True, description="Incluir datos de categoría")


class VideoListResponse(BaseModel):
    """Paginated video list response"""
    videos: List[VideoResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class VideoStatsResponse(BaseModel):
    """Video statistics response"""
    total_videos: int
    published_videos: int
    draft_videos: int
    total_views: int
    total_duration: int  # en segundos
    by_category: dict
    by_content_type: dict
    by_status: dict
    by_month: dict


class YouTubeVideoInfo(BaseModel):
    """YouTube video information"""
    video_id: str
    title: str
    description: str
    thumbnail_url: str
    duration: int
    embed_url: str
    published_at: datetime
    view_count: int
    like_count: int