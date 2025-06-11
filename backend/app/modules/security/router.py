"""
Security Router - API endpoints for security management
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.security.controllers.security_controller import (
    role_controller,
    permission_controller,
    security_analytics_controller
)
from app.modules.security.schemas.security_schemas import (
    # Role schemas
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleListResponse,
    RoleSearchParams,
    RoleStatistics,
    RoleValidationResponse,
    
    # Permission schemas
    PermissionResponse,
    PermissionListResponse,
    PermissionValidationResponse,
    PermissionCategory,
    
    # Role-Permission schemas
    RolePermissionAssign,
    RolePermissionRemove,
    RolePermissionResponse,
    
    # User-Role schemas
    UserRoleAssign,
    UserRoleRemove,
    BulkRoleAssign,
    
    # Analytics schemas
    PermissionUsageStats
)

# Create router instance
router = APIRouter(prefix="/security", tags=["Security"])

# ===================================
# ROLE MANAGEMENT ENDPOINTS
# ===================================

@router.post("/roles", response_model=RoleResponse, status_code=201)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):
    """Create new role with permissions"""
    return await role_controller.create_role(role_data, db)


@router.get("/roles", response_model=RoleListResponse)
async def get_roles(
    q: Optional[str] = Query(None, description="Search query"),
    role_type: Optional[str] = Query(None, description="Filter by role type"),
    target_user_type: Optional[str] = Query(None, description="Filter by target user type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    level_min: Optional[int] = Query(None, ge=1, description="Minimum level"),
    level_max: Optional[int] = Query(None, le=1000, description="Maximum level"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    include_permissions: bool = Query(False, description="Include permission details"),
    db: Session = Depends(get_db)
):
    """Get paginated list of roles with filters"""
    params = RoleSearchParams(
        q=q,
        role_type=role_type,
        target_user_type=target_user_type,
        is_active=is_active,
        level_min=level_min,
        level_max=level_max,
        page=page,
        per_page=per_page,
        include_permissions=include_permissions
    )
    return await role_controller.get_roles(params, db)

@router.get("/roles/templates")
async def get_role_templates():
    """Get predefined role templates for quick creation"""
    return {
        "internal_user_templates": [
            {
                "name": "content_creator",
                "display_name": "Content Creator",
                "description": "Can create and manage content",
                "level": 300,
                "target_user_type": "internal_user",
                "suggested_permissions": [
                    "content.create", "content.edit", "content.publish",
                    "dashboard.access", "profile.edit"
                ]
            },
            {
                "name": "project_manager",
                "display_name": "Project Manager",
                "description": "Can manage projects and team assignments",
                "level": 500,
                "target_user_type": "internal_user",
                "suggested_permissions": [
                    "projects.create", "projects.edit", "projects.assign",
                    "users.view", "dashboard.access", "reports.view"
                ]
            },
            {
                "name": "administrator",
                "display_name": "Administrator",
                "description": "Full system access",
                "level": 900,
                "target_user_type": "internal_user",
                "suggested_permissions": [
                    "users.create", "users.edit", "users.delete",
                    "roles.create", "roles.edit", "system.admin",
                    "reports.all", "dashboard.admin"
                ]
            }
        ],
        "institutional_user_templates": [
            {
                "name": "faculty_basic",
                "display_name": "Faculty Member",
                "description": "Basic faculty permissions",
                "level": 200,
                "target_user_type": "institutional_user",
                "suggested_permissions": [
                    "projects.request", "content.view", "profile.edit"
                ]
            },
            {
                "name": "student_basic",
                "display_name": "Student",
                "description": "Basic student permissions",
                "level": 100,
                "target_user_type": "institutional_user",
                "suggested_permissions": [
                    "content.view", "profile.edit"
                ]
            },
            {
                "name": "external_client",
                "display_name": "External Client",
                "description": "External client permissions",
                "level": 150,
                "target_user_type": "institutional_user",
                "suggested_permissions": [
                    "projects.request", "content.view", "profile.edit"
                ]
            }
        ]
    }



@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int = Path(..., description="Role ID"),
    db: Session = Depends(get_db)
):
    """Get role by ID with full details"""
    return await role_controller.get_role(role_id, db)


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int = Path(..., description="Role ID"),
    update_data: RoleUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update role"""
    return await role_controller.update_role(role_id, update_data, db)


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int = Path(..., description="Role ID"),
    hard_delete: bool = Query(False, description="Perform hard delete (permanent)"),
    db: Session = Depends(get_db)
):
    """Delete role (soft or hard delete)"""
    return await role_controller.delete_role(role_id, db, hard_delete)


