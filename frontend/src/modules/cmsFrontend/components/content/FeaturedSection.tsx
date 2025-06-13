// frontend/src/modules/cmsFrontend/components/content/FeaturedSection.tsx
import React from 'react';
import { Play, Images, Eye, Calendar } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

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

interface FeaturedSectionProps {
  items: ContentItem[];
  onItemClick?: (item: ContentItem) => void;
}

export const FeaturedSection: React.FC<FeaturedSectionProps> = ({ items, onItemClick }) => {
  const { isDark } = useTheme();

  if (items.length === 0) return null;

  const [mainItem, ...sideItems] = items;

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className={`text-2xl font-bold ${
          isDark ? 'text-slate-100' : 'text-slate-900'
        }`}>
          Contenido Destacado
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Featured Item */}
        <div className="lg:col-span-2">
          <div 
            onClick={() => onItemClick?.(mainItem)}
            className={`group cursor-pointer rounded-xl overflow-hidden border-2 transition-all hover:shadow-xl ${
              isDark 
                ? 'bg-slate-800 border-slate-700 hover:border-slate-600' 
                : 'bg-white border-slate-200 hover:border-slate-300'
            }`}
          >
            <div className="relative aspect-video overflow-hidden">
              <img 
                src={mainItem.thumbnail} 
                alt={mainItem.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
              
              {/* Play/Gallery Icon */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center group-hover:scale-110 transition-transform">
                  {mainItem.type === 'video' ? (
                    <Play className="w-7 h-7 text-slate-900 ml-1" fill="currentColor" />
                  ) : (
                    <Images className="w-7 h-7 text-slate-900" />
                  )}
                </div>
              </div>

              {/* Category Badge */}
              <div className="absolute top-4 left-4">
                <span className={`px-3 py-1 text-sm font-medium rounded-full text-white ${
                  mainItem.type === 'video' ? 'bg-blue-600' : 'bg-emerald-600'
                }`}>
                  {mainItem.category}
                </span>
              </div>

              {/* Photo Count for galleries */}
              {mainItem.type === 'gallery' && mainItem.photoCount && (
                <div className="absolute bottom-4 right-4">
                  <span className="px-2 py-1 text-sm font-medium bg-black/70 text-white rounded-full">
                    {mainItem.photoCount} fotos
                  </span>
                </div>
              )}
            </div>

            <div className="p-6">
              <h3 className={`text-xl font-bold mb-3 group-hover:text-blue-600 transition-colors ${
                isDark ? 'text-slate-100' : 'text-slate-900'
              }`}>
                {mainItem.title}
              </h3>
              
              {mainItem.description && (
                <p className={`text-base mb-4 line-clamp-2 ${
                  isDark ? 'text-slate-400' : 'text-slate-600'
                }`}>
                  {mainItem.description}
                </p>
              )}

              <div className={`flex items-center justify-between ${
                isDark ? 'text-slate-400' : 'text-slate-500'
              }`}>
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span className="text-sm">{mainItem.date}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  <span className="text-sm">{mainItem.views.toLocaleString()} vistas</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Side Featured Items */}
        <div className="space-y-4">
          {sideItems.map(item => (
            <div 
              key={item.id} 
              onClick={() => onItemClick?.(item)}
              className={`group cursor-pointer rounded-lg overflow-hidden border transition-all hover:shadow-lg ${
                isDark 
                  ? 'bg-slate-800 border-slate-700 hover:border-slate-600' 
                  : 'bg-white border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="flex gap-4 p-4">
                <div className="relative w-24 h-16 flex-shrink-0 rounded-lg overflow-hidden">
                  <img 
                    src={item.thumbnail} 
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-6 h-6 rounded-full bg-white/90 flex items-center justify-center">
                      {item.type === 'video' ? (
                        <Play className="w-3 h-3 text-slate-900" fill="currentColor" />
                      ) : (
                        <Images className="w-3 h-3 text-slate-900" />
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex-1 min-w-0">
                  <h4 className={`font-semibold text-sm mb-1 line-clamp-2 group-hover:text-blue-600 transition-colors ${
                    isDark ? 'text-slate-100' : 'text-slate-900'
                  }`}>
                    {item.title}
                  </h4>
                  
                  <div className={`flex items-center gap-3 text-xs ${
                    isDark ? 'text-slate-400' : 'text-slate-500'
                  }`}>
                    <span className={`px-2 py-0.5 rounded-full ${
                      item.type === 'video' 
                        ? isDark ? 'bg-blue-600/20 text-blue-400' : 'bg-blue-100 text-blue-700'
                        : isDark ? 'bg-emerald-600/20 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
                    }`}>
                      {item.category}
                    </span>
                    <span>{item.views.toLocaleString()} vistas</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};