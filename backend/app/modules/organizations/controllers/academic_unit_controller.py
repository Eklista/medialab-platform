# backend/app/modules/organizations/controllers/academic_unit_controller.py
"""
Academic Unit Controller - Business logic for academic unit endpoints
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.organizations.models import AcademicUnit, AcademicUnitType
from app.modules.organizations.schemas import (
    # Academic Unit Type schemas
    AcademicUnitTypeCreate, AcademicUnitTypeUpdate, AcademicUnitTypeResponse,
    AcademicUnitTypeListResponse,
    # Academic Unit schemas
    AcademicUnitCreate, AcademicUnitUpdate, AcademicUnitResponse,
    AcademicUnitListResponse, AcademicUnitSearchParams,
    AcademicUnitMemberAssign, AcademicUnitMemberRemove, AcademicUnitStatistics
)
from app.modules.organizations.repositories import AcademicUnitRepository, AcademicUnitTypeRepository
from app.modules.organizations.services import academic_unit_service, academic_unit_type_service


class AcademicUnitTypeController:
    """Controller for academic unit type operations"""
    
    def __init__(self):
        self.repo = AcademicUnitTypeRepository()
        self.service = academic_unit_type_service
    
    async def create_academic_unit_type(self, type_data: AcademicUnitTypeCreate, db: Session) -> AcademicUnitTypeResponse:
        """Create new academic unit type"""
        try:
            # Create type with validation
            unit_type = self.service.create_academic_unit_type_with_validation(type_data, db)
            db.commit()
            
            return self._build_type_response(unit_type, db)
            
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
                detail=f"Error creating academic unit type: {str(e)}"
            )
    
    async def get_academic_unit_type(self, type_id: int, db: Session) -> AcademicUnitTypeResponse:
        """Get academic unit type by ID"""
        unit_type = self.repo.get_by_id(db, type_id)
        if not unit_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic unit type not found"
            )
        
        return self._build_type_response(unit_type, db)
    
    async def get_academic_unit_types(
        self, 
        skip: int = 0, 
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        hierarchy_level: Optional[int] = None,
        db: Session = None
    ) -> AcademicUnitTypeListResponse:
        """Get paginated list of academic unit types"""
        types, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            category=category,
            is_active=is_active,
            hierarchy_level=hierarchy_level
        )
        
        type_responses = [self._build_type_response(unit_type, db) for unit_type in types]
        
        return AcademicUnitTypeListResponse(
            academic_unit_types=type_responses,
            total=total,
            page=(skip // limit) + 1,
            per_page=limit,
            pages=(total + limit - 1) // limit
        )
    
    async def update_academic_unit_type(
        self, 
        type_id: int, 
        update_data: AcademicUnitTypeUpdate, 
        db: Session
    ) -> AcademicUnitTypeResponse:
        """Update academic unit type"""
        try:
            # Update type with validation
            unit_type = self.service.update_academic_unit_type_with_validation(type_id, update_data, db)
            db.commit()
            
            return self._build_type_response(unit_type, db)
            
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
                detail=f"Error updating academic unit type: {str(e)}"
            )
    
    async def delete_academic_unit_type(self, type_id: int, db: Session, hard_delete: bool = False) -> Dict[str, str]:
        """Delete academic unit type"""
        unit_type = self.repo.get_by_id(db, type_id)
        if not unit_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic unit type not found"
            )
        
        try:
            if hard_delete:
                success = self.repo.hard_delete(db, unit_type)
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot hard delete type with existing academic units"
                    )
                message = "Academic unit type permanently deleted"
            else:
                self.repo.delete(db, unit_type)
                message = "Academic unit type deactivated"
            
            db.commit()
            return {"message": message}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting academic unit type: {str(e)}"
            )
    
    def _build_type_response(self, unit_type: AcademicUnitType, db: Session) -> AcademicUnitTypeResponse:
        """Build academic unit type response"""
        # Get count of academic units for this type
        units_count = self.repo.get_academic_units_count(db, unit_type.id)
        
        return AcademicUnitTypeResponse(
            id=unit_type.id,
            name=unit_type.name,
            display_name=unit_type.display_name,
            description=unit_type.description,
            hierarchy_level=unit_type.hierarchy_level,
            abbreviation=unit_type.abbreviation,
            category=unit_type.category,
            is_active=unit_type.is_active,
            sort_order=unit_type.sort_order,
            allows_students=unit_type.allows_students,
            allows_faculty=unit_type.allows_faculty,
            requires_approval=unit_type.requires_approval,
            created_at=unit_type.created_at,
            updated_at=unit_type.updated_at,
            academic_units_count=units_count
        )


class AcademicUnitController:
    """Controller for academic unit operations"""
    
    def __init__(self):
        self.repo = AcademicUnitRepository()
        self.type_repo = AcademicUnitTypeRepository()
        self.service = academic_unit_service
    
    async def create_academic_unit(self, unit_data: AcademicUnitCreate, db: Session) -> AcademicUnitResponse:
        """Create new academic unit"""
        try:
            # Create unit with validation
            unit = self.service.create_academic_unit_with_validation(unit_data, db)
            db.commit()
            
            # Refresh unit with relationships
            unit = self.repo.get_by_id(db, unit.id, include_members=True)
            
            return self._build_unit_response(unit)
            
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
                detail=f"Error creating academic unit: {str(e)}"
            )
    
    async def get_academic_unit(self, unit_id: int, db: Session) -> AcademicUnitResponse:
        """Get academic unit by ID with full details"""
        unit = self.repo.get_by_id(db, unit_id, include_members=True)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic unit not found"
            )
        
        return self._build_unit_response(unit)
    
    async def get_academic_units(self, params: AcademicUnitSearchParams, db: Session) -> AcademicUnitListResponse:
        """Get paginated list of academic units with filters"""
        skip = (params.page - 1) * params.per_page
        
        units, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            academic_unit_type_id=params.academic_unit_type_id,
            is_active=params.is_active,
            allows_public_content=params.allows_public_content,
            include_members=False  # For performance in listings
        )
        
        unit_responses = [self._build_unit_response(unit) for unit in units]
        
        return AcademicUnitListResponse(
            academic_units=unit_responses,
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=(total + params.per_page - 1) // params.per_page
        )
    
    async def update_academic_unit(
        self, 
        unit_id: int, 
        update_data: AcademicUnitUpdate, 
        db: Session
    ) -> AcademicUnitResponse:
        """Update academic unit"""
        try:
            # Update unit with validation
            unit = self.service.update_academic_unit_with_validation(unit_id, update_data, db)
            db.commit()
            
            # Refresh unit with relationships
            unit = self.repo.get_by_id(db, unit_id, include_members=True)
            
            return self._build_unit_response(unit)
            
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
                detail=f"Error updating academic unit: {str(e)}"
            )
    
    async def delete_academic_unit(self, unit_id: int, db: Session, hard_delete: bool = False) -> Dict[str, str]:
        """Delete academic unit"""
        unit = self.repo.get_by_id(db, unit_id)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic unit not found"
            )
        
        try:
            if hard_delete:
                success = self.repo.hard_delete(db, unit)
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot hard delete unit with active members"
                    )
                message = "Academic unit permanently deleted"
            else:
                self.repo.delete(db, unit)
                message = "Academic unit deactivated"
            
            db.commit()
            return {"message": message}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting academic unit: {str(e)}"
            )
    
    async def assign_member_to_academic_unit(
        self, 
        unit_id: int, 
        member_data: AcademicUnitMemberAssign, 
        db: Session
    ) -> Dict[str, str]:
        """Assign member to academic unit"""
        try:
            assignment_dict = member_data.dict()
            assignments = self.service.assign_members_to_academic_unit(unit_id, [assignment_dict], db)
            db.commit()
            
            return {"message": f"Member {member_data.user_id} assigned to academic unit successfully"}
            
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
    
    async def remove_member_from_academic_unit(
        self, 
        unit_id: int, 
        member_data: AcademicUnitMemberRemove, 
        db: Session
    ) -> Dict[str, str]:
        """Remove member from academic unit"""
        try:
            success = self.service.remove_member_from_academic_unit(unit_id, member_data.user_id, db)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member assignment not found"
                )
            
            db.commit()
            return {"message": f"Member {member_data.user_id} removed from academic unit successfully"}
            
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
    
    async def assign_multiple_members_to_academic_unit(
        self, 
        unit_id: int, 
        members_data: List[AcademicUnitMemberAssign], 
        db: Session
    ) -> Dict[str, Any]:
        """Assign multiple members to academic unit"""
        try:
            member_assignments = [member.dict() for member in members_data]
            assignments = self.service.assign_members_to_academic_unit(unit_id, member_assignments, db)
            db.commit()
            
            return {
                "message": f"Successfully assigned {len(assignments)} members to academic unit",
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
    
    async def get_academic_unit_overview(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Get academic unit overview"""
        overview = self.service.get_academic_unit_overview(unit_id, db)
        if "error" in overview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=overview["error"]
            )
        
        return overview
    
    async def get_academic_unit_member_analysis(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Get academic unit member analysis"""
        analysis = self.service.get_academic_unit_member_analysis(unit_id, db)
        if "error" in analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=analysis["error"]
            )
        
        return analysis
    
    async def get_academic_unit_optimization_suggestions(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Get optimization suggestions for academic unit"""
        suggestions = self.service.suggest_academic_unit_optimizations(unit_id, db)
        if "error" in suggestions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=suggestions["error"]
            )
        
        return suggestions
    
    async def get_academic_units_by_type(self, type_id: int, db: Session) -> List[AcademicUnitResponse]:
        """Get academic units filtered by type"""
        units = self.service.get_units_by_type(type_id, db)
        return [self._build_unit_response(unit) for unit in units]
    
    async def get_academic_unit_statistics(self, db: Session) -> AcademicUnitStatistics:
        """Get academic unit statistics"""
        stats = self.repo.get_statistics(db)
        return AcademicUnitStatistics(
            total_units=stats["total_units"],
            active_units=stats["active_units"],
            by_type=stats["by_type"],
            total_students=stats["total_students"],
            total_faculty=stats["total_faculty"],
            units_with_projects=stats["units_with_projects"],
            average_members_per_unit=stats["average_members_per_unit"]
        )
    
    async def get_hierarchy_structure(self, db: Session) -> Dict[str, Any]:
        """Get academic unit hierarchy structure"""
        return self.service.get_hierarchy_structure(db)
    
    async def bulk_update_academic_units(
        self, 
        unit_ids: List[int], 
        update_data: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """Bulk update academic units"""
        try:
            result = self.service.bulk_update_academic_units(unit_ids, update_data, db)
            db.commit()
            return result
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error in bulk update: {str(e)}"
            )
    
    async def validate_academic_unit_creation(self, unit_data: AcademicUnitCreate, db: Session) -> Dict[str, Any]:
        """Validate academic unit creation without creating"""
        return self.service.validate_academic_unit_creation(unit_data, db)
    
    def _build_unit_response(self, unit: AcademicUnit) -> AcademicUnitResponse:
        """Build academic unit response with calculated fields"""
        # Build academic unit type info
        academic_unit_type = {}
        if unit.academic_unit_type:
            academic_unit_type = {
                "id": unit.academic_unit_type.id,
                "name": unit.academic_unit_type.name,
                "display_name": unit.academic_unit_type.display_name,
                "hierarchy_level": unit.academic_unit_type.hierarchy_level,
                "category": unit.academic_unit_type.category
            }
        
        # Get members info if available
        members = []
        if hasattr(unit, 'user_academic_units') and unit.user_academic_units:
            for user_unit in unit.user_academic_units:
                if user_unit.is_active and user_unit.user:
                    members.append({
                        "id": user_unit.user.id,
                        "uuid": user_unit.user.uuid,
                        "username": user_unit.user.username,
                        "full_name": f"{user_unit.user.first_name} {user_unit.user.last_name}",
                        "faculty_id": user_unit.user.faculty_id,
                        "relationship_type": user_unit.relationship_type,
                        "position_title": user_unit.position_title,
                        "department": user_unit.department,
                        "degree_program": user_unit.degree_program,
                        "academic_year": user_unit.academic_year,
                        "is_primary": user_unit.is_primary,
                        "can_represent_unit": user_unit.can_represent_unit,
                        "has_budget_authority": user_unit.has_budget_authority,
                        "is_faculty": user_unit.user.is_faculty,
                        "is_student": user_unit.user.is_student,
                        "is_external_client": user_unit.user.is_external_client
                    })
        
        # Get categories info if available (placeholder for CMS integration)
        categories = []
        if hasattr(unit, 'categories') and unit.categories:
            for category in unit.categories:
                if category.is_active:
                    categories.append({
                        "id": category.id,
                        "name": category.name,
                        "display_name": category.display_name,
                        "category_type": category.category_type,
                        "total_videos": category.total_videos,
                        "total_galleries": category.total_galleries
                    })
        
        return AcademicUnitResponse(
            id=unit.id,
            name=unit.name,
            short_name=unit.short_name,
            abbreviation=unit.abbreviation,
            description=unit.description,
            academic_unit_type_id=unit.academic_unit_type_id,
            academic_unit_type=academic_unit_type,
            website=unit.website,
            email=unit.email,
            phone=unit.phone,
            address=unit.address,
            building=unit.building,
            logo_url=unit.logo_url,
            color_primary=unit.color_primary,
            color_secondary=unit.color_secondary,
            is_active=unit.is_active,
            sort_order=unit.sort_order,
            allows_public_content=unit.allows_public_content,
            requires_approval=unit.requires_approval,
            total_students=unit.total_students,
            total_faculty=unit.total_faculty,
            total_projects=unit.total_projects,
            created_at=unit.created_at,
            updated_at=unit.updated_at,
            members=members,
            categories=categories
        )


# Create controller instances
academic_unit_type_controller = AcademicUnitTypeController()
academic_unit_controller = AcademicUnitController()