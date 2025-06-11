# backend/app/modules/organizations/schemas/academic_unit_schemas.py
"""
Academic Unit schemas for API validation and serialization
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class AcademicUnitCategory(str, Enum):
    """Academic unit category options"""
    ACADEMIC = "academic"
    RESEARCH = "research"
    ADMINISTRATIVE = "administrative"
    SERVICE = "service"


# ===================================
# ACADEMIC UNIT TYPE SCHEMAS
# ===================================

class AcademicUnitTypeCreate(BaseModel):
    """Academic unit type creation schema"""
    name: str = Field(..., min_length=3, max_length=100)
    display_name: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    hierarchy_level: int = Field(default=1, ge=1, le=10, description="1=Facultad, 2=Escuela, 3=Instituto, etc.")
    abbreviation: Optional[str] = Field(None, max_length=10)
    category: AcademicUnitCategory = Field(default=AcademicUnitCategory.ACADEMIC)
    sort_order: int = Field(default=100, ge=0)
    allows_students: bool = Field(default=True, description="¿Permite estudiantes?")
    allows_faculty: bool = Field(default=True, description="¿Permite faculty?")
    requires_approval: bool = Field(default=False, description="¿Requiere aprobación para asignación?")


class AcademicUnitTypeUpdate(BaseModel):
    """Academic unit type update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    display_name: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    hierarchy_level: Optional[int] = Field(None, ge=1, le=10)
    abbreviation: Optional[str] = Field(None, max_length=10)
    category: Optional[AcademicUnitCategory] = None
    sort_order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    allows_students: Optional[bool] = None
    allows_faculty: Optional[bool] = None
    requires_approval: Optional[bool] = None


class AcademicUnitTypeResponse(BaseModel):
    """Academic unit type response schema"""
    id: int
    name: str
    display_name: str
    description: Optional[str]
    hierarchy_level: int
    abbreviation: Optional[str]
    category: str
    is_active: bool
    sort_order: int
    allows_students: bool
    allows_faculty: bool
    requires_approval: bool
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    academic_units_count: int = 0
    
    class Config:
        from_attributes = True


class AcademicUnitTypeListResponse(BaseModel):
    """Paginated academic unit type list response"""
    academic_unit_types: List[AcademicUnitTypeResponse]
    total: int
    page: int
    per_page: int
    pages: int


# ===================================
# ACADEMIC UNIT SCHEMAS
# ===================================

class AcademicUnitCreate(BaseModel):
    """Academic unit creation schema"""
    name: str = Field(..., min_length=3, max_length=200)
    short_name: Optional[str] = Field(None, max_length=100)
    abbreviation: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    academic_unit_type_id: int = Field(..., ge=1, description="ID del tipo de unidad académica")
    
    # Contact information
    website: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)
    building: Optional[str] = Field(None, max_length=100)
    
    # Visual identity
    logo_url: Optional[str] = Field(None, max_length=500)
    color_primary: Optional[str] = Field(None, max_length=20)
    color_secondary: Optional[str] = Field(None, max_length=20)
    
    # Configuration
    sort_order: int = Field(default=100, ge=0)
    allows_public_content: bool = Field(default=True, description="¿Permite contenido público?")
    requires_approval: bool = Field(default=False, description="¿Requiere aprobación para contenido?")


class AcademicUnitUpdate(BaseModel):
    """Academic unit update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    short_name: Optional[str] = Field(None, max_length=100)
    abbreviation: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    academic_unit_type_id: Optional[int] = Field(None, ge=1)
    
    # Contact information
    website: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)
    building: Optional[str] = Field(None, max_length=100)
    
    # Visual identity
    logo_url: Optional[str] = Field(None, max_length=500)
    color_primary: Optional[str] = Field(None, max_length=20)
    color_secondary: Optional[str] = Field(None, max_length=20)
    
    # Status and configuration
    is_active: Optional[bool] = None
    sort_order: Optional[int] = Field(None, ge=0)
    allows_public_content: Optional[bool] = None
    requires_approval: Optional[bool] = None


class AcademicUnitResponse(BaseModel):
    """Academic unit response schema"""
    id: int
    name: str
    short_name: Optional[str]
    abbreviation: Optional[str]
    description: Optional[str]
    
    # Type relationship
    academic_unit_type_id: int
    academic_unit_type: dict = {}
    
    # Contact information
    website: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    building: Optional[str]
    
    # Visual identity
    logo_url: Optional[str]
    color_primary: Optional[str]
    color_secondary: Optional[str]
    
    # Status and configuration
    is_active: bool
    sort_order: int
    allows_public_content: bool
    requires_approval: bool
    
    # Statistics
    total_students: int
    total_faculty: int
    total_projects: int
    
    created_at: datetime
    updated_at: datetime
    
    # Relaciones
    members: List[dict] = []
    categories: List[dict] = []
    
    class Config:
        from_attributes = True


class AcademicUnitListResponse(BaseModel):
    """Paginated academic unit list response"""
    academic_units: List[AcademicUnitResponse]
    total: int
    page: int
    per_page: int
    pages: int


class AcademicUnitSearchParams(BaseModel):
    """Academic unit search parameters"""
    q: Optional[str] = Field(None, description="Search query")
    academic_unit_type_id: Optional[int] = Field(None, ge=1, description="Filter by type")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    allows_public_content: Optional[bool] = Field(None, description="Filter by public content permission")
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class AcademicUnitMemberAssign(BaseModel):
    """Assign member to academic unit"""
    user_id: int = Field(..., ge=1)
    relationship_type: str = Field(default="member", max_length=50, description="Tipo de relación (student, faculty, staff)")
    position_title: Optional[str] = Field(None, max_length=150, description="Cargo específico")
    department: Optional[str] = Field(None, max_length=100, description="Departamento")
    degree_program: Optional[str] = Field(None, max_length=200, description="Programa académico (estudiantes)")
    academic_year: Optional[str] = Field(None, max_length=20, description="Año académico")
    is_primary: bool = Field(default=False, description="¿Es su unidad principal?")
    can_represent_unit: bool = Field(default=False, description="¿Puede representar la unidad?")
    has_budget_authority: bool = Field(default=False, description="¿Tiene autoridad presupuestaria?")
    office_number: Optional[str] = Field(None, max_length=50)
    internal_phone: Optional[str] = Field(None, max_length=50)


class AcademicUnitMemberRemove(BaseModel):
    """Remove member from academic unit"""
    user_id: int = Field(..., ge=1)


class AcademicUnitStatistics(BaseModel):
    """Academic unit statistics"""
    total_units: int
    active_units: int
    by_type: dict = {}
    total_students: int
    total_faculty: int
    units_with_projects: int
    average_members_per_unit: float