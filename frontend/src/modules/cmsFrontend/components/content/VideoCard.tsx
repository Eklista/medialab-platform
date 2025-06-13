// frontend/src/modules/cmsFrontend/components/content/VideoCard.tsx
import React from 'react';
import { Play, Eye, Calendar } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface VideoCardProps {
  item: {
    id: number;
    title: string;
    thumbnail: string;
    description?: string;
    date: string;
    views: number;
    category: string;
  };
}

export const VideoCard: React.FC<VideoCardProps> = ({ item }) => {
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
        <div className="absolute inset-0 bg-black/20 group-hover:bg-black/30 transition-colors" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-12 h-12 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform">
            <Play className="w-5 h-5 text-slate-900 ml-0.5" fill="currentColor" />
          </div>
        </div>
        
        {/* Category Badge */}
        <div className="absolute top-3 left-3">
          <span className="px-2 py-1 text-xs font-medium bg-blue-600 text-white rounded-full">
            {item.category}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className={`font-semibold mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors ${
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