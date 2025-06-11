# backend/app/modules/organizations/services/area_service.py
"""
Area service - Business logic for area operations
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.modules.organizations.models import Area
from app.modules.organizations.repositories import AreaRepository
from app.modules.organizations.schemas import AreaCreate, AreaUpdate


class AreaService:
    """Service for area operations"""
    
    def __init__(self):
        self.repo = AreaRepository()
    
    def validate_area_creation(self, area_data: AreaCreate, db: Session) -> Dict[str, Any]:
        """Validate area creation data"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness
        if not self.repo.validate_name_unique(db, area_data.name):
            errors.append(f"Area name '{area_data.name}' already exists")
        
        # Check capacity logic
        if (area_data.max_concurrent_projects and 
            area_data.estimated_capacity_hours and 
            area_data.max_concurrent_projects > area_data.estimated_capacity_hours / 40):
            warnings.append("Max concurrent projects might exceed realistic capacity based on estimated hours")
        
        # Suggest collaboration for complex areas
        if area_data.category in ["production", "technical"] and not area_data.requires_collaboration:
            suggestions.append("Consider enabling collaboration requirement for production/technical areas")
        
        # Check contact information completeness
        if not area_data.contact_email and not area_data.contact_phone:
            warnings.append("Consider adding contact information for better communication")
        
        # Validate specialization for certain categories
        if area_data.category == "technical" and not area_data.specialization:
            suggestions.append("Technical areas should specify their specialization")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def validate_area_update(self, area: Area, update_data: AreaUpdate, db: Session) -> Dict[str, Any]:
        """Validate area update data"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness if name is being changed
        if update_data.name and update_data.name != area.name:
            if not self.repo.validate_name_unique(db, update_data.name, area.id):
                errors.append(f"Area name '{update_data.name}' already exists")
        
        # Check if deactivating area with active members
        if update_data.is_active is False and area.is_active:
            members = self.repo.get_members(db, area.id)
            if members:
                warnings.append(f"Deactivating area will affect {len(members)} active members")
        
        # Capacity validation
        new_max_projects = update_data.max_concurrent_projects or area.max_concurrent_projects
        new_capacity_hours = update_data.estimated_capacity_hours or area.estimated_capacity_hours
        
        if (new_max_projects and new_capacity_hours and 
            new_max_projects > new_capacity_hours / 40):
            warnings.append("Updated capacity settings might be unrealistic")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def create_area_with_validation(self, area_data: AreaCreate, db: Session) -> Area:
        """Create area with validation"""
        validation = self.validate_area_creation(area_data, db)
        if not validation["is_valid"]:
            raise ValueError(f"Area validation failed: {', '.join(validation['errors'])}")
        
        area_dict = area_data.dict()
        area = self.repo.create(db, area_dict)
        return area
    
    def update_area_with_validation(self, area_id: int, update_data: AreaUpdate, db: Session) -> Area:
        """Update area with validation"""
        area = self.repo.get_by_id(db, area_id)
        if not area:
            raise ValueError("Area not found")
        
        validation = self.validate_area_update(area, update_data, db)
        if not validation["is_valid"]:
            raise ValueError(f"Area update validation failed: {', '.join(validation['errors'])}")
        
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        updated_area = self.repo.update(db, area, update_dict)
        return updated_area
    
    def assign_members_to_area(self, area_id: int, member_assignments: List[Dict], db: Session) -> List[Any]:
        """Assign multiple members to area"""
        area = self.repo.get_by_id(db, area_id)
        if not area:
            raise ValueError("Area not found")
        
        assignments = []
        for assignment in member_assignments:
            user_id = assignment.get("user_id")
            if not user_id:
                continue
                
            assignment_data = {k: v for k, v in assignment.items() if k != "user_id"}
            
            # Validate assignment data
            if assignment_data.get("time_allocation_percentage"):
                if not (1 <= assignment_data["time_allocation_percentage"] <= 100):
                    raise ValueError(f"Invalid time allocation percentage for user {user_id}")
            
            assignment_result = self.repo.assign_member(db, area_id, user_id, **assignment_data)
            assignments.append(assignment_result)
        
        # Update statistics
        self.repo.update_member_statistics(db, area_id)
        
        return assignments
    
    def remove_member_from_area(self, area_id: int, user_id: int, db: Session) -> bool:
        """Remove member from area"""
        area = self.repo.get_by_id(db, area_id)
        if not area:
            raise ValueError("Area not found")
        
        result = self.repo.remove_member(db, area_id, user_id)
        if result:
            # Update statistics
            self.repo.update_member_statistics(db, area_id)
        
        return result
    
    def get_area_workload_analysis(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Analyze area workload and capacity"""
        area = self.repo.get_by_id(db, area_id, include_members=True)
        if not area:
            return {"error": "Area not found"}
        
        members = self.repo.get_members(db, area_id)
        total_members = len(members)
        
        # Calculate capacity metrics
        if area.estimated_capacity_hours and area.max_concurrent_projects:
            hours_per_project = area.estimated_capacity_hours / area.max_concurrent_projects
            capacity_utilization = (area.active_projects / area.max_concurrent_projects) * 100 if area.max_concurrent_projects > 0 else 0
        else:
            hours_per_project = None
            capacity_utilization = None
        
        # Workload recommendations
        recommendations = []
        if capacity_utilization and capacity_utilization > 90:
            recommendations.append("Area is at high capacity, consider reducing new project assignments")
        elif capacity_utilization and capacity_utilization < 50:
            recommendations.append("Area has available capacity for additional projects")
        
        if total_members < 2 and area.requires_collaboration:
            recommendations.append("Area requires collaboration but has few members, consider adding team members")
        
        if area.can_lead_projects and total_members == 0:
            recommendations.append("Area can lead projects but has no assigned members")
        
        # Member analysis
        member_roles = {}
        if hasattr(area, 'user_areas') and area.user_areas:
            for user_area in area.user_areas:
                if user_area.is_active and user_area.role_in_area:
                    role = user_area.role_in_area
                    member_roles[role] = member_roles.get(role, 0) + 1
        
        return {
            "area_name": area.name,
            "category": area.category,
            "total_members": total_members,
            "active_projects": area.active_projects,
            "completed_projects": area.completed_projects,
            "max_concurrent_projects": area.max_concurrent_projects,
            "capacity_utilization": capacity_utilization,
            "hours_per_project": hours_per_project,
            "member_roles": member_roles,
            "can_lead_projects": area.can_lead_projects,
            "requires_collaboration": area.requires_collaboration,
            "recommendations": recommendations
        }
    
    def get_area_performance_metrics(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Get area performance metrics"""
        area = self.repo.get_by_id(db, area_id)
        if not area:
            return {"error": "Area not found"}
        
        # Calculate performance ratios
        total_projects = area.active_projects + area.completed_projects
        completion_rate = (area.completed_projects / total_projects * 100) if total_projects > 0 else 0
        
        # Efficiency metrics
        if area.total_members > 0:
            projects_per_member = total_projects / area.total_members
            active_projects_per_member = area.active_projects / area.total_members
        else:
            projects_per_member = 0
            active_projects_per_member = 0
        
        # Capacity analysis
        if area.max_concurrent_projects:
            capacity_usage = (area.active_projects / area.max_concurrent_projects) * 100
        else:
            capacity_usage = None
        
        return {
            "area_id": area_id,
            "area_name": area.name,
            "performance": {
                "total_projects": total_projects,
                "active_projects": area.active_projects,
                "completed_projects": area.completed_projects,
                "completion_rate": round(completion_rate, 2),
                "projects_per_member": round(projects_per_member, 2),
                "active_projects_per_member": round(active_projects_per_member, 2)
            },
            "capacity": {
                "total_members": area.total_members,
                "max_concurrent_projects": area.max_concurrent_projects,
                "capacity_usage": round(capacity_usage, 2) if capacity_usage else None,
                "estimated_capacity_hours": area.estimated_capacity_hours
            },
            "settings": {
                "can_lead_projects": area.can_lead_projects,
                "requires_collaboration": area.requires_collaboration,
                "is_active": area.is_active
            }
        }
    
    def suggest_area_optimizations(self, area_id: int, db: Session) -> Dict[str, Any]:
        """Suggest optimizations for area"""
        area = self.repo.get_by_id(db, area_id, include_members=True)
        if not area:
            return {"error": "Area not found"}
        
        suggestions = []
        
        # Member-based suggestions
        if area.total_members == 0:
            suggestions.append({
                "type": "critical",
                "category": "staffing",
                "message": "Area has no assigned members",
                "action": "Assign team members to enable project execution"
            })
        elif area.total_members == 1 and area.requires_collaboration:
            suggestions.append({
                "type": "warning",
                "category": "staffing", 
                "message": "Area requires collaboration but only has one member",
                "action": "Add additional team members for effective collaboration"
            })
        
        # Capacity-based suggestions
        if area.max_concurrent_projects and area.active_projects >= area.max_concurrent_projects:
            suggestions.append({
                "type": "warning",
                "category": "capacity",
                "message": "Area is at maximum project capacity",
                "action": "Complete current projects before taking on new ones"
            })
        
        # Performance-based suggestions
        total_projects = area.active_projects + area.completed_projects
        if total_projects > 0:
            completion_rate = (area.completed_projects / total_projects) * 100
            if completion_rate < 70:
                suggestions.append({
                    "type": "improvement",
                    "category": "performance",
                    "message": f"Low project completion rate ({completion_rate:.1f}%)",
                    "action": "Review project management processes and resource allocation"
                })
        
        # Configuration suggestions
        if not area.contact_email and not area.contact_phone:
            suggestions.append({
                "type": "improvement",
                "category": "communication",
                "message": "No contact information provided",
                "action": "Add contact email or phone for better communication"
            })
        
        return {
            "area_id": area_id,
            "area_name": area.name,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "critical_issues": len([s for s in suggestions if s["type"] == "critical"]),
            "warnings": len([s for s in suggestions if s["type"] == "warning"]),
            "improvements": len([s for s in suggestions if s["type"] == "improvement"])
        }
    
    def get_areas_by_category(self, category: str, db: Session) -> List[Area]:
        """Get areas filtered by category"""
        return self.repo.get_by_category(db, category)
    
    def bulk_update_areas(self, area_ids: List[int], update_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Bulk update multiple areas"""
        updated_count = 0
        errors = []
        
        for area_id in area_ids:
            try:
                area = self.repo.get_by_id(db, area_id)
                if not area:
                    errors.append(f"Area ID {area_id} not found")
                    continue
                
                self.repo.update(db, area, update_data)
                updated_count += 1
                
            except Exception as e:
                errors.append(f"Error updating area ID {area_id}: {str(e)}")
        
        return {
            "updated_count": updated_count,
            "total_requested": len(area_ids),
            "errors": errors
        }


# Create service instance
area_service = AreaService()