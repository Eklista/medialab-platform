# backend/app/modules/organizations/schemas/area_schemas.py
"""
Area schemas for API validation and serialization
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class AreaCategory(str, Enum):
    """Area category options"""
    PRODUCTION = "production"
    TECHNICAL = "technical"
    ADMINISTRATIVE = "administrative"
    CREATIVE = "creative"


# ===================================
# AREA SCHEMAS
# ===================================

class AreaCreate(BaseModel):
    """Area creation schema"""
    name: str = Field(..., min_length=3, max_length=150)
    short_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    category: AreaCategory = Field(default=AreaCategory.PRODUCTION)
    specialization: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=20, description="Color hex para UI")
    icon: Optional[str] = Field(None, max_length=50, description="Ícono para UI")
    sort_order: int = Field(default=100, ge=0)
    can_lead_projects: bool = Field(default=True)
    requires_collaboration: bool = Field(default=False)
    max_concurrent_projects: Optional[int] = Field(None, ge=1)
    estimated_capacity_hours: Optional[int] = Field(None, ge=1)
    contact_email: Optional[str] = Field(None, max_length=150)
    contact_phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=200)


class AreaUpdate(BaseModel):
    """Area update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=150)
    short_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[AreaCategory] = None
    specialization: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    can_lead_projects: Optional[bool] = None
    requires_collaboration: Optional[bool] = None
    max_concurrent_projects: Optional[int] = Field(None, ge=1)
    estimated_capacity_hours: Optional[int] = Field(None, ge=1)
    contact_email: Optional[str] = Field(None, max_length=150)
    contact_phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=200)


class AreaResponse(BaseModel):
    """Area response schema"""
    id: int
    name: str
    short_name: Optional[str]
    description: Optional[str]
    category: str
    specialization: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    is_active: bool
    sort_order: int
    can_lead_projects: bool
    requires_collaboration: bool
    max_concurrent_projects: Optional[int]
    estimated_capacity_hours: Optional[int]
    total_members: int
    active_projects: int
    completed_projects: int
    contact_email: Optional[str]
    contact_phone: Optional[str]
    location: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Relaciones
    members: List[dict] = []
    
    class Config:
        from_attributes = True


class AreaListResponse(BaseModel):
    """Paginated area list response"""
    areas: List[AreaResponse]
    total: int
    page: int
    per_page: int
    pages: int


class AreaSearchParams(BaseModel):
    """Area search parameters"""
    q: Optional[str] = Field(None, description="Search query")
    category: Optional[AreaCategory] = Field(None, description="Filter by category")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    can_lead_projects: Optional[bool] = Field(None, description="Filter by project leadership capability")
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class AreaMemberAssign(BaseModel):
    """Assign member to area"""
    user_id: int = Field(..., ge=1)
    role_in_area: Optional[str] = Field(None, max_length=100, description="Rol específico en el área")
    specialization: Optional[str] = Field(None, max_length=150, description="Especialización del miembro")
    is_primary: bool = Field(default=False, description="¿Es su área principal?")
    can_lead_projects: bool = Field(default=False, description="¿Puede liderar proyectos?")
    time_allocation_percentage: Optional[int] = Field(None, ge=1, le=100, description="% de tiempo asignado")


class AreaMemberRemove(BaseModel):
    """Remove member from area"""
    user_id: int = Field(..., ge=1)


class AreaStatistics(BaseModel):
    """Area statistics"""
    total_areas: int
    active_areas: int
    by_category: dict = {}
    total_members: int
    areas_with_projects: int
    average_members_per_area: float