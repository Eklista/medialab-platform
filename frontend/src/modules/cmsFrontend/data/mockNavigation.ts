// src/modules/cmsFrontend/data/mockNavigation.ts
import type { NavigationItem, GlobalStats } from './types'
import { mockFaculties } from './mockFaculties'
import { getContentStats } from './mockContent'
import { getLiveStreamStats } from './mockLiveStream'

// Navegación principal
export const primaryNavigation: NavigationItem[] = [
  {
    id: 'home',
    label: 'Inicio',
    icon: 'Home',
    href: '/',
    isActive: true,
    order: 1
  },
  {
    id: 'live',
    label: 'En Vivo',
    icon: 'Radio',
    href: '/live',
    badge: 'LIVE',
    badgeVariant: 'live',
    order: 2
  },
  {
    id: 'videos',
    label: 'Videos',
    icon: 'Video',
    href: '/videos',
    badge: 245,
    order: 3
  },
  {
    id: 'galleries',
    label: 'Galerías',
    icon: 'Images',
    href: '/galleries',
    badge: 89,
    order: 4
  },
  {
    id: 'search',
    label: 'Búsqueda',
    icon: 'Search',
    href: '/search',
    order: 5
  }
]

// Navegación por facultades (dinámicamente generada)
export const facultyNavigation: NavigationItem[] = mockFaculties.map((faculty, index) => ({
  id: faculty.id,
  label: faculty.name,
  icon: 'GraduationCap',
  href: `/faculty/${faculty.slug}`,
  badge: faculty.stats.totalVideos + faculty.stats.totalGalleries,
  order: index + 1,
  children: faculty.categories.map((category, catIndex) => ({
    id: category.id,
    label: category.name,
    icon: category.icon,
    href: `/faculty/${faculty.slug}/${category.slug}`,
    badge: category.count,
    order: catIndex + 1
  }))
}))

// Navegación footer
export const footerNavigation: NavigationItem[] = [
  {
    id: 'about',
    label: 'Acerca de',
    icon: 'Info',
    href: '/about',
    order: 1
  },
  {
    id: 'contact',
    label: 'Contacto',
    icon: 'Mail',
    href: '/contact',
    order: 2
  },
  {
    id: 'help',
    label: 'Ayuda',
    icon: 'HelpCircle',
    href: '/help',
    order: 3
  },
  {
    id: 'privacy',
    label: 'Privacidad',
    icon: 'Shield',
    href: '/privacy',
    order: 4
  },
  {
    id: 'terms',
    label: 'Términos',
    icon: 'FileText',
    href: '/terms',
    order: 5
  }
]

// Links externos/sociales
export const socialNavigation: NavigationItem[] = [
  {
    id: 'youtube',
    label: 'YouTube',
    icon: 'Youtube',
    href: 'https://youtube.com/@universidadgalileo',
    isExternal: true,
    order: 1
  },
  {
    id: 'facebook',
    label: 'Facebook',
    icon: 'Facebook',
    href: 'https://facebook.com/universidadgalileo',
    isExternal: true,
    order: 2
  },
  {
    id: 'instagram',
    label: 'Instagram',
    icon: 'Instagram',
    href: 'https://instagram.com/universidadgalileo',
    isExternal: true,
    order: 3
  },
  {
    id: 'website',
    label: 'Sitio Web',
    icon: 'Globe',
    href: 'https://galileo.edu',
    isExternal: true,
    order: 4
  }
]

// Estadísticas globales para el dashboard
export const mockGlobalStats: GlobalStats = {
  totalFaculties: mockFaculties.length,
  totalVideos: getContentStats().videos,
  totalGalleries: getContentStats().galleries,
  totalViews: getContentStats().totalViews,
  totalHours: 1247, // Total estimado de horas de contenido
  liveViewers: getLiveStreamStats().currentViewers,
  monthlyViews: 45892,
  topContent: [], // Se llenaría con getPopularContent()
  recentContent: [] // Se llenaría con getRecentContent()
}

// Helper functions para navegación dinámica
export const getNavigationByRole = (): NavigationItem[] => {
  // Por ahora todos ven la misma navegación
  // En el futuro se podría filtrar por rol
  return primaryNavigation
}

export const getFacultyNavigation = (): NavigationItem[] => {
  return facultyNavigation
}

