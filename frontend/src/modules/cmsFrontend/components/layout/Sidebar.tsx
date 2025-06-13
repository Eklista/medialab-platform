// frontend/src/modules/cmsFrontend/components/layout/Sidebar.tsx
import React from 'react';
import { useTheme } from '../../context/ThemeContext';
import { FacultyFilter } from '../filters/FacultyFilter';

export const Sidebar: React.FC = () => {
  const { isDark } = useTheme();
  
  return (
    <aside className={`fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 border-r overflow-y-auto ${
      isDark 
        ? 'bg-slate-800 border-slate-700' 
        : 'bg-white border-slate-200'
    }`}>
      <div className="p-6">
        <h2 className={`text-lg font-semibold mb-6 ${
          isDark ? 'text-slate-100' : 'text-slate-900'
        }`}>
          Explorar Contenido
        </h2>
        
        <FacultyFilter />
      </div>
    </aside>
  );
};