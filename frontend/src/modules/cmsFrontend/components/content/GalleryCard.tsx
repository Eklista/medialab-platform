// frontend/src/modules/cmsFrontend/components/content/GalleryCard.tsx
import React from 'react';
import { Images, Eye, Calendar } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface GalleryCardProps {
  item: {
    id: number;
    title: string;
    thumbnail: string;
    description?: string;
    date: string;
    views: number;
    category: string;
    photoCount?: number;
  };
}

export const GalleryCard: React.FC<GalleryCardProps> = ({ item }) => {
  const { isDark } = useTheme();

  return (
    <div className={`group cursor-pointer rounded-lg overflow-hidden border transition-all hover:shadow-lg ${
      isDark 
        ? 'bg-slate-800 border-slate-700 hover:border-slate-600' 
        : 'bg-white border-slate-200 hover:border-slate-300'
    }`}>
      {/* Thumbnail */}
      <div className="relative aspect-video overflow-hidden">
        <img 
          src={item.thumbnail} 
          alt={item.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors" />
        
        {/* Gallery Icon */}
        <div className="absolute top-3 right-3">
          <div className="p-2 rounded-full bg-black/50 text-white">
            <Images className="w-4 h-4" />
          </div>
        </div>
        
        {/* Category Badge */}
        <div className="absolute top-3 left-3">
          <span className="px-2 py-1 text-xs font-medium bg-emerald-600 text-white rounded-full">
            {item.category}
          </span>
        </div>

        {/* Photo Count */}
        {item.photoCount && (
          <div className="absolute bottom-3 right-3">
            <span className="px-2 py-1 text-xs font-medium bg-black/70 text-white rounded-full">
              {item.photoCount} fotos
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className={`font-semibold mb-2 line-clamp-2 group-hover:text-emerald-600 transition-colors ${
          isDark ? 'text-slate-100' : 'text-slate-900'
        }`}>
          {item.title}
        </h3>
        
        {item.description && (
          <p className={`text-sm mb-3 line-clamp-2 ${
            isDark ? 'text-slate-400' : 'text-slate-600'
          }`}>
            {item.description}
          </p>
        )}

        <div className={`flex items-center justify-between text-xs ${
          isDark ? 'text-slate-400' : 'text-slate-500'
        }`}>
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            <span>{item.date}</span>
          </div>
          <div className="flex items-center gap-1">
            <Eye className="w-3 h-3" />
            <span>{item.views.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};