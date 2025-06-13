// frontend/src/modules/cmsFrontend/pages/HomePage.tsx
import React, { useState, useEffect } from 'react';
import { CMSLayout } from '../components/layout/CMSLayout';
import { ContentGrid } from '../components/content/ContentGrid';
import { FeaturedSection } from '../components/content/FeaturedSection';
import { useTheme } from '../context/ThemeContext';
import { useCMSNavigation } from '../context/CMSNavigationContext';

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

// Mock data
const mockContent: ContentItem[] = [
  {
    id: 1,
    type: 'video',
    title: 'Graduación FISICC 2024 - Ceremonia Principal',
    thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=400&h=225&fit=crop',
    description: 'Ceremonia de graduación de la promoción 2024 de la Facultad de Ingeniería de Sistemas',
    date: '2024-06-15',
    views: 1245,
    category: 'Graduaciones',
    slug: 'graduacion-fisicc-2024-ceremonia-principal'
  },
  {
    id: 2,
    type: 'gallery',
    title: 'Conferencia de Inteligencia Artificial',
    thumbnail: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400&h=225&fit=crop',
    description: 'Fotos de la conferencia magistral sobre IA en la educación',
    date: '2024-06-10',
    views: 892,
    category: 'Conferencias',
    slug: 'conferencia-inteligencia-artificial',
    photoCount: 24
  },
  {
    id: 3,
    type: 'video',
    title: 'Feria de Ciencias FING 2024',
    thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=225&fit=crop',
    description: 'Presentación de proyectos estudiantiles en la feria anual',
    date: '2024-06-08',
    views: 2103,
    category: 'Eventos',
    slug: 'feria-ciencias-fing-2024'
  },
  {
    id: 4,
    type: 'gallery',
    title: 'Graduación FACMED - Medicina General',
    thumbnail: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=225&fit=crop',
    description: 'Ceremonia de graduación de médicos generales',
    date: '2024-06-05',
    views: 3401,
    category: 'Graduaciones',
    slug: 'graduacion-facmed-medicina-general',
    photoCount: 48
  }
];

export const HomePage: React.FC = () => {
  const { isDark } = useTheme();
  const { navigateToVideo, navigateToGallery } = useCMSNavigation();
  const [content] = useState<ContentItem[]>(mockContent);
  const [loading, setLoading] = useState(false);
  const [selectedCategory] = useState<string | null>(null);

  // Simular carga de contenido
  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 800);
    return () => clearTimeout(timer);
  }, [selectedCategory]);

  const filteredContent = selectedCategory 
    ? content.filter(item => item.category === selectedCategory)
    : content;

  const handleContentClick = (item: ContentItem) => {
    if (item.type === 'video') {
      navigateToVideo(item.slug);
    } else {
      navigateToGallery(item.slug);
    }
  };

  return (
    <CMSLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className={`text-4xl font-bold ${
            isDark ? 'text-slate-100' : 'text-slate-900'
          }`}>
            MediaLab Universidad Galileo
          </h1>
          <p className={`text-lg max-w-2xl mx-auto ${
            isDark ? 'text-slate-400' : 'text-slate-600'
          }`}>
            Explora videos, galerías y contenido multimedia de las diferentes facultades 
            de la Universidad Galileo
          </p>
        </div>

        {/* Featured Section */}
        <FeaturedSection items={content.slice(0, 3)} onItemClick={handleContentClick} />

        {/* Content Section */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className={`text-2xl font-bold ${
              isDark ? 'text-slate-100' : 'text-slate-900'
            }`}>
              {selectedCategory ? `Contenido de ${selectedCategory}` : 'Todo el Contenido'}
            </h2>
            
            <div className={`text-sm ${
              isDark ? 'text-slate-400' : 'text-slate-600'
            }`}>
              {filteredContent.length} elementos encontrados
            </div>
          </div>

          <ContentGrid 
            items={filteredContent} 
            loading={loading} 
            onItemClick={handleContentClick}
          />
        </div>
      </div>
    </CMSLayout>
  );
};