"""
CMS Gallery Repository - Acceso a datos optimizado para galerías
"""
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from sqlalchemy import or_, and_, func, desc, asc, text

from app.modules.cms.models import Gallery, Category
from app.modules.users.models import InternalUser
from app.modules.organizations.models import AcademicUnit


class GalleryRepository:
    """Repository para operaciones de galerías con optimizaciones"""
    
    @staticmethod
    def create(db: Session, gallery_data: Dict[str, Any]) -> Gallery:
        """Crear nueva galería"""
        gallery = Gallery(**gallery_data)
        db.add(gallery)
        db.flush()
        return gallery
    
    @staticmethod
    def get_by_id(db: Session, gallery_id: int, include_relations: bool = True) -> Optional[Gallery]:
        """Obtener galería por ID con carga optimizada"""
        query = db.query(Gallery)
        
        if include_relations:
            query = query.options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug, Category.color
                ).joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name, 
                    InternalUser.profile_photo, InternalUser.position
                )
            )
        
        return query.filter(Gallery.id == gallery_id).first()
    
    @staticmethod
    def get_by_uuid(db: Session, uuid: str, include_relations: bool = True) -> Optional[Gallery]:
        """Obtener galería por UUID"""
        query = db.query(Gallery)
        
        if include_relations:
            query = query.options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug, Category.color
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name, 
                    InternalUser.profile_photo
                )
            )
        
        return query.filter(Gallery.uuid == uuid).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str, include_relations: bool = True) -> Optional[Gallery]:
        """Obtener galería por slug"""
        query = db.query(Gallery)
        
        if include_relations:
            query = query.options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
        
        return query.filter(Gallery.slug == slug).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        author_id: Optional[int] = None,
        content_type: Optional[str] = None,
        status: Optional[str] = None,
        is_published: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        is_public: Optional[bool] = None,
        event_date_from: Optional[date] = None,
        event_date_to: Optional[date] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        min_photos: Optional[int] = None,
        max_photos: Optional[int] = None,
        photographer: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        minimal: bool = False,
        include_photos: bool = False,
        include_author: bool = True,
        include_category: bool = True,
        photos_limit: int = 10
    ) -> Tuple[List[Gallery], int]:
        """Obtener lista paginada de galerías con filtros avanzados"""
        
        if minimal:
            # Para listings, solo campos esenciales
            query = db.query(Gallery).options(
                load_only(
                    Gallery.id,
                    Gallery.uuid,
                    Gallery.title,
                    Gallery.slug,
                    Gallery.thumbnail_url,
                    Gallery.cover_photo,
                    Gallery.photo_count,
                    Gallery.is_published,
                    Gallery.is_featured,
                    Gallery.view_count,
                    Gallery.event_date,
                    Gallery.category_id,
                    Gallery.author_id,
                    Gallery.created_at
                )
            )
        else:
            # Para detalles, incluir relaciones selectivas
            options = []
            
            if include_category:
                options.append(
                    joinedload(Gallery.category).load_only(
                        Category.id, Category.name, Category.display_name, 
                        Category.slug, Category.color, Category.academic_unit_id
                    ).joinedload(Category.academic_unit).load_only(
                        AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                    )
                )
            
            if include_author:
                options.append(
                    joinedload(Gallery.author).load_only(
                        InternalUser.id, InternalUser.first_name, InternalUser.last_name,
                        InternalUser.profile_photo, InternalUser.position
                    )
                )
            
            if options:
                query = db.query(Gallery).options(*options)
            else:
                query = db.query(Gallery)
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Gallery.title.ilike(f"%{search}%"),
                Gallery.subtitle.ilike(f"%{search}%"),
                Gallery.description.ilike(f"%{search}%"),
                Gallery.tags.ilike(f"%{search}%"),
                Gallery.photographer.ilike(f"%{search}%"),
                Gallery.location.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category_id:
            query = query.filter(Gallery.category_id == category_id)
        
        if author_id:
            query = query.filter(Gallery.author_id == author_id)
        
        if content_type:
            query = query.filter(Gallery.content_type == content_type)
        
        if status:
            query = query.filter(Gallery.status == status)
        
        if is_published is not None:
            query = query.filter(Gallery.is_published == is_published)
        
        if is_featured is not None:
            query = query.filter(Gallery.is_featured == is_featured)
        
        if is_public is not None:
            query = query.filter(Gallery.is_public == is_public)
        
        # Filtros de fecha
        if event_date_from:
            query = query.filter(Gallery.event_date >= event_date_from)
        
        if event_date_to:
            query = query.filter(Gallery.event_date <= event_date_to)
        
        if created_from:
            query = query.filter(Gallery.created_at >= created_from)
        
        if created_to:
            query = query.filter(Gallery.created_at <= created_to)
        
        # Filtros de fotos
        if min_photos:
            query = query.filter(Gallery.photo_count >= min_photos)
        
        if max_photos:
            query = query.filter(Gallery.photo_count <= max_photos)
        
        if photographer:
            query = query.filter(Gallery.photographer.ilike(f"%{photographer}%"))
        
        # Contar total
        total = query.count()
        
        # Aplicar ordenamiento
        if sort_by == "created_at":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Gallery.created_at))
        elif sort_by == "event_date":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Gallery.event_date))
        elif sort_by == "title":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Gallery.title))
        elif sort_by == "view_count":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Gallery.view_count))
        elif sort_by == "photo_count":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Gallery.photo_count))
        elif sort_by == "photographer":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Gallery.photographer))
        else:
            # Orden por defecto
            query = query.order_by(desc(Gallery.created_at))
        
        # Aplicar paginación
        galleries = query.offset(skip).limit(limit).all()
        
        return galleries, total
    
    @staticmethod
    def get_by_category(
        db: Session, 
        category_id: int, 
        is_published: bool = True,
        limit: int = 20
    ) -> List[Gallery]:
        """Obtener galerías de una categoría específica"""
        query = db.query(Gallery).options(
            joinedload(Gallery.author).load_only(
                InternalUser.id, InternalUser.first_name, InternalUser.last_name
            )
        ).filter(Gallery.category_id == category_id)
        
        if is_published:
            query = query.filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
        
        return query.order_by(desc(Gallery.event_date)).limit(limit).all()
    
    @staticmethod
    def get_featured(db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías destacadas"""
        return (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Gallery.is_featured == True,
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .order_by(desc(Gallery.event_date))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_recent(db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías más recientes"""
        return (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .order_by(desc(Gallery.created_at))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular(db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías más populares por vistas"""
        return (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .order_by(desc(Gallery.view_count))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_by_academic_unit(
        db: Session, 
        academic_unit_id: int, 
        limit: int = 20,
        is_published: bool = True
    ) -> List[Gallery]:
        """Obtener galerías de una unidad académica"""
        query = (
            db.query(Gallery)
            .join(Category, Gallery.category_id == Category.id)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(Category.academic_unit_id == academic_unit_id)
        )
        
        if is_published:
            query = query.filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
        
        return query.order_by(desc(Gallery.event_date)).limit(limit).all()
    
    @staticmethod
    def get_by_photographer(
        db: Session, 
        photographer: str, 
        limit: int = 20,
        is_published: bool = True
    ) -> List[Gallery]:
        """Obtener galerías de un fotógrafo específico"""
        query = (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(Gallery.photographer.ilike(f"%{photographer}%"))
        )
        
        if is_published:
            query = query.filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
        
        return query.order_by(desc(Gallery.event_date)).limit(limit).all()
    
    @staticmethod
    def update(db: Session, gallery: Gallery, update_data: Dict[str, Any]) -> Gallery:
        """Actualizar galería"""
        for field, value in update_data.items():
            if hasattr(gallery, field) and value is not None:
                setattr(gallery, field, value)
        
        db.flush()
        return gallery
    
    @staticmethod
    def delete(db: Session, gallery: Gallery) -> bool:
        """Eliminar galería"""
        db.delete(gallery)
        db.flush()
        return True
    
    @staticmethod
    def update_photo_count(db: Session, gallery_id: int):
        """Actualizar contador de fotos"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery and gallery.photos:
            photo_count = len(gallery.photos)
            gallery.photo_count = photo_count
            db.flush()
    
    @staticmethod
    def add_photos(db: Session, gallery_id: int, photos_data: List[Dict[str, Any]]):
        """Agregar fotos a una galería"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery:
            current_photos = gallery.photos or []
            current_photos.extend(photos_data)
            gallery.photos = current_photos
            gallery.photo_count = len(current_photos)
            
            # Calcular tamaño total
            total_size = sum(photo.get('file_size', 0) for photo in current_photos)
            gallery.total_size_mb = total_size // (1024 * 1024)  # Convertir a MB
            
            db.flush()
    
    @staticmethod
    def remove_photo(db: Session, gallery_id: int, photo_filename: str):
        """Remover foto de una galería"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery and gallery.photos:
            gallery.photos = [
                photo for photo in gallery.photos 
                if photo.get('filename') != photo_filename
            ]
            gallery.photo_count = len(gallery.photos)
            
            # Recalcular tamaño total
            total_size = sum(photo.get('file_size', 0) for photo in gallery.photos)
            gallery.total_size_mb = total_size // (1024 * 1024)
            
            db.flush()
    
    @staticmethod
    def reorder_photos(db: Session, gallery_id: int, photo_orders: List[Dict[str, int]]):
        """Reordenar fotos en una galería"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery and gallery.photos:
            # Crear diccionario de órdenes
            order_map = {item['filename']: item['sort_order'] for item in photo_orders}
            
            # Actualizar sort_order de cada foto
            for photo in gallery.photos:
                if photo['filename'] in order_map:
                    photo['sort_order'] = order_map[photo['filename']]
            
            # Ordenar fotos por sort_order
            gallery.photos.sort(key=lambda x: x.get('sort_order', 0))
            
            db.flush()
    
    @staticmethod
    def update_photo_metadata(db: Session, gallery_id: int, photo_filename: str, metadata: Dict[str, Any]):
        """Actualizar metadata de una foto específica"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery and gallery.photos:
            for photo in gallery.photos:
                if photo['filename'] == photo_filename:
                    photo.update(metadata)
                    break
            db.flush()
    
    @staticmethod
    def set_cover_photo(db: Session, gallery_id: int, photo_filename: str):
        """Establecer foto de portada"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery:
            # Buscar la foto en la galería
            for photo in gallery.photos or []:
                if photo['filename'] == photo_filename:
                    gallery.cover_photo = photo['processed_path']
                    gallery.thumbnail_url = photo['thumbnail_path']
                    break
            db.flush()
    
    @staticmethod
    def increment_view_count(db: Session, gallery_id: int):
        """Incrementar contador de vistas"""
        db.query(Gallery).filter(Gallery.id == gallery_id).update({
            "view_count": Gallery.view_count + 1
        })
        db.flush()
    
    @staticmethod
    def increment_like_count(db: Session, gallery_id: int):
        """Incrementar contador de likes"""
        db.query(Gallery).filter(Gallery.id == gallery_id).update({
            "like_count": Gallery.like_count + 1
        })
        db.flush()
    
    @staticmethod
    def increment_share_count(db: Session, gallery_id: int):
        """Incrementar contador de shares"""
        db.query(Gallery).filter(Gallery.id == gallery_id).update({
            "share_count": Gallery.share_count + 1
        })
        db.flush()
    
    @staticmethod
    def increment_download_count(db: Session, gallery_id: int):
        """Incrementar contador de descargas"""
        db.query(Gallery).filter(Gallery.id == gallery_id).update({
            "download_count": Gallery.download_count + 1
        })
        db.flush()
    
    @staticmethod
    def search_by_tags(db: Session, tags: List[str], limit: int = 20) -> List[Gallery]:
        """Buscar galerías por tags"""
        filters = []
        for tag in tags:
            filters.append(Gallery.tags.ilike(f"%{tag}%"))
        
        return (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                or_(*filters),
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .order_by(desc(Gallery.view_count))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_related(db: Session, gallery: Gallery, limit: int = 5) -> List[Gallery]:
        """Obtener galerías relacionadas"""
        # Galerías de la misma categoría, excluyendo la actual
        related = (
            db.query(Gallery)
            .options(
                joinedload(Gallery.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Gallery.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Gallery.category_id == gallery.category_id,
                Gallery.id != gallery.id,
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .order_by(desc(Gallery.view_count))
            .limit(limit)
            .all()
        )
        
        # Si no hay suficientes, agregar galerías del mismo tipo de contenido
        if len(related) < limit:
            additional = (
                db.query(Gallery)
                .options(
                    joinedload(Gallery.category).load_only(
                        Category.id, Category.name, Category.display_name, Category.slug
                    ),
                    joinedload(Gallery.author).load_only(
                        InternalUser.id, InternalUser.first_name, InternalUser.last_name
                    )
                )
                .filter(
                    Gallery.content_type == gallery.content_type,
                    Gallery.id != gallery.id,
                    Gallery.is_published == True,
                    Gallery.is_public == True,
                    Gallery.id.notin_([g.id for g in related])
                )
                .order_by(desc(Gallery.view_count))
                .limit(limit - len(related))
                .all()
            )
            related.extend(additional)
        
        return related
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de galerías"""
        stats = {}
        
        # Estadísticas básicas
        stats['total_galleries'] = db.query(Gallery).count()
        stats['published_galleries'] = db.query(Gallery).filter(Gallery.is_published == True).count()
        stats['draft_galleries'] = db.query(Gallery).filter(Gallery.status == 'draft').count()
        
        # Estadísticas de contenido
        content_stats = (
            db.query(
                func.sum(Gallery.photo_count).label('total_photos'),
                func.sum(Gallery.view_count).label('total_views'),
                func.sum(Gallery.like_count).label('total_likes'),
                func.sum(Gallery.share_count).label('total_shares'),
                func.sum(Gallery.download_count).label('total_downloads'),
                func.sum(Gallery.total_size_mb).label('total_size_mb')
            )
            .filter(Gallery.is_published == True)
            .first()
        )
        
        stats['total_photos'] = content_stats.total_photos or 0
        stats['total_views'] = content_stats.total_views or 0
        stats['total_likes'] = content_stats.total_likes or 0
        stats['total_shares'] = content_stats.total_shares or 0
        stats['total_downloads'] = content_stats.total_downloads or 0
        stats['total_size_gb'] = round((content_stats.total_size_mb or 0) / 1024, 2)
        
        # Por categoría
        category_stats = (
            db.query(
                Category.name,
                func.count(Gallery.id).label('gallery_count'),
                func.sum(Gallery.photo_count).label('total_photos'),
                func.sum(Gallery.view_count).label('total_views')
            )
            .join(Gallery, Category.id == Gallery.category_id)
            .filter(Gallery.is_published == True)
            .group_by(Category.id, Category.name)
            .all()
        )
        stats['by_category'] = {
            stat.name: {
                'count': stat.gallery_count,
                'photos': stat.total_photos or 0,
                'views': stat.total_views or 0
            }
            for stat in category_stats
        }
        
        # Por tipo de contenido
        content_type_stats = (
            db.query(
                Gallery.content_type,
                func.count(Gallery.id).label('count'),
                func.sum(Gallery.photo_count).label('total_photos'),
                func.sum(Gallery.view_count).label('total_views')
            )
            .filter(Gallery.is_published == True)
            .group_by(Gallery.content_type)
            .all()
        )
        stats['by_content_type'] = {
            stat.content_type: {
                'count': stat.count,
                'photos': stat.total_photos or 0,
                'views': stat.total_views or 0
            }
            for stat in content_type_stats
        }
        
        # Por estado
        status_stats = (
            db.query(
                Gallery.status,
                func.count(Gallery.id).label('count')
            )
            .group_by(Gallery.status)
            .all()
        )
        stats['by_status'] = {stat.status: stat.count for stat in status_stats}
        
        # Por mes (últimos 12 meses)
        monthly_stats = (
            db.query(
                func.date_format(Gallery.created_at, '%Y-%m').label('month'),
                func.count(Gallery.id).label('count'),
                func.sum(Gallery.photo_count).label('photos')
            )
            .filter(Gallery.created_at >= func.date_sub(func.now(), func.interval(12, 'month')))
            .group_by(func.date_format(Gallery.created_at, '%Y-%m'))
            .order_by(func.date_format(Gallery.created_at, '%Y-%m'))
            .all()
        )
        stats['by_month'] = {
            stat.month: {
                'galleries': stat.count,
                'photos': stat.photos or 0
            }
            for stat in monthly_stats
        }
        
        # Top fotógrafos
        photographer_stats = (
            db.query(
                Gallery.photographer,
                func.count(Gallery.id).label('gallery_count'),
                func.sum(Gallery.photo_count).label('total_photos')
            )
            .filter(
                Gallery.is_published == True,
                Gallery.photographer.isnot(None),
                Gallery.photographer != ''
            )
            .group_by(Gallery.photographer)
            .order_by(desc(func.count(Gallery.id)))
            .limit(10)
            .all()
        )
        stats['top_photographers'] = [
            {
                'name': stat.photographer,
                'galleries': stat.gallery_count,
                'photos': stat.total_photos or 0
            }
            for stat in photographer_stats
        ]
        
        return stats
    
    @staticmethod
    def get_galleries_for_sitemap(db: Session) -> List[Dict[str, Any]]:
        """Obtener galerías para sitemap XML"""
        galleries = (
            db.query(Gallery)
            .options(
                load_only(
                    Gallery.slug, Gallery.updated_at, Gallery.created_at
                )
            )
            .filter(
                Gallery.is_published == True,
                Gallery.is_public == True
            )
            .all()
        )
        
        return [
            {
                'slug': gallery.slug,
                'updated_at': gallery.updated_at,
                'created_at': gallery.created_at
            }
            for gallery in galleries
        ]
    
    @staticmethod
    def bulk_update_status(db: Session, gallery_ids: List[int], status: str) -> int:
        """Actualización masiva de estado"""
        updated = (
            db.query(Gallery)
            .filter(Gallery.id.in_(gallery_ids))
            .update({'status': status}, synchronize_session=False)
        )
        db.flush()
        return updated
    
    @staticmethod
    def bulk_feature(db: Session, gallery_ids: List[int], is_featured: bool) -> int:
        """Actualización masiva de destacados"""
        updated = (
            db.query(Gallery)
            .filter(Gallery.id.in_(gallery_ids))
            .update({'is_featured': is_featured}, synchronize_session=False)
        )
        db.flush()
        return updated
    
    @staticmethod
    def get_empty_galleries(db: Session) -> List[Gallery]:
        """Obtener galerías sin fotos"""
        return (
            db.query(Gallery)
            .filter(
                or_(
                    Gallery.photo_count == 0,
                    Gallery.photos.is_(None)
                )
            )
            .all()
        )
    
    @staticmethod
    def cleanup_orphaned_photos(db: Session, gallery_id: int, existing_filenames: List[str]):
        """Limpiar fotos huérfanas de una galería"""
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery and gallery.photos:
            # Filtrar solo fotos que existen físicamente
            gallery.photos = [
                photo for photo in gallery.photos
                if photo.get('filename') in existing_filenames
            ]
            gallery.photo_count = len(gallery.photos)
            db.flush()