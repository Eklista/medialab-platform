"""
CMS Category Schemas - Validation and serialization
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class CategoryType(str, Enum):
    """Category type options"""
    EVENT = "event"
    ACADEMIC = "academic"
    INSTITUTIONAL = "institutional"
    GRADUATION = "graduation"
    CEREMONY = "ceremony"
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    GENERAL = "general"


class ContentTypeFocus(str, Enum):
    """Content type focus options"""
    MIXED = "mixed"
    VIDEO_FOCUSED = "video_focused"
    GALLERY_FOCUSED = "gallery_focused"


class CategoryStatus(str, Enum):
    """Category status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


# ===================================
# BASE CATEGORY SCHEMAS
# ===================================

class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    display_name: Optional[str] = Field(None, max_length=150, description="Nombre para mostrar")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción de la categoría")
    
    category_type: CategoryType = Field(default=CategoryType.EVENT, description="Tipo de categoría")
    content_type_focus: ContentTypeFocus = Field(default=ContentTypeFocus.MIXED, description="Enfoque de contenido")
    
    color: Optional[str] = Field(None, max_length=20, description="Color en formato hex")
    icon: Optional[str] = Field(None, max_length=50, description="Icono CSS/nombre")
    cover_image: Optional[str] = Field(None, max_length=500, description="Imagen de portada")
    
    is_featured: bool = Field(default=False, description="Destacar categoría")
    is_public: bool = Field(default=True, description="Visible públicamente")
    sort_order: int = Field(default=100, ge=0, le=9999, description="Orden de visualización")
    
    auto_approve_content: bool = Field(default=False, description="Auto aprobar contenido")
    requires_review: bool = Field(default=True, description="Requiere revisión")


class CategoryCreate(CategoryBase):
    """Category creation schema"""
    academic_unit_id: int = Field(..., description="ID de la unidad académica")
    
    @validator('display_name', pre=True, always=True)
    def set_display_name(cls, v, values):
        if v is None and 'name' in values:
            return values['name']
        return v


class CategoryUpdate(BaseModel):
    """Category update schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    display_name: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    
    category_type: Optional[CategoryType] = None
    content_type_focus: Optional[ContentTypeFocus] = None
    
    color: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)
    cover_image: Optional[str] = Field(None, max_length=500)
    
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    sort_order: Optional[int] = Field(None, ge=0, le=9999)
    
    auto_approve_content: Optional[bool] = None
    requires_review: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Category response schema"""
    id: int
    slug: Optional[str]
    academic_unit_id: int
    is_active: bool
    
    # Statistics
    total_videos: int
    total_galleries: int
    total_views: int
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Related data
    academic_unit: Optional[dict] = None
    
    class Config:
        from_attributes = True


class CategoryMinimal(BaseModel):
    """Minimal category for dropdowns/selects"""
    id: int
    name: str
    display_name: Optional[str]
    slug: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


class CategoryWithContent(CategoryResponse):
    """Category with content counts by type"""
    content_summary: dict = Field(default_factory=dict)
    recent_videos: List[dict] = Field(default_factory=list)
    recent_galleries: List[dict] = Field(default_factory=list)


# ===================================
# SEARCH AND FILTERING
# ===================================

class CategorySearchParams(BaseModel):
    """Category search parameters"""
    q: Optional[str] = Field(None, description="Búsqueda por nombre/descripción")
    academic_unit_id: Optional[int] = Field(None, description="Filtrar por unidad académica")
    category_type: Optional[CategoryType] = Field(None, description="Filtrar por tipo")
    content_type_focus: Optional[ContentTypeFocus] = Field(None, description="Filtrar por enfoque")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    is_featured: Optional[bool] = Field(None, description="Filtrar destacadas")
    is_public: Optional[bool] = Field(None, description="Filtrar públicas")
    
    # Pagination
    page: int = Field(default=1, ge=1, description="Número de página")
    per_page: int = Field(default=20, ge=1, le=100, description="Items por página")
    
    # Sorting
    sort_by: str = Field(default="sort_order", description="Campo para ordenar")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Dirección del orden")
    
    # Response options
    minimal: bool = Field(default=False, description="Respuesta mínima para performance")
    include_content: bool = Field(default=False, description="Incluir conteo de contenido")


class CategoryListResponse(BaseModel):
    """Paginated category list response"""
    categories: List[CategoryResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class CategoryStatsResponse(BaseModel):
    """Category statistics response"""
    total_categories: int
    active_categories: int
    featured_categories: int
    by_academic_unit: dict
    by_type: dict
    by_content_focus: dict
    content_distribution: dict