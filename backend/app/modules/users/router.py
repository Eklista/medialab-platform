"""
Users Router - API endpoints for user management
All business logic is delegated to controllers
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.controllers import (
    internal_users_controller,
    institutional_users_controller
)
from app.modules.users.schemas import (
    # Internal User Schemas
    InternalUserCreate,
    InternalUserUpdate,
    InternalUserResponse,
    # Institutional User Schemas
    InstitutionalUserCreate,
    InstitutionalUserUpdate,
    InstitutionalUserResponse,
    # Common Schemas
    UserListResponse,
    UserSearchParams,
    ProfileCompletion,
    PasswordChangeRequest,
    UserStatusUpdate
)

# Create router instance
router = APIRouter(prefix="/users", tags=["Users"])

# ===================================
# INTERNAL USERS ENDPOINTS
# ===================================

@router.post("/internal", response_model=InternalUserResponse, status_code=201)
async def create_internal_user(
    user_data: InternalUserCreate,
    db: Session = Depends(get_db)
):
    """Create new internal user"""
    return await internal_users_controller.create_internal_user(user_data, db)


@router.get("/internal", response_model=UserListResponse)
async def get_internal_users(
    q: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    area_id: Optional[int] = Query(None, description="Filter by area"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    minimal: bool = Query(True, description="Return minimal data for performance"),
    db: Session = Depends(get_db)
):
    """Get paginated list of internal users"""
    params = UserSearchParams(
        q=q,
        is_active=is_active,
        area_id=area_id,
        page=page,
        per_page=per_page,
        minimal=minimal
    )
    return await internal_users_controller.get_internal_users(params, db, minimal)


@router.get("/internal/{user_id}", response_model=InternalUserResponse)
async def get_internal_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get internal user by ID (full details)"""
    return await internal_users_controller.get_internal_user(user_id, db)


@router.get("/internal/uuid/{uuid}", response_model=InternalUserResponse)
async def get_internal_user_by_uuid(
    uuid: str = Path(..., description="User UUID"),
    db: Session = Depends(get_db)
):
    """Get internal user by UUID (full details)"""
    return await internal_users_controller.get_internal_user_by_uuid(uuid, db)


