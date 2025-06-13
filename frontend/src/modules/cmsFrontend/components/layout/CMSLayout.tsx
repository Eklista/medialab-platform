// frontend/src/modules/cmsFrontend/components/layout/CMSLayout.tsx
import React from 'react';
import { useTheme } from '../../context/ThemeContext';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface CMSLayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

export const CMSLayout: React.FC<CMSLayoutProps> = ({ 
  children, 
  showSidebar = true 
}) => {
  const { isDark } = useTheme();
  
  return (
    <div className={`min-h-screen ${
      isDark 
        ? 'bg-slate-900 text-slate-100' 
        : 'bg-slate-50 text-slate-900'
    }`}>
      <Header />
      
      <div className="flex">
        {showSidebar && <Sidebar />}
        
        <main className={`flex-1 ${showSidebar ? 'ml-64' : ''}`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};