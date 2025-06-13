// frontend/src/modules/cmsFrontend/components/navigation/Breadcrumbs.tsx
import React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({ items }) => {
  const { isDark } = useTheme();

  return (
    <nav className="flex" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        <li>
          <button className={`p-1 rounded transition-colors ${
            isDark
              ? 'text-slate-400 hover:text-slate-300'
              : 'text-slate-500 hover:text-slate-700'
          }`}>
            <Home className="w-4 h-4" />
          </button>
        </li>

        {items.map((item, index) => (
          <li key={index} className="flex items-center space-x-2">
            <ChevronRight className={`w-4 h-4 ${
              isDark ? 'text-slate-600' : 'text-slate-400'
            }`} />
            
            {item.current ? (
              <span className={`text-sm font-medium ${
                isDark ? 'text-slate-100' : 'text-slate-900'
              }`}>
                {item.label}
              </span>
            ) : (
              <button className={`text-sm transition-colors ${
                isDark
                  ? 'text-slate-400 hover:text-slate-300'
                  : 'text-slate-600 hover:text-slate-900'
              }`}>
                {item.label}
              </button>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};