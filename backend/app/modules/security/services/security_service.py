"""
Security service - Business logic for security operations
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.modules.security.models import Role, Permission, RolePermission
from app.modules.security.repositories.security_repository import (
    RoleRepository, PermissionRepository, RolePermissionRepository, SecurityAnalyticsRepository
)
from app.modules.security.schemas.security_schemas import (
    RoleCreate, RoleUpdate, RoleValidationResponse, PermissionValidationResponse
)


class SecurityService:
    """Service for security operations"""
    
    def __init__(self):
        self.role_repo = RoleRepository()
        self.permission_repo = PermissionRepository()
        self.role_permission_repo = RolePermissionRepository()
        self.analytics_repo = SecurityAnalyticsRepository()
    
    # ===================================
    # ROLE VALIDATION
    # ===================================
    
    def validate_role_creation(self, role_data: RoleCreate, db: Session) -> RoleValidationResponse:
        """Validate role creation data"""
        conflicts = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness
        if not self.analytics_repo.validate_role_name_unique(db, role_data.name):
            conflicts.append(f"Role name '{role_data.name}' already exists")
        
        # Check level conflicts
        existing_role_at_level = (
            db.query(Role)
            .filter(Role.level == role_data.level, Role.is_active == True)
            .first()
        )
        if existing_role_at_level:
            warnings.append(f"Another role '{existing_role_at_level.name}' exists at level {role_data.level}")
        
        # Validate permission assignments
        if role_data.permission_ids:
            invalid_permissions = []
            for permission_id in role_data.permission_ids:
                permission = self.permission_repo.get_by_id(db, permission_id)
                if not permission or not permission.is_active:
                    invalid_permissions.append(str(permission_id))
            
            if invalid_permissions:
                conflicts.append(f"Invalid permission IDs: {', '.join(invalid_permissions)}")
        
        # Check target user type logic
        if role_data.target_user_type and role_data.permission_ids:
            permission_suggestions = self._get_permission_suggestions_for_user_type(
                db, role_data.target_user_type, role_data.permission_ids
            )
            if permission_suggestions:
                suggestions.extend(permission_suggestions)
        
        # Level-based suggestions
        if role_data.level >= 800:
            suggestions.append("High-level roles should include administrative permissions")
        elif role_data.level <= 200:
            suggestions.append("Low-level roles should have limited permissions")
        
        is_valid = len(conflicts) == 0
        
        return RoleValidationResponse(
            is_valid=is_valid,
            conflicts=conflicts,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def validate_role_update(self, role: Role, update_data: RoleUpdate, db: Session) -> RoleValidationResponse:
        """Validate role update data"""
        conflicts = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness if name is being changed
        if update_data.name and update_data.name != role.name:
            if not self.analytics_repo.validate_role_name_unique(db, update_data.name, role.id):
                conflicts.append(f"Role name '{update_data.name}' already exists")
        
        # Check if system role is being modified inappropriately
        if role.is_system and update_data.role_type and update_data.role_type != "system":
            conflicts.append("Cannot change type of system role")
        
        # Level change impact
        if update_data.level and update_data.level != role.level:
            assignment_count = self.role_repo.get_assignment_count(db, role.id)
            if assignment_count > 0:
                warnings.append(f"Changing level will affect {assignment_count} user assignments")
        
        # Check if deactivating role with assignments
        if update_data.is_active is False and role.is_active:
            assignment_count = self.role_repo.get_assignment_count(db, role.id)
            if assignment_count > 0:
                warnings.append(f"Deactivating role will affect {assignment_count} active assignments")
        
        is_valid = len(conflicts) == 0
        
        return RoleValidationResponse(
            is_valid=is_valid,
            conflicts=conflicts,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def validate_permission_assignment(self, role_id: int, permission_ids: List[int], db: Session) -> PermissionValidationResponse:
        """Validate permission assignment to role"""
        role = self.role_repo.get_by_id(db, role_id)
        if not role:
            return PermissionValidationResponse(
                is_valid=False,
                missing_permissions=[],
                conflicting_permissions=["Role not found"],
                recommended_permissions=[]
            )
        
        missing_permissions = []
        conflicting_permissions = []
        recommended_permissions = []
        
        # Check if permissions exist and are active
        for permission_id in permission_ids:
            permission = self.permission_repo.get_by_id(db, permission_id)
            if not permission:
                missing_permissions.append(f"Permission ID {permission_id} not found")
            elif not permission.is_active:
                conflicting_permissions.append(f"Permission '{permission.name}' is inactive")
        
        # Get recommended permissions based on role type and existing permissions
        if role.target_user_type:
            recommended = self._get_permission_suggestions_for_user_type(
                db, role.target_user_type, permission_ids
            )
            recommended_permissions.extend(recommended)
        
        is_valid = len(missing_permissions) == 0 and len(conflicting_permissions) == 0
        
        return PermissionValidationResponse(
            is_valid=is_valid,
            missing_permissions=missing_permissions,
            conflicting_permissions=conflicting_permissions,
            recommended_permissions=recommended_permissions
        )
    
    # ===================================
    # PERMISSION SUGGESTIONS
    # ===================================
    
    def _get_permission_suggestions_for_user_type(self, db: Session, user_type: str, current_permission_ids: List[int]) -> List[str]:
        """Get permission suggestions based on user type"""
        suggestions = []
        
        # Define permission sets for different user types
        internal_user_permissions = {
            "dashboard.access": "Internal users should have dashboard access",
            "content.create": "Internal users typically create content",
            "projects.manage": "Internal users manage projects"
        }
        
        institutional_user_permissions = {
            "projects.request": "Institutional users can request projects",
            "content.view": "Institutional users can view content",
            "profile.edit": "Users should be able to edit their profiles"
        }
        
        # Get current permission names
        current_permissions = []
        for permission_id in current_permission_ids:
            permission = self.permission_repo.get_by_id(db, permission_id)
            if permission:
                current_permissions.append(permission.name)
        
        # Check suggestions based on user type
        target_permissions = {}
        if user_type == "internal_user":
            target_permissions = internal_user_permissions
        elif user_type == "institutional_user":
            target_permissions = institutional_user_permissions
        elif user_type == "both":
            target_permissions = {**internal_user_permissions, **institutional_user_permissions}
        
        # Find missing recommended permissions
        for perm_name, reason in target_permissions.items():
            if perm_name not in current_permissions:
                permission = self.permission_repo.get_by_name(db, perm_name)
                if permission and permission.is_active:
                    suggestions.append(f"Consider adding '{permission.display_name}': {reason}")
        
        return suggestions
    
    # ===================================
    # ROLE MANAGEMENT
    # ===================================
    
    def create_role_with_permissions(self, role_data: RoleCreate, db: Session) -> Role:
        """Create role and assign permissions in one transaction"""
        # Validate first
        validation = self.validate_role_creation(role_data, db)
        if not validation.is_valid:
            raise ValueError(f"Role validation failed: {', '.join(validation.conflicts)}")
        
        # Create role
        role_dict = role_data.dict(exclude={'permission_ids'})
        role = self.role_repo.create(db, role_dict)
        
        # Assign permissions if provided
        if role_data.permission_ids:
            self.role_permission_repo.assign_permissions(
                db, role.id, role_data.permission_ids,
                grant_type="direct",
                assigned_reason="Initial role creation"
            )
        
        return role
    
    def update_role_permissions(self, role_id: int, permission_ids: List[int], db: Session, replace: bool = True) -> List[RolePermission]:
        """Update role permissions"""
        # Validate permission assignment
        validation = self.validate_permission_assignment(role_id, permission_ids, db)
        if not validation.is_valid:
            raise ValueError(f"Permission validation failed: {', '.join(validation.conflicting_permissions)}")
        
        if replace:
            # Replace all permissions
            return self.role_permission_repo.replace_permissions(
                db, role_id, permission_ids,
                grant_type="direct",
                assigned_reason="Permission update"
            )
        else:
            # Add to existing permissions
            return self.role_permission_repo.assign_permissions(
                db, role_id, permission_ids,
                grant_type="direct",
                assigned_reason="Permission addition"
            )
    
    def clone_role(self, source_role_id: int, new_name: str, new_display_name: str, db: Session) -> Role:
        """Clone an existing role with its permissions"""
        source_role = self.role_repo.get_by_id(db, source_role_id, include_permissions=True)
        if not source_role:
            raise ValueError("Source role not found")
        
        # Check name uniqueness
        if not self.analytics_repo.validate_role_name_unique(db, new_name):
            raise ValueError(f"Role name '{new_name}' already exists")
        
        # Create new role based on source
        new_role_data = {
            "name": new_name,
            "display_name": new_display_name,
            "description": f"Cloned from {source_role.name}",
            "level": source_role.level,
            "role_type": "custom",  # Cloned roles are always custom
            "target_user_type": source_role.target_user_type,
            "color": source_role.color,
            "icon": source_role.icon,
            "sort_order": source_role.sort_order,
            "max_assignments": source_role.max_assignments
        }
        
        new_role = self.role_repo.create(db, new_role_data)
        
        # Copy permissions
        if hasattr(source_role, 'role_permissions') and source_role.role_permissions:
            permission_ids = [rp.permission_id for rp in source_role.role_permissions if rp.is_active]
            if permission_ids:
                self.role_permission_repo.assign_permissions(
                    db, new_role.id, permission_ids,
                    grant_type="direct",
                    assigned_reason=f"Cloned from role {source_role.name}"
                )
        
        return new_role
    
    # ===================================
    # PERMISSION MANAGEMENT
    # ===================================
    
    def get_permissions_by_category(self, db: Session) -> Dict[str, List[Permission]]:
        """Get all permissions grouped by category"""
        return self.permission_repo.get_grouped_by_category(db)
    
    def get_role_permissions_with_details(self, role_id: int, db: Session) -> List[RolePermission]:
        """Get role permissions with full details"""
        return self.role_permission_repo.get_role_permission_details(db, role_id)
    
    # ===================================
    # ANALYTICS AND REPORTING
    # ===================================
    
    def get_security_dashboard_data(self, db: Session) -> Dict[str, Any]:
        """Get comprehensive security dashboard data"""
        stats = self.analytics_repo.get_role_statistics(db)
        permission_usage = self.analytics_repo.get_permission_usage_stats(db)
        popular_roles = self.analytics_repo.get_most_used_roles(db, limit=5)
        
        return {
            "statistics": stats,
            "permission_usage": permission_usage[:10],  # Top 10 most used
            "popular_roles": popular_roles,
            "underused_permissions": [p for p in permission_usage if p['usage_percentage'] < 5][:5]
        }
    
    def analyze_role_complexity(self, role_id: int, db: Session) -> Dict[str, Any]:
        """Analyze role complexity and suggest optimizations"""
        role = self.role_repo.get_by_id(db, role_id, include_permissions=True)
        if not role:
            return {"error": "Role not found"}
        
        permissions = self.role_permission_repo.get_role_permissions(db, role_id)
        assignment_count = self.role_repo.get_assignment_count(db, role_id)
        
        # Analyze permission distribution by category
        category_distribution = {}
        for permission in permissions:
            category = permission.category
            if category not in category_distribution:
                category_distribution[category] = 0
            category_distribution[category] += 1
        
        # Calculate complexity score
        complexity_score = len(permissions) * 2 + len(category_distribution) * 3
        if assignment_count > 10:
            complexity_score += 5  # High assignment count increases complexity
        
        # Generate recommendations
        recommendations = []
        if len(permissions) > 20:
            recommendations.append("Consider splitting this role into multiple smaller roles")
        if len(category_distribution) > 5:
            recommendations.append("Role spans too many categories, consider specialization")
        if assignment_count > 50:
            recommendations.append("High assignment count, ensure permissions are necessary")
        
        return {
            "role_name": role.name,
            "permission_count": len(permissions),
            "category_count": len(category_distribution),
            "category_distribution": category_distribution,
            "assignment_count": assignment_count,
            "complexity_score": complexity_score,
            "complexity_level": "High" if complexity_score > 50 else "Medium" if complexity_score > 25 else "Low",
            "recommendations": recommendations
        }
    
    # ===================================
    # BULK OPERATIONS
    # ===================================
    
    def bulk_update_role_status(self, role_ids: List[int], is_active: bool, db: Session) -> Dict[str, Any]:
        """Bulk update role status"""
        updated_count = 0
        errors = []
        
        for role_id in role_ids:
            try:
                role = self.role_repo.get_by_id(db, role_id)
                if not role:
                    errors.append(f"Role ID {role_id} not found")
                    continue
                
                if role.is_system and not is_active:
                    errors.append(f"Cannot deactivate system role '{role.name}'")
                    continue
                
                role.is_active = is_active
                updated_count += 1
                
            except Exception as e:
                errors.append(f"Error updating role ID {role_id}: {str(e)}")
        
        return {
            "updated_count": updated_count,
            "total_requested": len(role_ids),
            "errors": errors
        }


# Create service instance
security_service = SecurityService()