"""
Security schemas for API validation and serialization
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class PermissionCategory(str, Enum):
    """Permission category options"""
    USERS = "users"
    CONTENT = "content"
    PROJECTS = "projects"
    ADMIN = "admin"
    DASHBOARD = "dashboard"
    REPORTS = "reports"


class RoleType(str, Enum):
    """Role type options"""
    SYSTEM = "system"
    STANDARD = "standard"
    CUSTOM = "custom"


# ===================================
# PERMISSION SCHEMAS
# ===================================

class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str = Field(..., max_length=100)
    display_name: str = Field(..., max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    category: PermissionCategory = Field(default=PermissionCategory.CONTENT)
    resource: Optional[str] = Field(None, max_length=50)
    action: Optional[str] = Field(None, max_length=50)
    sort_order: int = Field(default=100)


class PermissionResponse(PermissionBase):
    """Permission response schema"""
    id: int
    is_active: bool
    is_system: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PermissionListResponse(BaseModel):
    """Paginated permission list response"""
    permissions: List[PermissionResponse]
    total: int
    by_category: Dict[str, List[PermissionResponse]] = {}


# ===================================
# ROLE SCHEMAS
# ===================================

class RoleCreate(BaseModel):
    """Role creation schema"""
    name: str = Field(..., min_length=3, max_length=100)
    display_name: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    level: int = Field(default=100, ge=1, le=1000)
    role_type: RoleType = Field(default=RoleType.CUSTOM)
    target_user_type: Optional[str] = Field(None, pattern="^(internal_user|institutional_user|both)$")
    color: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)
    sort_order: int = Field(default=100)
    max_assignments: Optional[int] = Field(None, ge=1)
    permission_ids: List[int] = Field(default=[], description="List of permission IDs")


class RoleUpdate(BaseModel):
    """Role update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    display_name: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    level: Optional[int] = Field(None, ge=1, le=1000)
    role_type: Optional[RoleType] = None
    target_user_type: Optional[str] = Field(None, pattern="^(internal_user|institutional_user|both)$")
    color: Optional[str] = Field(None, max_length=20)
    icon: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[int] = Field(None, ge=0)
    max_assignments: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class RoleResponse(BaseModel):
    """Role response schema"""
    id: int
    name: str
    display_name: str
    description: Optional[str]
    level: int
    role_type: str
    target_user_type: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    sort_order: int
    max_assignments: Optional[int]
    is_active: bool
    is_system: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    # Calculated fields
    permission_count: int = 0
    assignment_count: int = 0
    permissions: List[PermissionResponse] = []
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Paginated role list response"""
    roles: List[RoleResponse]
    total: int
    page: int
    per_page: int
    pages: int


class RoleSearchParams(BaseModel):
    """Role search parameters"""
    q: Optional[str] = Field(None, description="Search query")
    role_type: Optional[RoleType] = Field(None, description="Filter by role type")
    target_user_type: Optional[str] = Field(None, description="Filter by target user type")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    level_min: Optional[int] = Field(None, ge=1, description="Minimum level")
    level_max: Optional[int] = Field(None, le=1000, description="Maximum level")
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    include_permissions: bool = Field(default=False, description="Include permission details")


# ===================================
# ROLE PERMISSION SCHEMAS
# ===================================

class RolePermissionAssign(BaseModel):
    """Role permission assignment schema"""
    permission_ids: List[int] = Field(..., min_items=1)
    grant_type: str = Field(default="direct", pattern="^(direct|inherited)$")
    assigned_reason: Optional[str] = Field(None, max_length=500)


class RolePermissionRemove(BaseModel):
    """Role permission removal schema"""
    permission_ids: List[int] = Field(..., min_items=1)


class RolePermissionResponse(BaseModel):
    """Role permission relationship response"""
    id: int
    role_id: int
    permission_id: int
    grant_type: str
    assigned_reason: Optional[str]
    is_active: bool
    created_at: datetime
    
    permission: PermissionResponse
    
    class Config:
        from_attributes = True


# ===================================
# ROLE ASSIGNMENT SCHEMAS
# ===================================

class UserRoleAssign(BaseModel):
    """User role assignment schema"""
    user_id: int = Field(..., ge=1)
    user_type: str = Field(..., pattern="^(internal_user|institutional_user)$")
    is_primary: bool = Field(default=False)
    assigned_reason: Optional[str] = Field(None, max_length=500)


class UserRoleRemove(BaseModel):
    """User role removal schema"""
    user_id: int = Field(..., ge=1)
    user_type: str = Field(..., pattern="^(internal_user|institutional_user)$")


class BulkRoleAssign(BaseModel):
    """Bulk role assignment schema"""
    role_ids: List[int] = Field(..., min_items=1, max_items=10)
    user_type: str = Field(..., pattern="^(internal_user|institutional_user)$")
    assigned_reason: Optional[str] = Field(None, max_length=500)


class UserRoleResponse(BaseModel):
    """User role response schema"""
    id: int
    user_id: int
    role_id: int
    user_type: str
    is_active: bool
    is_primary: bool
    assigned_reason: Optional[str]
    created_at: datetime
    
    role: RoleResponse
    
    class Config:
        from_attributes = True


# ===================================
# ANALYTICS SCHEMAS
# ===================================

class RoleStatistics(BaseModel):
    """Role statistics schema"""
    total_roles: int
    active_roles: int
    system_roles: int
    custom_roles: int
    total_permissions: int
    active_permissions: int
    total_assignments: int
    by_user_type: Dict[str, int] = {}
    by_role_type: Dict[str, int] = {}
    by_permission_category: Dict[str, int] = {}


class PermissionUsageStats(BaseModel):
    """Permission usage statistics"""
    permission_id: int
    permission_name: str
    roles_count: int
    users_count: int
    usage_percentage: float
    
    class Config:
        from_attributes = True


# ===================================
# VALIDATION SCHEMAS
# ===================================

class RoleValidationResponse(BaseModel):
    """Role validation response"""
    is_valid: bool
    conflicts: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []


class PermissionValidationResponse(BaseModel):
    """Permission validation response"""
    is_valid: bool
    missing_permissions: List[str] = []
    conflicting_permissions: List[str] = []
    recommended_permissions: List[str] = []