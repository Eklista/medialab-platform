// frontend/src/modules/cmsFrontend/pages/GalleryPage.tsx (actualizado)
import React, { useState, useEffect } from 'react';
import { ArrowLeft, Download, Share, Heart, Eye, ChevronLeft, ChevronRight, X } from 'lucide-react';
import { CMSLayout } from '../components/layout/CMSLayout';
import { useTheme } from '../context/ThemeContext';
import { useCMSNavigation } from '../context/CMSNavigationContext';

interface GalleryPageProps {
  gallerySlug: string;
}

// Mock gallery data
const mockGallery = {
  id: 2,
  title: 'Conferencia de Inteligencia Artificial',
  description: `Galería fotográfica de la conferencia magistral sobre Inteligencia Artificial en la Educación, realizada en el Auditorio Principal de la Universidad Galileo.

El evento contó con la participación de reconocidos expertos internacionales en el campo de la IA aplicada a la educación, quienes compartieron sus conocimientos y experiencias sobre las últimas tendencias y tecnologías.

Durante la conferencia se abordaron temas como machine learning, deep learning, procesamiento de lenguaje natural y sus aplicaciones prácticas en el ámbito educativo.`,
  date: '2024-06-10',
  views: 892,
  likes: 45,
  category: 'Conferencias',
  faculty: 'FISICC',
  photographer: 'Equipo MediaLab',
  photos: [
    {
      id: 1,
      url: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=300&h=200&fit=crop',
      caption: 'Conferencia magistral en el Auditorio Principal'
    },
    {
      id: 2,
      url: 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=300&h=200&fit=crop',
      caption: 'Participantes durante la sesión de networking'
    },
    {
      id: 3,
      url: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=200&fit=crop',
      caption: 'Mesa redonda con expertos internacionales'
    },
    {
      id: 4,
      url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop',
      caption: 'Demostración de tecnologías de IA'
    },
    {
      id: 5,
      url: 'https://images.unsplash.com/photo-1591115765373-5207764f72e7?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1591115765373-5207764f72e7?w=300&h=200&fit=crop',
      caption: 'Sesión de preguntas y respuestas'
    },
    {
      id: 6,
      url: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800&h=600&fit=crop',
      thumbnail: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=300&h=200&fit=crop',
      caption: 'Clausura del evento'
    }
  ]
};

