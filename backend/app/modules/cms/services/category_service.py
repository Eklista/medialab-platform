"""
CMS Category Service - Lógica de negocio para categorías
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.modules.cms.models import Category
from app.modules.cms.repositories.category_repository import CategoryRepository
from app.modules.cms.schemas.category_schemas import (
    CategoryCreate, CategoryUpdate, CategorySearchParams
)
from app.modules.cms.utils.slug_generator import slug_generator
from app.modules.organizations.models import AcademicUnit


class CategoryService:
    """Servicio para lógica de negocio de categorías"""
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def create_category(self, db: Session, category_data: CategoryCreate) -> Category:
        """Crear nueva categoría con validaciones"""
        # Validar que existe la unidad académica
        academic_unit = db.query(AcademicUnit).filter(
            AcademicUnit.id == category_data.academic_unit_id,
            AcademicUnit.is_active == True
        ).first()
        
        if not academic_unit:
            raise ValueError("Unidad académica no encontrada o inactiva")
        
        # Generar slug único
        slug = slug_generator.generate_category_slug(
            category_data.name,
            academic_unit.name,
            db
        )
        
        # Preparar datos
        category_dict = category_data.dict()
        category_dict.update({
            'slug': slug,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        # Crear categoría
        category = self.repository.create(db, category_dict)
        db.commit()
        
        return category
    
    def get_category(self, db: Session, category_id: int) -> Optional[Category]:
        """Obtener categoría por ID"""
        return self.repository.get_by_id(db, category_id)
    
    def get_category_by_slug(self, db: Session, slug: str) -> Optional[Category]:
        """Obtener categoría por slug"""
        return self.repository.get_by_slug(db, slug)
    
    def get_categories(
        self, 
        db: Session, 
        params: CategorySearchParams
    ) -> Dict[str, Any]:
        """Obtener lista paginada de categorías"""
        skip = (params.page - 1) * params.per_page
        
        categories, total = self.repository.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            academic_unit_id=params.academic_unit_id,
            category_type=params.category_type,
            content_type_focus=params.content_type_focus,
            is_active=params.is_active,
            is_featured=params.is_featured,
            is_public=params.is_public,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            minimal=params.minimal
        )
        
        return {
            'categories': categories,
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'pages': (total + params.per_page - 1) // params.per_page,
            'has_next': params.page * params.per_page < total,
            'has_prev': params.page > 1
        }
    
    def update_category(
        self, 
        db: Session, 
        category_id: int, 
        update_data: CategoryUpdate
    ) -> Category:
        """Actualizar categoría"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        
        # Preparar datos de actualización
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        
        # Actualizar slug si cambió el nombre
        if 'name' in update_dict and update_dict['name'] != category.name:
            academic_unit = db.query(AcademicUnit).filter(
                AcademicUnit.id == category.academic_unit_id
            ).first()
            
            if academic_unit:
                new_slug = slug_generator.update_slug_if_needed(
                    category.slug,
                    f"{academic_unit.name}-{update_dict['name']}",
                    db,
                    Category,
                    category_id
                )
                update_dict['slug'] = new_slug
        
        # Actualizar timestamp
        update_dict['updated_at'] = datetime.utcnow()
        
        # Aplicar actualización
        updated_category = self.repository.update(db, category, update_dict)
        db.commit()
        
        return updated_category
    
    def delete_category(self, db: Session, category_id: int) -> bool:
        """Eliminar categoría con validaciones"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        
        # Verificar si tiene contenido
        if self.repository.has_content(db, category_id):
            raise ValueError("No se puede eliminar una categoría con contenido asociado")
        
        # Eliminar categoría
        success = self.repository.delete(db, category)
        if success:
            db.commit()
        
        return success
    
    def get_categories_by_academic_unit(
        self, 
        db: Session, 
        academic_unit_id: int,
        is_active: bool = True,
        is_public: bool = True
    ) -> List[Category]:
        """Obtener categorías de una unidad académica"""
        return self.repository.get_by_academic_unit(
            db, academic_unit_id, is_active, is_public
        )
    
    def get_featured_categories(self, db: Session, limit: int = 10) -> List[Category]:
        """Obtener categorías destacadas"""
        return self.repository.get_featured(db, limit)
    
    def get_popular_categories(self, db: Session, limit: int = 10) -> List[Category]:
        """Obtener categorías populares"""
        return self.repository.get_popular(db, limit)
    
    def update_content_statistics(self, db: Session, category_id: int):
        """Actualizar estadísticas de contenido"""
        self.repository.update_content_statistics(db, category_id)
        db.commit()
    
    def reorder_categories(
        self, 
        db: Session, 
        academic_unit_id: int, 
        category_orders: List[Dict[str, int]]
    ):
        """Reordenar categorías de una unidad académica"""
        # Validar que todas las categorías pertenecen a la unidad académica
        category_ids = [item['id'] for item in category_orders]
        categories = db.query(Category).filter(
            Category.id.in_(category_ids),
            Category.academic_unit_id == academic_unit_id
        ).all()
        
        if len(categories) != len(category_ids):
            raise ValueError("Algunas categorías no pertenecen a la unidad académica especificada")
        
        # Aplicar reordenamiento
        self.repository.reorder_categories(db, academic_unit_id, category_orders)
        db.commit()
    
    def toggle_featured(self, db: Session, category_id: int) -> Category:
        """Alternar estado destacado de categoría"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        
        update_data = {
            'is_featured': not category.is_featured,
            'updated_at': datetime.utcnow()
        }
        
        updated_category = self.repository.update(db, category, update_data)
        db.commit()
        
        return updated_category
    
    def toggle_active(self, db: Session, category_id: int) -> Category:
        """Alternar estado activo de categoría"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        
        update_data = {
            'is_active': not category.is_active,
            'updated_at': datetime.utcnow()
        }
        
        updated_category = self.repository.update(db, category, update_data)
        db.commit()
        
        return updated_category
    
    def get_categories_for_select(
        self, 
        db: Session, 
        academic_unit_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtener categorías para dropdowns/selects"""
        return self.repository.get_categories_for_select(db, academic_unit_id)
    
    def validate_category_access(
        self, 
        db: Session, 
        category_id: int, 
        user_academic_units: List[int]
    ) -> bool:
        """Validar si un usuario tiene acceso a una categoría"""
        category = self.repository.get_by_id(db, category_id, include_relations=False)
        if not category:
            return False
        
        # Verificar si la unidad académica está en la lista del usuario
        return category.academic_unit_id in user_academic_units
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de categorías"""
        return self.repository.get_statistics(db)
    
    def search_categories(
        self, 
        db: Session, 
        query: str, 
        academic_unit_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Category]:
        """Búsqueda simple de categorías"""
        categories, _ = self.repository.get_all(
            db=db,
            skip=0,
            limit=limit,
            search=query,
            academic_unit_id=academic_unit_id,
            is_active=True,
            is_public=True,
            minimal=True
        )
        
        return categories
    
    def duplicate_category(
        self, 
        db: Session, 
        category_id: int, 
        new_name: str,
        target_academic_unit_id: Optional[int] = None
    ) -> Category:
        """Duplicar categoría"""
        original = self.repository.get_by_id(db, category_id)
        if not original:
            raise ValueError("Categoría original no encontrada")
        
        # Determinar unidad académica de destino
        academic_unit_id = target_academic_unit_id or original.academic_unit_id
        academic_unit = db.query(AcademicUnit).filter(
            AcademicUnit.id == academic_unit_id,
            AcademicUnit.is_active == True
        ).first()
        
        if not academic_unit:
            raise ValueError("Unidad académica de destino no encontrada")
        
        # Generar slug único
        slug = slug_generator.generate_category_slug(
            new_name,
            academic_unit.name,
            db
        )
        
        # Crear datos de la nueva categoría
        new_data = {
            'name': new_name,
            'display_name': f"{new_name} (Copia)",
            'description': original.description,
            'academic_unit_id': academic_unit_id,
            'category_type': original.category_type,
            'content_type_focus': original.content_type_focus,
            'color': original.color,
            'icon': original.icon,
            'is_featured': False,  # No destacar duplicados
            'is_public': original.is_public,
            'sort_order': original.sort_order,
            'auto_approve_content': original.auto_approve_content,
            'requires_review': original.requires_review,
            'slug': slug,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Crear nueva categoría
        new_category = self.repository.create(db, new_data)
        db.commit()
        
        return new_category
    
    def bulk_update_status(
        self, 
        db: Session, 
        category_ids: List[int], 
        is_active: bool
    ) -> int:
        """Actualización masiva de estado activo"""
        # Validar que todas las categorías existen
        existing_categories = db.query(Category).filter(
            Category.id.in_(category_ids)
        ).count()
        
        if existing_categories != len(category_ids):
            raise ValueError("Algunas categorías no existen")
        
        # Actualizar
        updated = db.query(Category).filter(
            Category.id.in_(category_ids)
        ).update({
            'is_active': is_active,
            'updated_at': datetime.utcnow()
        }, synchronize_session=False)
        
        db.commit()
        return updated


# Instancia global del servicio
category_service = CategoryService()