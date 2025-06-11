# backend/app/modules/organizations/controllers/__init__.py
"""
Organizations controllers
"""
from .area_controller import area_controller
from .academic_unit_controller import academic_unit_controller, academic_unit_type_controller

__all__ = [
    "area_controller",
    "academic_unit_controller",
    "academic_unit_type_controller"
]