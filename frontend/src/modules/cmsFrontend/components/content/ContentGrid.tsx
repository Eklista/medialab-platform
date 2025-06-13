// frontend/src/modules/cmsFrontend/components/content/ContentGrid.tsx
import React from 'react';
import { useTheme } from '../../context/ThemeContext';
import { VideoCard } from './VideoCard';
import { GalleryCard } from './GalleryCard';
import { Camera } from 'lucide-react';

interface ContentItem {
  id: number;
  type: 'video' | 'gallery';
  title: string;
  thumbnail: string;
  description?: string;
  date: string;
  views: number;
  category: string;
  slug: string;
  photoCount?: number;
}

interface ContentGridProps {
  items: ContentItem[];
  loading?: boolean;
  onItemClick?: (item: ContentItem) => void;
}

export const ContentGrid: React.FC<ContentGridProps> = ({ items, loading, onItemClick }) => {
  const { isDark } = useTheme();

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className={`animate-pulse rounded-lg ${
            isDark ? 'bg-slate-700' : 'bg-slate-200'
          }`}>
            <div className="aspect-video rounded-t-lg bg-current opacity-20" />
            <div className="p-4 space-y-2">
              <div className="h-4 bg-current opacity-20 rounded" />
              <div className="h-3 bg-current opacity-20 rounded w-3/4" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className={`text-center py-12 ${
        isDark ? 'text-slate-400' : 'text-slate-500'
      }`}>
        <Camera className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p className="text-lg font-medium mb-2">No hay contenido disponible</p>
        <p className="text-sm">Intenta seleccionar otra categoría</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map(item => (
        <div key={item.id} onClick={() => onItemClick?.(item)}>
          {item.type === 'video' ? (
            <VideoCard item={item} />
          ) : (
            <GalleryCard item={item} />
          )}
        </div>
      ))}
    </div>
  );
};