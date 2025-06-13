// frontend/src/modules/cmsFrontend/CMSRouter.tsx
import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { CMSNavigationProvider, useCMSNavigation } from './context/CMSNavigationContext';
import { HomePage } from './pages/HomePage';
import { VideoPage } from './pages/VideoPage';
import { GalleryPage } from './pages/GalleryPage';
import { CategoryPage } from './pages/CategoryPage';
import { SearchPage } from './pages/SearchPage';

const CMSContent: React.FC = () => {
  const { currentRoute, routeParams } = useCMSNavigation();

  const renderRoute = () => {
    switch (currentRoute) {
      case 'home':
        return <HomePage />;
      case 'video':
        return <VideoPage videoSlug={routeParams.slug} />;
      case 'gallery':
        return <GalleryPage gallerySlug={routeParams.slug} />;
      case 'category':
        return <CategoryPage categorySlug={routeParams.categorySlug} facultySlug={routeParams.facultySlug} />;
      case 'search':
        return <SearchPage query={routeParams.q} />;
      default:
        return <HomePage />;
    }
  };

  return <>{renderRoute()}</>;
};

export const CMSRouter: React.FC = () => {
  return (
    <ThemeProvider>
      <CMSNavigationProvider>
        <CMSContent />
      </CMSNavigationProvider>
    </ThemeProvider>
  );
};