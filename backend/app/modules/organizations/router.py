# backend/app/modules/organizations/router.py
"""
Organizations Router - API endpoints for organizations management
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.organizations.controllers import (
    area_controller,
    academic_unit_controller,
    academic_unit_type_controller
)
from app.modules.organizations.schemas import (
    # Area schemas
    AreaCreate, AreaUpdate, AreaResponse, AreaListResponse, AreaSearchParams,
    AreaMemberAssign, AreaMemberRemove, AreaStatistics, AreaCategory,
    
    # Academic Unit Type schemas
    AcademicUnitTypeCreate, AcademicUnitTypeUpdate, AcademicUnitTypeResponse,
    AcademicUnitTypeListResponse, AcademicUnitCategory,
    
    # Academic Unit schemas
    AcademicUnitCreate, AcademicUnitUpdate, AcademicUnitResponse,
    AcademicUnitListResponse, AcademicUnitSearchParams,
    AcademicUnitMemberAssign, AcademicUnitMemberRemove, AcademicUnitStatistics
)

# Create router instance
router = APIRouter(prefix="/organizations", tags=["Organizations"])

# ===================================
# AREAS ENDPOINTS
# ===================================

@router.post("/areas", response_model=AreaResponse, status_code=201)
async def create_area(
    area_data: AreaCreate,
    db: Session = Depends(get_db)
):
    """Create new area"""
    return await area_controller.create_area(area_data, db)


@router.get("/areas", response_model=AreaListResponse)
async def get_areas(
    q: Optional[str] = Query(None, description="Search query"),
    category: Optional[AreaCategory] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    can_lead_projects: Optional[bool] = Query(None, description="Filter by project leadership capability"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get paginated list of areas with filters"""
    params = AreaSearchParams(
        q=q,
        category=category,
        is_active=is_active,
        can_lead_projects=can_lead_projects,
        page=page,
        per_page=per_page
    )
    return await area_controller.get_areas(params, db)


@router.get("/areas/categories/{category}", response_model=List[AreaResponse])
async def get_areas_by_category(
    category: AreaCategory = Path(..., description="Area category"),
    db: Session = Depends(get_db)
):
    """Get areas filtered by category"""
    return await area_controller.get_areas_by_category(category, db)


@router.get("/areas/statistics", response_model=AreaStatistics)
async def get_area_statistics(
    db: Session = Depends(get_db)
):
    """Get area statistics"""
    return await area_controller.get_area_statistics(db)


@router.get("/areas/{area_id}", response_model=AreaResponse)
async def get_area(
    area_id: int = Path(..., description="Area ID"),
    db: Session = Depends(get_db)
):
    """Get area by ID with full details"""
    return await area_controller.get_area(area_id, db)


