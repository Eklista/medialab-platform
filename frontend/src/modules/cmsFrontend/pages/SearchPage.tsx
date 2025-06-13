// frontend/src/modules/cmsFrontend/pages/SearchPage.tsx
import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { CMSLayout } from '../components/layout/CMSLayout';
import { ContentGrid } from '../components/content/ContentGrid';
import { SearchFilters } from '../components/ui/SearchFilters';
import { useTheme } from '../context/ThemeContext';
import { useCMSNavigation } from '../context/CMSNavigationContext';

interface SearchPageProps {
  query?: string;
}

export const SearchPage: React.FC<SearchPageProps> = ({ query = '' }) => {
  const { isDark } = useTheme();
  const { navigateToVideo, navigateToGallery, navigateToSearch } = useCMSNavigation();
  const [searchQuery, setSearchQuery] = useState(query);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    type: 'all',
    faculty: 'all',
    category: 'all',
    sortBy: 'relevance'
  });

  useEffect(() => {
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  }, [searchQuery, filters]);

  const handleSearch = async (query: string) => {
    setLoading(true);
    
    // Simular búsqueda
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Mock results
    const mockResults = [
      {
        id: 1,
        type: 'video' as const,
        title: `Graduación FISICC 2024 - Ceremonia Principal`,
        thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=400&h=225&fit=crop',
        description: 'Ceremonia de graduación de la promoción 2024',
        date: '2024-06-15',
        views: 1245,
        category: 'Graduaciones',
        slug: 'graduacion-fisicc-2024'
      }
    ].filter(item => 
      item.title.toLowerCase().includes(query.toLowerCase()) ||
      item.description.toLowerCase().includes(query.toLowerCase()) ||
      item.category.toLowerCase().includes(query.toLowerCase())
    );

    setResults(mockResults);
    setLoading(false);
  };

  const handleContentClick = (item: any) => {
    if (item.type === 'video') {
      navigateToVideo(item.slug);
    } else {
      navigateToGallery(item.slug);
    }
  };

  return (
    <CMSLayout>
      <div className="space-y-6">
        {/* Search Header */}
        <div className="space-y-4">
          <div className="relative">
            <Search className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 ${
              isDark ? 'text-slate-400' : 'text-slate-500'
            }`} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  navigateToSearch(searchQuery);
                }
              }}
              placeholder="Buscar contenido, eventos, graduaciones..."
              className={`w-full pl-11 pr-4 py-3 rounded-lg border transition-colors ${
                isDark 
                  ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-400 focus:border-blue-500' 
                  : 'bg-white border-slate-300 text-slate-900 placeholder-slate-500 focus:border-blue-500'
              } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
            />
          </div>

          {searchQuery && (
            <div className={`text-sm ${
              isDark ? 'text-slate-400' : 'text-slate-600'
            }`}>
              {loading ? 'Buscando...' : `${results.length} resultados para "${searchQuery}"`}
            </div>
          )}
        </div>

        {/* Search Filters */}
        <SearchFilters 
          onSearch={handleSearch}
          onFilterChange={setFilters}
          onSortChange={(sort) => setFilters(prev => ({ ...prev, sortBy: sort }))}
        />

        {/* Results */}
        <ContentGrid 
          items={results} 
          loading={loading}
          onItemClick={handleContentClick}
        />
      </div>
    </CMSLayout>
  );
};