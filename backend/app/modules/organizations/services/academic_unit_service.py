# backend/app/modules/organizations/services/academic_unit_service.py
"""
Academic Unit service - Business logic for academic unit operations
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.modules.organizations.models import AcademicUnit, AcademicUnitType
from app.modules.organizations.repositories import AcademicUnitRepository, AcademicUnitTypeRepository
from app.modules.organizations.schemas import (
    AcademicUnitCreate, AcademicUnitUpdate, 
    AcademicUnitTypeCreate, AcademicUnitTypeUpdate
)


class AcademicUnitTypeService:
    """Service for academic unit type operations"""
    
    def __init__(self):
        self.repo = AcademicUnitTypeRepository()
    
    def validate_academic_unit_type_creation(self, type_data: AcademicUnitTypeCreate, db: Session) -> Dict[str, Any]:
        """Validate academic unit type creation"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness
        if not self.repo.validate_name_unique(db, type_data.name):
            errors.append(f"Academic unit type name '{type_data.name}' already exists")
        
        # Check hierarchy level logic
        existing_at_level = (
            db.query(AcademicUnitType)
            .filter(AcademicUnitType.hierarchy_level == type_data.hierarchy_level)
            .filter(AcademicUnitType.is_active == True)
            .count()
        )
        
        if existing_at_level > 0:
            warnings.append(f"Other unit types exist at hierarchy level {type_data.hierarchy_level}")
        
        # Suggest appropriate permissions based on hierarchy level
        if type_data.hierarchy_level <= 2:  # High level (Faculty, School)
            if not type_data.allows_faculty:
                suggestions.append("High-level units (Faculty/School) typically allow faculty members")
            if not type_data.allows_students:
                suggestions.append("High-level units (Faculty/School) typically allow students")
        elif type_data.hierarchy_level >= 5:  # Low level (Department, Lab)
            if type_data.requires_approval:
                suggestions.append("Low-level units typically don't require approval for assignments")
        
        # Validate abbreviation length for hierarchy
        if type_data.abbreviation and len(type_data.abbreviation) > 5 and type_data.hierarchy_level <= 3:
            warnings.append("High-level units should have shorter abbreviations (≤5 characters)")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def create_academic_unit_type_with_validation(self, type_data: AcademicUnitTypeCreate, db: Session) -> AcademicUnitType:
        """Create academic unit type with validation"""
        validation = self.validate_academic_unit_type_creation(type_data, db)
        if not validation["is_valid"]:
            raise ValueError(f"Academic unit type validation failed: {', '.join(validation['errors'])}")
        
        type_dict = type_data.dict()
        unit_type = self.repo.create(db, type_dict)
        return unit_type
    
    def update_academic_unit_type_with_validation(self, type_id: int, update_data: AcademicUnitTypeUpdate, db: Session) -> AcademicUnitType:
        """Update academic unit type with validation"""
        unit_type = self.repo.get_by_id(db, type_id)
        if not unit_type:
            raise ValueError("Academic unit type not found")
        
        # Check name uniqueness if name is being changed
        if update_data.name and update_data.name != unit_type.name:
            if not self.repo.validate_name_unique(db, update_data.name, type_id):
                raise ValueError(f"Academic unit type name '{update_data.name}' already exists")
        
        # Check impact of deactivation
        if update_data.is_active is False and unit_type.is_active:
            units_count = self.repo.get_academic_units_count(db, type_id)
            if units_count > 0:
                raise ValueError(f"Cannot deactivate unit type with {units_count} active academic units")
        
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        updated_type = self.repo.update(db, unit_type, update_dict)
        return updated_type


