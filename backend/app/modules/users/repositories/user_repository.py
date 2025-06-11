"""
User repositories - Data access layer for user operations
"""
from .user_repository import *

__all__ = [
    "InternalUserRepository",
    "InstitutionalUserRepository", 
    "UserRoleRepository",
    "UserSearchRepository"
]
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from sqlalchemy import or_, and_, func, desc, exists

from app.modules.users.models import (
    InternalUser, InstitutionalUser, UserArea, UserAcademicUnit, UserRole
)
from app.modules.organizations.models import Area, AcademicUnit
from app.modules.security.models import Role


class InternalUserRepository:
    """Repository for internal user operations"""
    
    @staticmethod
    def create(db: Session, user_data: Dict[str, Any]) -> InternalUser:
        """Create new internal user"""
        user = InternalUser(**user_data)
        db.add(user)
        db.flush()  # Get ID without committing
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[InternalUser]:
        """Get internal user by ID with optimized loading"""
        return (
            db.query(InternalUser)
            .options(
                selectinload(InternalUser.user_areas.and_(UserArea.is_active == True))
                .selectinload(UserArea.area)
                .load_only(Area.id, Area.name, Area.short_name),
                selectinload(InternalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
            .filter(InternalUser.id == user_id)
            .first()
        )
    
    @staticmethod
    def get_by_uuid(db: Session, uuid: str) -> Optional[InternalUser]:
        """Get internal user by UUID with optimized loading"""
        return (
            db.query(InternalUser)
            .options(
                selectinload(InternalUser.user_areas.and_(UserArea.is_active == True))
                .selectinload(UserArea.area)
                .load_only(Area.id, Area.name, Area.short_name),
                selectinload(InternalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
            .filter(InternalUser.uuid == uuid)
            .first()
        )
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[InternalUser]:
        """Get internal user by username"""
        return db.query(InternalUser).filter(InternalUser.username == username).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[InternalUser]:
        """Get internal user by email"""
        return db.query(InternalUser).filter(InternalUser.email == email).first()
    
    @staticmethod
    def get_by_employee_id(db: Session, employee_id: str) -> Optional[InternalUser]:
        """Get internal user by employee ID"""
        return db.query(InternalUser).filter(InternalUser.employee_id == employee_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        area_id: Optional[int] = None,
        can_access_dashboard: Optional[bool] = None,
        minimal: bool = False
    ) -> Tuple[List[InternalUser], int]:
        """Get paginated list of internal users with filters"""
        
        if minimal:
            # For listings, only load essential fields
            query = db.query(InternalUser).options(
                load_only(
                    InternalUser.id,
                    InternalUser.uuid, 
                    InternalUser.username,
                    InternalUser.email,
                    InternalUser.first_name,
                    InternalUser.last_name,
                    InternalUser.employee_id,
                    InternalUser.is_active,
                    InternalUser.created_at,
                    InternalUser.profile_photo
                )
            )
        else:
            # For details, use selective loading
            query = db.query(InternalUser).options(
                selectinload(InternalUser.user_areas.and_(UserArea.is_active == True))
                .selectinload(UserArea.area)
                .load_only(Area.id, Area.name, Area.short_name),
                selectinload(InternalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
        
        # Apply filters
        if search:
            search_filter = or_(
                InternalUser.first_name.ilike(f"%{search}%"),
                InternalUser.last_name.ilike(f"%{search}%"),
                InternalUser.username.ilike(f"%{search}%"),
                InternalUser.email.ilike(f"%{search}%"),
                InternalUser.employee_id.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if is_active is not None:
            query = query.filter(InternalUser.is_active == is_active)
        
        if can_access_dashboard is not None:
            query = query.filter(InternalUser.can_access_dashboard == can_access_dashboard)
        
        if area_id:
            # Use EXISTS subquery for better performance
            area_exists = db.query(UserArea.user_id).filter(
                UserArea.area_id == area_id,
                UserArea.is_active == True,
                UserArea.user_id == InternalUser.id
            ).exists()
            query = query.filter(area_exists)
        
        # Get total count efficiently
        total = query.count()
        
        # Apply pagination and ordering
        users = query.order_by(desc(InternalUser.created_at)).offset(skip).limit(limit).all()
        
        return users, total
    
    @staticmethod
    def update(db: Session, user: InternalUser, update_data: Dict[str, Any]) -> InternalUser:
        """Update internal user"""
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        db.flush()
        return user
    
    @staticmethod
    def delete(db: Session, user: InternalUser) -> bool:
        """Delete internal user"""
        db.delete(user)
        db.flush()
        return True
    
    @staticmethod
    def assign_areas(db: Session, user_id: int, area_ids: List[int]) -> List[UserArea]:
        """Assign areas to internal user"""
        # Remove existing assignments
        db.query(UserArea).filter(UserArea.user_id == user_id).delete()
        
        # Add new assignments
        assignments = []
        for area_id in area_ids:
            assignment = UserArea(user_id=user_id, area_id=area_id)
            db.add(assignment)
            assignments.append(assignment)
        
        db.flush()
        return assignments
    
    @staticmethod
    def get_areas(db: Session, user_id: int) -> List[Area]:
        """Get areas assigned to internal user"""
        return (
            db.query(Area)
            .join(UserArea)
            .filter(UserArea.user_id == user_id, UserArea.is_active == True)
            .all()
        )


class InstitutionalUserRepository:
    """Repository for institutional user operations"""
    
    @staticmethod
    def create(db: Session, user_data: Dict[str, Any]) -> InstitutionalUser:
        """Create new institutional user"""
        user = InstitutionalUser(**user_data)
        db.add(user)
        db.flush()
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[InstitutionalUser]:
        """Get institutional user by ID with optimized loading"""
        return (
            db.query(InstitutionalUser)
            .options(
                selectinload(InstitutionalUser.user_academic_units.and_(UserAcademicUnit.is_active == True))
                .selectinload(UserAcademicUnit.academic_unit)
                .load_only(AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation),
                selectinload(InstitutionalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
            .filter(InstitutionalUser.id == user_id)
            .first()
        )
    
    @staticmethod
    def get_by_uuid(db: Session, uuid: str) -> Optional[InstitutionalUser]:
        """Get institutional user by UUID with optimized loading"""
        return (
            db.query(InstitutionalUser)
            .options(
                selectinload(InstitutionalUser.user_academic_units.and_(UserAcademicUnit.is_active == True))
                .selectinload(UserAcademicUnit.academic_unit)
                .load_only(AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation),
                selectinload(InstitutionalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
            .filter(InstitutionalUser.uuid == uuid)
            .first()
        )
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[InstitutionalUser]:
        """Get institutional user by username"""
        return db.query(InstitutionalUser).filter(InstitutionalUser.username == username).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[InstitutionalUser]:
        """Get institutional user by email"""
        return db.query(InstitutionalUser).filter(InstitutionalUser.email == email).first()
    
    @staticmethod
    def get_by_faculty_id(db: Session, faculty_id: str) -> Optional[InstitutionalUser]:
        """Get institutional user by faculty ID"""
        return db.query(InstitutionalUser).filter(InstitutionalUser.faculty_id == faculty_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        academic_unit_id: Optional[int] = None,
        user_type_filter: Optional[str] = None,
        minimal: bool = False
    ) -> Tuple[List[InstitutionalUser], int]:
        """Get paginated list of institutional users with filters"""
        
        if minimal:
            # For listings, only load essential fields
            query = db.query(InstitutionalUser).options(
                load_only(
                    InstitutionalUser.id,
                    InstitutionalUser.uuid,
                    InstitutionalUser.username,
                    InstitutionalUser.email,
                    InstitutionalUser.first_name,
                    InstitutionalUser.last_name,
                    InstitutionalUser.faculty_id,
                    InstitutionalUser.is_active,
                    InstitutionalUser.is_faculty,
                    InstitutionalUser.is_student,
                    InstitutionalUser.is_external_client,
                    InstitutionalUser.created_at,
                    InstitutionalUser.profile_photo
                )
            )
        else:
            # For details, use selective loading
            query = db.query(InstitutionalUser).options(
                selectinload(InstitutionalUser.user_academic_units.and_(UserAcademicUnit.is_active == True))
                .selectinload(UserAcademicUnit.academic_unit)
                .load_only(AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation),
                selectinload(InstitutionalUser.user_roles.and_(UserRole.is_active == True))
                .selectinload(UserRole.role)
                .load_only(Role.id, Role.name, Role.display_name)
            )
        
        # Apply filters
        if search:
            search_filter = or_(
                InstitutionalUser.first_name.ilike(f"%{search}%"),
                InstitutionalUser.last_name.ilike(f"%{search}%"),
                InstitutionalUser.username.ilike(f"%{search}%"),
                InstitutionalUser.email.ilike(f"%{search}%"),
                InstitutionalUser.faculty_id.ilike(f"%{search}%"),
                InstitutionalUser.institution.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if is_active is not None:
            query = query.filter(InstitutionalUser.is_active == is_active)
        
        if academic_unit_id:
            # Use EXISTS subquery for better performance
            unit_exists = db.query(UserAcademicUnit.user_id).filter(
                UserAcademicUnit.academic_unit_id == academic_unit_id,
                UserAcademicUnit.is_active == True,
                UserAcademicUnit.user_id == InstitutionalUser.id
            ).exists()
            query = query.filter(unit_exists)
        
        if user_type_filter:
            if user_type_filter == "faculty":
                query = query.filter(InstitutionalUser.is_faculty == True)
            elif user_type_filter == "student":
                query = query.filter(InstitutionalUser.is_student == True)
            elif user_type_filter == "external":
                query = query.filter(InstitutionalUser.is_external_client == True)
        
        # Get total count efficiently
        total = query.count()
        
        # Apply pagination and ordering
        users = query.order_by(desc(InstitutionalUser.created_at)).offset(skip).limit(limit).all()
        
        return users, total
    
    @staticmethod
    def update(db: Session, user: InstitutionalUser, update_data: Dict[str, Any]) -> InstitutionalUser:
        """Update institutional user"""
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        db.flush()
        return user
    
    @staticmethod
    def delete(db: Session, user: InstitutionalUser) -> bool:
        """Delete institutional user"""
        db.delete(user)
        db.flush()
        return True
    
    @staticmethod
    def assign_academic_units(db: Session, user_id: int, academic_unit_ids: List[int]) -> List[UserAcademicUnit]:
        """Assign academic units to institutional user"""
        # Remove existing assignments
        db.query(UserAcademicUnit).filter(UserAcademicUnit.user_id == user_id).delete()
        
        # Add new assignments
        assignments = []
        for unit_id in academic_unit_ids:
            assignment = UserAcademicUnit(user_id=user_id, academic_unit_id=unit_id)
            db.add(assignment)
            assignments.append(assignment)
        
        db.flush()
        return assignments
    
    @staticmethod
    def get_academic_units(db: Session, user_id: int) -> List[AcademicUnit]:
        """Get academic units assigned to institutional user"""
        return (
            db.query(AcademicUnit)
            .join(UserAcademicUnit)
            .filter(UserAcademicUnit.user_id == user_id, UserAcademicUnit.is_active == True)
            .all()
        )


class UserRoleRepository:
    """Repository for user role operations"""
    
    @staticmethod
    def assign_role(db: Session, user_id: int, role_id: int, user_type: str) -> UserRole:
        """Assign role to user"""
        # Check if assignment already exists
        existing = (
            db.query(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
                UserRole.user_type == user_type
            )
            .first()
        )
        
        if existing:
            existing.is_active = True
            db.flush()
            return existing
        
        # Create new assignment
        assignment = UserRole(
            user_id=user_id,
            role_id=role_id,
            user_type=user_type
        )
        db.add(assignment)
        db.flush()
        return assignment
    
    @staticmethod
    def remove_role(db: Session, user_id: int, role_id: int, user_type: str) -> bool:
        """Remove role from user"""
        assignment = (
            db.query(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
                UserRole.user_type == user_type
            )
            .first()
        )
        
        if assignment:
            assignment.is_active = False
            db.flush()
            return True
        
        return False
    
    @staticmethod
    def get_user_roles(db: Session, user_id: int, user_type: str) -> List[Role]:
        """Get roles assigned to user"""
        return (
            db.query(Role)
            .join(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.user_type == user_type,
                UserRole.is_active == True
            )
            .all()
        )
    
    @staticmethod
    def assign_multiple_roles(db: Session, user_id: int, role_ids: List[int], user_type: str) -> List[UserRole]:
        """Assign multiple roles to user"""
        # Remove existing role assignments
        db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.user_type == user_type
        ).update({"is_active": False})
        
        # Add new assignments
        assignments = []
        for role_id in role_ids:
            assignment = UserRoleRepository.assign_role(db, user_id, role_id, user_type)
            assignments.append(assignment)
        
        return assignments


class UserSearchRepository:
    """Repository for user search operations"""
    
    @staticmethod
    def search_all_users(
        db: Session,
        search: str,
        skip: int = 0,
        limit: int = 20,
        user_type: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Search across both internal and institutional users"""
        results = []
        total_count = 0
        
        if user_type is None or user_type == "internal":
            # Search internal users
            internal_query = db.query(InternalUser).options(
                joinedload(InternalUser.user_areas).joinedload(UserArea.area)
            )
            
            if search:
                search_filter = or_(
                    InternalUser.first_name.ilike(f"%{search}%"),
                    InternalUser.last_name.ilike(f"%{search}%"),
                    InternalUser.username.ilike(f"%{search}%"),
                    InternalUser.email.ilike(f"%{search}%"),
                    InternalUser.employee_id.ilike(f"%{search}%")
                )
                internal_query = internal_query.filter(search_filter)
            
            internal_users = internal_query.order_by(desc(InternalUser.created_at)).all()
            
            for user in internal_users:
                results.append({
                    "user": user,
                    "user_type": "internal",
                    "created_at": user.created_at
                })
        
        if user_type is None or user_type == "institutional":
            # Search institutional users
            institutional_query = db.query(InstitutionalUser).options(
                joinedload(InstitutionalUser.user_academic_units).joinedload(UserAcademicUnit.academic_unit)
            )
            
            if search:
                search_filter = or_(
                    InstitutionalUser.first_name.ilike(f"%{search}%"),
                    InstitutionalUser.last_name.ilike(f"%{search}%"),
                    InstitutionalUser.username.ilike(f"%{search}%"),
                    InstitutionalUser.email.ilike(f"%{search}%"),
                    InstitutionalUser.faculty_id.ilike(f"%{search}%")
                )
                institutional_query = institutional_query.filter(search_filter)
            
            institutional_users = institutional_query.order_by(desc(InstitutionalUser.created_at)).all()
            
            for user in institutional_users:
                results.append({
                    "user": user,
                    "user_type": "institutional",
                    "created_at": user.created_at
                })
        
        # Sort by creation date
        results.sort(key=lambda x: x["created_at"], reverse=True)
        
        total_count = len(results)
        
        # Apply pagination
        paginated_results = results[skip:skip + limit]
        
        return paginated_results, total_count
    
    @staticmethod
    def get_user_statistics(db: Session) -> Dict[str, Any]:
        """Get user statistics"""
        internal_total = db.query(InternalUser).count()
        internal_active = db.query(InternalUser).filter(InternalUser.is_active == True).count()
        
        institutional_total = db.query(InstitutionalUser).count()
        institutional_active = db.query(InstitutionalUser).filter(InstitutionalUser.is_active == True).count()
        
        faculty_count = db.query(InstitutionalUser).filter(InstitutionalUser.is_faculty == True).count()
        student_count = db.query(InstitutionalUser).filter(InstitutionalUser.is_student == True).count()
        external_count = db.query(InstitutionalUser).filter(InstitutionalUser.is_external_client == True).count()
        
        return {
            "internal_users": {
                "total": internal_total,
                "active": internal_active,
                "inactive": internal_total - internal_active
            },
            "institutional_users": {
                "total": institutional_total,
                "active": institutional_active,
                "inactive": institutional_total - institutional_active,
                "faculty": faculty_count,
                "students": student_count,
                "external_clients": external_count
            },
            "grand_total": internal_total + institutional_total
        }