"""
CMS Category Repository - Acceso a datos optimizado para categorías
"""
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from sqlalchemy import or_, and_, func, desc, asc, exists

from app.modules.cms.models import Category
from app.modules.organizations.models import AcademicUnit


class CategoryRepository:
    """Repository para operaciones de categorías con optimizaciones"""
    
    @staticmethod
    def create(db: Session, category_data: Dict[str, Any]) -> Category:
        """Crear nueva categoría"""
        category = Category(**category_data)
        db.add(category)
        db.flush()
        return category
    
    @staticmethod
    def get_by_id(db: Session, category_id: int, include_relations: bool = True) -> Optional[Category]:
        """Obtener categoría por ID con carga optimizada"""
        query = db.query(Category)
        
        if include_relations:
            query = query.options(
                joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                )
            )
        
        return query.filter(Category.id == category_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str, include_relations: bool = True) -> Optional[Category]:
        """Obtener categoría por slug"""
        query = db.query(Category)
        
        if include_relations:
            query = query.options(
                joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                )
            )
        
        return query.filter(Category.slug == slug).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        academic_unit_id: Optional[int] = None,
        category_type: Optional[str] = None,
        content_type_focus: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        is_public: Optional[bool] = None,
        sort_by: str = "sort_order",
        sort_order: str = "asc",
        minimal: bool = False
    ) -> Tuple[List[Category], int]:
        """Obtener lista paginada de categorías con filtros"""
        
        if minimal:
            # Para listings, solo campos esenciales
            query = db.query(Category).options(
                load_only(
                    Category.id,
                    Category.name,
                    Category.display_name,
                    Category.slug,
                    Category.color,
                    Category.icon,
                    Category.is_active,
                    Category.is_featured,
                    Category.is_public,
                    Category.sort_order,
                    Category.academic_unit_id,
                    Category.total_videos,
                    Category.total_galleries,
                    Category.created_at
                )
            )
        else:
            # Para detalles, incluir relaciones
            query = db.query(Category).options(
                joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation, AcademicUnit.color
                )
            )
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Category.name.ilike(f"%{search}%"),
                Category.display_name.ilike(f"%{search}%"),
                Category.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if academic_unit_id:
            query = query.filter(Category.academic_unit_id == academic_unit_id)
        
        if category_type:
            query = query.filter(Category.category_type == category_type)
        
        if content_type_focus:
            query = query.filter(Category.content_type_focus == content_type_focus)
        
        if is_active is not None:
            query = query.filter(Category.is_active == is_active)
        
        if is_featured is not None:
            query = query.filter(Category.is_featured == is_featured)
        
        if is_public is not None:
            query = query.filter(Category.is_public == is_public)
        
        # Contar total antes de paginación
        total = query.count()
        
        # Aplicar ordenamiento
        if sort_by == "sort_order":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Category.sort_order), Category.name)
        elif sort_by == "name":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Category.name))
        elif sort_by == "created_at":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Category.created_at))
        elif sort_by == "total_content":
            # Ordenar por total de contenido (videos + galerías)
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Category.total_videos + Category.total_galleries))
        else:
            # Orden por defecto
            query = query.order_by(Category.sort_order, Category.name)
        
        # Aplicar paginación
        categories = query.offset(skip).limit(limit).all()
        
        return categories, total
    
    @staticmethod
    def get_by_academic_unit(
        db: Session, 
        academic_unit_id: int, 
        is_active: bool = True,
        is_public: bool = True
    ) -> List[Category]:
        """Obtener categorías de una unidad académica específica"""
        query = db.query(Category).filter(Category.academic_unit_id == academic_unit_id)
        
        if is_active:
            query = query.filter(Category.is_active == True)
        
        if is_public:
            query = query.filter(Category.is_public == True)
        
        return query.order_by(Category.sort_order, Category.name).all()
    
    @staticmethod
    def get_featured(db: Session, limit: int = 10) -> List[Category]:
        """Obtener categorías destacadas"""
        return (
            db.query(Category)
            .options(
                joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                )
            )
            .filter(
                Category.is_featured == True,
                Category.is_active == True,
                Category.is_public == True
            )
            .order_by(Category.sort_order, Category.name)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular(db: Session, limit: int = 10) -> List[Category]:
        """Obtener categorías más populares por contenido"""
        return (
            db.query(Category)
            .options(
                joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                )
            )
            .filter(
                Category.is_active == True,
                Category.is_public == True
            )
            .order_by(desc(Category.total_videos + Category.total_galleries))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def update(db: Session, category: Category, update_data: Dict[str, Any]) -> Category:
        """Actualizar categoría"""
        for field, value in update_data.items():
            if hasattr(category, field) and value is not None:
                setattr(category, field, value)
        
        db.flush()
        return category
    
    @staticmethod
    def delete(db: Session, category: Category) -> bool:
        """Eliminar categoría (verificar dependencias primero)"""
        # Verificar si tiene contenido asociado
        has_content = CategoryRepository.has_content(db, category.id)
        
        if has_content:
            return False  # No eliminar si tiene contenido
        
        db.delete(category)
        db.flush()
        return True
    
    @staticmethod
    def has_content(db: Session, category_id: int) -> bool:
        """Verificar si la categoría tiene contenido asociado"""
        # Importar aquí para evitar importación circular
        from app.modules.cms.models import Video, Gallery
        
        has_videos = db.query(exists().where(Video.category_id == category_id)).scalar()
        has_galleries = db.query(exists().where(Gallery.category_id == category_id)).scalar()
        
        return has_videos or has_galleries
    
    @staticmethod
    def update_content_statistics(db: Session, category_id: int):
        """Actualizar estadísticas de contenido de la categoría"""
        from app.modules.cms.models import Video, Gallery
        
        # Contar videos
        video_count = (
            db.query(func.count(Video.id))
            .filter(Video.category_id == category_id, Video.is_published == True)
            .scalar() or 0
        )
        
        # Contar galerías
        gallery_count = (
            db.query(func.count(Gallery.id))
            .filter(Gallery.category_id == category_id, Gallery.is_published == True)
            .scalar() or 0
        )
        
        # Sumar vistas totales
        total_video_views = (
            db.query(func.sum(Video.view_count))
            .filter(Video.category_id == category_id, Video.is_published == True)
            .scalar() or 0
        )
        
        total_gallery_views = (
            db.query(func.sum(Gallery.view_count))
            .filter(Gallery.category_id == category_id, Gallery.is_published == True)
            .scalar() or 0
        )
        
        # Actualizar categoría
        db.query(Category).filter(Category.id == category_id).update({
            "total_videos": video_count,
            "total_galleries": gallery_count,
            "total_views": total_video_views + total_gallery_views
        })
        
        db.flush()
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas generales de categorías"""
        stats = {}
        
        # Total de categorías
        stats['total_categories'] = db.query(Category).count()
        stats['active_categories'] = db.query(Category).filter(Category.is_active == True).count()
        stats['featured_categories'] = db.query(Category).filter(Category.is_featured == True).count()
        
        # Por unidad académica
        unit_stats = (
            db.query(
                AcademicUnit.name,
                func.count(Category.id).label('category_count')
            )
            .join(Category, AcademicUnit.id == Category.academic_unit_id)
            .filter(Category.is_active == True)
            .group_by(AcademicUnit.id, AcademicUnit.name)
            .all()
        )
        stats['by_academic_unit'] = {unit.name: unit.category_count for unit in unit_stats}
        
        # Por tipo
        type_stats = (
            db.query(
                Category.category_type,
                func.count(Category.id).label('count')
            )
            .filter(Category.is_active == True)
            .group_by(Category.category_type)
            .all()
        )
        stats['by_type'] = {stat.category_type: stat.count for stat in type_stats}
        
        # Por enfoque de contenido
        focus_stats = (
            db.query(
                Category.content_type_focus,
                func.count(Category.id).label('count')
            )
            .filter(Category.is_active == True)
            .group_by(Category.content_type_focus)
            .all()
        )
        stats['by_content_focus'] = {stat.content_type_focus: stat.count for stat in focus_stats}
        
        # Distribución de contenido
        content_stats = (
            db.query(
                func.sum(Category.total_videos).label('total_videos'),
                func.sum(Category.total_galleries).label('total_galleries'),
                func.sum(Category.total_views).label('total_views')
            )
            .filter(Category.is_active == True)
            .first()
        )
        
        stats['content_distribution'] = {
            'total_videos': content_stats.total_videos or 0,
            'total_galleries': content_stats.total_galleries or 0,
            'total_views': content_stats.total_views or 0
        }
        
        return stats
    
    @staticmethod
    def reorder_categories(db: Session, academic_unit_id: int, category_orders: List[Dict[str, int]]):
        """Reordenar categorías de una unidad académica"""
        for item in category_orders:
            category_id = item.get('id')
            sort_order = item.get('sort_order')
            
            if category_id and sort_order is not None:
                db.query(Category).filter(
                    Category.id == category_id,
                    Category.academic_unit_id == academic_unit_id
                ).update({'sort_order': sort_order})
        
        db.flush()
    
    @staticmethod
    def get_categories_for_select(db: Session, academic_unit_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener categorías para dropdowns/selects"""
        query = db.query(Category).options(
            load_only(
                Category.id,
                Category.name,
                Category.display_name,
                Category.slug,
                Category.color,
                Category.icon,
                Category.academic_unit_id
            )
        ).filter(
            Category.is_active == True,
            Category.is_public == True
        )
        
        if academic_unit_id:
            query = query.filter(Category.academic_unit_id == academic_unit_id)
        
        categories = query.order_by(Category.sort_order, Category.name).all()
        
        return [
            {
                'id': cat.id,
                'name': cat.name,
                'display_name': cat.display_name or cat.name,
                'slug': cat.slug,
                'color': cat.color,
                'icon': cat.icon,
                'academic_unit_id': cat.academic_unit_id
            }
            for cat in categories
        ]