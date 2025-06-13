"""
CMS Video Controller - Orquestación de endpoints para videos
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.cms.schemas.video_schemas import (
    VideoCreate, VideoUpdate, VideoResponse, VideoMinimal, VideoEmbed,
    VideoSearchParams, VideoListResponse, VideoStatsResponse
)
from app.modules.cms.services.video_service import video_service


class VideoController:
    """Controller para operaciones de videos"""
    
    def __init__(self):
        self.service = video_service
    
    async def create_video(
        self, 
        video_data: VideoCreate, 
        author_id: int,
        db: Session
    ) -> VideoResponse:
        """Crear nuevo video"""
        try:
            video = await self.service.create_video(db, video_data, author_id)
            return self._build_video_response(video)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creando video: {str(e)}"
            )
    
    async def get_video(self, video_id: int, db: Session) -> VideoResponse:
        """Obtener video por ID"""
        video = self.service.get_video(db, video_id)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video no encontrado"
            )
        
        return self._build_video_response(video)
    
    async def get_video_by_uuid(self, uuid: str, db: Session) -> VideoResponse:
        """Obtener video por UUID"""
        video = self.service.get_video_by_uuid(db, uuid)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video no encontrado"
            )
        
        return self._build_video_response(video)
    
    async def get_video_by_slug(
        self, 
        slug: str, 
        increment_views: bool, 
        db: Session
    ) -> VideoResponse:
        """Obtener video por slug"""
        video = self.service.get_video_by_slug(db, slug, increment_views)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video no encontrado"
            )
        
        return self._build_video_response(video)
    
    async def get_videos(
        self, 
        params: VideoSearchParams, 
        db: Session
    ) -> VideoListResponse:
        """Obtener lista paginada de videos"""
        try:
            result = self.service.get_videos(db, params)
            
            videos = [
                self._build_video_response(video, minimal=params.minimal) 
                for video in result['videos']
            ]
            
            return VideoListResponse(
                videos=videos,
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
                detail=f"Error obteniendo videos: {str(e)}"
            )
    
    async def update_video(
        self, 
        video_id: int, 
        update_data: VideoUpdate, 
        db: Session
    ) -> VideoResponse:
        """Actualizar video"""
        try:
            video = await self.service.update_video(db, video_id, update_data)
            return self._build_video_response(video)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error actualizando video: {str(e)}"
            )
    
    async def delete_video(self, video_id: int, db: Session) -> Dict[str, str]:
        """Eliminar video"""
        try:
            success = self.service.delete_video(db, video_id)
            if success:
                return {"message": "Video eliminado exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo eliminar el video"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error eliminando video: {str(e)}"
            )
    
    async def publish_video(self, video_id: int, db: Session) -> VideoResponse:
        """Publicar video"""
        try:
            video = self.service.publish_video(db, video_id)
            return self._build_video_response(video)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error publicando video: {str(e)}"
            )
    
    async def unpublish_video(self, video_id: int, db: Session) -> VideoResponse:
        """Despublicar video"""
        try:
            video = self.service.unpublish_video(db, video_id)
            return self._build_video_response(video)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error despublicando video: {str(e)}"
            )
    
    async def toggle_featured(self, video_id: int, db: Session) -> VideoResponse:
        """Alternar estado destacado"""
        try:
            video = self.service.toggle_featured(db, video_id)
            return self._build_video_response(video)
            
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
    
    async def get_videos_by_category(
        self, 
        category_id: int, 
        limit: int, 
        is_published: bool, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos de una categoría"""
        videos = self.service.get_videos_by_category(db, category_id, limit, is_published)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def get_featured_videos(
        self, 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos destacados"""
        videos = self.service.get_featured_videos(db, limit)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def get_recent_videos(
        self, 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos recientes"""
        videos = self.service.get_recent_videos(db, limit)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def get_popular_videos(
        self, 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos populares"""
        videos = self.service.get_popular_videos(db, limit)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def get_videos_by_academic_unit(
        self, 
        academic_unit_id: int, 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos de una unidad académica"""
        videos = self.service.get_videos_by_academic_unit(db, academic_unit_id, limit)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def get_related_videos(
        self, 
        video_id: int, 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Obtener videos relacionados"""
        video = self.service.get_video(db, video_id)
        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video no encontrado"
            )
        
        related_videos = self.service.get_related_videos(db, video, limit)
        return [self._build_video_response(vid, minimal=True) for vid in related_videos]
    
    async def search_videos_by_tags(
        self, 
        tags: List[str], 
        limit: int, 
        db: Session
    ) -> List[VideoResponse]:
        """Buscar videos por tags"""
        videos = self.service.search_videos_by_tags(db, tags, limit)
        return [self._build_video_response(video, minimal=True) for video in videos]
    
    async def like_video(self, video_id: int, db: Session) -> VideoResponse:
        """Dar like a video"""
        try:
            video = self.service.like_video(db, video_id)
            return self._build_video_response(video, minimal=True)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error dando like: {str(e)}"
            )
    
    async def share_video(self, video_id: int, db: Session) -> VideoResponse:
        """Compartir video"""
        try:
            video = self.service.share_video(db, video_id)
            return self._build_video_response(video, minimal=True)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error compartiendo video: {str(e)}"
            )
    
    async def get_video_embed(self, video_id: int, db: Session) -> VideoEmbed:
        """Obtener datos para embed"""
        try:
            embed_data = self.service.get_video_embed_data(db, video_id)
            return VideoEmbed(**embed_data)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo embed: {str(e)}"
            )
    
    async def get_statistics(self, db: Session) -> VideoStatsResponse:
        """Obtener estadísticas de videos"""
        try:
            stats = self.service.get_statistics(db)
            return VideoStatsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo estadísticas: {str(e)}"
            )
    
    async def bulk_update_status(
        self, 
        video_ids: List[int], 
        status: str, 
        db: Session
    ) -> Dict[str, Any]:
        """Actualización masiva de estado"""
        try:
            updated = self.service.bulk_update_status(db, video_ids, status)
            return {
                "message": f"{updated} videos actualizados",
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
    
    async def bulk_feature(
        self, 
        video_ids: List[int], 
        is_featured: bool, 
        db: Session
    ) -> Dict[str, Any]:
        """Actualización masiva de destacados"""
        try:
            updated = self.service.bulk_feature(db, video_ids, is_featured)
            return {
                "message": f"{updated} videos actualizados",
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
    
    async def refresh_youtube_metadata(
        self, 
        video_id: int, 
        db: Session
    ) -> VideoResponse:
        """Actualizar metadata de YouTube"""
        try:
            video = await self.service.refresh_youtube_metadata(db, video_id)
            return self._build_video_response(video)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error actualizando metadata: {str(e)}"
            )
    
    def _build_video_response(self, video, minimal: bool = False) -> VideoResponse:
        """Construir respuesta de video"""
        response_data = {
            'id': video.id,
            'uuid': video.uuid,
            'title': video.title,
            'subtitle': video.subtitle,
            'description': video.description,
            'slug': video.slug,
            'embed_url': video.embed_url,
            'original_url': video.original_url,
            'video_id': video.video_id,
            'thumbnail_url': video.thumbnail_url,
            'duration': video.duration,
            'event_date': video.event_date,
            'content_type': video.content_type,
            'tags': video.tags,
            'video_quality': video.video_quality,
            'aspect_ratio': video.aspect_ratio,
            'is_published': video.is_published,
            'is_featured': video.is_featured,
            'is_public': video.is_public,
            'status': video.status,
            'approval_required': video.approval_required,
            'seo_title': video.seo_title,
            'seo_description': video.seo_description,
            'allow_comments': video.allow_comments,
            'allow_embedding': video.allow_embedding,
            'view_count': video.view_count,
            'like_count': video.like_count,
            'share_count': video.share_count,
            'category_id': video.category_id,
            'author_id': video.author_id,
            'created_at': video.created_at,
            'updated_at': video.updated_at
        }
        
        # Agregar datos relacionados si están disponibles y no es minimal
        if not minimal:
            if hasattr(video, 'category') and video.category:
                response_data['category'] = {
                    'id': video.category.id,
                    'name': video.category.name,
                    'display_name': video.category.display_name,
                    'slug': video.category.slug,
                    'color': video.category.color
                }
            
            if hasattr(video, 'author') and video.author:
                response_data['author'] = {
                    'id': video.author.id,
                    'first_name': video.author.first_name,
                    'last_name': video.author.last_name,
                    'profile_photo': video.author.profile_photo,
                    'position': video.author.position
                }
        
        return VideoResponse(**response_data)


# Instancia global del controlador
video_controller = VideoController()