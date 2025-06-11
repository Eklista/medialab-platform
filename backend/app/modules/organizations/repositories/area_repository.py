# backend/app/modules/organizations/repositories/area_repository.py
"""
Area repository - Data access layer for area operations
"""
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy import or_, and_, func, desc

from app.modules.organizations.models import Area
from app.modules.users.models import UserArea, InternalUser


class AreaRepository:
    """Repository for area operations"""
    
    @staticmethod
    def create(db: Session, area_data: Dict[str, Any]) -> Area:
        """Create new area"""
        area = Area(**area_data)
        db.add(area)
        db.flush()
        return area
    
    @staticmethod
    def get_by_id(db: Session, area_id: int, include_members: bool = False) -> Optional[Area]:
        """Get area by ID with optional members"""
        query = db.query(Area)
        
        if include_members:
            query = query.options(
                selectinload(Area.user_areas.and_(UserArea.is_active == True))
                .selectinload(UserArea.user)
                .load_only(
                    InternalUser.id, 
                    InternalUser.uuid,
                    InternalUser.first_name, 
                    InternalUser.last_name,
                    InternalUser.username,
                    InternalUser.employee_id,
                    InternalUser.position
                )
            )
        
        return query.filter(Area.id == area_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Area]:
        """Get area by name"""
        return db.query(Area).filter(Area.name == name).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        can_lead_projects: Optional[bool] = None,
        include_members: bool = False
    ) -> Tuple[List[Area], int]:
        """Get paginated list of areas with filters"""
        
        query = db.query(Area)
        
        if include_members:
            query = query.options(
                selectinload(Area.user_areas.and_(UserArea.is_active == True))
                .selectinload(UserArea.user)
                .load_only(
                    InternalUser.id,
                    InternalUser.uuid, 
                    InternalUser.first_name,
                    InternalUser.last_name,
                    InternalUser.username
                )
            )
        
        # Apply filters
        if search:
            search_filter = or_(
                Area.name.ilike(f"%{search}%"),
                Area.short_name.ilike(f"%{search}%"),
                Area.description.ilike(f"%{search}%"),
                Area.specialization.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(Area.category == category)
        
        if is_active is not None:
            query = query.filter(Area.is_active == is_active)
        
        if can_lead_projects is not None:
            query = query.filter(Area.can_lead_projects == can_lead_projects)
        
        # Get total count
        total = query.count()
        
        # Apply ordering and pagination
        areas = (
            query
            .order_by(Area.sort_order, Area.name)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return areas, total
    
    @staticmethod
    def update(db: Session, area: Area, update_data: Dict[str, Any]) -> Area:
        """Update area"""
        for field, value in update_data.items():
            if hasattr(area, field) and value is not None:
                setattr(area, field, value)
        
        db.flush()
        return area
    
    @staticmethod
    def delete(db: Session, area: Area) -> bool:
        """Delete area (soft delete by setting inactive)"""
        area.is_active = False
        db.flush()
        return True
    
    @staticmethod
    def hard_delete(db: Session, area: Area) -> bool:
        """Hard delete area (only if no active members)"""
        # Check if area has any active members
        members_count = db.query(UserArea).filter(
            UserArea.area_id == area.id,
            UserArea.is_active == True
        ).count()
        
        if members_count > 0:
            return False
        
        # Delete user area relationships first
        db.query(UserArea).filter(UserArea.area_id == area.id).delete()
        
        # Delete area
        db.delete(area)
        db.flush()
        return True
    
    @staticmethod
    def assign_member(db: Session, area_id: int, user_id: int, **kwargs) -> UserArea:
        """Assign member to area"""
        # Check if assignment already exists
        existing = (
            db.query(UserArea)
            .filter(UserArea.area_id == area_id, UserArea.user_id == user_id)
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
        assignment = UserArea(
            area_id=area_id,
            user_id=user_id,
            **kwargs
        )
        db.add(assignment)
        db.flush()
        return assignment
    
    @staticmethod
    def remove_member(db: Session, area_id: int, user_id: int) -> bool:
        """Remove member from area"""
        assignment = (
            db.query(UserArea)
            .filter(UserArea.area_id == area_id, UserArea.user_id == user_id)
            .first()
        )
        
        if assignment:
            assignment.is_active = False
            db.flush()
            return True
        
        return False
    
    @staticmethod
    def get_members(db: Session, area_id: int) -> List[InternalUser]:
        """Get members assigned to area"""
        return (
            db.query(InternalUser)
            .join(UserArea)
            .filter(
                UserArea.area_id == area_id,
                UserArea.is_active == True
            )
            .order_by(InternalUser.first_name, InternalUser.last_name)
            .all()
        )
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Get area statistics"""
        # Basic counts
        total_areas = db.query(Area).count()
        active_areas = db.query(Area).filter(Area.is_active == True).count()
        
        # By category
        by_category = {}
        category_stats = (
            db.query(Area.category, func.count(Area.id))
            .filter(Area.is_active == True)
            .group_by(Area.category)
            .all()
        )
        for category, count in category_stats:
            by_category[category] = count
        
        # Member counts
        total_members = (
            db.query(func.count(func.distinct(UserArea.user_id)))
            .filter(UserArea.is_active == True)
            .scalar() or 0
        )
        
        # Areas with active projects (this would need project integration)
        areas_with_projects = 0  # Placeholder
        
        # Average members per area
        if active_areas > 0:
            average_members_per_area = total_members / active_areas
        else:
            average_members_per_area = 0
        
        return {
            "total_areas": total_areas,
            "active_areas": active_areas,
            "by_category": by_category,
            "total_members": total_members,
            "areas_with_projects": areas_with_projects,
            "average_members_per_area": round(average_members_per_area, 2)
        }
    
    @staticmethod
    def validate_name_unique(db: Session, name: str, exclude_area_id: Optional[int] = None) -> bool:
        """Validate area name is unique"""
        query = db.query(Area).filter(Area.name == name)
        if exclude_area_id:
            query = query.filter(Area.id != exclude_area_id)
        return query.first() is None
    
    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Area]:
        """Get areas by category"""
        return (
            db.query(Area)
            .filter(Area.category == category, Area.is_active == True)
            .order_by(Area.sort_order, Area.name)
            .all()
        )
    
    @staticmethod
    def update_member_statistics(db: Session, area_id: int) -> None:
        """Update member statistics for area"""
        area = db.query(Area).filter(Area.id == area_id).first()
        if area:
            # Count active members
            member_count = (
                db.query(UserArea)
                .filter(UserArea.area_id == area_id, UserArea.is_active == True)
                .count()
            )
            area.total_members = member_count
            db.flush()