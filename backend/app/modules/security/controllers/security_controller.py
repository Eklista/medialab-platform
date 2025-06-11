"""
Security Controllers - Business logic for security endpoints
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.security.models import Role, Permission, RolePermission
from app.modules.security.schemas.security_schemas import (
    RoleCreate, RoleUpdate, RoleResponse, RoleListResponse, RoleSearchParams,
    PermissionResponse, PermissionListResponse,
    RolePermissionAssign, RolePermissionRemove, RolePermissionResponse,
    UserRoleAssign, UserRoleRemove, BulkRoleAssign,
    RoleStatistics, RoleValidationResponse, PermissionValidationResponse
)
from app.modules.security.repositories.security_repository import (
    RoleRepository, PermissionRepository, RolePermissionRepository, SecurityAnalyticsRepository
)
from app.modules.security.services.security_service import security_service


class RoleController:
    """Controller for role operations"""
    
    def __init__(self):
        self.repo = RoleRepository()
        self.permission_repo = PermissionRepository()
        self.role_permission_repo = RolePermissionRepository()
        self.service = security_service
    
    async def create_role(self, role_data: RoleCreate, db: Session) -> RoleResponse:
        """Create new role with permissions"""
        try:
            # Validate role creation
            validation = self.service.validate_role_creation(role_data, db)
            if not validation.is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Role validation failed",
                        "conflicts": validation.conflicts,
                        "warnings": validation.warnings
                    }
                )
            
            # Create role with permissions
            role = self.service.create_role_with_permissions(role_data, db)
            db.commit()
            
            # Refresh with relationships
            role = self.repo.get_by_id(db, role.id, include_permissions=True)
            
            return self._build_role_response(role, db)
            
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating role: {str(e)}"
            )
    
    async def get_role(self, role_id: int, db: Session) -> RoleResponse:
        """Get role by ID with full details"""
        role = self.repo.get_by_id(db, role_id, include_permissions=True)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        return self._build_role_response(role, db)
    
    async def get_roles(self, params: RoleSearchParams, db: Session) -> RoleListResponse:
        """Get paginated list of roles with filters"""
        skip = (params.page - 1) * params.per_page
        
        roles, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            role_type=params.role_type,
            target_user_type=params.target_user_type,
            is_active=params.is_active,
            level_min=params.level_min,
            level_max=params.level_max,
            include_permissions=params.include_permissions
        )
        
        role_responses = [self._build_role_response(role, db) for role in roles]
        
        return RoleListResponse(
            roles=role_responses,
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=(total + params.per_page - 1) // params.per_page
        )
    
    async def update_role(self, role_id: int, update_data: RoleUpdate, db: Session) -> RoleResponse:
        """Update role"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Validate update
        validation = self.service.validate_role_update(role, update_data, db)
        if not validation.is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Role update validation failed",
                    "conflicts": validation.conflicts,
                    "warnings": validation.warnings
                }
            )
        
        try:
            # Update role
            update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
            updated_role = self.repo.update(db, role, update_dict)
            
            db.commit()
            
            # Refresh with relationships
            updated_role = self.repo.get_by_id(db, role_id, include_permissions=True)
            
            return self._build_role_response(updated_role, db)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating role: {str(e)}"
            )
    
    async def delete_role(self, role_id: int, db: Session, hard_delete: bool = False) -> Dict[str, str]:
        """Delete role (soft or hard delete)"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete system role"
            )
        
        try:
            if hard_delete:
                success = self.repo.hard_delete(db, role)
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot hard delete role with active assignments"
                    )
                message = "Role permanently deleted"
            else:
                self.repo.delete(db, role)
                message = "Role deactivated"
            
            db.commit()
            return {"message": message}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting role: {str(e)}"
            )
    
    async def assign_permissions_to_role(
        self, 
        role_id: int, 
        permission_data: RolePermissionAssign, 
        db: Session
    ) -> List[RolePermissionResponse]:
        """Assign permissions to role"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        try:
            # Validate and assign permissions
            assignments = self.service.update_role_permissions(
                role_id, permission_data.permission_ids, db, replace=False
            )
            
            db.commit()
            
            # Return assignments with details
            return [self._build_role_permission_response(assignment, db) for assignment in assignments]
            
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error assigning permissions: {str(e)}"
            )
    
    async def remove_permissions_from_role(
        self, 
        role_id: int, 
        permission_data: RolePermissionRemove, 
        db: Session
    ) -> Dict[str, str]:
        """Remove permissions from role"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        try:
            self.role_permission_repo.remove_permissions(db, role_id, permission_data.permission_ids)
            db.commit()
            
            return {"message": f"Removed {len(permission_data.permission_ids)} permissions from role"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error removing permissions: {str(e)}"
            )
    
    async def replace_role_permissions(
        self, 
        role_id: int, 
        permission_data: RolePermissionAssign, 
        db: Session
    ) -> List[RolePermissionResponse]:
        """Replace all role permissions"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        try:
            # Replace all permissions
            assignments = self.service.update_role_permissions(
                role_id, permission_data.permission_ids, db, replace=True
            )
            
            db.commit()
            
            return [self._build_role_permission_response(assignment, db) for assignment in assignments]
            
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error replacing permissions: {str(e)}"
            )
    
    async def get_role_permissions(self, role_id: int, db: Session) -> List[RolePermissionResponse]:
        """Get permissions assigned to role"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        assignments = self.role_permission_repo.get_role_permission_details(db, role_id)
        return [self._build_role_permission_response(assignment, db) for assignment in assignments]
    
    async def clone_role(self, role_id: int, new_name: str, new_display_name: str, db: Session) -> RoleResponse:
        """Clone existing role"""
        try:
            cloned_role = self.service.clone_role(role_id, new_name, new_display_name, db)
            db.commit()
            
            # Refresh with relationships
            cloned_role = self.repo.get_by_id(db, cloned_role.id, include_permissions=True)
            
            return self._build_role_response(cloned_role, db)
            
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error cloning role: {str(e)}"
            )
    
    async def validate_role(self, role_data: RoleCreate, db: Session) -> RoleValidationResponse:
        """Validate role data without creating"""
        return self.service.validate_role_creation(role_data, db)
    
    async def analyze_role_complexity(self, role_id: int, db: Session) -> Dict[str, Any]:
        """Analyze role complexity"""
        role = self.repo.get_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        return self.service.analyze_role_complexity(role_id, db)
    
    async def bulk_update_roles(self, role_ids: List[int], is_active: bool, db: Session) -> Dict[str, Any]:
        """Bulk update role status"""
        try:
            result = self.service.bulk_update_role_status(role_ids, is_active, db)
            db.commit()
            return result
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error in bulk update: {str(e)}"
            )
    
    def _build_role_response(self, role: Role, db: Session) -> RoleResponse:
        """Build role response with calculated fields"""
        # Get permission count
        permission_count = 0
        permissions = []
        
        if hasattr(role, 'role_permissions') and role.role_permissions:
            active_permissions = [rp for rp in role.role_permissions if rp.is_active]
            permission_count = len(active_permissions)
            
            for role_perm in active_permissions:
                if role_perm.permission:
                    permissions.append(PermissionResponse(
                        id=role_perm.permission.id,
                        name=role_perm.permission.name,
                        display_name=role_perm.permission.display_name,
                        description=role_perm.permission.description,
                        category=role_perm.permission.category,
                        resource=role_perm.permission.resource,
                        action=role_perm.permission.action,
                        sort_order=role_perm.permission.sort_order,
                        is_active=role_perm.permission.is_active,
                        is_system=role_perm.permission.is_system,
                        created_at=role_perm.permission.created_at,
                        updated_at=role_perm.permission.updated_at
                    ))
        
        # Get assignment count
        assignment_count = self.repo.get_assignment_count(db, role.id)
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            display_name=role.display_name,
            description=role.description,
            level=role.level,
            role_type=role.role_type,
            target_user_type=role.target_user_type,
            color=role.color,
            icon=role.icon,
            sort_order=role.sort_order,
            max_assignments=role.max_assignments,
            is_active=role.is_active,
            is_system=role.is_system,
            is_default=role.is_default,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permission_count=permission_count,
            assignment_count=assignment_count,
            permissions=permissions
        )
    
    def _build_role_permission_response(self, assignment: RolePermission, db: Session) -> RolePermissionResponse:
        """Build role permission response"""
        permission_response = PermissionResponse(
            id=assignment.permission.id,
            name=assignment.permission.name,
            display_name=assignment.permission.display_name,
            description=assignment.permission.description,
            category=assignment.permission.category,
            resource=assignment.permission.resource,
            action=assignment.permission.action,
            sort_order=assignment.permission.sort_order,
            is_active=assignment.permission.is_active,
            is_system=assignment.permission.is_system,
            created_at=assignment.permission.created_at,
            updated_at=assignment.permission.updated_at
        )
        
        return RolePermissionResponse(
            id=assignment.id,
            role_id=assignment.role_id,
            permission_id=assignment.permission_id,
            grant_type=assignment.grant_type,
            assigned_reason=assignment.assigned_reason,
            is_active=assignment.is_active,
            created_at=assignment.created_at,
            permission=permission_response
        )


class PermissionController:
    """Controller for permission operations"""
    
    def __init__(self):
        self.repo = PermissionRepository()
        self.service = security_service
    
    async def get_permissions(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        grouped: bool = False,
        db: Session = None
    ) -> PermissionListResponse:
        """Get paginated list of permissions"""
        if grouped:
            # Return permissions grouped by category
            grouped_permissions = self.service.get_permissions_by_category(db)
            
            all_permissions = []
            by_category = {}
            
            for category_name, permissions in grouped_permissions.items():
                category_responses = []
                for permission in permissions:
                    perm_response = PermissionResponse(
                        id=permission.id,
                        name=permission.name,
                        display_name=permission.display_name,
                        description=permission.description,
                        category=permission.category,
                        resource=permission.resource,
                        action=permission.action,
                        sort_order=permission.sort_order,
                        is_active=permission.is_active,
                        is_system=permission.is_system,
                        created_at=permission.created_at,
                        updated_at=permission.updated_at
                    )
                    category_responses.append(perm_response)
                    all_permissions.append(perm_response)
                
                by_category[category_name] = category_responses
            
            return PermissionListResponse(
                permissions=all_permissions,
                total=len(all_permissions),
                by_category=by_category
            )
        else:
            # Regular paginated list
            permissions, total = self.repo.get_all(
                db, skip, limit, search, category, is_active
            )
            
            permission_responses = [
                PermissionResponse(
                    id=permission.id,
                    name=permission.name,
                    display_name=permission.display_name,
                    description=permission.description,
                    category=permission.category,
                    resource=permission.resource,
                    action=permission.action,
                    sort_order=permission.sort_order,
                    is_active=permission.is_active,
                    is_system=permission.is_system,
                    created_at=permission.created_at,
                    updated_at=permission.updated_at
                ) for permission in permissions
            ]
            
            return PermissionListResponse(
                permissions=permission_responses,
                total=total,
                by_category={}
            )
    
    async def get_permission(self, permission_id: int, db: Session) -> PermissionResponse:
        """Get permission by ID"""
        permission = self.repo.get_by_id(db, permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        return PermissionResponse(
            id=permission.id,
            name=permission.name,
            display_name=permission.display_name,
            description=permission.description,
            category=permission.category,
            resource=permission.resource,
            action=permission.action,
            sort_order=permission.sort_order,
            is_active=permission.is_active,
            is_system=permission.is_system,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )


class SecurityAnalyticsController:
    """Controller for security analytics and reporting"""
    
    def __init__(self):
        self.analytics_repo = SecurityAnalyticsRepository()
        self.service = security_service
    
    async def get_security_statistics(self, db: Session) -> RoleStatistics:
        """Get comprehensive security statistics"""
        stats = self.analytics_repo.get_role_statistics(db)
        
        return RoleStatistics(
            total_roles=stats["total_roles"],
            active_roles=stats["active_roles"],
            system_roles=stats["system_roles"],
            custom_roles=stats["custom_roles"],
            total_permissions=stats["total_permissions"],
            active_permissions=stats["active_permissions"],
            total_assignments=stats["total_assignments"],
            by_user_type=stats["by_user_type"],
            by_role_type=stats["by_role_type"],
            by_permission_category=stats["by_permission_category"]
        )
    
    async def get_dashboard_data(self, db: Session) -> Dict[str, Any]:
        """Get security dashboard data"""
        return self.service.get_security_dashboard_data(db)
    
    async def get_permission_usage_stats(self, db: Session) -> List[Dict[str, Any]]:
        """Get permission usage statistics"""
        return self.analytics_repo.get_permission_usage_stats(db)
    
    async def get_most_used_roles(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most used roles"""
        return self.analytics_repo.get_most_used_roles(db, limit)
    
    async def validate_permission_assignment(
        self, 
        role_id: int, 
        permission_ids: List[int], 
        db: Session
    ) -> PermissionValidationResponse:
        """Validate permission assignment"""
        return self.service.validate_permission_assignment(role_id, permission_ids, db)


# Create controller instances
role_controller = RoleController()
permission_controller = PermissionController()
security_analytics_controller = SecurityAnalyticsController()