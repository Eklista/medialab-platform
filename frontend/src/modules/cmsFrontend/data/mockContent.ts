// src/modules/cmsFrontend/data/mockContent.ts
import type { ContentItem, Photo } from './types'

// Mock photos para galerías
export const graduationPhotos: Photo[] = [
  {
    id: 'photo-1',
    url: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=800&h=600&fit=crop',
    thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=300&h=200&fit=crop',
    caption: 'Ceremonia principal de graduación',
    alt: 'Estudiantes en ceremonia de graduación',
    width: 800,
    height: 600,
    fileSize: 245680,
    order: 1
  },
  {
    id: 'photo-2',
    url: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop',
    thumbnail: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=300&h=200&fit=crop',
    caption: 'Entrega de diplomas',
    alt: 'Entrega de diplomas a graduados',
    width: 800,
    height: 600,
    fileSize: 312450,
    order: 2
  },
  {
    id: 'photo-3',
    url: 'https://images.unsplash.com/photo-1551818255-e6e10975bc17?w=800&h=600&fit=crop',
    thumbnail: 'https://images.unsplash.com/photo-1551818255-e6e10975bc17?w=300&h=200&fit=crop',
    caption: 'Familias celebrando',
    alt: 'Familias celebrando la graduación',
    width: 800,
    height: 600,
    fileSize: 198750,
    order: 3
  }
]

export const conferencePhotos: Photo[] = [
  {
    id: 'photo-4',
    url: 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800&h=600&fit=crop',
    thumbnail: 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=300&h=200&fit=crop',
    caption: 'Ponente principal',
    alt: 'Conferenciasta dando presentación',
    width: 800,
    height: 600,
    fileSize: 278920,
    order: 1
  },
  {
    id: 'photo-5',
    url: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=600&fit=crop',
    thumbnail: 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=200&fit=crop',
    caption: 'Audiencia participando',
    alt: 'Audiencia en conferencia',
    width: 800,
    height: 600,
    fileSize: 325640,
    order: 2
  }
]

export const mockContent: ContentItem[] = [
  // Videos
  {
    id: 'video-1',
    type: 'video',
    title: 'Graduación FISICC 2024 - Ceremonia Principal',
    slug: 'graduacion-fisicc-2024-ceremonia-principal',
    description: 'Ceremonia de graduación de la promoción 2024 de la Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación. Un momento histórico donde celebramos los logros de nuestros nuevos profesionales.',
    thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=400&h=225&fit=crop',
    facultyId: 'fisicc',
    categoryId: 'fisicc-graduaciones',
    tags: ['graduacion', 'fisicc', '2024', 'ceremonia', 'sistemas', 'informatica'],
    status: 'published',
    visibility: 'public',
    featured: true,
    publishedAt: '2024-06-15T10:00:00Z',
    createdAt: '2024-06-14T08:00:00Z',
    updatedAt: '2024-06-15T10:00:00Z',
    stats: {
      views: 1245,
      likes: 89,
      shares: 23,
      comments: 15
    },
    video: {
      duration: '1:45:32',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      provider: 'youtube',
      videoId: 'dQw4w9WgXcQ',
      quality: ['720p', '1080p']
    },
    author: {
      name: 'MediaLab FISICC',
      email: 'medialab@fisicc.galileo.edu',
      role: 'admin'
    }
  },
  {
    id: 'video-2',
    type: 'video',
    title: 'Conferencia: Inteligencia Artificial en la Educación',
    slug: 'conferencia-ia-educacion-2024',
    description: 'Conferencia magistral sobre el impacto de la Inteligencia Artificial en los procesos educativos modernos. Incluye casos de uso prácticos y tendencias futuras.',
    thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=225&fit=crop',
    facultyId: 'fisicc',
    categoryId: 'fisicc-conferencias',
    tags: ['ia', 'inteligencia-artificial', 'educacion', 'tecnologia', 'futuro'],
    status: 'published',
    visibility: 'public',
    featured: true,
    publishedAt: '2024-06-10T14:30:00Z',
    createdAt: '2024-06-09T10:00:00Z',
    updatedAt: '2024-06-10T14:30:00Z',
    stats: {
      views: 2103,
      likes: 156,
      shares: 45,
      comments: 28
    },
    video: {
      duration: '52:18',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      provider: 'youtube',
      videoId: 'dQw4w9WgXcQ',
      quality: ['720p', '1080p']
    },
    author: {
      name: 'Dr. Carlos Méndez',
      email: 'cmendez@galileo.edu',
      role: 'professor'
    }
  },
  {
    id: 'video-3',
    type: 'video',
    title: 'Feria de Ciencias FING 2024',
    slug: 'feria-ciencias-fing-2024',
    description: 'Resumen de la Feria de Ciencias 2024 donde estudiantes de ingeniería presentaron sus proyectos más innovadores.',
    thumbnail: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=225&fit=crop',
    facultyId: 'fing',
    categoryId: 'fing-ferias',
    tags: ['feria', 'ciencias', 'proyectos', 'estudiantes', 'innovacion'],
    status: 'published',
    visibility: 'public',
    featured: false,
    publishedAt: '2024-06-08T16:00:00Z',
    createdAt: '2024-06-07T12:00:00Z',
    updatedAt: '2024-06-08T16:00:00Z',
    stats: {
      views: 892,
      likes: 67,
      shares: 18,
      comments: 12
    },
    video: {
      duration: '28:45',
      embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
      provider: 'youtube',
      videoId: 'dQw4w9WgXcQ',
      quality: ['720p', '1080p']
    },
    author: {
      name: 'MediaLab FING',
      email: 'medialab@fing.galileo.edu',
      role: 'admin'
    }
  },
  
  // Galerías
  {
    id: 'gallery-1',
    type: 'gallery',
    title: 'Galería: Graduación FACMED 2024',
    slug: 'galeria-graduacion-facmed-2024',
    description: 'Momentos destacados de la ceremonia de graduación de la Facultad de Medicina 2024. Fotos oficiales del evento y celebraciones.',
    thumbnail: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=225&fit=crop',
    facultyId: 'facmed',
    categoryId: 'facmed-graduaciones',
    tags: ['graduacion', 'medicina', 'ceremonia', 'doctores', 'celebracion'],
    status: 'published',
    visibility: 'public',
    featured: true,
    publishedAt: '2024-06-05T18:00:00Z',
    createdAt: '2024-06-04T14:00:00Z',
    updatedAt: '2024-06-05T18:00:00Z',
    stats: {
      views: 3401,
      likes: 234,
      shares: 67,
      comments: 42
    },
    gallery: {
      photoCount: 48,
      photos: graduationPhotos,
      downloadUrl: 'https://drive.google.com/download/facmed-graduacion-2024'
    },
    author: {
      name: 'Fotografía FACMED',
      email: 'foto@facmed.galileo.edu',
      role: 'photographer'
    }
  },
  {
    id: 'gallery-2',
    type: 'gallery',
    title: 'Congreso Médico Internacional 2024',
    slug: 'congreso-medico-internacional-2024',
    description: 'Documentación fotográfica del Congreso Médico Internacional con participación de especialistas de toda Latinoamérica.',
    thumbnail: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=400&h=225&fit=crop',
    facultyId: 'facmed',
    categoryId: 'facmed-congresos',
    tags: ['congreso', 'medicina', 'internacional', 'especialistas', 'conferencias'],
    status: 'published',
    visibility: 'public',
    featured: false,
    publishedAt: '2024-05-28T12:00:00Z',
    createdAt: '2024-05-27T08:00:00Z',
    updatedAt: '2024-05-28T12:00:00Z',
    stats: {
      views: 1876,
      likes: 142,
      shares: 35,
      comments: 18
    },
    gallery: {
      photoCount: 32,
      photos: conferencePhotos,
      downloadUrl: 'https://drive.google.com/download/congreso-medico-2024'
    },
    author: {
      name: 'MediaLab Central',
      email: 'medialab@galileo.edu',
      role: 'admin'
    }
  }
]

