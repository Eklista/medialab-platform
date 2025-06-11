# backend/app/modules/organizations/services/__init__.py
"""
Organizations services
"""
from .area_service import area_service
from .academic_unit_service import academic_unit_service, academic_unit_type_service

__all__ = [
    "area_service",
    "academic_unit_service", 
    "academic_unit_type_service"
]