@router.put("/areas/{area_id}", response_model=AreaResponse)
async def update_area(
    area_id: int = Path(..., description="Area ID"),
    update_data: AreaUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update area"""
    return await area_controller.update_area(area_id, update_data, db)


@router.delete("/areas/{area_id}")
async def delete_area(
    area_id: int = Path(..., description="Area ID"),
    hard_delete: bool = Query(False, description="Perform hard delete (permanent)"),
    db: Session = Depends(get_db)
):
    """Delete area (soft or hard delete)"""
    return await area_controller.delete_area(area_id, db, hard_delete)


@router.post("/areas/{area_id}/members")
async def assign_member_to_area(
    area_id: int = Path(..., description="Area ID"),
    member_data: AreaMemberAssign = ...,
    db: Session = Depends(get_db)
):
    """Assign member to area"""
    return await area_controller.assign_member_to_area(area_id, member_data, db)


@router.post("/areas/{area_id}/members/bulk")
async def assign_multiple_members_to_area(
    area_id: int = Path(..., description="Area ID"),
    members_data: List[AreaMemberAssign] = ...,
    db: Session = Depends(get_db)
):
    """Assign multiple members to area"""
    return await area_controller.assign_multiple_members_to_area(area_id, members_data, db)


@router.delete("/areas/{area_id}/members")
async def remove_member_from_area(
    area_id: int = Path(..., description="Area ID"),
    member_data: AreaMemberRemove = ...,
    db: Session = Depends(get_db)
):
    """Remove member from area"""
    return await area_controller.remove_member_from_area(area_id, member_data, db)


@router.get("/areas/{area_id}/workload-analysis")
async def get_area_workload_analysis(
    area_id: int = Path(..., description="Area ID"),
    db: Session = Depends(get_db)
):
    """Get area workload analysis"""
    return await area_controller.get_area_workload_analysis(area_id, db)


@router.get("/areas/{area_id}/performance-metrics")
async def get_area_performance_metrics(
    area_id: int = Path(..., description="Area ID"),
    db: Session = Depends(get_db)
):
    """Get area performance metrics"""
    return await area_controller.get_area_performance_metrics(area_id, db)


@router.get("/areas/{area_id}/optimization-suggestions")
async def get_area_optimization_suggestions(
    area_id: int = Path(..., description="Area ID"),
    db: Session = Depends(get_db)
):
    """Get optimization suggestions for area"""
    return await area_controller.get_area_optimization_suggestions(area_id, db)


@router.post("/areas/validate")
async def validate_area_creation(
    area_data: AreaCreate,
    db: Session = Depends(get_db)
):
    """Validate area creation without creating"""
    return await area_controller.validate_area_creation(area_data, db)


@router.patch("/areas/bulk-update")
async def bulk_update_areas(
    area_ids: List[int] = Body(..., description="List of area IDs"),
    update_data: Dict[str, Any] = Body(..., description="Update data"),
    db: Session = Depends(get_db)
):
    """Bulk update areas"""
    return await area_controller.bulk_update_areas(area_ids, update_data, db)


# ===================================
# ACADEMIC UNIT TYPES ENDPOINTS
# ===================================

@router.post("/academic-unit-types", response_model=AcademicUnitTypeResponse, status_code=201)
async def create_academic_unit_type(
    type_data: AcademicUnitTypeCreate,
    db: Session = Depends(get_db)
):
    """Create new academic unit type"""
    return await academic_unit_type_controller.create_academic_unit_type(type_data, db)


@router.get("/academic-unit-types", response_model=AcademicUnitTypeListResponse)
async def get_academic_unit_types(
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(20, ge=1, le=100, description="Limit items"),
    search: Optional[str] = Query(None, description="Search query"),
    category: Optional[AcademicUnitCategory] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    hierarchy_level: Optional[int] = Query(None, ge=1, le=10, description="Filter by hierarchy level"),
    db: Session = Depends(get_db)
):
    """Get paginated list of academic unit types"""
    return await academic_unit_type_controller.get_academic_unit_types(
        skip, limit, search, category, is_active, hierarchy_level, db
    )


@router.get("/academic-unit-types/{type_id}", response_model=AcademicUnitTypeResponse)
async def get_academic_unit_type(
    type_id: int = Path(..., description="Academic unit type ID"),
    db: Session = Depends(get_db)
):
    """Get academic unit type by ID"""
    return await academic_unit_type_controller.get_academic_unit_type(type_id, db)


@router.put("/academic-unit-types/{type_id}", response_model=AcademicUnitTypeResponse)
async def update_academic_unit_type(
    type_id: int = Path(..., description="Academic unit type ID"),
    update_data: AcademicUnitTypeUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update academic unit type"""
    return await academic_unit_type_controller.update_academic_unit_type(type_id, update_data, db)


@router.delete("/academic-unit-types/{type_id}")
async def delete_academic_unit_type(
    type_id: int = Path(..., description="Academic unit type ID"),
    hard_delete: bool = Query(False, description="Perform hard delete (permanent)"),
    db: Session = Depends(get_db)
):
    """Delete academic unit type"""
    return await academic_unit_type_controller.delete_academic_unit_type(type_id, db, hard_delete)


# ===================================
# ACADEMIC UNITS ENDPOINTS
# ===================================

@router.post("/academic-units", response_model=AcademicUnitResponse, status_code=201)
async def create_academic_unit(
    unit_data: AcademicUnitCreate,
    db: Session = Depends(get_db)
):
    """Create new academic unit"""
    return await academic_unit_controller.create_academic_unit(unit_data, db)


@router.get("/academic-units", response_model=AcademicUnitListResponse)
async def get_academic_units(
    q: Optional[str] = Query(None, description="Search query"),
    academic_unit_type_id: Optional[int] = Query(None, ge=1, description="Filter by academic unit type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    allows_public_content: Optional[bool] = Query(None, description="Filter by public content permission"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get paginated list of academic units with filters"""
    params = AcademicUnitSearchParams(
        q=q,
        academic_unit_type_id=academic_unit_type_id,
        is_active=is_active,
        allows_public_content=allows_public_content,
        page=page,
        per_page=per_page
    )
    return await academic_unit_controller.get_academic_units(params, db)


@router.get("/academic-units/types/{type_id}", response_model=List[AcademicUnitResponse])
async def get_academic_units_by_type(
    type_id: int = Path(..., description="Academic unit type ID"),
    db: Session = Depends(get_db)
):
    """Get academic units filtered by type"""
    return await academic_unit_controller.get_academic_units_by_type(type_id, db)


@router.get("/academic-units/hierarchy")
async def get_academic_unit_hierarchy(
    db: Session = Depends(get_db)
):
    """Get academic unit hierarchy structure"""
    return await academic_unit_controller.get_hierarchy_structure(db)


@router.get("/academic-units/statistics", response_model=AcademicUnitStatistics)
async def get_academic_unit_statistics(
    db: Session = Depends(get_db)
):
    """Get academic unit statistics"""
    return await academic_unit_controller.get_academic_unit_statistics(db)


@router.get("/academic-units/{unit_id}", response_model=AcademicUnitResponse)
async def get_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    db: Session = Depends(get_db)
):
    """Get academic unit by ID with full details"""
    return await academic_unit_controller.get_academic_unit(unit_id, db)


@router.put("/academic-units/{unit_id}", response_model=AcademicUnitResponse)
async def update_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    update_data: AcademicUnitUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update academic unit"""
    return await academic_unit_controller.update_academic_unit(unit_id, update_data, db)


@router.delete("/academic-units/{unit_id}")
async def delete_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    hard_delete: bool = Query(False, description="Perform hard delete (permanent)"),
    db: Session = Depends(get_db)
):
    """Delete academic unit"""
    return await academic_unit_controller.delete_academic_unit(unit_id, db, hard_delete)


@router.post("/academic-units/{unit_id}/members")
async def assign_member_to_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    member_data: AcademicUnitMemberAssign = ...,
    db: Session = Depends(get_db)
):
    """Assign member to academic unit"""
    return await academic_unit_controller.assign_member_to_academic_unit(unit_id, member_data, db)


@router.post("/academic-units/{unit_id}/members/bulk")
async def assign_multiple_members_to_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    members_data: List[AcademicUnitMemberAssign] = ...,
    db: Session = Depends(get_db)
):
    """Assign multiple members to academic unit"""
    return await academic_unit_controller.assign_multiple_members_to_academic_unit(unit_id, members_data, db)


@router.delete("/academic-units/{unit_id}/members")
async def remove_member_from_academic_unit(
    unit_id: int = Path(..., description="Academic unit ID"),
    member_data: AcademicUnitMemberRemove = ...,
    db: Session = Depends(get_db)
):
    """Remove member from academic unit"""
    return await academic_unit_controller.remove_member_from_academic_unit(unit_id, member_data, db)


@router.get("/academic-units/{unit_id}/overview")
async def get_academic_unit_overview(
    unit_id: int = Path(..., description="Academic unit ID"),
    db: Session = Depends(get_db)
):
    """Get comprehensive academic unit overview"""
    return await academic_unit_controller.get_academic_unit_overview(unit_id, db)


@router.get("/academic-units/{unit_id}/member-analysis")
async def get_academic_unit_member_analysis(
    unit_id: int = Path(..., description="Academic unit ID"),
    db: Session = Depends(get_db)
):
    """Get academic unit member composition analysis"""
    return await academic_unit_controller.get_academic_unit_member_analysis(unit_id, db)


@router.get("/academic-units/{unit_id}/optimization-suggestions")
async def get_academic_unit_optimization_suggestions(
    unit_id: int = Path(..., description="Academic unit ID"),
    db: Session = Depends(get_db)
):
    """Get optimization suggestions for academic unit"""
    return await academic_unit_controller.get_academic_unit_optimization_suggestions(unit_id, db)


@router.post("/academic-units/validate")
async def validate_academic_unit_creation(
    unit_data: AcademicUnitCreate,
    db: Session = Depends(get_db)
):
    """Validate academic unit creation without creating"""
    return await academic_unit_controller.validate_academic_unit_creation(unit_data, db)


@router.patch("/academic-units/bulk-update")
async def bulk_update_academic_units(
    unit_ids: List[int] = Body(..., description="List of academic unit IDs"),
    update_data: Dict[str, Any] = Body(..., description="Update data"),
    db: Session = Depends(get_db)
):
    """Bulk update academic units"""
    return await academic_unit_controller.bulk_update_academic_units(unit_ids, update_data, db)


# ===================================
# UTILITY ENDPOINTS
# ===================================

@router.get("/area-categories")
async def get_area_categories():
    """Get available area categories from enum"""
    categories = []
    
    # Mapping de labels en español para cada categoría
    category_labels = {
        AreaCategory.PRODUCTION: {
            "label": "Producción",
            "description": "Áreas enfocadas en la producción de contenido audiovisual"
        },
        AreaCategory.TECHNICAL: {
            "label": "Técnica", 
            "description": "Áreas especializadas en aspectos técnicos y equipamiento"
        },
        AreaCategory.ADMINISTRATIVE: {
            "label": "Administrativa",
            "description": "Áreas de gestión y administración"
        },
        AreaCategory.CREATIVE: {
            "label": "Creativa",
            "description": "Áreas enfocadas en aspectos creativos y de diseño"
        }
    }
    
    for category in AreaCategory:
        label_info = category_labels.get(category, {
            "label": category.value.title(),
            "description": f"Área de {category.value}"
        })
        
        categories.append({
            "value": category.value,
            "label": label_info["label"],
            "description": label_info["description"]
        })
    
    return {"categories": categories}


@router.get("/academic-unit-categories")
async def get_academic_unit_categories():
    """Get available academic unit categories from enum"""
    categories = []
    
    # Mapping de labels en español para cada categoría
    category_labels = {
        AcademicUnitCategory.ACADEMIC: {
            "label": "Académica",
            "description": "Unidades académicas de enseñanza e investigación"
        },
        AcademicUnitCategory.RESEARCH: {
            "label": "Investigación",
            "description": "Unidades especializadas en investigación"
        },
        AcademicUnitCategory.ADMINISTRATIVE: {
            "label": "Administrativa", 
            "description": "Unidades de gestión y administración"
        },
        AcademicUnitCategory.SERVICE: {
            "label": "Servicio",
            "description": "Unidades de apoyo y servicios"
        }
    }
    
    for category in AcademicUnitCategory:
        label_info = category_labels.get(category, {
            "label": category.value.title(),
            "description": f"Unidad de {category.value}"
        })
        
        categories.append({
            "value": category.value,
            "label": label_info["label"],
            "description": label_info["description"]
        })
    
    return {"categories": categories}


@router.get("/health")
async def organizations_health_check(db: Session = Depends(get_db)):
    """Organizations module health check"""
    try:
        # Test basic database connectivity for organizations tables
        area_stats = await area_controller.get_area_statistics(db)
        unit_stats = await academic_unit_controller.get_academic_unit_statistics(db)
        
        return {
            "status": "healthy",
            "module": "organizations",
            "areas": {
                "total": area_stats.total_areas,
                "active": area_stats.active_areas
            },
            "academic_units": {
                "total": unit_stats.total_units,
                "active": unit_stats.active_units
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Organizations module health check failed: {str(e)}"
        )