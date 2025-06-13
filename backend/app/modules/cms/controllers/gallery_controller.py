"""
CMS Gallery Controller - Orquestación de endpoints para galerías
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile

from app.modules.cms.schemas.gallery_schemas import (
    GalleryCreate, GalleryUpdate, GalleryResponse, GalleryMinimal,
    GallerySearchParams, GalleryListResponse, GalleryStatsResponse,
    PhotoUpload, FileUploadResponse, BulkUploadResponse,
    PhotoReorderRequest, PhotoUpdateRequest
)
from app.modules.cms.services.gallery_service import gallery_service


class GalleryController:
    """Controller para operaciones de galerías"""
    
    def __init__(self):
        self.service = gallery_service
    
    async def create_gallery(
        self, 
        gallery_data: GalleryCreate, 
        author_id: int,
        db: Session
    ) -> GalleryResponse:
        """Crear nueva galería"""
        try:
            gallery = self.service.create_gallery(db, gallery_data, author_id)
            return self._build_gallery_response(gallery)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creando galería: {str(e)}"
            )
    
    async def get_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Obtener galería por ID"""
        gallery = self.service.get_gallery(db, gallery_id)
        if not gallery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Galería no encontrada"
            )
        
        return self._build_gallery_response(gallery)
    
    async def get_gallery_by_uuid(self, uuid: str, db: Session) -> GalleryResponse:
        """Obtener galería por UUID"""
        gallery = self.service.get_gallery_by_uuid(db, uuid)
        if not gallery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Galería no encontrada"
            )
        
        return self._build_gallery_response(gallery)
    
    async def get_gallery_by_slug(
        self, 
        slug: str, 
        increment_views: bool, 
        db: Session
    ) -> GalleryResponse:
        """Obtener galería por slug"""
        gallery = self.service.get_gallery_by_slug(db, slug, increment_views)
        if not gallery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Galería no encontrada"
            )
        
        return self._build_gallery_response(gallery)
    
    async def get_galleries(
        self, 
        params: GallerySearchParams, 
        db: Session
    ) -> GalleryListResponse:
        """Obtener lista paginada de galerías"""
        try:
            result = self.service.get_galleries(db, params)
            
            galleries = [
                self._build_gallery_response(
                    gallery, 
                    minimal=params.minimal,
                    include_photos=params.include_photos,
                    photos_limit=params.photos_limit
                ) 
                for gallery in result['galleries']
            ]
            
            return GalleryListResponse(
                galleries=galleries,
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
                detail=f"Error obteniendo galerías: {str(e)}"
            )
    
    async def update_gallery(
        self, 
        gallery_id: int, 
        update_data: GalleryUpdate, 
        db: Session
    ) -> GalleryResponse:
        """Actualizar galería"""
        try:
            gallery = self.service.update_gallery(db, gallery_id, update_data)
            return self._build_gallery_response(gallery)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error actualizando galería: {str(e)}"
            )
    
    async def delete_gallery(self, gallery_id: int, db: Session) -> Dict[str, str]:
        """Eliminar galería"""
        try:
            success = self.service.delete_gallery(db, gallery_id)
            if success:
                return {"message": "Galería eliminada exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo eliminar la galería"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error eliminando galería: {str(e)}"
            )
    
    async def upload_photos(
        self, 
        gallery_id: int,
        files: List[UploadFile],
        photo_metadata: List[PhotoUpload],
        db: Session
    ) -> BulkUploadResponse:
        """Subir fotos a galería"""
        try:
            result = await self.service.upload_photos(db, gallery_id, files, photo_metadata)
            return BulkUploadResponse(**result)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error subiendo fotos: {str(e)}"
            )
    
    async def delete_photo(
        self, 
        gallery_id: int, 
        photo_filename: str, 
        db: Session
    ) -> Dict[str, str]:
        """Eliminar foto de galería"""
        try:
            success = await self.service.delete_photo(db, gallery_id, photo_filename)
            if success:
                return {"message": "Foto eliminada exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo eliminar la foto"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error eliminando foto: {str(e)}"
            )
    
    async def reorder_photos(
        self, 
        gallery_id: int, 
        reorder_data: PhotoReorderRequest, 
        db: Session
    ) -> Dict[str, str]:
        """Reordenar fotos en galería"""
        try:
            success = self.service.reorder_photos(db, gallery_id, reorder_data.photo_orders)
            if success:
                return {"message": "Fotos reordenadas exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudieron reordenar las fotos"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reordenando fotos: {str(e)}"
            )
    
    async def update_photo_metadata(
        self, 
        gallery_id: int, 
        update_data: PhotoUpdateRequest, 
        db: Session
    ) -> Dict[str, str]:
        """Actualizar metadata de foto"""
        try:
            metadata = update_data.dict(exclude={'filename'}, exclude_unset=True)
            success = self.service.update_photo_metadata(
                db, gallery_id, update_data.filename, metadata
            )
            if success:
                return {"message": "Metadata de foto actualizada exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo actualizar la metadata"
                )
                
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
    
    async def set_cover_photo(
        self, 
        gallery_id: int, 
        photo_filename: str, 
        db: Session
    ) -> Dict[str, str]:
        """Establecer foto de portada"""
        try:
            success = self.service.set_cover_photo(db, gallery_id, photo_filename)
            if success:
                return {"message": "Foto de portada establecida exitosamente"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo establecer la foto de portada"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error estableciendo portada: {str(e)}"
            )
    
    async def publish_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Publicar galería"""
        try:
            gallery = self.service.publish_gallery(db, gallery_id)
            return self._build_gallery_response(gallery)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error publicando galería: {str(e)}"
            )
    
    async def unpublish_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Despublicar galería"""
        try:
            gallery = self.service.unpublish_gallery(db, gallery_id)
            return self._build_gallery_response(gallery)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error despublicando galería: {str(e)}"
            )
    
    async def toggle_featured(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Alternar estado destacado"""
        try:
            gallery = self.service.toggle_featured(db, gallery_id)
            return self._build_gallery_response(gallery)
            
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
    
    async def get_galleries_by_category(
        self, 
        category_id: int, 
        limit: int, 
        is_published: bool, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías de una categoría"""
        galleries = self.service.get_galleries_by_category(db, category_id, limit, is_published)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_featured_galleries(
        self, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías destacadas"""
        galleries = self.service.get_featured_galleries(db, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_recent_galleries(
        self, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías recientes"""
        galleries = self.service.get_recent_galleries(db, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_popular_galleries(
        self, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías populares"""
        galleries = self.service.get_popular_galleries(db, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_galleries_by_academic_unit(
        self, 
        academic_unit_id: int, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías de una unidad académica"""
        galleries = self.service.get_galleries_by_academic_unit(db, academic_unit_id, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_galleries_by_photographer(
        self, 
        photographer: str, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías de un fotógrafo"""
        galleries = self.service.get_galleries_by_photographer(db, photographer, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def get_related_galleries(
        self, 
        gallery_id: int, 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Obtener galerías relacionadas"""
        gallery = self.service.get_gallery(db, gallery_id)
        if not gallery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Galería no encontrada"
            )
        
        related_galleries = self.service.get_related_galleries(db, gallery, limit)
        return [self._build_gallery_response(gal, minimal=True) for gal in related_galleries]
    
    async def search_galleries_by_tags(
        self, 
        tags: List[str], 
        limit: int, 
        db: Session
    ) -> List[GalleryResponse]:
        """Buscar galerías por tags"""
        galleries = self.service.search_galleries_by_tags(db, tags, limit)
        return [self._build_gallery_response(gallery, minimal=True) for gallery in galleries]
    
    async def like_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Dar like a galería"""
        try:
            gallery = self.service.like_gallery(db, gallery_id)
            return self._build_gallery_response(gallery, minimal=True)
            
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
    
    async def share_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Compartir galería"""
        try:
            gallery = self.service.share_gallery(db, gallery_id)
            return self._build_gallery_response(gallery, minimal=True)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error compartiendo galería: {str(e)}"
            )
    
    async def download_gallery(self, gallery_id: int, db: Session) -> GalleryResponse:
        """Registrar descarga de galería"""
        try:
            gallery = self.service.download_gallery(db, gallery_id)
            return self._build_gallery_response(gallery, minimal=True)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error registrando descarga: {str(e)}"
            )
    
    async def get_gallery_file_urls(
        self, 
        gallery_id: int, 
        db: Session
    ) -> Dict[str, Any]:
        """Obtener URLs de archivos de galería"""
        try:
            urls = self.service.get_gallery_file_urls(db, gallery_id)
            return urls
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo URLs: {str(e)}"
            )
    
    async def get_statistics(self, db: Session) -> GalleryStatsResponse:
        """Obtener estadísticas de galerías"""
        try:
            stats = self.service.get_statistics(db)
            return GalleryStatsResponse(**stats)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error obteniendo estadísticas: {str(e)}"
            )
    
    async def bulk_update_status(
        self, 
        gallery_ids: List[int], 
        status: str, 
        db: Session
    ) -> Dict[str, Any]:
        """Actualización masiva de estado"""
        try:
            updated = self.service.bulk_update_status(db, gallery_ids, status)
            return {
                "message": f"{updated} galerías actualizadas",
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
        gallery_ids: List[int], 
        is_featured: bool, 
        db: Session
    ) -> Dict[str, Any]:
        """Actualización masiva de destacados"""
        try:
            updated = self.service.bulk_feature(db, gallery_ids, is_featured)
            return {
                "message": f"{updated} galerías actualizadas",
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
    
    async def cleanup_empty_galleries(self, db: Session) -> Dict[str, Any]:
        """Limpiar galerías vacías"""
        try:
            deleted_count = self.service.cleanup_empty_galleries(db)
            return {
                "message": f"{deleted_count} galerías vacías eliminadas",
                "deleted_count": deleted_count
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error limpiando galerías: {str(e)}"
            )
    
    async def optimize_gallery_images(
        self, 
        gallery_id: int, 
        db: Session
    ) -> Dict[str, Any]:
        """Optimizar imágenes de galería"""
        try:
            result = await self.service.optimize_gallery_images(db, gallery_id)
            return result
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error optimizando imágenes: {str(e)}"
            )
    
    async def duplicate_gallery(
        self, 
        gallery_id: int, 
        new_title: str, 
        copy_photos: bool, 
        db: Session
    ) -> GalleryResponse:
        """Duplicar galería"""
        try:
            gallery = self.service.duplicate_gallery(db, gallery_id, new_title, copy_photos)
            return self._build_gallery_response(gallery)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error duplicando galería: {str(e)}"
            )
    
    def _build_gallery_response(
        self, 
        gallery, 
        minimal: bool = False,
        include_photos: bool = False,
        photos_limit: int = 10
    ) -> GalleryResponse:
        """Construir respuesta de galería"""
        response_data = {
            'id': gallery.id,
            'uuid': gallery.uuid,
            'title': gallery.title,
            'subtitle': gallery.subtitle,
            'description': gallery.description,
            'slug': gallery.slug,
            'photos': gallery.photos[:photos_limit] if include_photos and gallery.photos else [],
            'photo_count': gallery.photo_count,
            'total_size_mb': gallery.total_size_mb,
            'cover_photo': gallery.cover_photo,
            'thumbnail_url': gallery.thumbnail_url,
            'event_date': gallery.event_date,
            'content_type': gallery.content_type,
            'tags': gallery.tags,
            'photographer': gallery.photographer,
            'camera_info': gallery.camera_info,
            'location': gallery.location,
            'is_published': gallery.is_published,
            'is_featured': gallery.is_featured,
            'is_public': gallery.is_public,
            'status': gallery.status,
            'approval_required': gallery.approval_required,
            'seo_title': gallery.seo_title,
            'seo_description': gallery.seo_description,
            'allow_download': gallery.allow_download,
            'allow_comments': gallery.allow_comments,
            'watermark_enabled': gallery.watermark_enabled,
            'view_count': gallery.view_count,
            'like_count': gallery.like_count,
            'share_count': gallery.share_count,
            'download_count': gallery.download_count,
            'category_id': gallery.category_id,
            'author_id': gallery.author_id,
            'created_at': gallery.created_at,
            'updated_at': gallery.updated_at
        }
        
        if not minimal:
            if hasattr(gallery, 'category') and gallery.category:
                response_data['category'] = {
                    'id': gallery.category.id,
                    'name': gallery.category.name,
                    'display_name': gallery.category.display_name,
                    'slug': gallery.category.slug,
                    'color': gallery.category.color
                }
            
            if hasattr(gallery, 'author') and gallery.author:
                response_data['author'] = {
                    'id': gallery.author.id,
                    'first_name': gallery.author.first_name,
                    'last_name': gallery.author.last_name,
                    'profile_photo': gallery.author.profile_photo,
                    'position': gallery.author.position
                }
        
        return GalleryResponse(**response_data)


# Instancia global del controlador
gallery_controller = GalleryController()