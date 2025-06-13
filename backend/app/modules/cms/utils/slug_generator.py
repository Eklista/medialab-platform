"""
CMS Slug Generator - Generación de slugs únicos para SEO
"""
import re
import unicodedata
from typing import Optional
from sqlalchemy.orm import Session


class SlugGenerator:
    """Generador de slugs para contenido del CMS"""
    
    def __init__(self):
        # Caracteres a reemplazar
        self.replacements = {
            'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ā': 'a', 'ã': 'a',
            'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e', 'ē': 'e',
            'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i', 'ī': 'i',
            'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o', 'ō': 'o', 'õ': 'o',
            'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u', 'ū': 'u',
            'ñ': 'n', 'ç': 'c',
            'Á': 'A', 'À': 'A', 'Ä': 'A', 'Â': 'A', 'Ā': 'A', 'Ã': 'A',
            'É': 'E', 'È': 'E', 'Ë': 'E', 'Ê': 'E', 'Ē': 'E',
            'Í': 'I', 'Ì': 'I', 'Ï': 'I', 'Î': 'I', 'Ī': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ô': 'O', 'Ō': 'O', 'Õ': 'O',
            'Ú': 'U', 'Ù': 'U', 'Ü': 'U', 'Û': 'U', 'Ū': 'U',
            'Ñ': 'N', 'Ç': 'C'
        }
    
    def generate_slug(self, text: str, max_length: int = 100) -> str:
        """
        Generar slug desde texto
        """
        if not text:
            return ""
        
        # Convertir a minúsculas
        slug = text.lower().strip()
        
        # Reemplazar caracteres especiales
        for char, replacement in self.replacements.items():
            slug = slug.replace(char, replacement)
        
        # Normalizar unicode y remover acentos
        slug = unicodedata.normalize('NFKD', slug)
        slug = ''.join(c for c in slug if not unicodedata.combining(c))
        
        # Reemplazar espacios y caracteres especiales con guiones
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        
        # Remover guiones al inicio y final
        slug = slug.strip('-')
        
        # Limitar longitud
        if len(slug) > max_length:
            slug = slug[:max_length].rstrip('-')
        
        return slug
    
    def generate_unique_slug(
        self, 
        text: str, 
        db: Session, 
        model_class, 
        exclude_id: Optional[int] = None,
        max_length: int = 100
    ) -> str:
        """
        Generar slug único verificando en base de datos
        """
        base_slug = self.generate_slug(text, max_length - 10)  # Reservar espacio para sufijo
        
        if not base_slug:
            base_slug = "content"
        
        slug = base_slug
        counter = 1
        
        while self._slug_exists(slug, db, model_class, exclude_id):
            # Agregar número al final
            suffix = f"-{counter}"
            max_base_length = max_length - len(suffix)
            
            if len(base_slug) > max_base_length:
                base_slug = base_slug[:max_base_length].rstrip('-')
            
            slug = f"{base_slug}{suffix}"
            counter += 1
            
            # Evitar bucle infinito
            if counter > 9999:
                slug = f"{base_slug}-{counter}"
                break
        
        return slug
    
    def _slug_exists(
        self, 
        slug: str, 
        db: Session, 
        model_class, 
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Verificar si el slug ya existe
        """
        query = db.query(model_class).filter(model_class.slug == slug)
        
        if exclude_id:
            query = query.filter(model_class.id != exclude_id)
        
        return query.first() is not None
    
    def generate_category_slug(
        self, 
        name: str, 
        academic_unit_name: str, 
        db: Session,
        exclude_id: Optional[int] = None
    ) -> str:
        """
        Generar slug específico para categorías incluyendo unidad académica
        """
        from app.modules.cms.models import Category
        
        # Crear slug base con unidad académica
        unit_slug = self.generate_slug(academic_unit_name, 20)
        category_slug = self.generate_slug(name, 50)
        
        combined_text = f"{unit_slug}-{category_slug}" if unit_slug and category_slug else (category_slug or unit_slug)
        
        return self.generate_unique_slug(
            combined_text, 
            db, 
            Category, 
            exclude_id,
            max_length=120
        )
    
    def generate_video_slug(
        self, 
        title: str, 
        event_date, 
        db: Session,
        exclude_id: Optional[int] = None
    ) -> str:
        """
        Generar slug específico para videos incluyendo fecha
        """
        from app.modules.cms.models import Video
        
        # Crear slug base con fecha
        date_part = event_date.strftime('%Y-%m-%d') if event_date else ""
        title_slug = self.generate_slug(title, 200)
        
        combined_text = f"{date_part}-{title_slug}" if date_part and title_slug else title_slug
        
        return self.generate_unique_slug(
            combined_text, 
            db, 
            Video, 
            exclude_id,
            max_length=250
        )
    
    def generate_gallery_slug(
        self, 
        title: str, 
        event_date, 
        db: Session,
        exclude_id: Optional[int] = None
    ) -> str:
        """
        Generar slug específico para galerías incluyendo fecha
        """
        from app.modules.cms.models import Gallery
        
        # Crear slug base con fecha
        date_part = event_date.strftime('%Y-%m-%d') if event_date else ""
        title_slug = self.generate_slug(title, 200)
        
        combined_text = f"{date_part}-{title_slug}" if date_part and title_slug else title_slug
        
        return self.generate_unique_slug(
            combined_text, 
            db, 
            Gallery, 
            exclude_id,
            max_length=250
        )
    
    def update_slug_if_needed(
        self, 
        current_slug: str, 
        new_text: str, 
        db: Session,
        model_class,
        record_id: int
    ) -> str:
        """
        Actualizar slug solo si es necesario (título cambió significativamente)
        """
        if not current_slug:
            # No hay slug, generar uno nuevo
            return self.generate_unique_slug(new_text, db, model_class, record_id)
        
        # Generar slug del nuevo texto
        new_base_slug = self.generate_slug(new_text)
        current_base_slug = self.generate_slug(current_slug.split('-')[0] if '-' in current_slug else current_slug)
        
        # Si el slug base cambió significativamente, generar nuevo slug
        if self._slug_changed_significantly(current_base_slug, new_base_slug):
            return self.generate_unique_slug(new_text, db, model_class, record_id)
        
        # Mantener slug actual
        return current_slug
    
    def _slug_changed_significantly(self, old_slug: str, new_slug: str) -> bool:
        """
        Determinar si el cambio en el slug es significativo
        """
        # Si son muy diferentes en longitud
        if abs(len(old_slug) - len(new_slug)) > 10:
            return True
        
        # Si la similitud es muy baja
        similarity = self._calculate_similarity(old_slug, new_slug)
        return similarity < 0.7
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcular similitud entre dos textos (Jaccard similarity)
        """
        if not text1 or not text2:
            return 0.0
        
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def validate_slug(self, slug: str) -> bool:
        """
        Validar formato de slug
        """
        if not slug:
            return False
        
        # Patrón: solo letras, números y guiones, no empieza/termina con guión
        pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
        return bool(re.match(pattern, slug))
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitizar nombre de archivo para uso seguro
        """
        # Mantener extensión
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        
        # Generar slug del nombre
        clean_name = self.generate_slug(name, 100)
        
        # Combinar con extensión
        return f"{clean_name}.{ext.lower()}" if ext else clean_name


# Instancia global del generador
slug_generator = SlugGenerator()