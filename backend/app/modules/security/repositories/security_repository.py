"""
Security repositories - Data access layer for security operations
"""
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from sqlalchemy import or_, and_, func, desc, exists, distinct

from app.modules.security.models import Permission, Role, RolePermission
from app.modules.users.models import UserRole


class PermissionRepository:
    """Repository for permission operations"""
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[Permission], int]:
        """Get paginated list of permissions with filters"""
        
        query = db.query(Permission)
        
        # Apply filters
        if search:
            search_filter = or_(
                Permission.name.ilike(f"%{search}%"),
                Permission.display_name.ilike(f"%{search}%"),
                Permission.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(Permission.category == category)
        
        if is_active is not None:
            query = query.filter(Permission.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply ordering and pagination
        permissions = (
            query
            .order_by(Permission.category, Permission.sort_order, Permission.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return permissions, total
    
    @staticmethod
    def get_by_id(db: Session, permission_id: int) -> Optional[Permission]:
        """Get permission by ID"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Permission]:
        """Get permission by name"""
        return db.query(Permission).filter(Permission.name == name).first()
    
    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Permission]:
        """Get permissions by category"""
        return (
            db.query(Permission)
            .filter(Permission.category == category, Permission.is_active == True)
            .order_by(Permission.sort_order, Permission.name)
            .all()
        )
    
    @staticmethod
    def get_grouped_by_category(db: Session) -> Dict[str, List[Permission]]:
        """Get all permissions grouped by category"""
        permissions = (
            db.query(Permission)
            .filter(Permission.is_active == True)
            .order_by(Permission.category, Permission.sort_order, Permission.name)
            .all()
        )
        
        grouped = {}
        for permission in permissions:
            if permission.category not in grouped:
                grouped[permission.category] = []
            grouped[permission.category].append(permission)
        
        return grouped


class RoleRepository:
    """Repository for role operations"""
    
    @staticmethod
    def create(db: Session, role_data: Dict[str, Any]) -> Role:
        """Create new role"""
        role = Role(**role_data)
        db.add(role)
        db.flush()
        return role
    
    @staticmethod
    def get_by_id(db: Session, role_id: int, include_permissions: bool = False) -> Optional[Role]:
        """Get role by ID with optional permissions"""
        query = db.query(Role)
        
        if include_permissions:
            query = query.options(
                selectinload(Role.role_permissions.and_(RolePermission.is_active == True))
                .selectinload(RolePermission.permission)
            )
        
        return query.filter(Role.id == role_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Role]:
        """Get role by name"""
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        role_type: Optional[str] = None,
        target_user_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        level_min: Optional[int] = None,
        level_max: Optional[int] = None,
        include_permissions: bool = False
    ) -> Tuple[List[Role], int]:
        """Get paginated list of roles with filters"""
        
        query = db.query(Role)
        
        if include_permissions:
            query = query.options(
                selectinload(Role.role_permissions.and_(RolePermission.is_active == True))
                .selectinload(RolePermission.permission)
            )
        
        # Apply filters
        if search:
            search_filter = or_(
                Role.name.ilike(f"%{search}%"),
                Role.display_name.ilike(f"%{search}%"),
                Role.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if role_type:
            query = query.filter(Role.role_type == role_type)
        
        if target_user_type:
            query = query.filter(
                or_(
                    Role.target_user_type == target_user_type,
                    Role.target_user_type == "both",
                    Role.target_user_type.is_(None)
                )
            )
        
        if is_active is not None:
            query = query.filter(Role.is_active == is_active)
        
        if level_min is not None:
            query = query.filter(Role.level >= level_min)
        
        if level_max is not None:
            query = query.filter(Role.level <= level_max)
        
        # Get total count
        total = query.count()
        
        # Apply ordering and pagination
        roles = (
            query
            .order_by(Role.level, Role.sort_order, Role.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return roles, total
    
    @staticmethod
    def update(db: Session, role: Role, update_data: Dict[str, Any]) -> Role:
        """Update role"""
        for field, value in update_data.items():
            if hasattr(role, field) and value is not None:
                setattr(role, field, value)
        
        db.flush()
        return role
    
    @staticmethod
    def delete(db: Session, role: Role) -> bool:
        """Delete role (soft delete by setting inactive)"""
        role.is_active = False
        db.flush()
        return True
    
    @staticmethod
    def hard_delete(db: Session, role: Role) -> bool:
        """Hard delete role (only for custom roles with no assignments)"""
        # Check if role has any assignments
        assignments_count = db.query(UserRole).filter(
            UserRole.role_id == role.id,
            UserRole.is_active == True
        ).count()
        
        if assignments_count > 0:
            return False
        
        # Delete role permissions first
        db.query(RolePermission).filter(RolePermission.role_id == role.id).delete()
        
        # Delete role
        db.delete(role)
        db.flush()
        return True
    
    @staticmethod
    def get_user_roles(db: Session, user_id: int, user_type: str) -> List[Role]:
        """Get roles assigned to user"""
        return (
            db.query(Role)
            .join(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.user_type == user_type,
                UserRole.is_active == True,
                Role.is_active == True
            )
            .order_by(Role.level, Role.name)
            .all()
        )
    
    @staticmethod
    def get_assignment_count(db: Session, role_id: int) -> int:
        """Get number of active assignments for role"""
        return (
            db.query(UserRole)
            .filter(UserRole.role_id == role_id, UserRole.is_active == True)
            .count()
        )


class RolePermissionRepository:
    """Repository for role-permission operations"""
    
    @staticmethod
    def assign_permissions(db: Session, role_id: int, permission_ids: List[int], **kwargs) -> List[RolePermission]:
        """Assign permissions to role"""
        assignments = []
        
        for permission_id in permission_ids:
            # Check if assignment already exists
            existing = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role_id,
                    RolePermission.permission_id == permission_id
                )
                .first()
            )
            
            if existing:
                # Reactivate if inactive
                existing.is_active = True
                existing.grant_type = kwargs.get('grant_type', 'direct')
                existing.assigned_reason = kwargs.get('assigned_reason')
                assignments.append(existing)
            else:
                # Create new assignment
                assignment = RolePermission(
                    role_id=role_id,
                    permission_id=permission_id,
                    grant_type=kwargs.get('grant_type', 'direct'),
                    assigned_reason=kwargs.get('assigned_reason')
                )
                db.add(assignment)
                assignments.append(assignment)
        
        db.flush()
        return assignments
    
    @staticmethod
    def remove_permissions(db: Session, role_id: int, permission_ids: List[int]) -> bool:
        """Remove permissions from role"""
        db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id.in_(permission_ids)
        ).update({"is_active": False})
        
        db.flush()
        return True
    
    @staticmethod
    def replace_permissions(db: Session, role_id: int, permission_ids: List[int], **kwargs) -> List[RolePermission]:
        """Replace all permissions for role"""
        # Deactivate all current permissions
        db.query(RolePermission).filter(
            RolePermission.role_id == role_id
        ).update({"is_active": False})
        
        # Assign new permissions
        return RolePermissionRepository.assign_permissions(db, role_id, permission_ids, **kwargs)
    
    @staticmethod
    def get_role_permissions(db: Session, role_id: int) -> List[Permission]:
        """Get permissions assigned to role"""
        return (
            db.query(Permission)
            .join(RolePermission)
            .filter(
                RolePermission.role_id == role_id,
                RolePermission.is_active == True,
                Permission.is_active == True
            )
            .order_by(Permission.category, Permission.sort_order, Permission.name)
            .all()
        )
    
    @staticmethod
    def get_role_permission_details(db: Session, role_id: int) -> List[RolePermission]:
        """Get role permission relationships with details"""
        return (
            db.query(RolePermission)
            .options(selectinload(RolePermission.permission))
            .filter(
                RolePermission.role_id == role_id,
                RolePermission.is_active == True
            )
            .all()
        )


class SecurityAnalyticsRepository:
    """Repository for security analytics and statistics"""
    
    @staticmethod
    def get_role_statistics(db: Session) -> Dict[str, Any]:
        """Get comprehensive role statistics"""
        # Basic counts
        total_roles = db.query(Role).count()
        active_roles = db.query(Role).filter(Role.is_active == True).count()
        system_roles = db.query(Role).filter(Role.is_system == True).count()
        custom_roles = db.query(Role).filter(Role.role_type == "custom").count()
        
        # Permission counts
        total_permissions = db.query(Permission).count()
        active_permissions = db.query(Permission).filter(Permission.is_active == True).count()
        
        # Assignment counts
        total_assignments = db.query(UserRole).filter(UserRole.is_active == True).count()
        
        # By user type
        by_user_type = {}
        user_type_stats = (
            db.query(UserRole.user_type, func.count(UserRole.id))
            .filter(UserRole.is_active == True)
            .group_by(UserRole.user_type)
            .all()
        )
        for user_type, count in user_type_stats:
            by_user_type[user_type] = count
        
        # By role type
        by_role_type = {}
        role_type_stats = (
            db.query(Role.role_type, func.count(Role.id))
            .filter(Role.is_active == True)
            .group_by(Role.role_type)
            .all()
        )
        for role_type, count in role_type_stats:
            by_role_type[role_type] = count
        
        # By permission category
        by_permission_category = {}
        perm_category_stats = (
            db.query(Permission.category, func.count(Permission.id))
            .filter(Permission.is_active == True)
            .group_by(Permission.category)
            .all()
        )
        for category, count in perm_category_stats:
            by_permission_category[category] = count
        
        return {
            "total_roles": total_roles,
            "active_roles": active_roles,
            "system_roles": system_roles,
            "custom_roles": custom_roles,
            "total_permissions": total_permissions,
            "active_permissions": active_permissions,
            "total_assignments": total_assignments,
            "by_user_type": by_user_type,
            "by_role_type": by_role_type,
            "by_permission_category": by_permission_category
        }
    
    @staticmethod
    def get_permission_usage_stats(db: Session) -> List[Dict[str, Any]]:
        """Get permission usage statistics"""
        stats = (
            db.query(
                Permission.id,
                Permission.name,
                func.count(distinct(RolePermission.role_id)).label('roles_count'),
                func.count(distinct(UserRole.user_id)).label('users_count')
            )
            .outerjoin(
                RolePermission,
                and_(
                    RolePermission.permission_id == Permission.id,
                    RolePermission.is_active == True
                )
            )
            .outerjoin(
                UserRole,
                and_(
                    UserRole.role_id == RolePermission.role_id,
                    UserRole.is_active == True
                )
            )
            .filter(Permission.is_active == True)
            .group_by(Permission.id, Permission.name)
            .all()
        )
        
        total_users = db.query(func.count(distinct(UserRole.user_id))).filter(UserRole.is_active == True).scalar() or 1
        
        result = []
        for permission_id, permission_name, roles_count, users_count in stats:
            usage_percentage = (users_count / total_users) * 100 if users_count else 0
            result.append({
                "permission_id": permission_id,
                "permission_name": permission_name,
                "roles_count": roles_count or 0,
                "users_count": users_count or 0,
                "usage_percentage": round(usage_percentage, 2)
            })
        
        return sorted(result, key=lambda x: x['usage_percentage'], reverse=True)
    
    @staticmethod
    def get_most_used_roles(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most used roles by assignment count"""
        return (
            db.query(
                Role.id,
                Role.name,
                Role.display_name,
                func.count(UserRole.id).label('assignment_count')
            )
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(
                Role.is_active == True,
                UserRole.is_active == True
            )
            .group_by(Role.id, Role.name, Role.display_name)
            .order_by(desc('assignment_count'))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def validate_role_name_unique(db: Session, name: str, exclude_role_id: Optional[int] = None) -> bool:
        """Validate role name is unique"""
        query = db.query(Role).filter(Role.name == name)
        if exclude_role_id:
            query = query.filter(Role.id != exclude_role_id)
        return query.first() is None