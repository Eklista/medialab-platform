"""
CMS Video Repository - Acceso a datos optimizado para videos
"""
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload, load_only
from sqlalchemy import or_, and_, func, desc, asc, between

from app.modules.cms.models import Video, Category
from app.modules.users.models import InternalUser
from app.modules.organizations.models import AcademicUnit


class VideoRepository:
    """Repository para operaciones de videos con optimizaciones"""
    
    @staticmethod
    def create(db: Session, video_data: Dict[str, Any]) -> Video:
        """Crear nuevo video"""
        video = Video(**video_data)
        db.add(video)
        db.flush()
        return video
    
    @staticmethod
    def get_by_id(db: Session, video_id: int, include_relations: bool = True) -> Optional[Video]:
        """Obtener video por ID con carga optimizada"""
        query = db.query(Video)
        
        if include_relations:
            query = query.options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug, Category.color
                ).joinedload(Category.academic_unit).load_only(
                    AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name, 
                    InternalUser.profile_photo, InternalUser.position
                )
            )
        
        return query.filter(Video.id == video_id).first()
    
    @staticmethod
    def get_by_uuid(db: Session, uuid: str, include_relations: bool = True) -> Optional[Video]:
        """Obtener video por UUID"""
        query = db.query(Video)
        
        if include_relations:
            query = query.options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug, Category.color
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name, 
                    InternalUser.profile_photo
                )
            )
        
        return query.filter(Video.uuid == uuid).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str, include_relations: bool = True) -> Optional[Video]:
        """Obtener video por slug"""
        query = db.query(Video)
        
        if include_relations:
            query = query.options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
        
        return query.filter(Video.slug == slug).first()
    
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
        sort_by: str = "created_at",
        sort_order: str = "desc",
        minimal: bool = False,
        include_author: bool = True,
        include_category: bool = True
    ) -> Tuple[List[Video], int]:
        """Obtener lista paginada de videos con filtros avanzados"""
        
        if minimal:
            # Para listings, solo campos esenciales
            query = db.query(Video).options(
                load_only(
                    Video.id,
                    Video.uuid,
                    Video.title,
                    Video.slug,
                    Video.thumbnail_url,
                    Video.embed_url,
                    Video.duration,
                    Video.is_published,
                    Video.is_featured,
                    Video.view_count,
                    Video.event_date,
                    Video.category_id,
                    Video.author_id,
                    Video.created_at
                )
            )
        else:
            # Para detalles, incluir relaciones selectivas
            options = []
            
            if include_category:
                options.append(
                    joinedload(Video.category).load_only(
                        Category.id, Category.name, Category.display_name, 
                        Category.slug, Category.color, Category.academic_unit_id
                    ).joinedload(Category.academic_unit).load_only(
                        AcademicUnit.id, AcademicUnit.name, AcademicUnit.abbreviation
                    )
                )
            
            if include_author:
                options.append(
                    joinedload(Video.author).load_only(
                        InternalUser.id, InternalUser.first_name, InternalUser.last_name,
                        InternalUser.profile_photo, InternalUser.position
                    )
                )
            
            if options:
                query = db.query(Video).options(*options)
            else:
                query = db.query(Video)
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                Video.title.ilike(f"%{search}%"),
                Video.subtitle.ilike(f"%{search}%"),
                Video.description.ilike(f"%{search}%"),
                Video.tags.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category_id:
            query = query.filter(Video.category_id == category_id)
        
        if author_id:
            query = query.filter(Video.author_id == author_id)
        
        if content_type:
            query = query.filter(Video.content_type == content_type)
        
        if status:
            query = query.filter(Video.status == status)
        
        if is_published is not None:
            query = query.filter(Video.is_published == is_published)
        
        if is_featured is not None:
            query = query.filter(Video.is_featured == is_featured)
        
        if is_public is not None:
            query = query.filter(Video.is_public == is_public)
        
        # Filtros de fecha
        if event_date_from:
            query = query.filter(Video.event_date >= event_date_from)
        
        if event_date_to:
            query = query.filter(Video.event_date <= event_date_to)
        
        if created_from:
            query = query.filter(Video.created_at >= created_from)
        
        if created_to:
            query = query.filter(Video.created_at <= created_to)
        
        # Contar total
        total = query.count()
        
        # Aplicar ordenamiento
        if sort_by == "created_at":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Video.created_at))
        elif sort_by == "event_date":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Video.event_date))
        elif sort_by == "title":
            order_func = asc if sort_order == "asc" else desc
            query = query.order_by(order_func(Video.title))
        elif sort_by == "view_count":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Video.view_count))
        elif sort_by == "duration":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(Video.duration))
        else:
            # Orden por defecto
            query = query.order_by(desc(Video.created_at))
        
        # Aplicar paginación
        videos = query.offset(skip).limit(limit).all()
        
        return videos, total
    
    @staticmethod
    def get_by_category(
        db: Session, 
        category_id: int, 
        is_published: bool = True,
        limit: int = 20
    ) -> List[Video]:
        """Obtener videos de una categoría específica"""
        query = db.query(Video).options(
            joinedload(Video.author).load_only(
                InternalUser.id, InternalUser.first_name, InternalUser.last_name
            )
        ).filter(Video.category_id == category_id)
        
        if is_published:
            query = query.filter(
                Video.is_published == True,
                Video.is_public == True
            )
        
        return query.order_by(desc(Video.event_date)).limit(limit).all()
    
    @staticmethod
    def get_featured(db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos destacados"""
        return (
            db.query(Video)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Video.is_featured == True,
                Video.is_published == True,
                Video.is_public == True
            )
            .order_by(desc(Video.event_date))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_recent(db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos más recientes"""
        return (
            db.query(Video)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Video.is_published == True,
                Video.is_public == True
            )
            .order_by(desc(Video.created_at))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular(db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos más populares por vistas"""
        return (
            db.query(Video)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Video.is_published == True,
                Video.is_public == True
            )
            .order_by(desc(Video.view_count))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_by_academic_unit(
        db: Session, 
        academic_unit_id: int, 
        limit: int = 20,
        is_published: bool = True
    ) -> List[Video]:
        """Obtener videos de una unidad académica"""
        query = (
            db.query(Video)
            .join(Category, Video.category_id == Category.id)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(Category.academic_unit_id == academic_unit_id)
        )
        
        if is_published:
            query = query.filter(
                Video.is_published == True,
                Video.is_public == True
            )
        
        return query.order_by(desc(Video.event_date)).limit(limit).all()
    
    @staticmethod
    def update(db: Session, video: Video, update_data: Dict[str, Any]) -> Video:
        """Actualizar video"""
        for field, value in update_data.items():
            if hasattr(video, field) and value is not None:
                setattr(video, field, value)
        
        db.flush()
        return video
    
    @staticmethod
    def delete(db: Session, video: Video) -> bool:
        """Eliminar video"""
        db.delete(video)
        db.flush()
        return True
    
    @staticmethod
    def increment_view_count(db: Session, video_id: int):
        """Incrementar contador de vistas"""
        db.query(Video).filter(Video.id == video_id).update({
            "view_count": Video.view_count + 1
        })
        db.flush()
    
    @staticmethod
    def increment_like_count(db: Session, video_id: int):
        """Incrementar contador de likes"""
        db.query(Video).filter(Video.id == video_id).update({
            "like_count": Video.like_count + 1
        })
        db.flush()
    
    @staticmethod
    def increment_share_count(db: Session, video_id: int):
        """Incrementar contador de shares"""
        db.query(Video).filter(Video.id == video_id).update({
            "share_count": Video.share_count + 1
        })
        db.flush()
    
    @staticmethod
    def get_by_video_id(db: Session, video_id_youtube: str) -> Optional[Video]:
        """Obtener video por video_id de YouTube"""
        return db.query(Video).filter(Video.video_id == video_id_youtube).first()
    
    @staticmethod
    def search_by_tags(db: Session, tags: List[str], limit: int = 20) -> List[Video]:
        """Buscar videos por tags"""
        filters = []
        for tag in tags:
            filters.append(Video.tags.ilike(f"%{tag}%"))
        
        return (
            db.query(Video)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                or_(*filters),
                Video.is_published == True,
                Video.is_public == True
            )
            .order_by(desc(Video.view_count))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_related(db: Session, video: Video, limit: int = 5) -> List[Video]:
        """Obtener videos relacionados"""
        # Videos de la misma categoría, excluyendo el actual
        related = (
            db.query(Video)
            .options(
                joinedload(Video.category).load_only(
                    Category.id, Category.name, Category.display_name, Category.slug
                ),
                joinedload(Video.author).load_only(
                    InternalUser.id, InternalUser.first_name, InternalUser.last_name
                )
            )
            .filter(
                Video.category_id == video.category_id,
                Video.id != video.id,
                Video.is_published == True,
                Video.is_public == True
            )
            .order_by(desc(Video.view_count))
            .limit(limit)
            .all()
        )
        
        # Si no hay suficientes, agregar videos del mismo tipo de contenido
        if len(related) < limit:
            additional = (
                db.query(Video)
                .options(
                    joinedload(Video.category).load_only(
                        Category.id, Category.name, Category.display_name, Category.slug
                    ),
                    joinedload(Video.author).load_only(
                        InternalUser.id, InternalUser.first_name, InternalUser.last_name
                    )
                )
                .filter(
                    Video.content_type == video.content_type,
                    Video.id != video.id,
                    Video.is_published == True,
                    Video.is_public == True,
                    Video.id.notin_([v.id for v in related])
                )
                .order_by(desc(Video.view_count))
                .limit(limit - len(related))
                .all()
            )
            related.extend(additional)
        
        return related
    
    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de videos"""
        stats = {}
        
        # Estadísticas básicas
        stats['total_videos'] = db.query(Video).count()
        stats['published_videos'] = db.query(Video).filter(Video.is_published == True).count()
        stats['draft_videos'] = db.query(Video).filter(Video.status == 'draft').count()
        
        # Estadísticas de engagement
        engagement_stats = (
            db.query(
                func.sum(Video.view_count).label('total_views'),
                func.sum(Video.like_count).label('total_likes'),
                func.sum(Video.share_count).label('total_shares'),
                func.sum(Video.duration).label('total_duration')
            )
            .filter(Video.is_published == True)
            .first()
        )
        
        stats['total_views'] = engagement_stats.total_views or 0
        stats['total_likes'] = engagement_stats.total_likes or 0
        stats['total_shares'] = engagement_stats.total_shares or 0
        stats['total_duration'] = engagement_stats.total_duration or 0  # en segundos
        
        # Por categoría
        category_stats = (
            db.query(
                Category.name,
                func.count(Video.id).label('video_count'),
                func.sum(Video.view_count).label('total_views')
            )
            .join(Video, Category.id == Video.category_id)
            .filter(Video.is_published == True)
            .group_by(Category.id, Category.name)
            .all()
        )
        stats['by_category'] = {
            stat.name: {
                'count': stat.video_count,
                'views': stat.total_views or 0
            }
            for stat in category_stats
        }
        
        # Por tipo de contenido
        content_type_stats = (
            db.query(
                Video.content_type,
                func.count(Video.id).label('count'),
                func.sum(Video.view_count).label('total_views')
            )
            .filter(Video.is_published == True)
            .group_by(Video.content_type)
            .all()
        )
        stats['by_content_type'] = {
            stat.content_type: {
                'count': stat.count,
                'views': stat.total_views or 0
            }
            for stat in content_type_stats
        }
        
        # Por estado
        status_stats = (
            db.query(
                Video.status,
                func.count(Video.id).label('count')
            )
            .group_by(Video.status)
            .all()
        )
        stats['by_status'] = {stat.status: stat.count for stat in status_stats}
        
        # Por mes (últimos 12 meses)
        monthly_stats = (
            db.query(
                func.date_format(Video.created_at, '%Y-%m').label('month'),
                func.count(Video.id).label('count')
            )
            .filter(Video.created_at >= func.date_sub(func.now(), func.interval(12, 'month')))
            .group_by(func.date_format(Video.created_at, '%Y-%m'))
            .order_by(func.date_format(Video.created_at, '%Y-%m'))
            .all()
        )
        stats['by_month'] = {stat.month: stat.count for stat in monthly_stats}
        
        return stats
    
    @staticmethod
    def get_videos_for_sitemap(db: Session) -> List[Dict[str, Any]]:
        """Obtener videos para sitemap XML"""
        videos = (
            db.query(Video)
            .options(
                load_only(
                    Video.slug, Video.updated_at, Video.created_at
                )
            )
            .filter(
                Video.is_published == True,
                Video.is_public == True
            )
            .all()
        )
        
        return [
            {
                'slug': video.slug,
                'updated_at': video.updated_at,
                'created_at': video.created_at
            }
            for video in videos
        ]
    
    @staticmethod
    def bulk_update_status(db: Session, video_ids: List[int], status: str) -> int:
        """Actualización masiva de estado"""
        updated = (
            db.query(Video)
            .filter(Video.id.in_(video_ids))
            .update({'status': status}, synchronize_session=False)
        )
        db.flush()
        return updated
    
    @staticmethod
    def bulk_feature(db: Session, video_ids: List[int], is_featured: bool) -> int:
        """Actualización masiva de destacados"""
        updated = (
            db.query(Video)
            .filter(Video.id.in_(video_ids))
            .update({'is_featured': is_featured}, synchronize_session=False)
        )
        db.flush()
        return updated