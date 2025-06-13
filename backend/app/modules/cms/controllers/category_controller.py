"""
CMS Category Controller - Orquestación de endpoints para categorías
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.cms.schemas.category_schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse, CategoryMinimal,
    CategorySearchParams, CategoryListResponse, CategoryStatsResponse
)
from app.modules.cms.services.category_service import category_service


class CategoryController:
    """Controller para operaciones de categorías"""
    
    def __init__(self):
        self.service = category_service
    
    async def create_category(
        self, 
        category_data: CategoryCreate, 
        db: Session
    ) -> CategoryResponse:
        """Crear nueva categoría"""
        try:
            category = self.service.create_category(db, category_data)
            return self._build_category_response(category)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creando categoría: {str(e)}"
            )
    
    async def get_category(self, category_id: int, db: Session) -> CategoryResponse:
        """Obtener categoría por ID"""
        category = self.service.get_category(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        return self._build_category_response(category)
    
    async def get_category_by_slug(self, slug: str, db: Session) -> CategoryResponse:
        """Obtener categoría por slug"""
        category = self.service.get_category_by_slug(db, slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        return self._build_category_response(category)
    
    async def get_categories(
        self, 
        params: CategorySearchParams, 
        db: Session
    ) -> CategoryListResponse:
        """Obtener lista paginada de categorías"""
        try:
            result = self.service.get_categories(db, params)
            
            categories = [
                self._build_category_response(cat, minimal=params.minimal) 
                for cat in result['categories']
            ]
            
            return CategoryListResponse(
                categories=categories,
                total=result['total'],
                page=result['page'],
                per_page=result['per_page'],
                pages=result['pages'],
                has_next=result['has_next'],
                has_prev=result['has_prev']
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo categorías: {str(e)}"
            )
    
    async def update_category(
        self, 
        category_id: int, 
        update_data: CategoryUpdate, 
        db: Session
    ) -> CategoryResponse:
        """Actualizar categoría"""
        try:
            category = self.service.update_category(db, category_id, update_data)
            return self._build_category_response(category)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error actualizando categoría: {str(e)}"
            )
    
    async def delete_category(self, category_id: int, db: Session) -> Dict[str, str]:
        """Eliminar categoría"""
        try:
            success = self.service.delete_category(db, category_id)
            if success:
                return {"message": "Categoría eliminada exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo eliminar la categoría"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error eliminando categoría: {str(e)}"
            )
    
    async def get_categories_by_academic_unit(
        self, 
        academic_unit_id: int, 
        is_active: bool, 
        is_public: bool, 
        db: Session
    ) -> List[CategoryMinimal]:
        """Obtener categorías de una unidad académica"""
        categories = self.service.get_categories_by_academic_unit(
            db, academic_unit_id, is_active, is_public
        )
        
        return [self._build_minimal_response(cat) for cat in categories]
    
    async def get_featured_categories(
        self, 
        limit: int, 
        db: Session
    ) -> List[CategoryResponse]:
        """Obtener categorías destacadas"""
        categories = self.service.get_featured_categories(db, limit)
        return [self._build_category_response(cat) for cat in categories]
    
    async def get_popular_categories(
        self, 
        limit: int, 
        db: Session
    ) -> List[CategoryResponse]:
        """Obtener categorías populares"""
        categories = self.service.get_popular_categories(db, limit)
        return [self._build_category_response(cat) for cat in categories]
    
    async def toggle_featured(
        self, 
        category_id: int, 
        db: Session
    ) -> CategoryResponse:
        """Alternar estado destacado"""
        try:
            category = self.service.toggle_featured(db, category_id)
            return self._build_category_response(category)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error cambiando estado destacado: {str(e)}"
            )
    
    async def toggle_active(
        self, 
        category_id: int, 
        db: Session
    ) -> CategoryResponse:
        """Alternar estado activo"""
        try:
            category = self.service.toggle_active(db, category_id)
            return self._build_category_response(category)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error cambiando estado activo: {str(e)}"
            )
    
    async def reorder_categories(
        self, 
        academic_unit_id: int, 
        category_orders: List[Dict[str, int]], 
        db: Session
    ) -> Dict[str, str]:
        """Reordenar categorías"""
        try:
            self.service.reorder_categories(db, academic_unit_id, category_orders)
            return {"message": "Categorías reordenadas exitosamente"}
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reordenando categorías: {str(e)}"
            )
    
    async def get_categories_for_select(
        self, 
        academic_unit_id: int, 
        db: Session
    ) -> List[Dict[str, Any]]:
        """Obtener categorías para dropdowns"""
        return self.service.get_categories_for_select(db, academic_unit_id)
    
    async def search_categories(
        self, 
        query: str, 
        academic_unit_id: int, 
        limit: int, 
        db: Session
    ) -> List[CategoryMinimal]:
        """Búsqueda de categorías"""
        categories = self.service.search_categories(db, query, academic_unit_id, limit)
        return [self._build_minimal_response(cat) for cat in categories]
    
    async def get_statistics(self, db: Session) -> CategoryStatsResponse:
        """Obtener estadísticas de categorías"""
        try:
            stats = self.service.get_statistics(db)
            return CategoryStatsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo estadísticas: {str(e)}"
            )
    
    async def duplicate_category(
        self, 
        category_id: int, 
        new_name: str, 
        target_academic_unit_id: int, 
        db: Session
    ) -> CategoryResponse:
        """Duplicar categoría"""
        try:
            category = self.service.duplicate_category(
                db, category_id, new_name, target_academic_unit_id
            )
            return self._build_category_response(category)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error duplicando categoría: {str(e)}"
            )
    
    async def bulk_update_status(
        self, 
        category_ids: List[int], 
        is_active: bool, 
        db: Session
    ) -> Dict[str, Any]:
        """Actualización masiva de estado"""
        try:
            updated = self.service.bulk_update_status(db, category_ids, is_active)
            return {
                "message": f"{updated} categorías actualizadas",
                "updated_count": updated
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en actualización masiva: {str(e)}"
            )
    
    def _build_category_response(self, category, minimal: bool = False) -> CategoryResponse:
        """Construir respuesta de categoría"""
        response_data = {
            'id': category.id,
            'name': category.name,
            'display_name': category.display_name,
            'description': category.description,
            'slug': category.slug,
            'academic_unit_id': category.academic_unit_id,
            'category_type': category.category_type,
            'content_type_focus': category.content_type_focus,
            'color': category.color,
            'icon': category.icon,
            'cover_image': category.cover_image,
            'is_active': category.is_active,
            'is_featured': category.is_featured,
            'is_public': category.is_public,
            'sort_order': category.sort_order,
            'auto_approve_content': category.auto_approve_content,
            'requires_review': category.requires_review,
            'total_videos': category.total_videos,
            'total_galleries': category.total_galleries,
            'total_views': category.total_views,
            'created_at': category.created_at,
            'updated_at': category.updated_at
        }
        
        # Agregar datos de unidad académica si están disponibles
        if hasattr(category, 'academic_unit') and category.academic_unit and not minimal:
            response_data['academic_unit'] = {
                'id': category.academic_unit.id,
                'name': category.academic_unit.name,
                'abbreviation': category.academic_unit.abbreviation,
                'color': getattr(category.academic_unit, 'color', None)
            }
        
        return CategoryResponse(**response_data)
    
    def _build_minimal_response(self, category) -> CategoryMinimal:
        """Construir respuesta mínima de categoría"""
        return CategoryMinimal(
            id=category.id,
            name=category.name,
            display_name=category.display_name,
            slug=category.slug,
            color=category.color,
            icon=category.icon,
            is_active=category.is_active
        )


# Instancia global del controlador
category_controller = CategoryController()