@router.post("/roles/{role_id}/clone", response_model=RoleResponse)
async def clone_role(
    role_id: int = Path(..., description="Source role ID"),
    new_name: str = Body(..., embed=True),
    new_display_name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Clone existing role with its permissions"""
    return await role_controller.clone_role(role_id, new_name, new_display_name, db)


@router.post("/roles/validate", response_model=RoleValidationResponse)
async def validate_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):
    """Validate role data without creating"""
    return await role_controller.validate_role(role_data, db)


@router.get("/roles/{role_id}/analysis")
async def analyze_role_complexity(
    role_id: int = Path(..., description="Role ID"),
    db: Session = Depends(get_db)
):
    """Analyze role complexity and get optimization suggestions"""
    return await role_controller.analyze_role_complexity(role_id, db)


@router.patch("/roles/bulk-update")
async def bulk_update_roles(
    role_ids: List[int] = Body(..., description="List of role IDs"),
    is_active: bool = Body(..., description="New active status"),
    db: Session = Depends(get_db)
):
    """Bulk update role status"""
    return await role_controller.bulk_update_roles(role_ids, is_active, db)


# ===================================
# ROLE PERMISSIONS ENDPOINTS
# ===================================

@router.get("/roles/{role_id}/permissions", response_model=List[RolePermissionResponse])
async def get_role_permissions(
    role_id: int = Path(..., description="Role ID"),
    db: Session = Depends(get_db)
):
    """Get permissions assigned to role"""
    return await role_controller.get_role_permissions(role_id, db)


@router.post("/roles/{role_id}/permissions", response_model=List[RolePermissionResponse])
async def assign_permissions_to_role(
    role_id: int = Path(..., description="Role ID"),
    permission_data: RolePermissionAssign = ...,
    db: Session = Depends(get_db)
):
    """Assign permissions to role (additive)"""
    return await role_controller.assign_permissions_to_role(role_id, permission_data, db)


@router.put("/roles/{role_id}/permissions", response_model=List[RolePermissionResponse])
async def replace_role_permissions(
    role_id: int = Path(..., description="Role ID"),
    permission_data: RolePermissionAssign = ...,
    db: Session = Depends(get_db)
):
    """Replace all role permissions"""
    return await role_controller.replace_role_permissions(role_id, permission_data, db)


@router.delete("/roles/{role_id}/permissions")
async def remove_permissions_from_role(
    role_id: int = Path(..., description="Role ID"),
    permission_data: RolePermissionRemove = ...,
    db: Session = Depends(get_db)
):
    """Remove permissions from role"""
    return await role_controller.remove_permissions_from_role(role_id, permission_data, db)


@router.post("/roles/{role_id}/permissions/validate", response_model=PermissionValidationResponse)
async def validate_permission_assignment(
    role_id: int = Path(..., description="Role ID"),
    permission_ids: List[int] = Body(..., description="Permission IDs to validate"),
    db: Session = Depends(get_db)
):
    """Validate permission assignment to role"""
    return await security_analytics_controller.validate_permission_assignment(role_id, permission_ids, db)


# ===================================
# PERMISSION ENDPOINTS
# ===================================

@router.get("/permissions", response_model=PermissionListResponse)
async def get_permissions(
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=500, description="Limit items"),
    search: Optional[str] = Query(None, description="Search query"),
    category: Optional[PermissionCategory] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    grouped: bool = Query(False, description="Group by category"),
    db: Session = Depends(get_db)
):
    """Get paginated list of permissions or grouped by category"""
    return await permission_controller.get_permissions(
        skip, limit, search, category, is_active, grouped, db
    )


@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int = Path(..., description="Permission ID"),
    db: Session = Depends(get_db)
):
    """Get permission by ID"""
    return await permission_controller.get_permission(permission_id, db)


# ===================================
# ANALYTICS AND REPORTING ENDPOINTS
# ===================================

@router.get("/analytics/statistics", response_model=RoleStatistics)
async def get_security_statistics(
    db: Session = Depends(get_db)
):
    """Get comprehensive security statistics"""
    return await security_analytics_controller.get_security_statistics(db)


@router.get("/analytics/dashboard")
async def get_security_dashboard(
    db: Session = Depends(get_db)
):
    """Get security dashboard data"""
    return await security_analytics_controller.get_dashboard_data(db)


@router.get("/analytics/permissions/usage")
async def get_permission_usage_stats(
    db: Session = Depends(get_db)
):
    """Get permission usage statistics"""
    return await security_analytics_controller.get_permission_usage_stats(db)


@router.get("/analytics/roles/popular")
async def get_most_used_roles(
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Get most used roles by assignment count"""
    return await security_analytics_controller.get_most_used_roles(db, limit)


# ===================================
# UTILITY ENDPOINTS
# ===================================
@router.get("/permissions/categories")
async def get_permission_categories():
    """Get available permission categories"""
    return {
        "categories": [
            {
                "value": "users",
                "label": "User Management",
                "description": "Permissions related to user account management"
            },
            {
                "value": "content",
                "label": "Content Management",
                "description": "Permissions for creating and managing content"
            },
            {
                "value": "projects",
                "label": "Project Management",
                "description": "Permissions for project lifecycle management"
            },
            {
                "value": "admin",
                "label": "System Administration",
                "description": "Administrative and system-level permissions"
            },
            {
                "value": "dashboard",
                "label": "Dashboard Access",
                "description": "Permissions for dashboard and interface access"
            },
            {
                "value": "reports",
                "label": "Reporting",
                "description": "Permissions for viewing and generating reports"
            }
        ]
    }


@router.get("/health")
async def security_health_check(db: Session = Depends(get_db)):
    """Security module health check"""
    try:
        # Test basic database connectivity for security tables
        stats = await security_analytics_controller.get_security_statistics(db)
        
        return {
            "status": "healthy",
            "module": "security",
            "total_roles": stats.total_roles,
            "total_permissions": stats.total_permissions,
            "total_assignments": stats.total_assignments
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Security module health check failed: {str(e)}"
        )