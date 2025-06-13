"""
CMS Gallery Schemas - Validation and serialization
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class GalleryStatus(str, Enum):
    """Gallery status options"""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class GalleryContentType(str, Enum):
    """Gallery content type options"""
    EVENT = "event"
    GRADUATION = "graduation"
    CEREMONY = "ceremony"
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    INSTITUTIONAL = "institutional"
    PROMOTIONAL = "promotional"
    DOCUMENTARY = "documentary"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    GENERAL = "general"


class PhotoOrientation(str, Enum):
    """Photo orientation options"""
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARE = "square"


# ===================================
# PHOTO SCHEMAS
# ===================================

class PhotoData(BaseModel):
    """Individual photo data structure"""
    filename: str = Field(..., description="Nombre del archivo")
    original_filename: str = Field(..., description="Nombre original del archivo")
    title: Optional[str] = Field(None, max_length=200, description="Título de la foto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción")
    
    # File paths
    original_path: str = Field(..., description="Ruta archivo original")
    processed_path: str = Field(..., description="Ruta archivo procesado (WebP)")
    thumbnail_path: str = Field(..., description="Ruta thumbnail")
    
    # Technical info
    width: int = Field(..., description="Ancho en píxeles")
    height: int = Field(..., description="Alto en píxeles")
    file_size: int = Field(..., description="Tamaño en bytes")
    orientation: PhotoOrientation = Field(..., description="Orientación")
    format: str = Field(..., description="Formato del archivo")
    
    # Metadata
    camera_info: Optional[str] = Field(None, description="Información de cámara")
    taken_at: Optional[datetime] = Field(None, description="Fecha de captura")
    location: Optional[str] = Field(None, description="Ubicación")
    
    # Processing
    processed_at: datetime = Field(..., description="Fecha de procesamiento")
    sort_order: int = Field(default=0, description="Orden en la galería")
    
    class Config:
        from_attributes = True


class PhotoUpload(BaseModel):
    """Photo upload schema"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    sort_order: int = Field(default=0, ge=0)


# ===================================
# BASE GALLERY SCHEMAS
# ===================================

class GalleryBase(BaseModel):
    """Base gallery schema"""
    title: str = Field(..., min_length=3, max_length=200, description="Título de la galería")
    subtitle: Optional[str] = Field(None, max_length=300, description="Subtítulo")
    description: Optional[str] = Field(None, max_length=2000, description="Descripción")
    
    # Classification
    event_date: date = Field(..., description="Fecha del evento")
    content_type: GalleryContentType = Field(default=GalleryContentType.EVENT, description="Tipo de contenido")
    tags: Optional[str] = Field(None, max_length=500, description="Tags separados por comas")
    
    # Technical information
    photographer: Optional[str] = Field(None, max_length=100, description="Fotógrafo")
    camera_info: Optional[str] = Field(None, max_length=200, description="Info de cámara")
    location: Optional[str] = Field(None, max_length=200, description="Ubicación")
    
    # Visibility
    is_featured: bool = Field(default=False, description="Galería destacada")
    is_public: bool = Field(default=True, description="Visible públicamente")
    
    # Publishing
    approval_required: bool = Field(default=True, description="Requiere aprobación")
    
    # SEO
    seo_title: Optional[str] = Field(None, max_length=200, description="Título SEO")
    seo_description: Optional[str] = Field(None, max_length=300, description="Descripción SEO")
    
    # Settings
    allow_download: bool = Field(default=True, description="Permitir descarga")
    allow_comments: bool = Field(default=True, description="Permitir comentarios")
    watermark_enabled: bool = Field(default=False, description="Marca de agua")


class GalleryCreate(GalleryBase):
    """Gallery creation schema"""
    category_id: int = Field(..., description="ID de la categoría")
    author_id: Optional[int] = Field(None, description="ID del autor (opcional)")


