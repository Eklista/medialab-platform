"""
CMS Video Service - Lógica de negocio para videos
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.modules.cms.models import Video, Category
from app.modules.cms.repositories.video_repository import VideoRepository
from app.modules.cms.repositories.category_repository import CategoryRepository
from app.modules.cms.schemas.video_schemas import (
    VideoCreate, VideoUpdate, VideoSearchParams
)
from app.modules.cms.utils.slug_generator import slug_generator
from app.modules.cms.utils.youtube_processor import youtube_processor
from app.modules.users.models import InternalUser


class VideoService:
    """Servicio para lógica de negocio de videos"""
    
    def __init__(self):
        self.video_repository = VideoRepository()
        self.category_repository = CategoryRepository()
    
    async def create_video(self, db: Session, video_data: VideoCreate, author_id: int) -> Video:
        """Crear nuevo video con procesamiento de YouTube"""
        # Validar categoría
        category = self.category_repository.get_by_id(db, video_data.category_id, include_relations=False)
        if not category or not category.is_active:
            raise ValueError("Categoría no encontrada o inactiva")
        
        # Validar autor
        author = db.query(InternalUser).filter(
            InternalUser.id == author_id,
            InternalUser.is_active == True
        ).first()
        if not author:
            raise ValueError("Autor no encontrado o inactivo")
        
        # Procesar URL de YouTube
        youtube_data = youtube_processor.process_youtube_url(video_data.original_url)
        if not youtube_data['success']:
            raise ValueError(f"URL de YouTube inválida: {youtube_data.get('error', 'Error desconocido')}")
        
        # Verificar si el video ya existe
        existing_video = self.video_repository.get_by_video_id(db, youtube_data['video_id'])
        if existing_video:
            raise ValueError("Este video de YouTube ya está registrado en el sistema")
        
        # Obtener metadata de YouTube
        youtube_metadata = await youtube_processor.get_video_metadata(youtube_data['video_id'])
        
        # Generar slug único
        slug = slug_generator.generate_video_slug(
            video_data.title,
            video_data.event_date,
            db
        )
        
        # Preparar datos del video
        video_dict = video_data.dict()
        video_dict.update({
            'author_id': author_id,
            'slug': slug,
            'embed_url': youtube_data['embed_url'],
            'video_id': youtube_data['video_id'],
            'thumbnail_url': youtube_data['thumbnail_url'],
            'status': 'draft',
            'is_published': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        # Agregar metadata de YouTube si está disponible
        if youtube_metadata['success']:
            metadata = youtube_metadata['metadata']
            # Solo sobrescribir si no se proporcionó título
            if not video_data.title.strip():
                video_dict['title'] = metadata.get('title', video_data.title)
            
            # Agregar información técnica
            if metadata.get('width') and metadata.get('height'):
                video_dict['aspect_ratio'] = metadata['aspect_ratio']
        
        # Crear video
        video = self.video_repository.create(db, video_dict)
        db.commit()
        
        # Actualizar estadísticas de categoría
        self.category_repository.update_content_statistics(db, video_data.category_id)
        
        return video
    
    def get_video(self, db: Session, video_id: int) -> Optional[Video]:
        """Obtener video por ID"""
        return self.video_repository.get_by_id(db, video_id)
    
    def get_video_by_uuid(self, db: Session, uuid: str) -> Optional[Video]:
        """Obtener video por UUID"""
        return self.video_repository.get_by_uuid(db, uuid)
    
    def get_video_by_slug(self, db: Session, slug: str, increment_views: bool = False) -> Optional[Video]:
        """Obtener video por slug con opción de incrementar vistas"""
        video = self.video_repository.get_by_slug(db, slug)
        
        if video and increment_views and video.is_published:
            self.video_repository.increment_view_count(db, video.id)
            db.commit()
        
        return video
    
    def get_videos(
        self, 
        db: Session, 
        params: VideoSearchParams
    ) -> Dict[str, Any]:
        """Obtener lista paginada de videos"""
        skip = (params.page - 1) * params.per_page
        
        videos, total = self.video_repository.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            category_id=params.category_id,
            author_id=params.author_id,
            content_type=params.content_type,
            status=params.status,
            is_published=params.is_published,
            is_featured=params.is_featured,
            is_public=params.is_public,
            event_date_from=params.event_date_from,
            event_date_to=params.event_date_to,
            created_from=params.created_from,
            created_to=params.created_to,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            minimal=params.minimal,
            include_author=params.include_author,
            include_category=params.include_category
        )
        
        return {
            'videos': videos,
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'pages': (total + params.per_page - 1) // params.per_page,
            'has_next': params.page * params.per_page < total,
            'has_prev': params.page > 1
        }
    
    async def update_video(
        self, 
        db: Session, 
        video_id: int, 
        update_data: VideoUpdate
    ) -> Video:
        """Actualizar video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        # Preparar datos de actualización
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        
        # Si cambió la URL de YouTube, reprocesar
        if 'original_url' in update_dict and update_dict['original_url'] != video.original_url:
            youtube_data = youtube_processor.process_youtube_url(update_dict['original_url'])
            if not youtube_data['success']:
                raise ValueError(f"URL de YouTube inválida: {youtube_data.get('error')}")
            
            # Verificar que no exista otro video con el mismo video_id
            existing = self.video_repository.get_by_video_id(db, youtube_data['video_id'])
            if existing and existing.id != video_id:
                raise ValueError("Este video de YouTube ya está registrado")
            
            update_dict.update({
                'embed_url': youtube_data['embed_url'],
                'video_id': youtube_data['video_id'],
                'thumbnail_url': youtube_data['thumbnail_url']
            })
            
            # Obtener nueva metadata
            youtube_metadata = await youtube_processor.get_video_metadata(youtube_data['video_id'])
            if youtube_metadata['success']:
                metadata = youtube_metadata['metadata']
                if metadata.get('width') and metadata.get('height'):
                    update_dict['aspect_ratio'] = metadata['aspect_ratio']
        
        # Actualizar slug si cambió el título o fecha
        if ('title' in update_dict or 'event_date' in update_dict):
            new_title = update_dict.get('title', video.title)
            new_date = update_dict.get('event_date', video.event_date)
            
            new_slug = slug_generator.update_slug_if_needed(
                video.slug,
                f"{new_date}-{new_title}",
                db,
                Video,
                video_id
            )
            update_dict['slug'] = new_slug
        
        # Actualizar timestamp
        update_dict['updated_at'] = datetime.utcnow()
        
        # Aplicar actualización
        updated_video = self.video_repository.update(db, video, update_dict)
        db.commit()
        
        # Actualizar estadísticas si cambió la categoría
        if 'category_id' in update_dict:
            # Actualizar categoría anterior y nueva
            if video.category_id != update_dict['category_id']:
                self.category_repository.update_content_statistics(db, video.category_id)
                self.category_repository.update_content_statistics(db, update_dict['category_id'])
        
        return updated_video
    
    def delete_video(self, db: Session, video_id: int) -> bool:
        """Eliminar video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        category_id = video.category_id
        
        # Eliminar video
        success = self.video_repository.delete(db, video)
        if success:
            db.commit()
            # Actualizar estadísticas de categoría
            self.category_repository.update_content_statistics(db, category_id)
        
        return success
    
    def publish_video(self, db: Session, video_id: int) -> Video:
        """Publicar video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        # Validar que tenga la información mínima requerida
        if not video.title or not video.embed_url:
            raise ValueError("El video debe tener título y URL válida para ser publicado")
        
        update_data = {
            'is_published': True,
            'status': 'published',
            'updated_at': datetime.utcnow()
        }
        
        updated_video = self.video_repository.update(db, video, update_data)
        db.commit()
        
        # Actualizar estadísticas
        self.category_repository.update_content_statistics(db, video.category_id)
        
        return updated_video
    
    def unpublish_video(self, db: Session, video_id: int) -> Video:
        """Despublicar video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        update_data = {
            'is_published': False,
            'status': 'draft',
            'updated_at': datetime.utcnow()
        }
        
        updated_video = self.video_repository.update(db, video, update_data)
        db.commit()
        
        # Actualizar estadísticas
        self.category_repository.update_content_statistics(db, video.category_id)
        
        return updated_video
    
    def toggle_featured(self, db: Session, video_id: int) -> Video:
        """Alternar estado destacado"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        update_data = {
            'is_featured': not video.is_featured,
            'updated_at': datetime.utcnow()
        }
        
        updated_video = self.video_repository.update(db, video, update_data)
        db.commit()
        
        return updated_video
    
    def get_videos_by_category(
        self, 
        db: Session, 
        category_id: int, 
        limit: int = 20,
        is_published: bool = True
    ) -> List[Video]:
        """Obtener videos de una categoría"""
        return self.video_repository.get_by_category(db, category_id, is_published, limit)
    
    def get_featured_videos(self, db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos destacados"""
        return self.video_repository.get_featured(db, limit)
    
    def get_recent_videos(self, db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos más recientes"""
        return self.video_repository.get_recent(db, limit)
    
    def get_popular_videos(self, db: Session, limit: int = 10) -> List[Video]:
        """Obtener videos más populares"""
        return self.video_repository.get_popular(db, limit)
    
    def get_videos_by_academic_unit(
        self, 
        db: Session, 
        academic_unit_id: int, 
        limit: int = 20
    ) -> List[Video]:
        """Obtener videos de una unidad académica"""
        return self.video_repository.get_by_academic_unit(db, academic_unit_id, limit)
    
    def get_related_videos(self, db: Session, video: Video, limit: int = 5) -> List[Video]:
        """Obtener videos relacionados"""
        return self.video_repository.get_related(db, video, limit)
    
    def search_videos_by_tags(self, db: Session, tags: List[str], limit: int = 20) -> List[Video]:
        """Buscar videos por tags"""
        return self.video_repository.search_by_tags(db, tags, limit)
    
    def like_video(self, db: Session, video_id: int) -> Video:
        """Dar like a un video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        self.video_repository.increment_like_count(db, video_id)
        db.commit()
        
        return self.video_repository.get_by_id(db, video_id, include_relations=False)
    
    def share_video(self, db: Session, video_id: int) -> Video:
        """Compartir video (incrementar contador)"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video:
            raise ValueError("Video no encontrado")
        
        self.video_repository.increment_share_count(db, video_id)
        db.commit()
        
        return self.video_repository.get_by_id(db, video_id, include_relations=False)
    
    def get_video_embed_data(self, db: Session, video_id: int) -> Dict[str, Any]:
        """Obtener datos para embed de video"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video or not video.is_published or not video.allow_embedding:
            raise ValueError("Video no disponible para embed")
        
        return {
            'id': video.id,
            'uuid': video.uuid,
            'title': video.title,
            'embed_url': video.embed_url,
            'thumbnail_url': video.thumbnail_url,
            'duration': video.duration,
            'allow_embedding': video.allow_embedding
        }
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de videos"""
        return self.video_repository.get_statistics(db)
    
    def bulk_update_status(
        self, 
        db: Session, 
        video_ids: List[int], 
        status: str
    ) -> int:
        """Actualización masiva de estado"""
        # Validar que todos los videos existen
        existing_videos = db.query(Video).filter(Video.id.in_(video_ids)).all()
        if len(existing_videos) != len(video_ids):
            raise ValueError("Algunos videos no existen")
        
        # Actualizar
        updated = self.video_repository.bulk_update_status(db, video_ids, status)
        db.commit()
        
        # Actualizar estadísticas de categorías afectadas
        affected_categories = set(video.category_id for video in existing_videos)
        for category_id in affected_categories:
            self.category_repository.update_content_statistics(db, category_id)
        
        return updated
    
    def bulk_feature(
        self, 
        db: Session, 
        video_ids: List[int], 
        is_featured: bool
    ) -> int:
        """Actualización masiva de destacados"""
        # Validar que todos los videos existen
        existing_count = db.query(Video).filter(Video.id.in_(video_ids)).count()
        if existing_count != len(video_ids):
            raise ValueError("Algunos videos no existen")
        
        # Actualizar
        updated = self.video_repository.bulk_feature(db, video_ids, is_featured)
        db.commit()
        
        return updated
    
    async def refresh_youtube_metadata(self, db: Session, video_id: int) -> Video:
        """Actualizar metadata de YouTube"""
        video = self.video_repository.get_by_id(db, video_id, include_relations=False)
        if not video or not video.video_id:
            raise ValueError("Video no encontrado o sin ID de YouTube")
        
        # Obtener metadata actualizada
        youtube_metadata = await youtube_processor.get_video_metadata(video.video_id)
        
        if not youtube_metadata['success']:
            raise ValueError(f"Error al obtener metadata: {youtube_metadata.get('error')}")
        
        metadata = youtube_metadata['metadata']
        update_data = {
            'thumbnail_url': metadata.get('thumbnail_url', video.thumbnail_url),
            'updated_at': datetime.utcnow()
        }
        
        if metadata.get('width') and metadata.get('height'):
            update_data['aspect_ratio'] = metadata['aspect_ratio']
        
        # Actualizar video
        updated_video = self.video_repository.update(db, video, update_data)
        db.commit()
        
        return updated_video
    
    def validate_video_access(
        self, 
        db: Session, 
        video_id: int, 
        user_academic_units: List[int]
    ) -> bool:
        """Validar acceso de usuario a video"""
        video = self.video_repository.get_by_id(db, video_id)
        if not video:
            return False
        
        # Verificar acceso a través de la categoría
        return video.category.academic_unit_id in user_academic_units


# Instancia global del servicio
video_service = VideoService()