// Helper functions para trabajar con el contenido
export const getContentById = (id: string): ContentItem | undefined => {
  return mockContent.find(item => item.id === id)
}

export const getContentBySlug = (slug: string): ContentItem | undefined => {
  return mockContent.find(item => item.slug === slug)
}

export const getContentByFaculty = (facultyId: string): ContentItem[] => {
  return mockContent.filter(item => item.facultyId === facultyId)
}

export const getContentByCategory = (categoryId: string): ContentItem[] => {
  return mockContent.filter(item => item.categoryId === categoryId)
}

export const getContentByType = (type: 'video' | 'gallery'): ContentItem[] => {
  return mockContent.filter(item => item.type === type)
}

export const getFeaturedContent = (): ContentItem[] => {
  return mockContent.filter(item => item.featured && item.status === 'published')
}

export const getRecentContent = (limit: number = 10): ContentItem[] => {
  return mockContent
    .filter(item => item.status === 'published')
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, limit)
}

export const getPopularContent = (limit: number = 10): ContentItem[] => {
  return mockContent
    .filter(item => item.status === 'published')
    .sort((a, b) => b.stats.views - a.stats.views)
    .slice(0, limit)
}

export const searchContent = (query: string): ContentItem[] => {
  const searchTerm = query.toLowerCase()
  return mockContent.filter(item => 
    item.status === 'published' && (
      item.title.toLowerCase().includes(searchTerm) ||
      item.description.toLowerCase().includes(searchTerm) ||
      item.tags.some(tag => tag.toLowerCase().includes(searchTerm))
    )
  )
}

export const getContentStats = () => {
  const published = mockContent.filter(item => item.status === 'published')
  const totalViews = published.reduce((sum, item) => sum + item.stats.views, 0)
  const totalLikes = published.reduce((sum, item) => sum + item.stats.likes, 0)
  
  return {
    total: mockContent.length,
    published: published.length,
    videos: published.filter(item => item.type === 'video').length,
    galleries: published.filter(item => item.type === 'gallery').length,
    featured: published.filter(item => item.featured).length,
    totalViews,
    totalLikes,
    averageViews: Math.round(totalViews / published.length),
    mostViewed: published.reduce((prev, current) => 
      prev.stats.views > current.stats.views ? prev : current
    )
  }
}