class GalleryUpdate(BaseModel):
    """Gallery update schema"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    subtitle: Optional[str] = Field(None, max_length=300)
    description: Optional[str] = Field(None, max_length=2000)
    
    event_date: Optional[date] = None
    content_type: Optional[GalleryContentType] = None
    tags: Optional[str] = Field(None, max_length=500)
    
    photographer: Optional[str] = Field(None, max_length=100)
    camera_info: Optional[str] = Field(None, max_length=200)
    location: Optional[str] = Field(None, max_length=200)
    
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    
    status: Optional[GalleryStatus] = None
    approval_required: Optional[bool] = None
    
    seo_title: Optional[str] = Field(None, max_length=200)
    seo_description: Optional[str] = Field(None, max_length=300)
    
    allow_download: Optional[bool] = None
    allow_comments: Optional[bool] = None
    watermark_enabled: Optional[bool] = None
    
    # Cover photo management
    cover_photo: Optional[str] = Field(None, description="Path de la foto de portada")


class GalleryResponse(GalleryBase):
    """Gallery response schema"""
    id: int
    uuid: str
    slug: Optional[str]
    
    # Photos
    photos: List[PhotoData] = Field(default_factory=list)
    photo_count: int
    total_size_mb: Optional[int]
    
    # Cover and thumbnails
    cover_photo: Optional[str]
    thumbnail_url: Optional[str]
    
    # Status
    is_published: bool
    status: GalleryStatus
    
    # Analytics
    view_count: int
    like_count: int
    share_count: int
    download_count: int
    
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


class GalleryMinimal(BaseModel):
    """Minimal gallery for lists/cards"""
    id: int
    uuid: str
    title: str
    slug: Optional[str]
    thumbnail_url: Optional[str]
    cover_photo: Optional[str]
    photo_count: int
    is_published: bool
    view_count: int
    event_date: date
    created_at: datetime
    
    class Config:
        from_attributes = True


class GalleryWithPhotos(GalleryResponse):
    """Gallery with full photo data"""
    photo_grid: List[PhotoData] = Field(default_factory=list)
    photo_metadata: Dict[str, Any] = Field(default_factory=dict)


# ===================================
# SEARCH AND FILTERING
# ===================================

class GallerySearchParams(BaseModel):
    """Gallery search parameters"""
    q: Optional[str] = Field(None, description="Búsqueda en título/descripción")
    category_id: Optional[int] = Field(None, description="Filtrar por categoría")
    author_id: Optional[int] = Field(None, description="Filtrar por autor")
    content_type: Optional[GalleryContentType] = Field(None, description="Filtrar por tipo")
    status: Optional[GalleryStatus] = Field(None, description="Filtrar por estado")
    is_published: Optional[bool] = Field(None, description="Filtrar publicadas")
    is_featured: Optional[bool] = Field(None, description="Filtrar destacadas")
    is_public: Optional[bool] = Field(None, description="Filtrar públicas")
    
    # Date filters
    event_date_from: Optional[date] = Field(None, description="Fecha evento desde")
    event_date_to: Optional[date] = Field(None, description="Fecha evento hasta")
    created_from: Optional[datetime] = Field(None, description="Creado desde")
    created_to: Optional[datetime] = Field(None, description="Creado hasta")
    
    # Photo filters
    min_photos: Optional[int] = Field(None, ge=0, description="Mínimo número de fotos")
    max_photos: Optional[int] = Field(None, ge=1, description="Máximo número de fotos")
    photographer: Optional[str] = Field(None, description="Filtrar por fotógrafo")
    
    # Pagination
    page: int = Field(default=1, ge=1, description="Número de página")
    per_page: int = Field(default=20, ge=1, le=100, description="Items por página")
    
    # Sorting
    sort_by: str = Field(default="created_at", description="Campo para ordenar")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="Dirección")
    
    # Response options
    minimal: bool = Field(default=False, description="Respuesta mínima")
    include_photos: bool = Field(default=False, description="Incluir datos de fotos")
    include_author: bool = Field(default=True, description="Incluir datos del autor")
    include_category: bool = Field(default=True, description="Incluir datos de categoría")
    photos_limit: int = Field(default=10, ge=1, le=50, description="Límite de fotos a incluir")


class GalleryListResponse(BaseModel):
    """Paginated gallery list response"""
    galleries: List[GalleryResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class GalleryStatsResponse(BaseModel):
    """Gallery statistics response"""
    total_galleries: int
    published_galleries: int
    draft_galleries: int
    total_photos: int
    total_views: int
    total_downloads: int
    total_size_gb: float
    by_category: dict
    by_content_type: dict
    by_status: dict
    by_month: dict
    top_photographers: List[dict]


# ===================================
# FILE UPLOAD SCHEMAS
# ===================================

class FileUploadResponse(BaseModel):
    """File upload response"""
    success: bool
    filename: str
    original_filename: str
    file_size: int
    processed_paths: Dict[str, str]
    metadata: Dict[str, Any]
    message: Optional[str] = None


class BulkUploadResponse(BaseModel):
    """Bulk upload response"""
    total_uploaded: int
    successful: List[FileUploadResponse]
    failed: List[Dict[str, str]]
    processing_time: float
    total_size: int


class PhotoReorderRequest(BaseModel):
    """Photo reorder request"""
    photo_orders: List[Dict[str, int]] = Field(..., description="Lista de {filename: order}")


class PhotoUpdateRequest(BaseModel):
    """Photo update request"""
    filename: str = Field(..., description="Nombre del archivo")
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    sort_order: Optional[int] = Field(None, ge=0)