@router.put("/internal/{user_id}", response_model=InternalUserResponse)
async def update_internal_user(
    user_id: int = Path(..., description="User ID"),
    update_data: InternalUserUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update internal user"""
    return await internal_users_controller.update_internal_user(user_id, update_data, db)


@router.delete("/internal/{user_id}")
async def delete_internal_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Delete internal user"""
    return await internal_users_controller.delete_internal_user(user_id, db)


@router.post("/internal/{user_id}/areas")
async def assign_areas_to_internal_user(
    user_id: int = Path(..., description="User ID"),
    area_ids: List[int] = ...,
    db: Session = Depends(get_db)
):
    """Assign areas to internal user"""
    return await internal_users_controller.assign_areas_to_user(user_id, area_ids, db)


@router.post("/internal/{user_id}/roles")
async def assign_roles_to_internal_user(
    user_id: int = Path(..., description="User ID"),
    role_ids: List[int] = ...,
    db: Session = Depends(get_db)
):
    """Assign roles to internal user"""
    return await internal_users_controller.assign_roles_to_user(user_id, role_ids, db)


@router.get("/internal/{user_id}/profile-completion", response_model=ProfileCompletion)
async def get_internal_user_profile_completion(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get internal user profile completion status"""
    return await internal_users_controller.get_user_profile_completion(user_id, db)


@router.patch("/internal/{user_id}/deactivate")
async def deactivate_internal_user(
    user_id: int = Path(..., description="User ID"),
    reason: str = Query(..., description="Reason for deactivation"),
    db: Session = Depends(get_db)
):
    """Deactivate internal user"""
    return await internal_users_controller.deactivate_user(user_id, reason, db)


@router.patch("/internal/{user_id}/activate")
async def activate_internal_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Activate internal user"""
    return await internal_users_controller.activate_user(user_id, db)


# ===================================
# INSTITUTIONAL USERS ENDPOINTS
# ===================================

@router.post("/institutional", response_model=InstitutionalUserResponse, status_code=201)
async def create_institutional_user(
    user_data: InstitutionalUserCreate,
    db: Session = Depends(get_db)
):
    """Create new institutional user"""
    return await institutional_users_controller.create_institutional_user(user_data, db)


@router.get("/institutional", response_model=UserListResponse)
async def get_institutional_users(
    q: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    academic_unit_id: Optional[int] = Query(None, description="Filter by academic unit"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    minimal: bool = Query(True, description="Return minimal data for performance"),
    db: Session = Depends(get_db)
):
    """Get paginated list of institutional users"""
    params = UserSearchParams(
        q=q,
        is_active=is_active,
        academic_unit_id=academic_unit_id,
        page=page,
        per_page=per_page,
        minimal=minimal
    )
    return await institutional_users_controller.get_institutional_users(params, db, minimal)


@router.get("/institutional/faculty", response_model=UserListResponse)
async def get_faculty_users(
    q: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    academic_unit_id: Optional[int] = Query(None, description="Filter by academic unit"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    minimal: bool = Query(True, description="Return minimal data for performance"),
    db: Session = Depends(get_db)
):
    """Get faculty users"""
    params = UserSearchParams(
        q=q,
        is_active=is_active,
        academic_unit_id=academic_unit_id,
        page=page,
        per_page=per_page,
        minimal=minimal
    )
    return await institutional_users_controller.get_users_by_type("faculty", params, db, minimal)


@router.get("/institutional/students", response_model=UserListResponse)
async def get_student_users(
    q: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    academic_unit_id: Optional[int] = Query(None, description="Filter by academic unit"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    minimal: bool = Query(True, description="Return minimal data for performance"),
    db: Session = Depends(get_db)
):
    """Get student users"""
    params = UserSearchParams(
        q=q,
        is_active=is_active,
        academic_unit_id=academic_unit_id,
        page=page,
        per_page=per_page,
        minimal=minimal
    )
    return await institutional_users_controller.get_users_by_type("student", params, db, minimal)


@router.get("/institutional/external", response_model=UserListResponse)
async def get_external_users(
    q: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    academic_unit_id: Optional[int] = Query(None, description="Filter by academic unit"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    minimal: bool = Query(True, description="Return minimal data for performance"),
    db: Session = Depends(get_db)
):
    """Get external client users"""
    params = UserSearchParams(
        q=q,
        is_active=is_active,
        academic_unit_id=academic_unit_id,
        page=page,
        per_page=per_page,
        minimal=minimal
    )
    return await institutional_users_controller.get_users_by_type("external", params, db, minimal)


@router.get("/institutional/{user_id}", response_model=InstitutionalUserResponse)
async def get_institutional_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get institutional user by ID (full details)"""
    return await institutional_users_controller.get_institutional_user(user_id, db)


@router.get("/institutional/uuid/{uuid}", response_model=InstitutionalUserResponse)
async def get_institutional_user_by_uuid(
    uuid: str = Path(..., description="User UUID"),
    db: Session = Depends(get_db)
):
    """Get institutional user by UUID (full details)"""
    return await institutional_users_controller.get_institutional_user_by_uuid(uuid, db)


@router.put("/institutional/{user_id}", response_model=InstitutionalUserResponse)
async def update_institutional_user(
    user_id: int = Path(..., description="User ID"),
    update_data: InstitutionalUserUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update institutional user"""
    return await institutional_users_controller.update_institutional_user(user_id, update_data, db)


@router.delete("/institutional/{user_id}")
async def delete_institutional_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Delete institutional user"""
    return await institutional_users_controller.delete_institutional_user(user_id, db)


@router.post("/institutional/{user_id}/academic-units")
async def assign_academic_units_to_institutional_user(
    user_id: int = Path(..., description="User ID"),
    academic_unit_ids: List[int] = ...,
    db: Session = Depends(get_db)
):
    """Assign academic units to institutional user"""
    return await institutional_users_controller.assign_academic_units_to_user(user_id, academic_unit_ids, db)


@router.post("/institutional/{user_id}/roles")
async def assign_roles_to_institutional_user(
    user_id: int = Path(..., description="User ID"),
    role_ids: List[int] = ...,
    db: Session = Depends(get_db)
):
    """Assign roles to institutional user"""
    return await institutional_users_controller.assign_roles_to_user(user_id, role_ids, db)


@router.get("/institutional/{user_id}/profile-completion", response_model=ProfileCompletion)
async def get_institutional_user_profile_completion(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get institutional user profile completion status"""
    return await institutional_users_controller.get_user_profile_completion(user_id, db)


@router.patch("/institutional/{user_id}/deactivate")
async def deactivate_institutional_user(
    user_id: int = Path(..., description="User ID"),
    reason: str = Query(..., description="Reason for deactivation"),
    db: Session = Depends(get_db)
):
    """Deactivate institutional user"""
    return await institutional_users_controller.deactivate_user(user_id, reason, db)


@router.patch("/institutional/{user_id}/activate")
async def activate_institutional_user(
    user_id: int = Path(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Activate institutional user"""
    return await institutional_users_controller.activate_user(user_id, db)