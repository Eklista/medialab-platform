# backend/app/modules/organizations/schemas/__init__.py
"""
Organizations schemas
"""
from .area_schemas import *
from .academic_unit_schemas import *

__all__ = [
    # Area schemas
    "AreaCategory",
    "AreaCreate",
    "AreaUpdate", 
    "AreaResponse",
    "AreaListResponse",
    "AreaSearchParams",
    "AreaMemberAssign",
    "AreaMemberRemove",
    "AreaStatistics",
    
    # Academic Unit Type schemas
    "AcademicUnitCategory",
    "AcademicUnitTypeCreate",
    "AcademicUnitTypeUpdate",
    "AcademicUnitTypeResponse",
    "AcademicUnitTypeListResponse",
    
    # Academic Unit schemas
    "AcademicUnitCreate",
    "AcademicUnitUpdate",
    "AcademicUnitResponse",
    "AcademicUnitListResponse",
    "AcademicUnitSearchParams",
    "AcademicUnitMemberAssign",
    "AcademicUnitMemberRemove",
    "AcademicUnitStatistics"
]