"""
Registro centralizado de modelos SQLAlchemy  
Universidad Galileo – Plataforma MediaLab

Este módulo garantiza la correcta importación y registro de todos los modelos  
utilizados en la plataforma.

📁 Todos los modelos están organizados dentro de `modules/<nombre_del_módulo>/models/
"""



# Base unificado
from app.shared.base.base_model import Base, BaseModelWithID, BaseModelWithUUID, BaseModelHybrid

# Organizations models (sin dependencias)
from app.modules.organizations.models.academic_unit_type import AcademicUnitType
from app.modules.organizations.models.area import Area
from app.modules.organizations.models.academic_unit import AcademicUnit

# Security models (sin dependencias)
from app.modules.security.models.permission import Permission
from app.modules.security.models.role import Role
from app.modules.security.models.role_permission import RolePermission

# Users models (orden específico para evitar dependencias)
from app.modules.users.models.user_role import UserRole
from app.modules.users.models.user_area import UserArea
from app.modules.users.models.user_academic_unit import UserAcademicUnit
from app.modules.users.models.internal_user import InternalUser
from app.modules.users.models.institutional_user import InstitutionalUser

# CMS models (dependen de usuarios y organizaciones)
from app.modules.cms.models.category import Category
from app.modules.cms.models.video import Video
from app.modules.cms.models.gallery import Gallery

# Exportar modelos para uso externo
__all__ = [
    # Base
    "Base",
    "BaseModelWithID", 
    "BaseModelWithUUID",
    "BaseModelHybrid",
    
    # Organizations
    "AcademicUnitType",
    "Area", 
    "AcademicUnit",
    
    # Security
    "Permission",
    "Role",
    "RolePermission",
    
    # Users
    "UserRole",
    "UserArea",
    "UserAcademicUnit", 
    "InternalUser",
    "InstitutionalUser",
    
    # CMS
    "Category",
    "Video",
    "Gallery"
]

def get_all_models():
    """
    Obtener lista de todos los modelos registrados
    """
    return [
        # Organizations
        AcademicUnitType,
        Area,
        AcademicUnit,
        
        # Security  
        Permission,
        Role,
        RolePermission,
        
        # Users
        UserRole,
        UserArea,
        UserAcademicUnit,
        InternalUser,
        InstitutionalUser,
        
        # CMS
        Category,
        Video,
        Gallery
    ]

def get_table_count():
    """
    Obtener número de tablas registradas
    """
    return len(Base.metadata.tables)

def get_registry_info():
    """
    Obtener información del registry para debugging
    """
    return {
        "base_registry_id": id(Base.registry),
        "registered_classes": list(Base.registry._class_registry.keys()),
        "total_tables": len(Base.metadata.tables),
        "table_names": list(Base.metadata.tables.keys())
    }