class AcademicUnitService:
    """Service for academic unit operations"""
    
    def __init__(self):
        self.repo = AcademicUnitRepository()
        self.type_repo = AcademicUnitTypeRepository()
    
    def validate_academic_unit_creation(self, unit_data: AcademicUnitCreate, db: Session) -> Dict[str, Any]:
        """Validate academic unit creation"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness
        if not self.repo.validate_name_unique(db, unit_data.name):
            errors.append(f"Academic unit name '{unit_data.name}' already exists")
        
        # Check abbreviation uniqueness
        if unit_data.abbreviation and not self.repo.validate_abbreviation_unique(db, unit_data.abbreviation):
            errors.append(f"Academic unit abbreviation '{unit_data.abbreviation}' already exists")
        
        # Validate academic unit type exists and is active
        unit_type = self.type_repo.get_by_id(db, unit_data.academic_unit_type_id)
        if not unit_type:
            errors.append("Invalid academic unit type ID")
        elif not unit_type.is_active:
            errors.append("Academic unit type is not active")
        
        # Check contact information
        if not unit_data.email and not unit_data.phone:
            warnings.append("Consider adding contact information for better communication")
        
        # Suggest visual identity
        if not unit_data.logo_url and not unit_data.color_primary:
            suggestions.append("Consider adding logo and brand colors for better visual identity")
        
        # Website validation
        if unit_data.website and not unit_data.website.startswith(('http://', 'https://')):
            warnings.append("Website URL should include protocol (http:// or https://)")
        
        # Abbreviation format suggestion
        if unit_data.abbreviation and len(unit_data.abbreviation) > 10:
            warnings.append("Consider using a shorter abbreviation (≤10 characters)")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def validate_academic_unit_update(self, unit: AcademicUnit, update_data: AcademicUnitUpdate, db: Session) -> Dict[str, Any]:
        """Validate academic unit update"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check name uniqueness if name is being changed
        if update_data.name and update_data.name != unit.name:
            if not self.repo.validate_name_unique(db, update_data.name, unit.id):
                errors.append(f"Academic unit name '{update_data.name}' already exists")
        
        # Check abbreviation uniqueness if abbreviation is being changed
        if update_data.abbreviation and update_data.abbreviation != unit.abbreviation:
            if not self.repo.validate_abbreviation_unique(db, update_data.abbreviation, unit.id):
                errors.append(f"Academic unit abbreviation '{update_data.abbreviation}' already exists")
        
        # Check if deactivating unit with active members
        if update_data.is_active is False and unit.is_active:
            members = self.repo.get_members(db, unit.id)
            if members:
                warnings.append(f"Deactivating unit will affect {len(members)} active members")
        
        # Validate unit type change
        if update_data.academic_unit_type_id and update_data.academic_unit_type_id != unit.academic_unit_type_id:
            new_type = self.type_repo.get_by_id(db, update_data.academic_unit_type_id)
            if not new_type:
                errors.append("Invalid academic unit type ID")
            elif not new_type.is_active:
                errors.append("New academic unit type is not active")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def create_academic_unit_with_validation(self, unit_data: AcademicUnitCreate, db: Session) -> AcademicUnit:
        """Create academic unit with validation"""
        validation = self.validate_academic_unit_creation(unit_data, db)
        if not validation["is_valid"]:
            raise ValueError(f"Academic unit validation failed: {', '.join(validation['errors'])}")
        
        unit_dict = unit_data.dict()
        unit = self.repo.create(db, unit_dict)
        return unit
    
    def update_academic_unit_with_validation(self, unit_id: int, update_data: AcademicUnitUpdate, db: Session) -> AcademicUnit:
        """Update academic unit with validation"""
        unit = self.repo.get_by_id(db, unit_id)
        if not unit:
            raise ValueError("Academic unit not found")
        
        validation = self.validate_academic_unit_update(unit, update_data, db)
        if not validation["is_valid"]:
            raise ValueError(f"Academic unit update validation failed: {', '.join(validation['errors'])}")
        
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        updated_unit = self.repo.update(db, unit, update_dict)
        return updated_unit
    
    def assign_members_to_academic_unit(self, unit_id: int, member_assignments: List[Dict], db: Session) -> List[Any]:
        """Assign multiple members to academic unit"""
        unit = self.repo.get_by_id(db, unit_id)
        if not unit:
            raise ValueError("Academic unit not found")
        
        # Check if unit type allows the member types
        unit_type = unit.academic_unit_type
        
        assignments = []
        for assignment in member_assignments:
            user_id = assignment.get("user_id")
            if not user_id:
                continue
            
            assignment_data = {k: v for k, v in assignment.items() if k != "user_id"}
            
            # Validate relationship type
            relationship_type = assignment_data.get("relationship_type", "member")
            if relationship_type == "faculty" and not unit_type.allows_faculty:
                raise ValueError(f"Unit type '{unit_type.name}' does not allow faculty members")
            elif relationship_type == "student" and not unit_type.allows_students:
                raise ValueError(f"Unit type '{unit_type.name}' does not allow students")
            
            assignment_result = self.repo.assign_member(db, unit_id, user_id, **assignment_data)
            assignments.append(assignment_result)
        
        # Update statistics
        self.repo.update_member_statistics(db, unit_id)
        
        return assignments
    
    def remove_member_from_academic_unit(self, unit_id: int, user_id: int, db: Session) -> bool:
        """Remove member from academic unit"""
        unit = self.repo.get_by_id(db, unit_id)
        if not unit:
            raise ValueError("Academic unit not found")
        
        result = self.repo.remove_member(db, unit_id, user_id)
        if result:
            # Update statistics
            self.repo.update_member_statistics(db, unit_id)
        
        return result
    
    def get_academic_unit_overview(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Get comprehensive academic unit overview"""
        unit = self.repo.get_by_id(db, unit_id, include_members=True)
        if not unit:
            return {"error": "Academic unit not found"}
        
        # Get member breakdown
        members = self.repo.get_members(db, unit_id)
        faculty_count = sum(1 for m in members if m.is_faculty)
        student_count = sum(1 for m in members if m.is_student)
        external_count = sum(1 for m in members if m.is_external_client)
        
        # Get unit type info
        unit_type = unit.academic_unit_type
        
        return {
            "unit": {
                "id": unit.id,
                "name": unit.name,
                "short_name": unit.short_name,
                "abbreviation": unit.abbreviation,
                "description": unit.description,
                "type": {
                    "id": unit_type.id,
                    "name": unit_type.name,
                    "display_name": unit_type.display_name,
                    "hierarchy_level": unit_type.hierarchy_level
                } if unit_type else None
            },
            "statistics": {
                "total_members": len(members),
                "faculty_count": faculty_count,
                "student_count": student_count,
                "external_count": external_count,
                "total_projects": unit.total_projects
            },
            "configuration": {
                "allows_public_content": unit.allows_public_content,
                "requires_approval": unit.requires_approval,
                "is_active": unit.is_active
            },
            "contact": {
                "email": unit.email,
                "phone": unit.phone,
                "website": unit.website,
                "address": unit.address,
                "building": unit.building
            },
            "visual_identity": {
                "logo_url": unit.logo_url,
                "color_primary": unit.color_primary,
                "color_secondary": unit.color_secondary
            }
        }
    
    def get_academic_unit_member_analysis(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Analyze academic unit member composition"""
        unit = self.repo.get_by_id(db, unit_id, include_members=True)
        if not unit:
            return {"error": "Academic unit not found"}
        
        members = self.repo.get_members(db, unit_id)
        
        # Member type breakdown
        member_types = {"faculty": 0, "student": 0, "external": 0, "other": 0}
        relationship_types = {}
        departments = {}
        
        for member in members:
            # Count by user type
            if member.is_faculty:
                member_types["faculty"] += 1
            elif member.is_student:
                member_types["student"] += 1
            elif member.is_external_client:
                member_types["external"] += 1
            else:
                member_types["other"] += 1
        
        # Get relationship details from UserAcademicUnit
        if hasattr(unit, 'user_academic_units') and unit.user_academic_units:
            for user_unit in unit.user_academic_units:
                if user_unit.is_active:
                    # Count relationship types
                    rel_type = user_unit.relationship_type or "member"
                    relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
                    
                    # Count departments
                    if user_unit.department:
                        departments[user_unit.department] = departments.get(user_unit.department, 0) + 1
        
        return {
            "unit_id": unit_id,
            "unit_name": unit.name,
            "total_members": len(members),
            "member_types": member_types,
            "relationship_types": relationship_types,
            "departments": departments,
            "member_distribution": {
                "faculty_percentage": round((member_types["faculty"] / len(members)) * 100, 2) if members else 0,
                "student_percentage": round((member_types["student"] / len(members)) * 100, 2) if members else 0,
                "external_percentage": round((member_types["external"] / len(members)) * 100, 2) if members else 0
            }
        }
    
    def suggest_academic_unit_optimizations(self, unit_id: int, db: Session) -> Dict[str, Any]:
        """Suggest optimizations for academic unit"""
        unit = self.repo.get_by_id(db, unit_id, include_members=True)
        if not unit:
            return {"error": "Academic unit not found"}
        
        suggestions = []
        
        # Member-based suggestions
        members = self.repo.get_members(db, unit_id)
        if len(members) == 0:
            suggestions.append({
                "type": "warning",
                "category": "membership",
                "message": "Academic unit has no assigned members",
                "action": "Assign faculty, students, or staff to activate the unit"
            })
        
        # Faculty/student balance for academic units
        faculty_count = sum(1 for m in members if m.is_faculty)
        student_count = sum(1 for m in members if m.is_student)
        
        if unit.academic_unit_type.category == "academic":
            if faculty_count == 0 and student_count > 0:
                suggestions.append({
                    "type": "warning",
                    "category": "academic_balance",
                    "message": "Academic unit has students but no faculty",
                    "action": "Assign faculty members to provide academic oversight"
                })
            elif faculty_count > 0 and student_count == 0:
                suggestions.append({
                    "type": "info",
                    "category": "academic_balance",
                    "message": "Academic unit has faculty but no students",
                    "action": "Consider assigning students if this is an active academic program"
                })
        
        # Contact information
        if not unit.email and not unit.phone:
            suggestions.append({
                "type": "improvement",
                "category": "communication",
                "message": "No contact information provided",
                "action": "Add email or phone for better communication with members"
            })
        
        # Visual identity
        if not unit.logo_url and not unit.color_primary:
            suggestions.append({
                "type": "improvement",
                "category": "branding",
                "message": "No visual identity elements configured",
                "action": "Add logo and brand colors for better recognition"
            })
        
        # Website presence
        if not unit.website:
            suggestions.append({
                "type": "improvement",
                "category": "online_presence",
                "message": "No website configured",
                "action": "Add website URL to improve unit visibility"
            })
        
        # Building/location information
        if not unit.building and not unit.address:
            suggestions.append({
                "type": "improvement",
                "category": "location",
                "message": "No physical location information",
                "action": "Add building or address information for easier location"
            })
        
        # Content permissions
        if unit.allows_public_content and unit.requires_approval:
            suggestions.append({
                "type": "info",
                "category": "content_policy",
                "message": "Unit allows public content but requires approval",
                "action": "Consider streamlining approval process for better content flow"
            })
        
        return {
            "unit_id": unit_id,
            "unit_name": unit.name,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "warnings": len([s for s in suggestions if s["type"] == "warning"]),
            "improvements": len([s for s in suggestions if s["type"] == "improvement"]),
            "info": len([s for s in suggestions if s["type"] == "info"])
        }
    
    def get_units_by_type(self, type_id: int, db: Session) -> List[AcademicUnit]:
        """Get academic units filtered by type"""
        return self.repo.get_by_type(db, type_id)
    
    def bulk_update_academic_units(self, unit_ids: List[int], update_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Bulk update multiple academic units"""
        updated_count = 0
        errors = []
        
        for unit_id in unit_ids:
            try:
                unit = self.repo.get_by_id(db, unit_id)
                if not unit:
                    errors.append(f"Academic unit ID {unit_id} not found")
                    continue
                
                self.repo.update(db, unit, update_data)
                updated_count += 1
                
            except Exception as e:
                errors.append(f"Error updating academic unit ID {unit_id}: {str(e)}")
        
        return {
            "updated_count": updated_count,
            "total_requested": len(unit_ids),
            "errors": errors
        }
    
    def get_hierarchy_structure(self, db: Session) -> Dict[str, Any]:
        """Get academic unit hierarchy structure"""
        # Get all unit types ordered by hierarchy
        unit_types = (
            db.query(AcademicUnitType)
            .filter(AcademicUnitType.is_active == True)
            .order_by(AcademicUnitType.hierarchy_level, AcademicUnitType.sort_order)
            .all()
        )
        
        hierarchy = {}
        for unit_type in unit_types:
            # Get units for this type
            units = self.repo.get_by_type(db, unit_type.id)
            
            hierarchy[unit_type.hierarchy_level] = {
                "type": {
                    "id": unit_type.id,
                    "name": unit_type.name,
                    "display_name": unit_type.display_name,
                    "category": unit_type.category,
                    "allows_students": unit_type.allows_students,
                    "allows_faculty": unit_type.allows_faculty
                },
                "units": [
                    {
                        "id": unit.id,
                        "name": unit.name,
                        "abbreviation": unit.abbreviation,
                        "total_members": unit.total_faculty + unit.total_students,
                        "is_active": unit.is_active
                    } for unit in units
                ],
                "total_units": len(units),
                "active_units": len([u for u in units if u.is_active])
            }
        
        return hierarchy


# Create service instances
academic_unit_type_service = AcademicUnitTypeService()
academic_unit_service = AcademicUnitService()