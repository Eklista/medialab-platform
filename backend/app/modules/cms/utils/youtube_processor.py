"""
CMS YouTube Processor - Procesamiento de URLs y metadata de YouTube
"""
import re
import httpx
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs


class YouTubeProcessor:
    """Procesador de URLs y metadata de YouTube"""
    
    def __init__(self):
        self.youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)'
        ]
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extraer video ID de URL de YouTube"""
        if not url:
            return None
        
        # Limpiar URL
        url = url.strip()
        
        # Probar cada patrón
        for pattern in self.youtube_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def validate_youtube_url(self, url: str) -> bool:
        """Validar si la URL es de YouTube válida"""
        return self.extract_video_id(url) is not None
    
    def generate_embed_url(self, video_id: str, **params) -> str:
        """Generar URL de embed para YouTube"""
        base_url = f"https://www.youtube.com/embed/{video_id}"
        
        # Parámetros por defecto
        default_params = {
            'rel': 0,  # No mostrar videos relacionados
            'modestbranding': 1,  # Branding mínimo
            'fs': 1,  # Permitir pantalla completa
            'cc_load_policy': 1,  # Cargar subtítulos si están disponibles
            'iv_load_policy': 3,  # No mostrar anotaciones
            'autohide': 1  # Auto-ocultar controles
        }
        
        # Combinar con parámetros personalizados
        all_params = {**default_params, **params}
        
        # Construir query string
        param_string = '&'.join([f"{k}={v}" for k, v in all_params.items()])
        
        return f"{base_url}?{param_string}"
    
    def generate_thumbnail_url(self, video_id: str, quality: str = "maxresdefault") -> str:
        """
        Generar URL de thumbnail de YouTube
        
        Calidades disponibles:
        - maxresdefault: 1280x720 (si está disponible)
        - sddefault: 640x480
        - hqdefault: 480x360
        - mqdefault: 320x180
        - default: 120x90
        """
        return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
    
    def get_multiple_thumbnail_urls(self, video_id: str) -> Dict[str, str]:
        """Obtener URLs de thumbnails en múltiples calidades"""
        qualities = {
            'maxres': 'maxresdefault',
            'standard': 'sddefault', 
            'high': 'hqdefault',
            'medium': 'mqdefault',
            'default': 'default'
        }
        
        return {
            name: self.generate_thumbnail_url(video_id, quality)
            for name, quality in qualities.items()
        }
    
    async def get_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """
        Obtener metadata básica del video (sin API key)
        Usando oEmbed endpoint de YouTube
        """
        try:
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(oembed_url, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Procesar metadata
                    metadata = {
                        'title': data.get('title', ''),
                        'author_name': data.get('author_name', ''),
                        'author_url': data.get('author_url', ''),
                        'thumbnail_url': data.get('thumbnail_url', ''),
                        'html': data.get('html', ''),
                        'width': data.get('width'),
                        'height': data.get('height'),
                        'provider_name': data.get('provider_name'),
                        'provider_url': data.get('provider_url')
                    }
                    
                    # Extraer dimensiones del HTML si están disponibles
                    if metadata['width'] and metadata['height']:
                        metadata['aspect_ratio'] = f"{metadata['width']}:{metadata['height']}"
                    
                    return {
                        'success': True,
                        'video_id': video_id,
                        'metadata': metadata
                    }
                else:
                    return {
                        'success': False,
                        'error': f"YouTube API returned status {response.status_code}",
                        'video_id': video_id
                    }
        
        except httpx.RequestError as e:
            return {
                'success': False,
                'error': f"Network error: {str(e)}",
                'video_id': video_id
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'video_id': video_id
            }
    
    def process_youtube_url(self, url: str) -> Dict[str, Any]:
        """
        Procesar URL de YouTube y extraer toda la información útil
        """
        # Validar y extraer video ID
        video_id = self.extract_video_id(url)
        
        if not video_id:
            return {
                'success': False,
                'error': 'URL de YouTube inválida',
                'original_url': url
            }
        
        # Generar URLs
        embed_url = self.generate_embed_url(video_id)
        thumbnails = self.get_multiple_thumbnail_urls(video_id)
        
        return {
            'success': True,
            'video_id': video_id,
            'original_url': url,
            'embed_url': embed_url,
            'watch_url': f"https://www.youtube.com/watch?v={video_id}",
            'thumbnail_urls': thumbnails,
            'thumbnail_url': thumbnails['high']  # URL principal
        }
    
    def generate_structured_data(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generar datos estructurados para SEO (Schema.org VideoObject)
        """
        return {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": video_data.get('title', ''),
            "description": video_data.get('description', ''),
            "thumbnailUrl": video_data.get('thumbnail_url', ''),
            "embedUrl": video_data.get('embed_url', ''),
            "uploadDate": video_data.get('created_at', ''),
            "publisher": {
                "@type": "Organization",
                "name": "Universidad Galileo MediaLab",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://medialab.galileo.edu/logo.png"
                }
            }
        }
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """Extraer ID de playlist de YouTube"""
        playlist_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*list=([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in playlist_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def is_youtube_shorts(self, url: str) -> bool:
        """Detectar si es un YouTube Short"""
        shorts_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)'
        return re.search(shorts_pattern, url) is not None
    
    def get_video_quality_from_url(self, url: str) -> Optional[str]:
        """Extraer calidad de video de parámetros de URL"""
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            # Buscar parámetros de calidad
            if 'vq' in params:
                return params['vq'][0]
            elif 'quality' in params:
                return params['quality'][0]
            
            return None
        except:
            return None


# Instancia global del procesador
youtube_processor = YouTubeProcessor()