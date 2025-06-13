// frontend/src/modules/cmsFrontend/pages/CategoryPage.tsx
import React, { useState, useEffect } from 'react';
import { ArrowLeft } from 'lucide-react';
import { CMSLayout } from '../components/layout/CMSLayout';
import { ContentGrid } from '../components/content/ContentGrid';
import { useTheme } from '../context/ThemeContext';
import { useCMSNavigation } from '../context/CMSNavigationContext';

interface CategoryPageProps {
  facultySlug: string;
  categorySlug: string;
}

interface ContentItem {
  id: number;
  type: 'video' | 'gallery';
  title: string;
  thumbnail: string;
  description: string;
  date: string;
  views: number;
  category: string;
  slug: string;
  photoCount?: number;
}

export const CategoryPage: React.FC<CategoryPageProps> = ({ facultySlug, categorySlug }) => {
  const { isDark } = useTheme();
  const { goBack, navigateToVideo, navigateToGallery } = useCMSNavigation();
  const [content, setContent] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [facultyInfo] = useState({ name: 'FISICC', fullName: 'Facultad de Ingeniería de Sistemas' });
  const [categoryInfo] = useState({ name: 'Graduaciones', type: 'mixed' });

  useEffect(() => {
    // Simular carga de datos
    const timer = setTimeout(() => {
      // Mock data filtrada
      const mockData: ContentItem[] = [
        {
          id: 1,
          type: 'video',
          title: `Graduación ${facultyInfo.name} 2024 - Ceremonia Principal`,
          thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=400&h=225&fit=crop',
          description: 'Ceremonia de graduación de la promoción 2024',
          date: '2024-06-15',
          views: 1245,
          category: categoryInfo.name,
          slug: 'graduacion-ceremony-2024'
        },
        {
          id: 2,
          type: 'gallery',
          title: `Galería ${categoryInfo.name} ${facultyInfo.name}`,
          thumbnail: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400&h=225&fit=crop',
          description: 'Fotos del evento de graduación',
          date: '2024-06-15',
          views: 892,
          category: categoryInfo.name,
          slug: 'gallery-graduacion-2024',
          photoCount: 48
        }
      ];
      setContent(mockData);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, [facultySlug, categorySlug, facultyInfo.name, categoryInfo.name]);

  const handleContentClick = (item: ContentItem) => {
    if (item.type === 'video') {
      navigateToVideo(item.slug);
    } else {
      navigateToGallery(item.slug);
    }
  };

  return (
    <CMSLayout>
      <div className="space-y-6">
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

        {/* Header */}
        <div className="space-y-4">
          <div>
            <div className={`text-sm font-medium mb-2 ${
              isDark ? 'text-slate-400' : 'text-slate-600'
            }`}>
              {facultyInfo.fullName}
            </div>
            <h1 className={`text-3xl font-bold ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              {categoryInfo.name}
            </h1>
          </div>

          <div className={`flex items-center justify-between ${
            isDark ? 'text-slate-400' : 'text-slate-600'
          }`}>
            <p className="text-sm">
              Contenido de {categoryInfo.name.toLowerCase()} de {facultyInfo.name}
            </p>
            <div className="text-sm">
              {content.length} elementos encontrados
            </div>
          </div>
        </div>

        {/* Content Grid */}
        <ContentGrid 
          items={content} 
          loading={loading}
          onItemClick={handleContentClick}
        />
      </div>
    </CMSLayout>
  );
};