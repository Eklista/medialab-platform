// frontend/src/modules/cmsFrontend/pages/VideoPage.tsx (actualizado)
import React, { useState, useEffect } from 'react';
import { ArrowLeft, Eye, Calendar, Share, Heart } from 'lucide-react';
import { CMSLayout } from '../components/layout/CMSLayout';
import { useTheme } from '../context/ThemeContext';
import { useCMSNavigation } from '../context/CMSNavigationContext';

interface VideoPageProps {
  videoSlug: string;
}

// Mock video data
const mockVideo = {
  id: 1,
  title: 'Graduación FISICC 2024 - Ceremonia Principal',
  description: `Ceremonia de graduación de la promoción 2024 de la Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación.

Durante este evento especial, celebramos el logro académico de nuestros graduados quienes han completado exitosamente sus estudios superiores. La ceremonia incluye palabras del Decano, reconocimientos especiales y la entrega de diplomas.

Este momento marca el inicio de una nueva etapa profesional para nuestros egresados, quienes están preparados para enfrentar los desafíos del mundo laboral con las competencias adquiridas durante su formación universitaria.`,
  embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
  thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=800&h=450&fit=crop',
  date: '2024-06-15',
  views: 1245,
  likes: 89,
  category: 'Graduaciones',
  faculty: 'FISICC',
  duration: '45:32',
  tags: ['graduación', 'fisicc', '2024', 'ceremonia', 'universidad-galileo']
};

export const VideoPage: React.FC<VideoPageProps> = ({ videoSlug }) => {
  const { isDark } = useTheme();
  const { goBack } = useCMSNavigation();
  const [video] = useState(mockVideo);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);

  useEffect(() => {
    // Simular carga de datos basado en slug
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, [videoSlug]);

  if (loading) {
    return (
      <CMSLayout showSidebar={false}>
        <div className="max-w-4xl mx-auto space-y-6">
          <div className={`animate-pulse ${isDark ? 'bg-slate-800' : 'bg-slate-200'} aspect-video rounded-xl`} />
          <div className="space-y-4">
            <div className={`animate-pulse h-8 ${isDark ? 'bg-slate-800' : 'bg-slate-200'} rounded`} />
            <div className={`animate-pulse h-4 ${isDark ? 'bg-slate-800' : 'bg-slate-200'} rounded w-3/4`} />
          </div>
        </div>
      </CMSLayout>
    );
  }

  return (
    <CMSLayout showSidebar={false}>
      <div className="max-w-4xl mx-auto space-y-6">
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

        {/* Video Player */}
        <div className="relative aspect-video rounded-xl overflow-hidden bg-black">
          <iframe
            src={video.embedUrl}
            title={video.title}
            className="w-full h-full"
            allowFullScreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          />
        </div>

        {/* Video Info */}
        <div className="space-y-6">
          <div>
            <h1 className={`text-3xl font-bold mb-4 ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              {video.title}
            </h1>

            <div className={`flex flex-wrap items-center gap-4 text-sm ${
              isDark ? 'text-slate-400' : 'text-slate-600'
            }`}>
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>{video.date}</span>
              </div>
              <div className="flex items-center gap-1">
                <Eye className="w-4 h-4" />
                <span>{video.views.toLocaleString()} vistas</span>
              </div>
              <span className="px-3 py-1 bg-blue-600 text-white rounded-full text-xs">
                {video.category}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs ${
                isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-700'
              }`}>
                {video.faculty}
              </span>
            </div>
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
              <span>{liked ? video.likes + 1 : video.likes}</span>
            </button>

            <button className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              isDark
                ? 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}>
              <Share className="w-4 h-4" />
              Compartir
            </button>
          </div>

          {/* Description */}
          <div>
            <h3 className={`text-lg font-semibold mb-3 ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              Descripción
            </h3>
            <div className={`whitespace-pre-line ${
              isDark ? 'text-slate-300' : 'text-slate-700'
            }`}>
              {video.description}
            </div>
          </div>

          {/* Tags */}
          {video.tags && video.tags.length > 0 && (
            <div>
              <h3 className={`text-lg font-semibold mb-3 ${
                isDark ? 'text-slate-100' : 'text-slate-900'
              }`}>
                Etiquetas
              </h3>
              <div className="flex flex-wrap gap-2">
                {video.tags.map(tag => (
                  <span
                    key={tag}
                    className={`px-3 py-1 rounded-full text-sm ${
                      isDark
                        ? 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                        : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                    } cursor-pointer transition-colors`}
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </CMSLayout>
  );
};