export const getNavigationItem = (id: string): NavigationItem | undefined => {
  const allNavigation = [
    ...primaryNavigation,
    ...facultyNavigation,
    ...footerNavigation,
    ...socialNavigation
  ]
  
  // Buscar en items principales
  let item = allNavigation.find(nav => nav.id === id)
  
  // Si no se encuentra, buscar en children
  if (!item) {
    for (const nav of allNavigation) {
      if (nav.children) {
        item = nav.children.find(child => child.id === id)
        if (item) break
      }
    }
  }
  
  return item
}

export const updateNavigationBadges = (): void => {
  // Actualizar badges con datos reales
  const contentStats = getContentStats()
  const liveStats = getLiveStreamStats()
  
  // Actualizar videos count
  const videosNav = primaryNavigation.find(nav => nav.id === 'videos')
  if (videosNav) {
    videosNav.badge = contentStats.videos
  }
  
  // Actualizar galleries count
  const galleriesNav = primaryNavigation.find(nav => nav.id === 'galleries')
  if (galleriesNav) {
    galleriesNav.badge = contentStats.galleries
  }
  
  // Actualizar live indicator
  const liveNav = primaryNavigation.find(nav => nav.id === 'live')
  if (liveNav) {
    liveNav.badge = liveStats.isLive ? 'LIVE' : undefined
    liveNav.badgeVariant = liveStats.isLive ? 'live' : undefined
  }
  
  // Actualizar faculty badges
  facultyNavigation.forEach(facultyNav => {
    const faculty = mockFaculties.find(f => f.id === facultyNav.id)
    if (faculty) {
      facultyNav.badge = faculty.stats.totalVideos + faculty.stats.totalGalleries
      
      // Actualizar categories badges
      if (facultyNav.children) {
        facultyNav.children.forEach(categoryNav => {
          const category = faculty.categories.find(c => c.id === categoryNav.id)
          if (category) {
            categoryNav.badge = category.count
          }
        })
      }
    }
  })
}

export const setActiveNavigation = (path: string): void => {
  // Reset all active states
  const allNavigation = [
    ...primaryNavigation,
    ...facultyNavigation,
    ...footerNavigation
  ]
  
  allNavigation.forEach(nav => {
    nav.isActive = false
    if (nav.children) {
      nav.children.forEach(child => child.isActive = false)
    }
  })
  
  // Set active based on current path
  for (const nav of allNavigation) {
    if (nav.href === path) {
      nav.isActive = true
      break
    }
    
    if (nav.children) {
      for (const child of nav.children) {
        if (child.href === path) {
          child.isActive = true
          nav.isActive = true // También marcar el padre como activo
          break
        }
      }
    }
  }
}

export const getBreadcrumbs = (path: string): NavigationItem[] => {
  const breadcrumbs: NavigationItem[] = []
  
  // Siempre empezar con Home
  breadcrumbs.push({
    id: 'home',
    label: 'Inicio',
    icon: 'Home',
    href: '/',
    order: 0
  })
  
  if (path === '/') return breadcrumbs
  
  // Buscar el item activo
  const allNavigation = [...primaryNavigation, ...facultyNavigation]
  
  for (const nav of allNavigation) {
    if (nav.href === path) {
      breadcrumbs.push(nav)
      break
    }
    
    if (nav.children) {
      for (const child of nav.children) {
        if (child.href === path) {
          breadcrumbs.push(nav)
          breadcrumbs.push(child)
          break
        }
      }
    }
  }
  
  return breadcrumbs
}

// Función para filtrar navegación por búsqueda
export const searchNavigation = (query: string): NavigationItem[] => {
  const searchTerm = query.toLowerCase()
  const results: NavigationItem[] = []
  
  const allNavigation = [...primaryNavigation, ...facultyNavigation]
  
  for (const nav of allNavigation) {
    // Buscar en el item principal
    if (nav.label.toLowerCase().includes(searchTerm)) {
      results.push(nav)
    }
    
    // Buscar en children
    if (nav.children) {
      const matchingChildren = nav.children.filter(child =>
        child.label.toLowerCase().includes(searchTerm)
      )
      
      if (matchingChildren.length > 0) {
        results.push({
          ...nav,
          children: matchingChildren
        })
      }
    }
  }
  
  return results
}

// Inicializar badges con datos actuales
updateNavigationBadges()