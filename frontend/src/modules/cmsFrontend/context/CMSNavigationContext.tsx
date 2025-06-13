// frontend/src/modules/cmsFrontend/context/CMSNavigationContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

type CMSRoute = 'home' | 'video' | 'gallery' | 'category' | 'search' | 'faculty';

interface RouteParams {
  slug?: string;
  categorySlug?: string;
  facultySlug?: string;
  q?: string;
  [key: string]: string | undefined;
}

interface CMSNavigationContextType {
  currentRoute: CMSRoute;
  routeParams: RouteParams;
  navigateToHome: () => void;
  navigateToVideo: (slug: string) => void;
  navigateToGallery: (slug: string) => void;
  navigateToCategory: (facultySlug: string, categorySlug: string) => void;
  navigateToSearch: (query: string) => void;
  navigateToFaculty: (facultySlug: string) => void;
  goBack: () => void;
}

const CMSNavigationContext = createContext<CMSNavigationContextType | undefined>(undefined);

export const CMSNavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentRoute, setCurrentRoute] = useState<CMSRoute>('home');
  const [routeParams, setRouteParams] = useState<RouteParams>({});

  // Parse current URL on mount and when URL changes
  useEffect(() => {
    const parseCurrentRoute = () => {
      const path = window.location.pathname;
      const search = new URLSearchParams(window.location.search);

      if (path === '/' || path === '') {
        setCurrentRoute('home');
        setRouteParams({});
      } else if (path.startsWith('/video/')) {
        const slug = path.replace('/video/', '');
        setCurrentRoute('video');
        setRouteParams({ slug });
      } else if (path.startsWith('/gallery/')) {
        const slug = path.replace('/gallery/', '');
        setCurrentRoute('gallery');
        setRouteParams({ slug });
      } else if (path.startsWith('/category/')) {
        const pathParts = path.split('/');
        const facultySlug = pathParts[2];
        const categorySlug = pathParts[3];
        setCurrentRoute('category');
        setRouteParams({ facultySlug, categorySlug });
      } else if (path === '/search') {
        const query = search.get('q') || '';
        setCurrentRoute('search');
        setRouteParams({ q: query });
      } else if (path.startsWith('/faculty/')) {
        const facultySlug = path.replace('/faculty/', '');
        setCurrentRoute('faculty');
        setRouteParams({ facultySlug });
      }
    };

    parseCurrentRoute();

    const handlePopState = () => {
      parseCurrentRoute();
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const updateURL = (path: string) => {
    window.history.pushState(null, '', path);
  };

  const navigateToHome = () => {
    setCurrentRoute('home');
    setRouteParams({});
    updateURL('/');
  };

  const navigateToVideo = (slug: string) => {
    setCurrentRoute('video');
    setRouteParams({ slug });
    updateURL(`/video/${slug}`);
  };

  const navigateToGallery = (slug: string) => {
    setCurrentRoute('gallery');
    setRouteParams({ slug });
    updateURL(`/gallery/${slug}`);
  };

  const navigateToCategory = (facultySlug: string, categorySlug: string) => {
    setCurrentRoute('category');
    setRouteParams({ facultySlug, categorySlug });
    updateURL(`/category/${facultySlug}/${categorySlug}`);
  };

  const navigateToSearch = (query: string) => {
    setCurrentRoute('search');
    setRouteParams({ q: query });
    updateURL(`/search?q=${encodeURIComponent(query)}`);
  };

  const navigateToFaculty = (facultySlug: string) => {
    setCurrentRoute('faculty');
    setRouteParams({ facultySlug });
    updateURL(`/faculty/${facultySlug}`);
  };

  const goBack = () => {
    window.history.back();
  };

  return (
    <CMSNavigationContext.Provider
      value={{
        currentRoute,
        routeParams,
        navigateToHome,
        navigateToVideo,
        navigateToGallery,
        navigateToCategory,
        navigateToSearch,
        navigateToFaculty,
        goBack,
      }}
    >
      {children}
    </CMSNavigationContext.Provider>
  );
};

export const useCMSNavigation = () => {
  const context = useContext(CMSNavigationContext);
  if (context === undefined) {
    throw new Error('useCMSNavigation must be used within a CMSNavigationProvider');
  }
  return context;
};
