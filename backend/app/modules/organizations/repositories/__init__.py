# backend/app/modules/organizations/repositories/__init__.py
"""
Organizations repositories
"""
from .area_repository import AreaRepository
from .academic_unit_repository import AcademicUnitTypeRepository, AcademicUnitRepository

__all__ = [
    "AreaRepository",
    "AcademicUnitTypeRepository",
    "AcademicUnitRepository"
]