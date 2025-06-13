"""
CMS Gallery Service - Lógica de negocio para galerías y manejo de archivos
"""
import asyncio
from typing import Optional, List, Dict, Any, BinaryIO
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import UploadFile

from app.modules.cms.models import Gallery, Category
from app.modules.cms.repositories.gallery_repository import GalleryRepository
from app.modules.cms.repositories.category_repository import CategoryRepository
from app.modules.cms.schemas.gallery_schemas import (
    GalleryCreate, GalleryUpdate, GallerySearchParams, PhotoUpload
)
from app.modules.cms.utils.slug_generator import slug_generator
from app.modules.cms.utils.image_processor import image_processor
from app.modules.users.models import InternalUser


class GalleryService:
    """Servicio para lógica de negocio de galerías"""
    
    def __init__(self):
        self.gallery_repository = GalleryRepository()
        self.category_repository = CategoryRepository()
    
    def create_gallery(self, db: Session, gallery_data: GalleryCreate, author_id: int) -> Gallery:
        """Crear nueva galería"""
        # Validar categoría
        category = self.category_repository.get_by_id(db, gallery_data.category_id, include_relations=False)
        if not category or not category.is_active:
            raise ValueError("Categoría no encontrada o inactiva")
        
        # Validar autor
        author = db.query(InternalUser).filter(
            InternalUser.id == author_id,
            InternalUser.is_active == True
        ).first()
        if not author:
            raise ValueError("Autor no encontrado o inactivo")
        
        # Generar slug único
        slug = slug_generator.generate_gallery_slug(
            gallery_data.title,
            gallery_data.event_date,
            db
        )
        
        # Preparar datos de la galería
        gallery_dict = gallery_data.dict()
        gallery_dict.update({
            'author_id': author_id,
            'slug': slug,
            'status': 'draft',
            'is_published': False,
            'photo_count': 0,
            'photos': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        # Crear galería
        gallery = self.gallery_repository.create(db, gallery_dict)
        db.commit()
        
        return gallery
    
    def get_gallery(self, db: Session, gallery_id: int) -> Optional[Gallery]:
        """Obtener galería por ID"""
        return self.gallery_repository.get_by_id(db, gallery_id)
    
    def get_gallery_by_uuid(self, db: Session, uuid: str) -> Optional[Gallery]:
        """Obtener galería por UUID"""
        return self.gallery_repository.get_by_uuid(db, uuid)
    
    def get_gallery_by_slug(self, db: Session, slug: str, increment_views: bool = False) -> Optional[Gallery]:
        """Obtener galería por slug con opción de incrementar vistas"""
        gallery = self.gallery_repository.get_by_slug(db, slug)
        
        if gallery and increment_views and gallery.is_published:
            self.gallery_repository.increment_view_count(db, gallery.id)
            db.commit()
        
        return gallery
    
    def get_galleries(
        self, 
        db: Session, 
        params: GallerySearchParams
    ) -> Dict[str, Any]:
        """Obtener lista paginada de galerías"""
        skip = (params.page - 1) * params.per_page
        
        galleries, total = self.gallery_repository.get_all(
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
            min_photos=params.min_photos,
            max_photos=params.max_photos,
            photographer=params.photographer,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            minimal=params.minimal,
            include_photos=params.include_photos,
            include_author=params.include_author,
            include_category=params.include_category,
            photos_limit=params.photos_limit
        )
        
        return {
            'galleries': galleries,
            'total': total,
            'page': params.page,
            'per_page': params.per_page,
            'pages': (total + params.per_page - 1) // params.per_page,
            'has_next': params.page * params.per_page < total,
            'has_prev': params.page > 1
        }
    
    def update_gallery(
        self, 
        db: Session, 
        gallery_id: int, 
        update_data: GalleryUpdate
    ) -> Gallery:
        """Actualizar galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        # Preparar datos de actualización
        update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        
        # Actualizar slug si cambió el título o fecha
        if ('title' in update_dict or 'event_date' in update_dict):
            new_title = update_dict.get('title', gallery.title)
            new_date = update_dict.get('event_date', gallery.event_date)
            
            new_slug = slug_generator.update_slug_if_needed(
                gallery.slug,
                f"{new_date}-{new_title}",
                db,
                Gallery,
                gallery_id
            )
            update_dict['slug'] = new_slug
        
        # Actualizar timestamp
        update_dict['updated_at'] = datetime.utcnow()
        
        # Aplicar actualización
        updated_gallery = self.gallery_repository.update(db, gallery, update_dict)
        db.commit()
        
        # Actualizar estadísticas si cambió la categoría
        if 'category_id' in update_dict:
            if gallery.category_id != update_dict['category_id']:
                self.category_repository.update_content_statistics(db, gallery.category_id)
                self.category_repository.update_content_statistics(db, update_dict['category_id'])
        
        return updated_gallery
    
    def delete_gallery(self, db: Session, gallery_id: int) -> bool:
        """Eliminar galería y sus archivos"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        category_id = gallery.category_id
        
        # Eliminar archivos físicos si existen
        if gallery.slug:
            try:
                asyncio.create_task(
                    image_processor.cleanup_gallery_directory(gallery.slug)
                )
            except Exception as e:
                print(f"Error limpiando archivos de galería {gallery.slug}: {e}")
        
        # Eliminar galería
        success = self.gallery_repository.delete(db, gallery)
        if success:
            db.commit()
            # Actualizar estadísticas de categoría
            self.category_repository.update_content_statistics(db, category_id)
        
        return success
    
    async def upload_photos(
        self, 
        db: Session, 
        gallery_id: int, 
        files: List[UploadFile],
        photo_metadata: List[PhotoUpload] = None
    ) -> Dict[str, Any]:
        """Subir múltiples fotos a una galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        if not gallery.slug:
            raise ValueError("Galería sin slug asignado")
        
        results = {
            'successful': [],
            'failed': [],
            'total_uploaded': 0,
            'processing_time': 0,
            'total_size': 0
        }
        
        start_time = datetime.now()
        
        # Procesar cada archivo
        for i, file in enumerate(files):
            try:
                # Leer contenido del archivo
                file_content = await file.read()
                results['total_size'] += len(file_content)
                
                # Obtener metadata si está disponible
                metadata = {}
                if photo_metadata and i < len(photo_metadata):
                    metadata = photo_metadata[i].dict()
                
                # Procesar imagen
                processed_result = await image_processor.process_image(
                    file_content,
                    file.filename,
                    gallery.slug,
                    metadata
                )
                
                if processed_result['success']:
                    # Preparar datos de la foto
                    photo_data = {
                        'filename': processed_result['filename'],
                        'original_filename': file.filename,
                        'title': metadata.get('title', ''),
                        'description': metadata.get('description', ''),
                        'original_path': processed_result['paths']['original'],
                        'processed_path': processed_result['paths']['processed'],
                        'thumbnail_path': processed_result['paths']['thumbnail'],
                        'width': processed_result['metadata'].get('width', 0),
                        'height': processed_result['metadata'].get('height', 0),
                        'file_size': len(file_content),
                        'orientation': processed_result['metadata'].get('orientation', 'landscape'),
                        'format': processed_result['metadata'].get('format', 'jpg'),
                        'camera_info': processed_result['metadata'].get('camera_make', ''),
                        'taken_at': processed_result['metadata'].get('datetime_taken'),
                        'processed_at': datetime.utcnow(),
                        'sort_order': metadata.get('sort_order', gallery.photo_count)
                    }
                    
                    # Agregar foto a la galería
                    self.gallery_repository.add_photos(db, gallery_id, [photo_data])
                    
                    results['successful'].append(processed_result)
                    results['total_uploaded'] += 1
                    
                    # Establecer como portada si es la primera foto
                    if gallery.photo_count == 0:
                        self.gallery_repository.set_cover_photo(db, gallery_id, processed_result['filename'])
                
                else:
                    results['failed'].append({
                        'filename': file.filename,
                        'error': processed_result.get('error', 'Error desconocido')
                    })
                
            except Exception as e:
                results['failed'].append({
                    'filename': file.filename,
                    'error': str(e)
                })
        
        # Calcular tiempo de procesamiento
        end_time = datetime.now()
        results['processing_time'] = (end_time - start_time).total_seconds()
        
        # Confirmar cambios
        db.commit()
        
        # Actualizar estadísticas de categoría
        self.category_repository.update_content_statistics(db, gallery.category_id)
        
        return results
    
    async def delete_photo(self, db: Session, gallery_id: int, photo_filename: str) -> bool:
        """Eliminar foto de galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        # Eliminar archivos físicos
        try:
            await image_processor.delete_image_files(gallery.slug, photo_filename)
        except Exception as e:
            print(f"Error eliminando archivos físicos: {e}")
        
        # Remover de la base de datos
        self.gallery_repository.remove_photo(db, gallery_id, photo_filename)
        db.commit()
        
        # Actualizar estadísticas
        self.category_repository.update_content_statistics(db, gallery.category_id)
        
        return True
    
    def reorder_photos(
        self, 
        db: Session, 
        gallery_id: int, 
        photo_orders: List[Dict[str, int]]
    ) -> bool:
        """Reordenar fotos en galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        self.gallery_repository.reorder_photos(db, gallery_id, photo_orders)
        db.commit()
        
        return True
    
    def update_photo_metadata(
        self, 
        db: Session, 
        gallery_id: int, 
        photo_filename: str, 
        metadata: Dict[str, Any]
    ) -> bool:
        """Actualizar metadata de una foto"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        self.gallery_repository.update_photo_metadata(db, gallery_id, photo_filename, metadata)
        db.commit()
        
        return True
    
    def set_cover_photo(self, db: Session, gallery_id: int, photo_filename: str) -> bool:
        """Establecer foto de portada"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        self.gallery_repository.set_cover_photo(db, gallery_id, photo_filename)
        db.commit()
        
        return True
    
    def publish_gallery(self, db: Session, gallery_id: int) -> Gallery:
        """Publicar galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        # Validar que tenga contenido mínimo
        if not gallery.title or gallery.photo_count == 0:
            raise ValueError("La galería debe tener título y al menos una foto para ser publicada")
        
        update_data = {
            'is_published': True,
            'status': 'published',
            'updated_at': datetime.utcnow()
        }
        
        updated_gallery = self.gallery_repository.update(db, gallery, update_data)
        db.commit()
        
        # Actualizar estadísticas
        self.category_repository.update_content_statistics(db, gallery.category_id)
        
        return updated_gallery
    
    def unpublish_gallery(self, db: Session, gallery_id: int) -> Gallery:
        """Despublicar galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        update_data = {
            'is_published': False,
            'status': 'draft',
            'updated_at': datetime.utcnow()
        }
        
        updated_gallery = self.gallery_repository.update(db, gallery, update_data)
        db.commit()
        
        # Actualizar estadísticas
        self.category_repository.update_content_statistics(db, gallery.category_id)
        
        return updated_gallery
    
    def toggle_featured(self, db: Session, gallery_id: int) -> Gallery:
        """Alternar estado destacado"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        update_data = {
            'is_featured': not gallery.is_featured,
            'updated_at': datetime.utcnow()
        }
        
        updated_gallery = self.gallery_repository.update(db, gallery, update_data)
        db.commit()
        
        return updated_gallery
    
    def get_galleries_by_category(
        self, 
        db: Session, 
        category_id: int, 
        limit: int = 20,
        is_published: bool = True
    ) -> List[Gallery]:
        """Obtener galerías de una categoría"""
        return self.gallery_repository.get_by_category(db, category_id, is_published, limit)
    
    def get_featured_galleries(self, db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías destacadas"""
        return self.gallery_repository.get_featured(db, limit)
    
    def get_recent_galleries(self, db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías más recientes"""
        return self.gallery_repository.get_recent(db, limit)
    
    def get_popular_galleries(self, db: Session, limit: int = 10) -> List[Gallery]:
        """Obtener galerías más populares"""
        return self.gallery_repository.get_popular(db, limit)
    
    def get_galleries_by_academic_unit(
        self, 
        db: Session, 
        academic_unit_id: int, 
        limit: int = 20
    ) -> List[Gallery]:
        """Obtener galerías de una unidad académica"""
        return self.gallery_repository.get_by_academic_unit(db, academic_unit_id, limit)
    
    def get_galleries_by_photographer(
        self, 
        db: Session, 
        photographer: str, 
        limit: int = 20
    ) -> List[Gallery]:
        """Obtener galerías de un fotógrafo"""
        return self.gallery_repository.get_by_photographer(db, photographer, limit)
    
    def get_related_galleries(self, db: Session, gallery: Gallery, limit: int = 5) -> List[Gallery]:
        """Obtener galerías relacionadas"""
        return self.gallery_repository.get_related(db, gallery, limit)
    
    def search_galleries_by_tags(self, db: Session, tags: List[str], limit: int = 20) -> List[Gallery]:
        """Buscar galerías por tags"""
        return self.gallery_repository.search_by_tags(db, tags, limit)
    
    def like_gallery(self, db: Session, gallery_id: int) -> Gallery:
        """Dar like a una galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        self.gallery_repository.increment_like_count(db, gallery_id)
        db.commit()
        
        return self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
    
    def share_gallery(self, db: Session, gallery_id: int) -> Gallery:
        """Compartir galería (incrementar contador)"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        self.gallery_repository.increment_share_count(db, gallery_id)
        db.commit()
        
        return self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
    
    def download_gallery(self, db: Session, gallery_id: int) -> Gallery:
        """Registrar descarga de galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        if not gallery.allow_download:
            raise ValueError("Descarga no permitida para esta galería")
        
        self.gallery_repository.increment_download_count(db, gallery_id)
        db.commit()
        
        return self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de galerías"""
        return self.gallery_repository.get_statistics(db)
    
    def bulk_update_status(
        self, 
        db: Session, 
        gallery_ids: List[int], 
        status: str
    ) -> int:
        """Actualización masiva de estado"""
        # Validar que todas las galerías existen
        existing_galleries = db.query(Gallery).filter(Gallery.id.in_(gallery_ids)).all()
        if len(existing_galleries) != len(gallery_ids):
            raise ValueError("Algunas galerías no existen")
        
        # Actualizar
        updated = self.gallery_repository.bulk_update_status(db, gallery_ids, status)
        db.commit()
        
        # Actualizar estadísticas de categorías afectadas
        affected_categories = set(gallery.category_id for gallery in existing_galleries)
        for category_id in affected_categories:
            self.category_repository.update_content_statistics(db, category_id)
        
        return updated
    
    def bulk_feature(
        self, 
        db: Session, 
        gallery_ids: List[int], 
        is_featured: bool
    ) -> int:
        """Actualización masiva de destacados"""
        # Validar que todas las galerías existen
        existing_count = db.query(Gallery).filter(Gallery.id.in_(gallery_ids)).count()
        if existing_count != len(gallery_ids):
            raise ValueError("Algunas galerías no existen")
        
        # Actualizar
        updated = self.gallery_repository.bulk_feature(db, gallery_ids, is_featured)
        db.commit()
        
        return updated
    
    def cleanup_empty_galleries(self, db: Session) -> int:
        """Limpiar galerías vacías"""
        empty_galleries = self.gallery_repository.get_empty_galleries(db)
        
        deleted_count = 0
        for gallery in empty_galleries:
            try:
                # Eliminar archivos físicos si existen
                if gallery.slug:
                    asyncio.create_task(
                        image_processor.cleanup_gallery_directory(gallery.slug)
                    )
                
                # Eliminar galería
                self.gallery_repository.delete(db, gallery)
                deleted_count += 1
                
            except Exception as e:
                print(f"Error eliminando galería vacía {gallery.id}: {e}")
        
        if deleted_count > 0:
            db.commit()
        
        return deleted_count
    
    def validate_gallery_access(
        self, 
        db: Session, 
        gallery_id: int, 
        user_academic_units: List[int]
    ) -> bool:
        """Validar acceso de usuario a galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id)
        if not gallery:
            return False
        
        # Verificar acceso a través de la categoría
        return gallery.category.academic_unit_id in user_academic_units
    
    def get_gallery_file_urls(self, db: Session, gallery_id: int) -> Dict[str, List[Dict[str, str]]]:
        """Obtener URLs de archivos de galería para frontend"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        file_urls = []
        for photo in gallery.photos or []:
            urls = image_processor.get_file_urls(gallery.slug, photo['filename'])
            file_urls.append({
                'filename': photo['filename'],
                'title': photo.get('title', ''),
                'description': photo.get('description', ''),
                **urls
            })
        
        return {
            'gallery_slug': gallery.slug,
            'photos': file_urls
        }
    
    async def optimize_gallery_images(self, db: Session, gallery_id: int) -> Dict[str, Any]:
        """Optimizar imágenes existentes de una galería"""
        gallery = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not gallery:
            raise ValueError("Galería no encontrada")
        
        results = {
            'total_optimized': 0,
            'failed': [],
            'size_saved': 0
        }
        
        for photo in gallery.photos or []:
            try:
                # Obtener ruta del archivo original
                original_path = image_processor.base_upload_path / photo['original_path']
                
                if original_path.exists():
                    old_size = original_path.stat().st_size
                    success = await image_processor.optimize_existing_image(original_path)
                    
                    if success:
                        new_size = original_path.stat().st_size
                        results['size_saved'] += (old_size - new_size)
                        results['total_optimized'] += 1
                    else:
                        results['failed'].append(photo['filename'])
                
            except Exception as e:
                results['failed'].append(f"{photo['filename']}: {str(e)}")
        
        return results
    
    def duplicate_gallery(
        self, 
        db: Session, 
        gallery_id: int, 
        new_title: str,
        copy_photos: bool = False
    ) -> Gallery:
        """Duplicar galería"""
        original = self.gallery_repository.get_by_id(db, gallery_id, include_relations=False)
        if not original:
            raise ValueError("Galería original no encontrada")
        
        # Generar slug único
        slug = slug_generator.generate_gallery_slug(
            new_title,
            original.event_date,
            db
        )
        
        # Crear datos de la nueva galería
        new_data = {
            'title': new_title,
            'subtitle': f"{original.subtitle} (Copia)" if original.subtitle else None,
            'description': original.description,
            'category_id': original.category_id,
            'author_id': original.author_id,
            'event_date': original.event_date,
            'content_type': original.content_type,
            'tags': original.tags,
            'photographer': original.photographer,
            'camera_info': original.camera_info,
            'location': original.location,
            'is_featured': False,  # No destacar duplicados
            'is_public': original.is_public,
            'approval_required': original.approval_required,
            'allow_download': original.allow_download,
            'allow_comments': original.allow_comments,
            'watermark_enabled': original.watermark_enabled,
            'slug': slug,
            'status': 'draft',
            'is_published': False,
            'photo_count': 0 if not copy_photos else original.photo_count,
            'photos': [] if not copy_photos else original.photos.copy(),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Crear nueva galería
        new_gallery = self.gallery_repository.create(db, new_data)
        db.commit()
        
        return new_gallery


# Instancia global del servicio
gallery_service = GalleryService()