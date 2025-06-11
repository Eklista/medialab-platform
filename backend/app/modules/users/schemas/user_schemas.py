"""
User schemas for API validation and serialization
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


class UserStatus(str, Enum):
    """User status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


class UserType(str, Enum):
    """User type for polymorphic operations"""
    INTERNAL = "internal_user"
    INSTITUTIONAL = "institutional_user"


# ===================================
# BASE USER SCHEMAS
# ===================================

class BaseUserCreate(BaseModel):
    """Base user creation schema"""
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    preferred_language: str = Field(default="es", max_length=10)
    timezone: str = Field(default="America/Guatemala", max_length=50)
    
    @validator('username')
    def validate_username(cls, v, values):
        """Generate username if not provided"""
        if v is None and 'first_name' in values and 'last_name' in values:
            first = values['first_name'].lower().strip()
            last = values['last_name'].lower().strip()
            return f"{first}.{last}"
        return v


class BaseUserUpdate(BaseModel):
    """Base user update schema"""
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    preferred_language: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class BaseUserResponse(BaseModel):
    """Base user response schema"""
    id: int
    uuid: str
    username: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    profile_photo: Optional[str]
    bio: Optional[str]
    preferred_language: str
    timezone: str
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    full_name: str
    profile_completion: int
    
    class Config:
        from_attributes = True


# ===================================
# INTERNAL USER SCHEMAS
# ===================================

class InternalUserCreate(BaseUserCreate):
    """Internal user creation schema"""
    position: Optional[str] = Field(None, max_length=100, description="Cargo específico (opcional)")
    can_access_dashboard: bool = Field(default=True)
    area_ids: Optional[List[int]] = Field(default=[], description="Lista de IDs de áreas")


class InternalUserUpdate(BaseUserUpdate):
    """Internal user update schema"""
    position: Optional[str] = Field(None, max_length=100)
    banner_photo: Optional[str] = Field(None, max_length=500)
    can_access_dashboard: Optional[bool] = None


class InternalUserResponse(BaseUserResponse):
    """Internal user response schema"""
    employee_id: Optional[str]
    position: Optional[str]
    banner_photo: Optional[str]
    last_activity: Optional[datetime]
    can_access_dashboard: bool
    
    # Related data
    areas: List[dict] = []
    roles: List[dict] = []
    
    class Config:
        from_attributes = True


# ===================================
# INSTITUTIONAL USER SCHEMAS  
# ===================================

class InstitutionalUserCreate(BaseUserCreate):
    """Institutional user creation schema"""
    institution: str = Field(default="Universidad Galileo", max_length=200)
    faculty_id: Optional[str] = Field(None, max_length=50)
    academic_title: Optional[str] = Field(None, max_length=100)
    position_title: Optional[str] = Field(None, max_length=150)
    office_phone: Optional[str] = Field(None, max_length=50)
    office_location: Optional[str] = Field(None, max_length=200)
    
    # User type flags
    is_faculty: bool = Field(default=False)
    is_student: bool = Field(default=False)
    is_external_client: bool = Field(default=False)
    
    # Permissions
    can_request_projects: bool = Field(default=True)
    
    # Academic units
    academic_unit_ids: Optional[List[int]] = Field(default=[], description="Lista de IDs de unidades académicas")


class InstitutionalUserUpdate(BaseUserUpdate):
    """Institutional user update schema"""
    institution: Optional[str] = Field(None, max_length=200)
    faculty_id: Optional[str] = Field(None, max_length=50)
    academic_title: Optional[str] = Field(None, max_length=100)
    position_title: Optional[str] = Field(None, max_length=150)
    office_phone: Optional[str] = Field(None, max_length=50)
    office_location: Optional[str] = Field(None, max_length=200)
    is_faculty: Optional[bool] = None
    is_student: Optional[bool] = None
    is_external_client: Optional[bool] = None
    can_request_projects: Optional[bool] = None


class InstitutionalUserResponse(BaseUserResponse):
    """Institutional user response schema"""
    institution: str
    faculty_id: Optional[str]
    academic_title: Optional[str]
    position_title: Optional[str]
    office_phone: Optional[str]
    office_location: Optional[str]
    
    # User type flags
    is_faculty: bool
    is_student: bool
    is_external_client: bool
    
    # Permissions
    can_request_projects: bool
    
    # Related data
    academic_units: List[dict] = []
    roles: List[dict] = []
    
    class Config:
        from_attributes = True


# ===================================
# COMMON SCHEMAS
# ===================================

class UserListResponse(BaseModel):
    """Paginated user list response"""
    users: List[BaseUserResponse]
    total: int
    page: int
    per_page: int
    pages: int


class UserSearchParams(BaseModel):
    """User search parameters"""
    q: Optional[str] = Field(None, description="Search query")
    user_type: Optional[UserType] = Field(None, description="Filter by user type")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    area_id: Optional[int] = Field(None, description="Filter by area (internal users)")
    academic_unit_id: Optional[int] = Field(None, description="Filter by academic unit (institutional users)")
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    minimal: bool = Field(default=True, description="Return minimal data for performance")


class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserStatusUpdate(BaseModel):
    """User status update schema"""
    is_active: bool
    reason: Optional[str] = Field(None, max_length=500, description="Reason for status change")


class BulkUserOperation(BaseModel):
    """Bulk user operation schema"""
    user_ids: List[int] = Field(..., min_items=1, max_items=100)
    operation: str = Field(..., pattern="^(activate|deactivate|delete)$")
    reason: Optional[str] = Field(None, max_length=500)


# ===================================
# PROFILE COMPLETION SCHEMA
# ===================================

class ProfileCompletion(BaseModel):
    """Profile completion details"""
    completion_percentage: int = Field(..., ge=0, le=100)
    missing_fields: List[str] = []
    suggestions: List[str] = []
    
    class Config:
        from_attributes = True