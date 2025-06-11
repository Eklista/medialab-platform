# backend/app/modules/organizations/repositories/academic_unit_repository.py
"""
Academic Unit repository - Data access layer for academic unit operations
"""
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, selectinload, load_only, joinedload
from sqlalchemy import or_, and_, func, desc

from app.modules.organizations.models import AcademicUnit, AcademicUnitType
from app.modules.users.models import UserAcademicUnit, InstitutionalUser


class AcademicUnitTypeRepository:
    """Repository for academic unit type operations"""
    
    @staticmethod
    def create(db: Session, type_data: Dict[str, Any]) -> AcademicUnitType:
        """Create new academic unit type"""
        unit_type = AcademicUnitType(**type_data)
        db.add(unit_type)
        db.flush()
        return unit_type
    
    @staticmethod
    def get_by_id(db: Session, type_id: int) -> Optional[AcademicUnitType]:
        """Get academic unit type by ID"""
        return db.query(AcademicUnitType).filter(AcademicUnitType.id == type_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[AcademicUnitType]:
        """Get academic unit type by name"""
        return db.query(AcademicUnitType).filter(AcademicUnitType.name == name).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        hierarchy_level: Optional[int] = None
    ) -> Tuple[List[AcademicUnitType], int]:
        """Get paginated list of academic unit types with filters"""
        
        query = db.query(AcademicUnitType)
        
        # Apply filters
        if search:
            search_filter = or_(
                AcademicUnitType.name.ilike(f"%{search}%"),
                AcademicUnitType.display_name.ilike(f"%{search}%"),
                AcademicUnitType.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(AcademicUnitType.category == category)
        
        if is_active is not None:
            query = query.filter(AcademicUnitType.is_active == is_active)
        
        if hierarchy_level:
            query = query.filter(AcademicUnitType.hierarchy_level == hierarchy_level)
        
        # Get total count
        total = query.count()
        
        # Apply ordering and pagination
        types = (
            query
            .order_by(AcademicUnitType.hierarchy_level, AcademicUnitType.sort_order, AcademicUnitType.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return types, total
    
    @staticmethod
    def update(db: Session, unit_type: AcademicUnitType, update_data: Dict[str, Any]) -> AcademicUnitType:
        """Update academic unit type"""
        for field, value in update_data.items():
            if hasattr(unit_type, field) and value is not None:
                setattr(unit_type, field, value)
        
        db.flush()
        return unit_type
    
    @staticmethod
    def delete(db: Session, unit_type: AcademicUnitType) -> bool:
        """Delete academic unit type (soft delete)"""
        unit_type.is_active = False
        db.flush()
        return True
    
    @staticmethod
    def hard_delete(db: Session, unit_type: AcademicUnitType) -> bool:
        """Hard delete academic unit type (only if no academic units)"""
        # Check if type has any academic units
        units_count = db.query(AcademicUnit).filter(
            AcademicUnit.academic_unit_type_id == unit_type.id
        ).count()
        
        if units_count > 0:
            return False
        
        # Delete type
        db.delete(unit_type)
        db.flush()
        return True
    
    @staticmethod
    def validate_name_unique(db: Session, name: str, exclude_type_id: Optional[int] = None) -> bool:
        """Validate academic unit type name is unique"""
        query = db.query(AcademicUnitType).filter(AcademicUnitType.name == name)
        if exclude_type_id:
            query = query.filter(AcademicUnitType.id != exclude_type_id)
        return query.first() is None
    
    @staticmethod
    def get_academic_units_count(db: Session, type_id: int) -> int:
        """Get count of academic units for this type"""
        return (
            db.query(AcademicUnit)
            .filter(AcademicUnit.academic_unit_type_id == type_id)
            .count()
        )


class AcademicUnitRepository:
    """Repository for academic unit operations"""
    
    @staticmethod
    def create(db: Session, unit_data: Dict[str, Any]) -> AcademicUnit:
        """Create new academic unit"""
        unit = AcademicUnit(**unit_data)
        db.add(unit)
        db.flush()
        return unit
    
    @staticmethod
    def get_by_id(db: Session, unit_id: int, include_members: bool = False) -> Optional[AcademicUnit]:
        """Get academic unit by ID with optional members"""
        query = db.query(AcademicUnit).options(
            joinedload(AcademicUnit.academic_unit_type)
        )
        
        if include_members:
            query = query.options(
                selectinload(AcademicUnit.user_academic_units.and_(UserAcademicUnit.is_active == True))
                .selectinload(UserAcademicUnit.user)
                .load_only(
                    InstitutionalUser.id,
                    InstitutionalUser.uuid,
                    InstitutionalUser.first_name,
                    InstitutionalUser.last_name,
                    InstitutionalUser.username,
                    InstitutionalUser.faculty_id,
                    InstitutionalUser.is_faculty,
                    InstitutionalUser.is_student,
                    InstitutionalUser.is_external_client
                )
            )
        
        return query.filter(AcademicUnit.id == unit_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[AcademicUnit]:
        """Get academic unit by name"""
        return db.query(AcademicUnit).filter(AcademicUnit.name == name).first()
    
    @staticmethod
    def get_by_abbreviation(db: Session, abbreviation: str) -> Optional[AcademicUnit]:
        """Get academic unit by abbreviation"""
        return db.query(AcademicUnit).filter(AcademicUnit.abbreviation == abbreviation).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        academic_unit_type_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        allows_public_content: Optional[bool] = None,
        include_members: bool = False
    ) -> Tuple[List[AcademicUnit], int]:
        """Get paginated list of academic units with filters"""
        
        query = db.query(AcademicUnit).options(
            joinedload(AcademicUnit.academic_unit_type)
        )
        
        if include_members:
            query = query.options(
                selectinload(AcademicUnit.user_academic_units.and_(UserAcademicUnit.is_active == True))
                .selectinload(UserAcademicUnit.user)
                .load_only(
                    InstitutionalUser.id,
                    InstitutionalUser.uuid,
                    InstitutionalUser.first_name,
                    InstitutionalUser.last_name,
                    InstitutionalUser.username
                )
            )
        
        # Apply filters
        if search:
            search_filter = or_(
                AcademicUnit.name.ilike(f"%{search}%"),
                AcademicUnit.short_name.ilike(f"%{search}%"),
                AcademicUnit.abbreviation.ilike(f"%{search}%"),
                AcademicUnit.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if academic_unit_type_id:
            query = query.filter(AcademicUnit.academic_unit_type_id == academic_unit_type_id)
        
        if is_active is not None:
            query = query.filter(AcademicUnit.is_active == is_active)
        
        if allows_public_content is not None:
            query = query.filter(AcademicUnit.allows_public_content == allows_public_content)
        
        # Get total count
        total = query.count()
        
        # Apply ordering and pagination
        units = (
            query
            .order_by(AcademicUnit.sort_order, AcademicUnit.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return units, total
    
    @staticmethod
    def update(db: Session, unit: AcademicUnit, update_data: Dict[str, Any]) -> AcademicUnit:
        """Update academic unit"""
        for field, value in update_data.items():
            if hasattr(unit, field) and value is not None:
                setattr(unit, field, value)
        
        db.flush()
        return unit
    
    @staticmethod
    def delete(db: Session, unit: AcademicUnit) -> bool:
        """Delete academic unit (soft delete)"""
        unit.is_active = False
        db.flush()
        return True
    
    @staticmethod
    def hard_delete(db: Session, unit: AcademicUnit) -> bool:
        """Hard delete academic unit (only if no active members)"""
        # Check if unit has any active members
        members_count = db.query(UserAcademicUnit).filter(
            UserAcademicUnit.academic_unit_id == unit.id,
            UserAcademicUnit.is_active == True
        ).count()
        
        if members_count > 0:
            return False
        
        # Delete user academic unit relationships first
        db.query(UserAcademicUnit).filter(UserAcademicUnit.academic_unit_id == unit.id).delete()
        
        # Delete unit
        db.delete(unit)
        db.flush()
        return True
    
    @staticmethod
    def assign_member(db: Session, unit_id: int, user_id: int, **kwargs) -> UserAcademicUnit:
        """Assign member to academic unit"""
        # Check if assignment already exists
        existing = (
            db.query(UserAcademicUnit)
            .filter(UserAcademicUnit.academic_unit_id == unit_id, UserAcademicUnit.user_id == user_id)
            .first()
        )
        
        if existing:
            # Reactivate and update if inactive
            existing.is_active = True
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            db.flush()
            return existing
        
        # Create new assignment
        assignment = UserAcademicUnit(
            academic_unit_id=unit_id,
            user_id=user_id,
            **kwargs
        )
        db.add(assignment)
        db.flush()
        return assignment
    
    @staticmethod
    def remove_member(db: Session, unit_id: int, user_id: int) -> bool:
        """Remove member from academic unit"""
        assignment = (
            db.query(UserAcademicUnit)
            .filter(UserAcademicUnit.academic_unit_id == unit_id, UserAcademicUnit.user_id == user_id)
            .first()
        )
        
        if assignment:
            assignment.is_active = False
            db.flush()
            return True
        
        return False
    
    @staticmethod
    def get_members(db: Session, unit_id: int) -> List[InstitutionalUser]:
        """Get members assigned to academic unit"""
        return (
            db.query(InstitutionalUser)
            .join(UserAcademicUnit)
            .filter(
                UserAcademicUnit.academic_unit_id == unit_id,
                UserAcademicUnit.is_active == True
            )
            .order_by(InstitutionalUser.first_name, InstitutionalUser.last_name)
            .all()
        )
    
    @staticmethod
    def get_by_type(db: Session, type_id: int) -> List[AcademicUnit]:
        """Get academic units by type"""
        return (
            db.query(AcademicUnit)
            .filter(AcademicUnit.academic_unit_type_id == type_id, AcademicUnit.is_active == True)
            .order_by(AcademicUnit.sort_order, AcademicUnit.name)
            .all()
        )
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Get academic unit statistics"""
        # Basic counts
        total_units = db.query(AcademicUnit).count()
        active_units = db.query(AcademicUnit).filter(AcademicUnit.is_active == True).count()
        
        # By type
        by_type = {}
        type_stats = (
            db.query(AcademicUnitType.name, func.count(AcademicUnit.id))
            .join(AcademicUnit, AcademicUnit.academic_unit_type_id == AcademicUnitType.id)
            .filter(AcademicUnit.is_active == True)
            .group_by(AcademicUnitType.name)
            .all()
        )
        for type_name, count in type_stats:
            by_type[type_name] = count
        
        # Member counts
        total_students = (
            db.query(func.count(func.distinct(UserAcademicUnit.user_id)))
            .join(InstitutionalUser, InstitutionalUser.id == UserAcademicUnit.user_id)
            .filter(
                UserAcademicUnit.is_active == True,
                InstitutionalUser.is_student == True
            )
            .scalar() or 0
        )
        
        total_faculty = (
            db.query(func.count(func.distinct(UserAcademicUnit.user_id)))
            .join(InstitutionalUser, InstitutionalUser.id == UserAcademicUnit.user_id)
            .filter(
                UserAcademicUnit.is_active == True,
                InstitutionalUser.is_faculty == True
            )
            .scalar() or 0
        )
        
        # Units with projects (placeholder)
        units_with_projects = 0
        
        # Average members per unit
        total_members = total_students + total_faculty
        if active_units > 0:
            average_members_per_unit = total_members / active_units
        else:
            average_members_per_unit = 0
        
        return {
            "total_units": total_units,
            "active_units": active_units,
            "by_type": by_type,
            "total_students": total_students,
            "total_faculty": total_faculty,
            "units_with_projects": units_with_projects,
            "average_members_per_unit": round(average_members_per_unit, 2)
        }
    
    @staticmethod
    def validate_name_unique(db: Session, name: str, exclude_unit_id: Optional[int] = None) -> bool:
        """Validate academic unit name is unique"""
        query = db.query(AcademicUnit).filter(AcademicUnit.name == name)
        if exclude_unit_id:
            query = query.filter(AcademicUnit.id != exclude_unit_id)
        return query.first() is None
    
    @staticmethod
    def validate_abbreviation_unique(db: Session, abbreviation: str, exclude_unit_id: Optional[int] = None) -> bool:
        """Validate academic unit abbreviation is unique"""
        query = db.query(AcademicUnit).filter(AcademicUnit.abbreviation == abbreviation)
        if exclude_unit_id:
            query = query.filter(AcademicUnit.id != exclude_unit_id)
        return query.first() is None
    
    @staticmethod
    def update_member_statistics(db: Session, unit_id: int) -> None:
        """Update member statistics for academic unit"""
        unit = db.query(AcademicUnit).filter(AcademicUnit.id == unit_id).first()
        if unit:
            # Count faculty
            faculty_count = (
                db.query(UserAcademicUnit)
                .join(InstitutionalUser, InstitutionalUser.id == UserAcademicUnit.user_id)
                .filter(
                    UserAcademicUnit.academic_unit_id == unit_id,
                    UserAcademicUnit.is_active == True,
                    InstitutionalUser.is_faculty == True
                )
                .count()
            )
            
            # Count students
            student_count = (
                db.query(UserAcademicUnit)
                .join(InstitutionalUser, InstitutionalUser.id == UserAcademicUnit.user_id)
                .filter(
                    UserAcademicUnit.academic_unit_id == unit_id,
                    UserAcademicUnit.is_active == True,
                    InstitutionalUser.is_student == True
                )
                .count()
            )
            
            unit.total_faculty = faculty_count
            unit.total_students = student_count
            db.flush()