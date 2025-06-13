// frontend/src/modules/cmsFrontend/components/ui/SearchFilters.tsx
import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface SearchFiltersProps {
  onSearch: (query: string) => void;
  onFilterChange: (filters: any) => void;
  onSortChange: (sort: string) => void;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({
  onSearch,
  onSortChange
}) => {
  const { isDark } = useTheme();
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [sortBy, setSortBy] = useState('newest');
  const [contentType, setContentType] = useState('all');
  const [dateRange, setDateRange] = useState('all');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(searchQuery);
  };

  return (
    <div className="space-y-4">
      {/* Search Bar */}
      <form onSubmit={handleSearch} className="relative">
        <Search className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 ${
          isDark ? 'text-slate-400' : 'text-slate-500'
        }`} />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar contenido, eventos, graduaciones..."
          className={`w-full pl-11 pr-12 py-3 rounded-lg border transition-colors ${
            isDark 
              ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-400 focus:border-blue-500' 
              : 'bg-white border-slate-300 text-slate-900 placeholder-slate-500 focus:border-blue-500'
          } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
        />
        <button
          type="button"
          onClick={() => setShowFilters(!showFilters)}
          className={`absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded transition-colors ${
            isDark
              ? 'text-slate-400 hover:text-slate-300 hover:bg-slate-700'
              : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100'
          }`}
        >
          <Filter className="w-5 h-5" />
        </button>
      </form>

      {/* Filters Panel */}
      {showFilters && (
        <div className={`p-4 rounded-lg border ${
          isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
        }`}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Content Type Filter */}
            <div>
              <label className={`block text-sm font-medium mb-2 ${
                isDark ? 'text-slate-300' : 'text-slate-700'
              }`}>
                Tipo de Contenido
              </label>
              <select
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                className={`w-full px-3 py-2 rounded-lg border ${
                  isDark 
                    ? 'bg-slate-700 border-slate-600 text-slate-100' 
                    : 'bg-white border-slate-300 text-slate-900'
                } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              >
                <option value="all">Todos</option>
                <option value="video">Videos</option>
                <option value="gallery">Galerías</option>
              </select>
            </div>

            {/* Date Range Filter */}
            <div>
              <label className={`block text-sm font-medium mb-2 ${
                isDark ? 'text-slate-300' : 'text-slate-700'
              }`}>
                Período
              </label>
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className={`w-full px-3 py-2 rounded-lg border ${
                  isDark 
                    ? 'bg-slate-700 border-slate-600 text-slate-100' 
                    : 'bg-white border-slate-300 text-slate-900'
                } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              >
                <option value="all">Todo el tiempo</option>
                <option value="week">Esta semana</option>
                <option value="month">Este mes</option>
                <option value="year">Este año</option>
              </select>
            </div>

            {/* Sort Options */}
            <div>
              <label className={`block text-sm font-medium mb-2 ${
                isDark ? 'text-slate-300' : 'text-slate-700'
              }`}>
                Ordenar por
              </label>
              <select
                value={sortBy}
                onChange={(e) => {
                  setSortBy(e.target.value);
                  onSortChange(e.target.value);
                }}
                className={`w-full px-3 py-2 rounded-lg border ${
                  isDark 
                    ? 'bg-slate-700 border-slate-600 text-slate-100' 
                    : 'bg-white border-slate-300 text-slate-900'
                } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              >
                <option value="newest">Más recientes</option>
                <option value="oldest">Más antiguos</option>
                <option value="popular">Más vistos</option>
                <option value="title">Título A-Z</option>
              </select>
            </div>
          </div>

          {/* Filter Actions */}
          <div className="flex justify-between items-center mt-4 pt-4 border-t border-current border-opacity-20">
            <button
              onClick={() => {
                setSearchQuery('');
                setContentType('all');
                setDateRange('all');
                setSortBy('newest');
              }}
              className={`text-sm px-4 py-2 rounded-lg transition-colors ${
                isDark
                  ? 'text-slate-400 hover:text-slate-300 hover:bg-slate-700'
                  : 'text-slate-600 hover:text-slate-700 hover:bg-slate-100'
              }`}
            >
              Limpiar filtros
            </button>
            
            <button
              onClick={() => setShowFilters(false)}
              className="text-sm px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Aplicar filtros
            </button>
          </div>
        </div>
      )}
    </div>
  );
};