"""
CMS Image Processor - Manejo y procesamiento de imágenes
"""
import os
import uuid
import shutil
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from PIL import Image, ImageOps, ExifTags
from PIL.ExifTags import TAGS
import pillow_heif
import aiofiles

from app.core.config import get_settings


# Registrar soporte HEIF/HEIC
pillow_heif.register_heif_opener()


class ImageProcessor:
    """Procesador de imágenes con optimización y conversión"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_upload_path = Path(self.settings.storage.UPLOAD_DIR)
        
        # Configuración de tamaños
        self.max_original_size = 1500  # píxeles
        self.max_file_size = 2 * 1024 * 1024  # 2MB
        self.thumbnail_size = (300, 300)
        self.webp_quality = 85
        self.jpg_quality = 90
        
        # Formatos soportados
        self.supported_formats = {
            'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 
            'tiff', 'heic', 'heif', 'avif'
        }
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Crear directorios necesarios"""
        directories = [
            self.base_upload_path / "original",
            self.base_upload_path / "processed", 
            self.base_upload_path / "thumbnails",
            self.base_upload_path / "temp"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def process_image(
        self, 
        file_content: bytes, 
        original_filename: str,
        gallery_slug: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Procesar imagen completa: original -> processed -> thumbnail
        """
        try:
            # Validar formato
            if not self._is_supported_format(original_filename):
                raise ValueError(f"Formato no soportado: {original_filename}")
            
            # Generar nombres únicos
            file_uuid = str(uuid.uuid4())
            file_extension = Path(original_filename).suffix.lower()
            base_filename = f"{file_uuid}"
            
            # Crear directorio de galería
            gallery_dir = self._create_gallery_directory(gallery_slug)
            
            # Procesar imagen original
            original_path = await self._process_original(
                file_content, base_filename, gallery_dir, file_extension
            )
            
            # Crear versión procesada (WebP)
            processed_path = await self._create_processed_version(
                original_path, base_filename, gallery_dir
            )
            
            # Crear thumbnail
            thumbnail_path = await self._create_thumbnail(
                original_path, base_filename, gallery_dir
            )
            
            # Extraer metadata
            image_metadata = await self._extract_metadata(original_path)
            
            # Calcular tamaños de archivo
            file_sizes = self._calculate_file_sizes([
                original_path, processed_path, thumbnail_path
            ])
            
            return {
                "success": True,
                "filename": f"{base_filename}.webp",
                "original_filename": original_filename,
                "uuid": file_uuid,
                "paths": {
                    "original": str(original_path.relative_to(self.base_upload_path)),
                    "processed": str(processed_path.relative_to(self.base_upload_path)),
                    "thumbnail": str(thumbnail_path.relative_to(self.base_upload_path))
                },
                "metadata": {
                    **image_metadata,
                    "file_sizes": file_sizes,
                    "processed_at": datetime.utcnow().isoformat(),
                    "gallery_slug": gallery_slug
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_filename": original_filename
            }
    
    def _is_supported_format(self, filename: str) -> bool:
        """Verificar si el formato es soportado"""
        extension = Path(filename).suffix.lower().lstrip('.')
        return extension in self.supported_formats
    
    def _create_gallery_directory(self, gallery_slug: str) -> Path:
        """Crear directorio específico para la galería"""
        gallery_dir = gallery_slug or f"gallery_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        directories = [
            self.base_upload_path / "original" / gallery_dir,
            self.base_upload_path / "processed" / gallery_dir,
            self.base_upload_path / "thumbnails" / gallery_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        return Path(gallery_dir)
    
    async def _process_original(
        self, 
        file_content: bytes, 
        base_filename: str, 
        gallery_dir: Path,
        original_extension: str
    ) -> Path:
        """Procesar imagen original: reescalar y optimizar como JPG"""
        
        # Guardar temporalmente
        temp_path = self.base_upload_path / "temp" / f"{base_filename}_temp{original_extension}"
        
        async with aiofiles.open(temp_path, 'wb') as f:
            await f.write(file_content)
        
        try:
            # Abrir imagen
            with Image.open(temp_path) as img:
                # Corregir orientación EXIF
                img = ImageOps.exif_transpose(img)
                
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Crear fondo blanco para transparencias
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Reescalar manteniendo aspecto
                img = self._resize_image(img, self.max_original_size)
                
                # Guardar como JPG optimizado
                original_path = self.base_upload_path / "original" / gallery_dir / f"{base_filename}.jpg"
                
                img.save(
                    original_path, 
                    'JPEG',
                    quality=self.jpg_quality,
                    optimize=True,
                    progressive=True
                )
                
                return original_path
                
        finally:
            # Limpiar archivo temporal
            if temp_path.exists():
                temp_path.unlink()
    
    async def _create_processed_version(
        self, 
        original_path: Path, 
        base_filename: str, 
        gallery_dir: Path
    ) -> Path:
        """Crear versión procesada en WebP"""
        processed_path = self.base_upload_path / "processed" / gallery_dir / f"{base_filename}.webp"
        
        with Image.open(original_path) as img:
            # Optimizar para WebP
            img.save(
                processed_path,
                'WEBP',
                quality=self.webp_quality,
                optimize=True,
                method=6  # Mejor compresión
            )
        
        return processed_path
    
    async def _create_thumbnail(
        self, 
        original_path: Path, 
        base_filename: str, 
        gallery_dir: Path
    ) -> Path:
        """Crear thumbnail en WebP"""
        thumbnail_path = self.base_upload_path / "thumbnails" / gallery_dir / f"{base_filename}.webp"
        
        with Image.open(original_path) as img:
            # Crear thumbnail cuadrado con crop inteligente
            thumbnail = ImageOps.fit(
                img, 
                self.thumbnail_size, 
                Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )
            
            thumbnail.save(
                thumbnail_path,
                'WEBP',
                quality=85,
                optimize=True
            )
        
        return thumbnail_path
    
    def _resize_image(self, img: Image.Image, max_size: int) -> Image.Image:
        """Reescalar imagen manteniendo aspecto"""
        width, height = img.size
        
        # Si la imagen es más pequeña, no hacer nada
        if width <= max_size and height <= max_size:
            return img
        
        # Calcular nueva dimensión
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    async def _extract_metadata(self, image_path: Path) -> Dict[str, Any]:
        """Extraer metadata de la imagen"""
        metadata = {}
        
        try:
            with Image.open(image_path) as img:
                # Información básica
                metadata.update({
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'orientation': self._get_orientation(img.width, img.height)
                })
                
                # EXIF data
                exif_data = img.getexif()
                if exif_data:
                    exif_dict = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_dict[tag] = value
                    
                    # Extraer datos útiles
                    metadata.update({
                        'camera_make': exif_dict.get('Make'),
                        'camera_model': exif_dict.get('Model'),
                        'datetime_taken': exif_dict.get('DateTime'),
                        'software': exif_dict.get('Software'),
                        'flash': exif_dict.get('Flash'),
                        'focal_length': exif_dict.get('FocalLength'),
                        'iso': exif_dict.get('ISOSpeedRatings'),
                        'exposure_time': exif_dict.get('ExposureTime'),
                        'f_number': exif_dict.get('FNumber')
                    })
        
        except Exception as e:
            metadata['metadata_error'] = str(e)
        
        return metadata
    
    def _get_orientation(self, width: int, height: int) -> str:
        """Determinar orientación de la imagen"""
        if width > height:
            return "landscape"
        elif height > width:
            return "portrait"
        else:
            return "square"
    
    def _calculate_file_sizes(self, file_paths: List[Path]) -> Dict[str, int]:
        """Calcular tamaños de archivos"""
        sizes = {}
        for path in file_paths:
            if path.exists():
                size = path.stat().st_size
                sizes[path.stem] = size
        return sizes
    
    async def delete_image_files(self, gallery_slug: str, filename: str):
        """Eliminar todos los archivos de una imagen"""
        base_name = Path(filename).stem
        
        files_to_delete = [
            self.base_upload_path / "original" / gallery_slug / f"{base_name}.jpg",
            self.base_upload_path / "processed" / gallery_slug / f"{base_name}.webp",
            self.base_upload_path / "thumbnails" / gallery_slug / f"{base_name}.webp"
        ]
        
        for file_path in files_to_delete:
            if file_path.exists():
                file_path.unlink()
    
    async def cleanup_gallery_directory(self, gallery_slug: str):
        """Limpiar directorio completo de galería"""
        directories = [
            self.base_upload_path / "original" / gallery_slug,
            self.base_upload_path / "processed" / gallery_slug,
            self.base_upload_path / "thumbnails" / gallery_slug
        ]
        
        for directory in directories:
            if directory.exists():
                shutil.rmtree(directory)
    
    def get_file_urls(self, gallery_slug: str, filename: str) -> Dict[str, str]:
        """Obtener URLs de archivos"""
        base_name = Path(filename).stem
        base_url = self.settings.BASE_URL
        
        return {
            'original': f"{base_url}/uploads/original/{gallery_slug}/{base_name}.jpg",
            'processed': f"{base_url}/uploads/processed/{gallery_slug}/{base_name}.webp",
            'thumbnail': f"{base_url}/uploads/thumbnails/{gallery_slug}/{base_name}.webp"
        }
    
    async def optimize_existing_image(self, image_path: Path) -> bool:
        """Optimizar imagen existente"""
        try:
            with Image.open(image_path) as img:
                # Reescalar si es necesario
                if img.width > self.max_original_size or img.height > self.max_original_size:
                    img = self._resize_image(img, self.max_original_size)
                
                # Guardar optimizada
                if image_path.suffix.lower() == '.webp':
                    img.save(image_path, 'WEBP', quality=self.webp_quality, optimize=True)
                else:
                    img.save(image_path, 'JPEG', quality=self.jpg_quality, optimize=True)
                
                return True
        except Exception:
            return False


# Instancia global del procesador
image_processor = ImageProcessor()