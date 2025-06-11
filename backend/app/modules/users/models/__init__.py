"""
Users module models - CORREGIDO con orden apropiado de importación
"""

from .user_role import UserRole

from .internal_user import InternalUser
from .institutional_user import InstitutionalUser

from .user_area import UserArea
from .user_academic_unit import UserAcademicUnit

__all__ = [
    "InternalUser",
    "InstitutionalUser",
    "UserRole",
    "UserArea", 
    "UserAcademicUnit"
]