export const GalleryPage: React.FC<GalleryPageProps> = ({ gallerySlug }) => {
  const { isDark } = useTheme();
  const { goBack } = useCMSNavigation();
  const [gallery] = useState(mockGallery);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState<number | null>(null);

  useEffect(() => {
    // Simular carga de datos basado en slug
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, [gallerySlug]);

  const nextPhoto = () => {
    if (selectedPhoto !== null) {
      const nextIndex = (selectedPhoto + 1) % gallery.photos.length;
      setSelectedPhoto(nextIndex);
    }
  };

  const prevPhoto = () => {
    if (selectedPhoto !== null) {
      const prevIndex = selectedPhoto === 0 ? gallery.photos.length - 1 : selectedPhoto - 1;
      setSelectedPhoto(prevIndex);
    }
  };

  if (loading) {
    return (
      <CMSLayout showSidebar={false}>
        <div className="max-w-6xl mx-auto space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {Array.from({ length: 12 }).map((_, i) => (
              <div key={i} className={`aspect-square ${isDark ? 'bg-slate-800' : 'bg-slate-200'} rounded-lg animate-pulse`} />
            ))}
          </div>
        </div>
      </CMSLayout>
    );
  }

  return (
    <CMSLayout showSidebar={false}>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Back Button */}
        <button 
          onClick={goBack}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
            isDark
              ? 'text-slate-400 hover:text-slate-300 hover:bg-slate-800'
              : 'text-slate-600 hover:text-slate-700 hover:bg-slate-100'
          }`}
        >
          <ArrowLeft className="w-4 h-4" />
          Volver
        </button>

        {/* Gallery Header */}
        <div className="space-y-4">
          <h1 className={`text-3xl font-bold ${
            isDark ? 'text-slate-100' : 'text-slate-900'
          }`}>
            {gallery.title}
          </h1>

          <div className={`flex flex-wrap items-center gap-4 text-sm ${
            isDark ? 'text-slate-400' : 'text-slate-600'
          }`}>
            <div className="flex items-center gap-1">
              <Eye className="w-4 h-4" />
              <span>{gallery.views.toLocaleString()} vistas</span>
            </div>
            <span className="px-3 py-1 bg-emerald-600 text-white rounded-full text-xs">
              {gallery.category}
            </span>
            <span className={`px-3 py-1 rounded-full text-xs ${
              isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-700'
            }`}>
              {gallery.faculty}
            </span>
            <span className={`px-3 py-1 rounded-full text-xs ${
              isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-700'
            }`}>
              {gallery.photos.length} fotos
            </span>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setLiked(!liked)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                liked
                  ? 'bg-red-600 text-white'
                  : isDark
                    ? 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              <Heart className={`w-4 h-4 ${liked ? 'fill-current' : ''}`} />
              <span>{liked ? gallery.likes + 1 : gallery.likes}</span>
            </button>

            <button className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              isDark
                ? 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}>
              <Share className="w-4 h-4" />
              Compartir
            </button>

            <button className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              isDark
                ? 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}>
              <Download className="w-4 h-4" />
              Descargar galería
            </button>
          </div>
        </div>

        {/* Photo Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {gallery.photos.map((photo, index) => (
            <div
              key={photo.id}
              className="group cursor-pointer relative aspect-square overflow-hidden rounded-lg"
              onClick={() => setSelectedPhoto(index)}
            >
              <img
                src={photo.thumbnail}
                alt={photo.caption}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors" />
            </div>
          ))}
        </div>

        {/* Gallery Info */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Description */}
          <div className="lg:col-span-2 space-y-4">
            <h3 className={`text-lg font-semibold ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              Descripción
            </h3>
            <div className={`whitespace-pre-line ${
              isDark ? 'text-slate-300' : 'text-slate-700'
            }`}>
              {gallery.description}
            </div>
          </div>

          {/* Details */}
          <div className={`p-6 rounded-lg ${
            isDark ? 'bg-slate-800' : 'bg-slate-100'
          }`}>
            <h3 className={`text-lg font-semibold mb-4 ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              Detalles
            </h3>
            <div className="space-y-3">
              <div>
                <span className={`text-sm font-medium ${
                  isDark ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  Fotógrafo:
                </span>
                <div className={`${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                  {gallery.photographer}
                </div>
              </div>
              <div>
                <span className={`text-sm font-medium ${
                  isDark ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  Facultad:
                </span>
                <div className={`${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                  {gallery.faculty}
                </div>
              </div>
              <div>
                <span className={`text-sm font-medium ${
                  isDark ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  Fecha:
                </span>
                <div className={`${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                  {gallery.date}
                </div>
              </div>
              <div>
                <span className={`text-sm font-medium ${
                  isDark ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  Total de fotos:
                </span>
                <div className={`${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                  {gallery.photos.length}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Photo Lightbox */}
      {selectedPhoto !== null && (
        <div className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4">
          <div className="relative max-w-4xl max-h-full">
            {/* Close Button */}
            <button
              onClick={() => setSelectedPhoto(null)}
              className="absolute top-4 right-4 z-10 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            {/* Navigation Buttons */}
            <button
              onClick={prevPhoto}
              className="absolute left-4 top-1/2 -translate-y-1/2 z-10 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>

            <button
              onClick={nextPhoto}
              className="absolute right-4 top-1/2 -translate-y-1/2 z-10 p-2 bg-black/50 text-white rounded-full hover:bg-black/70 transition-colors"
            >
              <ChevronRight className="w-6 h-6" />
            </button>

            {/* Photo */}
            <img
              src={gallery.photos[selectedPhoto].url}
              alt={gallery.photos[selectedPhoto].caption}
              className="max-w-full max-h-full object-contain"
            />

            {/* Caption */}
            {gallery.photos[selectedPhoto].caption && (
              <div className="absolute bottom-4 left-4 right-4 bg-black/70 text-white p-4 rounded-lg">
                <p className="text-sm">{gallery.photos[selectedPhoto].caption}</p>
                <p className="text-xs text-gray-300 mt-1">
                  {selectedPhoto + 1} de {gallery.photos.length}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </CMSLayout>
  );
};