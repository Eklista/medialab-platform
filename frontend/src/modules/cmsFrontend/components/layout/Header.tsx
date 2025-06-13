// frontend/src/modules/cmsFrontend/components/layout/Header.tsx
import React from 'react';
import { Search, Sun, Moon, Menu } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

export const Header: React.FC = () => {
  const { isDark, toggleTheme } = useTheme();
  
  return (
    <header className={`sticky top-0 z-50 border-b ${
      isDark 
        ? 'bg-slate-800/95 border-slate-700 backdrop-blur' 
        : 'bg-white/95 border-slate-200 backdrop-blur'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
              isDark ? 'bg-blue-600' : 'bg-blue-600'
            }`}>
              <span className="text-white font-bold text-sm">ML</span>
            </div>
            <div>
              <h1 className={`text-xl font-bold ${
                isDark ? 'text-slate-100' : 'text-slate-900'
              }`}>
                MediaLab
              </h1>
              <p className={`text-xs ${
                isDark ? 'text-slate-400' : 'text-slate-500'
              }`}>
                Universidad Galileo
              </p>
            </div>
          </div>

          {/* Search Bar */}
          <div className="hidden md:flex flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <Search className={`absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 ${
                isDark ? 'text-slate-400' : 'text-slate-500'
              }`} />
              <input
                type="text"
                placeholder="Buscar contenido..."
                className={`w-full pl-10 pr-4 py-2 rounded-lg border transition-colors ${
                  isDark 
                    ? 'bg-slate-700 border-slate-600 text-slate-100 placeholder-slate-400 focus:border-blue-500' 
                    : 'bg-white border-slate-300 text-slate-900 placeholder-slate-500 focus:border-blue-500'
                } focus:outline-none focus:ring-2 focus:ring-blue-500/20`}
              />
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                isDark
                  ? 'hover:bg-slate-700 text-slate-300 hover:text-slate-100'
                  : 'hover:bg-slate-100 text-slate-600 hover:text-slate-900'
              }`}
            >
              {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            
            <button className={`md:hidden p-2 rounded-lg transition-colors ${
              isDark
                ? 'hover:bg-slate-700 text-slate-300'
                : 'hover:bg-slate-100 text-slate-600'
            }`}>
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};