# backend/app/modules/organizations/controllers/area_controller.py
"""
Area Controller - Business logic for area endpoints
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.organizations.models import Area
from app.modules.organizations.schemas import (
    AreaCreate, AreaUpdate, AreaResponse, AreaListResponse, AreaSearchParams,
    AreaMemberAssign, AreaMemberRemove, AreaStatistics
)
from app.modules.organizations.repositories import AreaRepository
from app.modules.organizations.services import area_service


class AreaController:
    """Controller for area operations"""
    
    def __init__(self):
        self.repo = AreaRepository()
        self.service = area_service
    
    async def create_area(self, area_data: AreaCreate, db: Session) -> AreaResponse:
        """Create new area"""
        try:
            # Create area with validation
            area = self.service.create_area_with_validation(area_data, db)
            db.commit()
            
            # Refresh area with relationships
            area = self.repo.get_by_id(db, area.id, include_members=True)
            
            return self._build_area_response(area)
            
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
                detail=f"Error creating area: {str(e)}"
            )
    
    async def get_area(self, area_id: int, db: Session) -> AreaResponse:
        """Get area by ID with full details"""
        area = self.repo.get_by_id(db, area_id, include_members=True)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )
        
        return self._build_area_response(area)
    
    async def get_areas(self, params: AreaSearchParams, db: Session) -> AreaListResponse:
        """Get paginated list of areas with filters"""
        skip = (params.page - 1) * params.per_page
        
        areas, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            category=params.category,
            is_active=params.is_active,
            can_lead_projects=params.can_lead_projects,
            include_members=False  # For performance in listings
        )
        
        area_responses = [self._build_area_response(area) for area in areas]
        
        return AreaListResponse(
            areas=area_responses,
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=(total + params.per_page - 1) // params.per_page
        )
    
    async def update_area(self, area_id: int, update_data: AreaUpdate, db: Session) -> AreaResponse:
        """Update area"""
        try:
            # Update area with validation
            area = self.service.update_area_with_validation(area_id, update_data, db)
            db.commit()
            
            # Refresh area with relationships
            area = self.repo.get_by_id(db, area_id, include_members=True)
            
            return self._build_area_response(area)
            
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
                detail=f"Error updating area: {str(e)}"
            )
    
    async def delete_area(self, area_id: int, db: Session, hard_delete: bool = False) -> Dict[str, str]:
        """Delete area (soft or hard delete)"""
        area = self.repo.get_by_id(db, area_id)
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )
        
        try:
            if hard_delete:
                success = self.repo.hard_delete(db, area)
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot hard delete area with active members"
                    )
                message = "Area permanently deleted"
            else:
                self.repo.delete(db, area)
                message = "Area deactivated"
            
            db.commit()
            return {"message": message}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting area: {str(e)}"
            )
    
    async def assign_member_to_area(
        self, 
        area_id: int, 
        member_data: AreaMemberAssign, 
        db: Session
    ) -> Dict[str, str]:
        """Assign member to area"""
        try:
            assignment_dict = member_data.dict()
            assignments = self.service.assign_members_to_area(area_id, [assignment_dict], db)
            db.commit()
            
            return {"message": f"Member {member_data.user_id} assigned to area successfully"}
            
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
                detail=f"Error assigning member: {str(e)}"
            )
    
    async def remove_member_from_area(
        self, 
        area_id: int, 
        member_data: AreaMemberRemove, 
        db: Session
    ) -> Dict[str, str]:
        """Remove member from area"""
        try:
            success = self.service.remove_member_from_area(area_id, member_data.user_id, db)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member assignment not found"
                )
            
            db.commit()
            return {"message": f"Member {member_data.user_id} removed from area successfully"}
            
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
                detail=f"Error removing member: {str(e)}"
            )
    
    async def assign_multiple_members_to_area(
        self, 
        area_id: int, 
        members_data: List[AreaMemberAssign], 
        db: Session
    ) -> Dict[str, Any]:
        """Assign multiple members to area"""
        try:
            member_assignments = [member.dict() for member in members_data]
            assignments = self.service.assign_members_to_area(area_id, member_assignments, db)
            db.commit()
            
            return {
                "message": f"Successfully assigned {len(assignments)} members to area",
                "assigned_count": len(assignments)
            }
            
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
                detail=f"Error assigning members: {str(e)}"
            )
    
    async def get_area_workload_analysis(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Get area workload analysis"""
        analysis = self.service.get_area_workload_analysis(area_id, db)
        if "error" in analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=analysis["error"]
            )
        
        return analysis
    
    async def get_area_performance_metrics(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Get area performance metrics"""
        metrics = self.service.get_area_performance_metrics(area_id, db)
        if "error" in metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=metrics["error"]
            )
        
        return metrics
    
    async def get_area_optimization_suggestions(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Get optimization suggestions for area"""
        suggestions = self.service.suggest_area_optimizations(area_id, db)
        if "error" in suggestions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=suggestions["error"]
            )
        
        return suggestions
    
    async def get_areas_by_category(self, category: str, db: Session) -> List[AreaResponse]:
        """Get areas filtered by category"""
        areas = self.service.get_areas_by_category(category, db)
        return [self._build_area_response(area) for area in areas]
    
    async def get_area_statistics(self, db: Session) -> AreaStatistics:
        """Get area statistics"""
        stats = self.repo.get_statistics(db)
        return AreaStatistics(
            total_areas=stats["total_areas"],
            active_areas=stats["active_areas"],
            by_category=stats["by_category"],
            total_members=stats["total_members"],
            areas_with_projects=stats["areas_with_projects"],
            average_members_per_area=stats["average_members_per_area"]
        )
    
    async def bulk_update_areas(
        self, 
        area_ids: List[int], 
        update_data: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """Bulk update areas"""
        try:
            result = self.service.bulk_update_areas(area_ids, update_data, db)
            db.commit()
            return result
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error in bulk update: {str(e)}"
            )
    
    async def validate_area_creation(self, area_data: AreaCreate, db: Session) -> Dict[str, Any]:
        """Validate area creation without creating"""
        return self.service.validate_area_creation(area_data, db)
    
    def _build_area_response(self, area: Area) -> AreaResponse:
        """Build area response with calculated fields"""
        # Get members info if available
        members = []
        if hasattr(area, 'user_areas') and area.user_areas:
            for user_area in area.user_areas:
                if user_area.is_active and user_area.user:
                    members.append({
                        "id": user_area.user.id,
                        "uuid": user_area.user.uuid,
                        "username": user_area.user.username,
                        "full_name": f"{user_area.user.first_name} {user_area.user.last_name}",
                        "employee_id": user_area.user.employee_id,
                        "role_in_area": user_area.role_in_area,
                        "specialization": user_area.specialization,
                        "is_primary": user_area.is_primary,
                        "can_lead_projects": user_area.can_lead_projects,
                        "time_allocation_percentage": user_area.time_allocation_percentage
                    })
        
        return AreaResponse(
            id=area.id,
            name=area.name,
            short_name=area.short_name,
            description=area.description,
            category=area.category,
            specialization=area.specialization,
            color=area.color,
            icon=area.icon,
            is_active=area.is_active,
            sort_order=area.sort_order,
            can_lead_projects=area.can_lead_projects,
            requires_collaboration=area.requires_collaboration,
            max_concurrent_projects=area.max_concurrent_projects,
            estimated_capacity_hours=area.estimated_capacity_hours,
            total_members=area.total_members,
            active_projects=area.active_projects,
            completed_projects=area.completed_projects,
            contact_email=area.contact_email,
            contact_phone=area.contact_phone,
            location=area.location,
            created_at=area.created_at,
            updated_at=area.updated_at,
            members=members
        )


# Create controller instance
area_controller = AreaController()