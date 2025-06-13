"""
CMS Router - Endpoints principales para el sistema de gestión de contenidos - CORREGIDO
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, Form, File, UploadFile, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.cms.controllers.category_controller import category_controller
from app.modules.cms.controllers.video_controller import video_controller
from app.modules.cms.controllers.gallery_controller import gallery_controller
from app.modules.cms.schemas import *

# Router principal del CMS
router = APIRouter(prefix="/cms", tags=["CMS"])

# ===================================
# CATEGORY ENDPOINTS
# ===================================

# Endpoints administrativos (Dashboard)
@router.post("/admin/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Crear nueva categoría (Admin)"""
    return await category_controller.create_category(category_data, db)


@router.get("/admin/categories", response_model=CategoryListResponse)
async def get_admin_categories(
    q: Optional[str] = Query(None, description="Búsqueda"),
    academic_unit_id: Optional[int] = Query(None, description="Filtrar por unidad académica"),
    category_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado"),
    is_featured: Optional[bool] = Query(None, description="Filtrar destacadas"),
    page: int = Query(1, ge=1, description="Página"),
    per_page: int = Query(20, ge=1, le=100, description="Items por página"),
    sort_by: str = Query("sort_order", description="Campo de ordenamiento"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Dirección"),
    minimal: bool = Query(False, description="Respuesta mínima"),
    db: Session = Depends(get_db)
):
    """Obtener categorías (Admin)"""
    params = CategorySearchParams(
        q=q, academic_unit_id=academic_unit_id, category_type=category_type,
        is_active=is_active, is_featured=is_featured, page=page, per_page=per_page,
        sort_by=sort_by, sort_order=sort_order, minimal=minimal
    )
    return await category_controller.get_categories(params, db)


@router.get("/admin/categories/{category_id}", response_model=CategoryResponse)
async def get_admin_category(
    category_id: int = Path(..., description="ID de categoría"),
    db: Session = Depends(get_db)
):
    """Obtener categoría por ID (Admin)"""
    return await category_controller.get_category(category_id, db)


@router.put("/admin/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int = Path(..., description="ID de categoría"),
    update_data: CategoryUpdate = ...,
    db: Session = Depends(get_db)
):
    """Actualizar categoría (Admin)"""
    return await category_controller.update_category(category_id, update_data, db)


@router.delete("/admin/categories/{category_id}")
async def delete_category(
    category_id: int = Path(..., description="ID de categoría"),
    db: Session = Depends(get_db)
):
    """Eliminar categoría (Admin)"""
    return await category_controller.delete_category(category_id, db)


@router.patch("/admin/categories/{category_id}/toggle-featured", response_model=CategoryResponse)
async def toggle_category_featured(
    category_id: int = Path(..., description="ID de categoría"),
    db: Session = Depends(get_db)
):
    """Alternar estado destacado (Admin)"""
    return await category_controller.toggle_featured(category_id, db)


@router.patch("/admin/categories/{category_id}/toggle-active", response_model=CategoryResponse)
async def toggle_category_active(
    category_id: int = Path(..., description="ID de categoría"),
    db: Session = Depends(get_db)
):
    """Alternar estado activo (Admin)"""
    return await category_controller.toggle_active(category_id, db)


@router.post("/admin/categories/reorder")
async def reorder_categories(
    academic_unit_id: int = Body(..., description="ID de unidad académica"),
    category_orders: List[dict] = Body(..., description="Nuevo orden de categorías"),
    db: Session = Depends(get_db)
):
    """Reordenar categorías (Admin)"""
    return await category_controller.reorder_categories(academic_unit_id, category_orders, db)


@router.get("/admin/categories/stats", response_model=CategoryStatsResponse)
async def get_category_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas de categorías (Admin)"""
    return await category_controller.get_statistics(db)


# Endpoints públicos (Frontend)
@router.get("/categories", response_model=List[CategoryMinimal])
async def get_public_categories(
    academic_unit_id: Optional[int] = Query(None, description="Filtrar por unidad académica"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener categorías públicas (Frontend)"""
    return await category_controller.get_categories_by_academic_unit(
        academic_unit_id or 0, True, True, db
    )


@router.get("/categories/featured", response_model=List[CategoryResponse])
async def get_featured_categories(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener categorías destacadas (Frontend)"""
    return await category_controller.get_featured_categories(limit, db)


@router.get("/categories/popular", response_model=List[CategoryResponse])
async def get_popular_categories(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener categorías populares (Frontend)"""
    return await category_controller.get_popular_categories(limit, db)


@router.get("/categories/{slug}", response_model=CategoryResponse)
async def get_category_by_slug(
    slug: str = Path(..., description="Slug de categoría"),
    db: Session = Depends(get_db)
):
    """Obtener categoría por slug (Frontend)"""
    return await category_controller.get_category_by_slug(slug, db)


# ===================================
# VIDEO ENDPOINTS
# ===================================

# Endpoints administrativos (Dashboard)
@router.post("/admin/videos", response_model=VideoResponse, status_code=201)
async def create_video(
    video_data: VideoCreate,
    author_id: int = Body(..., description="ID del autor"),
    db: Session = Depends(get_db)
):
    """Crear nuevo video (Admin)"""
    return await video_controller.create_video(video_data, author_id, db)


@router.get("/admin/videos", response_model=VideoListResponse)
async def get_admin_videos(
    q: Optional[str] = Query(None, description="Búsqueda"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    author_id: Optional[int] = Query(None, description="Filtrar por autor"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    is_published: Optional[bool] = Query(None, description="Filtrar publicados"),
    is_featured: Optional[bool] = Query(None, description="Filtrar destacados"),
    page: int = Query(1, ge=1, description="Página"),
    per_page: int = Query(20, ge=1, le=100, description="Items por página"),
    sort_by: str = Query("created_at", description="Campo de ordenamiento"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Dirección"),
    minimal: bool = Query(False, description="Respuesta mínima"),
    db: Session = Depends(get_db)
):
    """Obtener videos (Admin)"""
    params = VideoSearchParams(
        q=q, category_id=category_id, author_id=author_id, status=status,
        is_published=is_published, is_featured=is_featured, page=page, per_page=per_page,
        sort_by=sort_by, sort_order=sort_order, minimal=minimal
    )
    return await video_controller.get_videos(params, db)


@router.get("/admin/videos/{video_id}", response_model=VideoResponse)
async def get_admin_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Obtener video por ID (Admin)"""
    return await video_controller.get_video(video_id, db)


@router.put("/admin/videos/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int = Path(..., description="ID de video"),
    update_data: VideoUpdate = ...,
    db: Session = Depends(get_db)
):
    """Actualizar video (Admin)"""
    return await video_controller.update_video(video_id, update_data, db)


@router.delete("/admin/videos/{video_id}")
async def delete_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Eliminar video (Admin)"""
    return await video_controller.delete_video(video_id, db)


@router.patch("/admin/videos/{video_id}/publish", response_model=VideoResponse)
async def publish_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Publicar video (Admin)"""
    return await video_controller.publish_video(video_id, db)


@router.patch("/admin/videos/{video_id}/unpublish", response_model=VideoResponse)
async def unpublish_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Despublicar video (Admin)"""
    return await video_controller.unpublish_video(video_id, db)


@router.patch("/admin/videos/{video_id}/toggle-featured", response_model=VideoResponse)
async def toggle_video_featured(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Alternar estado destacado (Admin)"""
    return await video_controller.toggle_featured(video_id, db)


@router.post("/admin/videos/bulk/status")
async def bulk_update_video_status(
    video_ids: List[int] = Body(..., description="IDs de videos"),
    status: str = Body(..., description="Nuevo estado"),
    db: Session = Depends(get_db)
):
    """Actualización masiva de estado (Admin)"""
    return await video_controller.bulk_update_status(video_ids, status, db)


@router.get("/admin/videos/stats", response_model=VideoStatsResponse)
async def get_video_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas de videos (Admin)"""
    return await video_controller.get_statistics(db)


# Endpoints públicos (Frontend)
@router.get("/videos", response_model=VideoListResponse)
async def get_public_videos(
    q: Optional[str] = Query(None, description="Búsqueda"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    content_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    page: int = Query(1, ge=1, description="Página"),
    per_page: int = Query(20, ge=1, le=50, description="Items por página"),
    sort_by: str = Query("created_at", description="Campo de ordenamiento"),
    db: Session = Depends(get_db)
):
    """Obtener videos públicos (Frontend)"""
    params = VideoSearchParams(
        q=q, category_id=category_id, content_type=content_type,
        is_published=True, is_public=True, page=page, per_page=per_page,
        sort_by=sort_by, minimal=True
    )
    return await video_controller.get_videos(params, db)


@router.get("/videos/featured", response_model=List[VideoResponse])
async def get_featured_videos(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener videos destacados (Frontend)"""
    return await video_controller.get_featured_videos(limit, db)


@router.get("/videos/recent", response_model=List[VideoResponse])
async def get_recent_videos(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener videos recientes (Frontend)"""
    return await video_controller.get_recent_videos(limit, db)


@router.get("/videos/popular", response_model=List[VideoResponse])
async def get_popular_videos(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener videos populares (Frontend)"""
    return await video_controller.get_popular_videos(limit, db)


@router.get("/videos/{slug}", response_model=VideoResponse)
async def get_video_by_slug(
    slug: str = Path(..., description="Slug de video"),
    increment_views: bool = Query(True, description="Incrementar contador de vistas"),
    db: Session = Depends(get_db)
):
    """Obtener video por slug (Frontend)"""
    return await video_controller.get_video_by_slug(slug, increment_views, db)


@router.get("/videos/{video_id}/related", response_model=List[VideoResponse])
async def get_related_videos(
    video_id: int = Path(..., description="ID de video"),
    limit: int = Query(5, ge=1, le=10, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener videos relacionados (Frontend)"""
    return await video_controller.get_related_videos(video_id, limit, db)


@router.get("/videos/{video_id}/embed", response_model=VideoEmbed)
async def get_video_embed(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Obtener datos para embed (Frontend)"""
    return await video_controller.get_video_embed(video_id, db)


@router.post("/videos/{video_id}/like", response_model=VideoResponse)
async def like_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Dar like a video (Frontend)"""
    return await video_controller.like_video(video_id, db)


@router.post("/videos/{video_id}/share", response_model=VideoResponse)
async def share_video(
    video_id: int = Path(..., description="ID de video"),
    db: Session = Depends(get_db)
):
    """Compartir video (Frontend)"""
    return await video_controller.share_video(video_id, db)


# ===================================
# GALLERY ENDPOINTS
# ===================================

# Endpoints administrativos (Dashboard)
@router.post("/admin/galleries", response_model=GalleryResponse, status_code=201)
async def create_gallery(
    gallery_data: GalleryCreate,
    author_id: int = Body(..., description="ID del autor"),
    db: Session = Depends(get_db)
):
    """Crear nueva galería (Admin)"""
    return await gallery_controller.create_gallery(gallery_data, author_id, db)


@router.get("/admin/galleries", response_model=GalleryListResponse)
async def get_admin_galleries(
    q: Optional[str] = Query(None, description="Búsqueda"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    author_id: Optional[int] = Query(None, description="Filtrar por autor"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    is_published: Optional[bool] = Query(None, description="Filtrar publicadas"),
    photographer: Optional[str] = Query(None, description="Filtrar por fotógrafo"),
    page: int = Query(1, ge=1, description="Página"),
    per_page: int = Query(20, ge=1, le=100, description="Items por página"),
    sort_by: str = Query("created_at", description="Campo de ordenamiento"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Dirección"),
    minimal: bool = Query(False, description="Respuesta mínima"),
    include_photos: bool = Query(False, description="Incluir fotos"),
    db: Session = Depends(get_db)
):
    """Obtener galerías (Admin)"""
    params = GallerySearchParams(
        q=q, category_id=category_id, author_id=author_id, status=status,
        is_published=is_published, photographer=photographer, page=page, per_page=per_page,
        sort_by=sort_by, sort_order=sort_order, minimal=minimal, include_photos=include_photos
    )
    return await gallery_controller.get_galleries(params, db)


@router.get("/admin/galleries/{gallery_id}", response_model=GalleryResponse)
async def get_admin_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Obtener galería por ID (Admin)"""
    return await gallery_controller.get_gallery(gallery_id, db)


@router.put("/admin/galleries/{gallery_id}", response_model=GalleryResponse)
async def update_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    update_data: GalleryUpdate = ...,
    db: Session = Depends(get_db)
):
    """Actualizar galería (Admin)"""
    return await gallery_controller.update_gallery(gallery_id, update_data, db)


@router.delete("/admin/galleries/{gallery_id}")
async def delete_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Eliminar galería (Admin)"""
    return await gallery_controller.delete_gallery(gallery_id, db)


@router.post("/admin/galleries/{gallery_id}/upload", response_model=BulkUploadResponse)
async def upload_photos(
    gallery_id: int = Path(..., description="ID de galería"),
    files: List[UploadFile] = File(..., description="Archivos de imagen"),
    metadata: Optional[str] = Form(None, description="Metadata de fotos en JSON"),
    db: Session = Depends(get_db)
):
    """Subir fotos a galería (Admin)"""
    import json
    
    # Parsear metadata si se proporciona
    photo_metadata = []
    if metadata:
        try:
            metadata_list = json.loads(metadata)
            photo_metadata = [PhotoUpload(**item) for item in metadata_list]
        except (json.JSONDecodeError, ValueError):
            photo_metadata = []
    
    return await gallery_controller.upload_photos(gallery_id, files, photo_metadata, db)


@router.delete("/admin/galleries/{gallery_id}/photos/{photo_filename}")
async def delete_photo(
    gallery_id: int = Path(..., description="ID de galería"),
    photo_filename: str = Path(..., description="Nombre del archivo"),
    db: Session = Depends(get_db)
):
    """Eliminar foto de galería (Admin)"""
    return await gallery_controller.delete_photo(gallery_id, photo_filename, db)


@router.post("/admin/galleries/{gallery_id}/photos/reorder")
async def reorder_photos(
    gallery_id: int = Path(..., description="ID de galería"),
    reorder_data: PhotoReorderRequest = ...,
    db: Session = Depends(get_db)
):
    """Reordenar fotos en galería (Admin)"""
    return await gallery_controller.reorder_photos(gallery_id, reorder_data, db)


@router.put("/admin/galleries/{gallery_id}/photos/{photo_filename}")
async def update_photo_metadata(
    gallery_id: int = Path(..., description="ID de galería"),
    photo_filename: str = Path(..., description="Nombre del archivo"),
    update_data: PhotoUpdateRequest = ...,
    db: Session = Depends(get_db)
):
    """Actualizar metadata de foto (Admin)"""
    # Asegurar que el filename coincida
    update_data.filename = photo_filename
    return await gallery_controller.update_photo_metadata(gallery_id, update_data, db)


@router.patch("/admin/galleries/{gallery_id}/cover/{photo_filename}")
async def set_cover_photo(
    gallery_id: int = Path(..., description="ID de galería"),
    photo_filename: str = Path(..., description="Nombre del archivo"),
    db: Session = Depends(get_db)
):
    """Establecer foto de portada (Admin)"""
    return await gallery_controller.set_cover_photo(gallery_id, photo_filename, db)


@router.patch("/admin/galleries/{gallery_id}/publish", response_model=GalleryResponse)
async def publish_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Publicar galería (Admin)"""
    return await gallery_controller.publish_gallery(gallery_id, db)


@router.patch("/admin/galleries/{gallery_id}/unpublish", response_model=GalleryResponse)
async def unpublish_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Despublicar galería (Admin)"""
    return await gallery_controller.unpublish_gallery(gallery_id, db)


@router.patch("/admin/galleries/{gallery_id}/toggle-featured", response_model=GalleryResponse)
async def toggle_gallery_featured(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Alternar estado destacado (Admin)"""
    return await gallery_controller.toggle_featured(gallery_id, db)


@router.post("/admin/galleries/bulk/status")
async def bulk_update_gallery_status(
    gallery_ids: List[int] = Body(..., description="IDs de galerías"),
    status: str = Body(..., description="Nuevo estado"),
    db: Session = Depends(get_db)
):
    """Actualización masiva de estado (Admin)"""
    return await gallery_controller.bulk_update_status(gallery_ids, status, db)


@router.post("/admin/galleries/cleanup")
async def cleanup_empty_galleries(db: Session = Depends(get_db)):
    """Limpiar galerías vacías (Admin)"""
    return await gallery_controller.cleanup_empty_galleries(db)


@router.post("/admin/galleries/{gallery_id}/optimize")
async def optimize_gallery_images(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Optimizar imágenes de galería (Admin)"""
    return await gallery_controller.optimize_gallery_images(gallery_id, db)


@router.get("/admin/galleries/stats", response_model=GalleryStatsResponse)
async def get_gallery_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas de galerías (Admin)"""
    return await gallery_controller.get_statistics(db)


# Endpoints públicos (Frontend)
@router.get("/galleries", response_model=GalleryListResponse)
async def get_public_galleries(
    q: Optional[str] = Query(None, description="Búsqueda"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    content_type: Optional[str] = Query(None, description="Filtrar por tipo"),
    photographer: Optional[str] = Query(None, description="Filtrar por fotógrafo"),
    page: int = Query(1, ge=1, description="Página"),
    per_page: int = Query(20, ge=1, le=50, description="Items por página"),
    sort_by: str = Query("created_at", description="Campo de ordenamiento"),
    db: Session = Depends(get_db)
):
    """Obtener galerías públicas (Frontend)"""
    params = GallerySearchParams(
        q=q, category_id=category_id, content_type=content_type, photographer=photographer,
        is_published=True, is_public=True, page=page, per_page=per_page,
        sort_by=sort_by, minimal=True
    )
    return await gallery_controller.get_galleries(params, db)


@router.get("/galleries/featured", response_model=List[GalleryResponse])
async def get_featured_galleries(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener galerías destacadas (Frontend)"""
    return await gallery_controller.get_featured_galleries(limit, db)


@router.get("/galleries/recent", response_model=List[GalleryResponse])
async def get_recent_galleries(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener galerías recientes (Frontend)"""
    return await gallery_controller.get_recent_galleries(limit, db)


@router.get("/galleries/popular", response_model=List[GalleryResponse])
async def get_popular_galleries(
    limit: int = Query(10, ge=1, le=20, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener galerías populares (Frontend)"""
    return await gallery_controller.get_popular_galleries(limit, db)


@router.get("/galleries/photographers/{photographer}", response_model=List[GalleryResponse])
async def get_galleries_by_photographer(
    photographer: str = Path(..., description="Nombre del fotógrafo"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener galerías por fotógrafo (Frontend)"""
    return await gallery_controller.get_galleries_by_photographer(photographer, limit, db)


@router.get("/galleries/{slug}", response_model=GalleryResponse)
async def get_gallery_by_slug(
    slug: str = Path(..., description="Slug de galería"),
    increment_views: bool = Query(True, description="Incrementar contador de vistas"),
    db: Session = Depends(get_db)
):
    """Obtener galería por slug (Frontend)"""
    return await gallery_controller.get_gallery_by_slug(slug, increment_views, db)


@router.get("/galleries/{gallery_id}/related", response_model=List[GalleryResponse])
async def get_related_galleries(
    gallery_id: int = Path(..., description="ID de galería"),
    limit: int = Query(5, ge=1, le=10, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener galerías relacionadas (Frontend)"""
    return await gallery_controller.get_related_galleries(gallery_id, limit, db)


@router.get("/galleries/{gallery_id}/files")
async def get_gallery_file_urls(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Obtener URLs de archivos de galería (Frontend)"""
    return await gallery_controller.get_gallery_file_urls(gallery_id, db)


@router.post("/galleries/{gallery_id}/like", response_model=GalleryResponse)
async def like_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Dar like a galería (Frontend)"""
    return await gallery_controller.like_gallery(gallery_id, db)


@router.post("/galleries/{gallery_id}/share", response_model=GalleryResponse)
async def share_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Compartir galería (Frontend)"""
    return await gallery_controller.share_gallery(gallery_id, db)


@router.post("/galleries/{gallery_id}/download", response_model=GalleryResponse)
async def download_gallery(
    gallery_id: int = Path(..., description="ID de galería"),
    db: Session = Depends(get_db)
):
    """Registrar descarga de galería (Frontend)"""
    return await gallery_controller.download_gallery(gallery_id, db)


# ===================================
# SEARCH & GENERAL ENDPOINTS
# ===================================

@router.get("/search")
async def search_content(
    q: str = Query(..., min_length=2, description="Términos de búsqueda"),
    content_type: Optional[str] = Query(None, description="Tipo de contenido (videos, galleries, all)"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    academic_unit_id: Optional[int] = Query(None, description="Filtrar por unidad académica"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Búsqueda general de contenido (Frontend)"""
    results = {"videos": [], "galleries": [], "categories": []}
    
    if not content_type or content_type in ["videos", "all"]:
        video_params = VideoSearchParams(
            q=q, category_id=category_id, is_published=True, is_public=True,
            page=1, per_page=limit//2 if content_type == "all" else limit, minimal=True
        )
        video_results = await video_controller.get_videos(video_params, db)
        results["videos"] = video_results.videos
    
    if not content_type or content_type in ["galleries", "all"]:
        gallery_params = GallerySearchParams(
            q=q, category_id=category_id, is_published=True, is_public=True,
            page=1, per_page=limit//2 if content_type == "all" else limit, minimal=True
        )
        gallery_results = await gallery_controller.get_galleries(gallery_params, db)
        results["galleries"] = gallery_results.galleries
    
    if not content_type or content_type in ["categories", "all"]:
        categories = await category_controller.search_categories(
            q, academic_unit_id, limit//4 if content_type == "all" else limit, db
        )
        results["categories"] = categories
    
    return results


@router.get("/categories/{category_slug}/content")
async def get_category_content(
    category_slug: str = Path(..., description="Slug de categoría"),
    content_type: Optional[str] = Query(None, description="Tipo de contenido (videos, galleries, all)"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener contenido de una categoría (Frontend)"""
    # Obtener categoría
    category = await category_controller.get_category_by_slug(category_slug, db)
    
    content = {"category": category, "videos": [], "galleries": []}
    
    if not content_type or content_type in ["videos", "all"]:
        videos = await video_controller.get_videos_by_category(
            category.id, limit//2 if content_type == "all" else limit, True, db
        )
        content["videos"] = videos
    
    if not content_type or content_type in ["galleries", "all"]:
        galleries = await gallery_controller.get_galleries_by_category(
            category.id, limit//2 if content_type == "all" else limit, True, db
        )
        content["galleries"] = galleries
    
    return content


@router.get("/academic-units/{academic_unit_id}/content")
async def get_academic_unit_content(
    academic_unit_id: int = Path(..., description="ID de unidad académica"),
    content_type: Optional[str] = Query(None, description="Tipo de contenido"),
    limit: int = Query(20, ge=1, le=50, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Obtener contenido de una unidad académica (Frontend)"""
    content = {"categories": [], "videos": [], "galleries": []}
    
    # Obtener categorías de la unidad académica
    categories = await category_controller.get_categories_by_academic_unit(
        academic_unit_id, True, True, db
    )
    content["categories"] = categories
    
    if not content_type or content_type in ["videos", "all"]:
        videos = await video_controller.get_videos_by_academic_unit(
            academic_unit_id, limit//2 if content_type == "all" else limit, db
        )
        content["videos"] = videos
    
    if not content_type or content_type in ["galleries", "all"]:
        galleries = await gallery_controller.get_galleries_by_academic_unit(
            academic_unit_id, limit//2 if content_type == "all" else limit, db
        )
        content["galleries"] = galleries
    
    return content


# ===================================
# STATS ENDPOINTS
# ===================================

@router.get("/stats")
async def get_cms_statistics(db: Session = Depends(get_db)):
    """Obtener estadísticas generales del CMS"""
    category_stats = await category_controller.get_statistics(db)
    video_stats = await video_controller.get_statistics(db)
    gallery_stats = await gallery_controller.get_statistics(db)
    
    return {
        "categories": category_stats,
        "videos": video_stats,
        "galleries": gallery_stats,
        "summary": {
            "total_categories": category_stats.total_categories,
            "total_videos": video_stats.total_videos,
            "total_galleries": gallery_stats.total_galleries,
            "total_photos": gallery_stats.total_photos,
            "total_views": video_stats.total_views + gallery_stats.total_views,
            "storage_used_gb": gallery_stats.total_size_gb
        }
    }