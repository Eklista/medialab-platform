// src/modules/cmsFrontend/data/mockFaculties.ts
import type { Faculty, Category } from './types'

// Mock categories para cada facultad
export const fisiccCategories: Category[] = [
  {
    id: 'fisicc-graduaciones',
    name: 'Graduaciones',
    slug: 'graduaciones',
    description: 'Ceremonias de graduación y entrega de diplomas',
    facultyId: 'fisicc',
    icon: 'GraduationCap',
    color: '#3b82f6',
    count: 24,
    isActive: true,
    order: 1,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fisicc-conferencias',
    name: 'Conferencias',
    slug: 'conferencias',
    description: 'Conferencias magistrales y charlas técnicas',
    facultyId: 'fisicc',
    icon: 'Calendar',
    color: '#10b981',
    count: 18,
    isActive: true,
    order: 2,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fisicc-talleres',
    name: 'Talleres',
    slug: 'talleres',
    description: 'Talleres prácticos y workshops',
    facultyId: 'fisicc',
    icon: 'Users',
    color: '#f59e0b',
    count: 31,
    isActive: true,
    order: 3,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fisicc-eventos',
    name: 'Eventos Especiales',
    slug: 'eventos-especiales',
    description: 'Hackathons, competencias y eventos especiales',
    facultyId: 'fisicc',
    icon: 'Trophy',
    color: '#8b5cf6',
    count: 12,
    isActive: true,
    order: 4,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fisicc-investigacion',
    name: 'Investigación',
    slug: 'investigacion',
    description: 'Presentaciones de proyectos de investigación',
    facultyId: 'fisicc',
    icon: 'Search',
    color: '#ef4444',
    count: 8,
    isActive: true,
    order: 5,
    createdAt: '2024-01-15T08:00:00Z'
  }
]

export const fingCategories: Category[] = [
  {
    id: 'fing-graduaciones',
    name: 'Graduaciones',
    slug: 'graduaciones',
    description: 'Ceremonias de graduación de ingeniería',
    facultyId: 'fing',
    icon: 'GraduationCap',
    color: '#3b82f6',
    count: 32,
    isActive: true,
    order: 1,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fing-simposiums',
    name: 'Simposiums',
    slug: 'simposiums',
    description: 'Simposiums de ingeniería y tecnología',
    facultyId: 'fing',
    icon: 'Presentation',
    color: '#10b981',
    count: 15,
    isActive: true,
    order: 2,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fing-ferias',
    name: 'Ferias de Ciencias',
    slug: 'ferias-ciencias',
    description: 'Ferias científicas y exposiciones',
    facultyId: 'fing',
    icon: 'Lightbulb',
    color: '#f59e0b',
    count: 22,
    isActive: true,
    order: 3,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'fing-laboratorios',
    name: 'Laboratorios',
    slug: 'laboratorios',
    description: 'Actividades de laboratorio y prácticas',
    facultyId: 'fing',
    icon: 'Beaker',
    color: '#8b5cf6',
    count: 28,
    isActive: true,
    order: 4,
    createdAt: '2024-01-15T08:00:00Z'
  }
]

export const facmedCategories: Category[] = [
  {
    id: 'facmed-graduaciones',
    name: 'Graduaciones',
    slug: 'graduaciones',
    description: 'Ceremonias de graduación médica',
    facultyId: 'facmed',
    icon: 'GraduationCap',
    color: '#3b82f6',
    count: 28,
    isActive: true,
    order: 1,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'facmed-congresos',
    name: 'Congresos Médicos',
    slug: 'congresos-medicos',
    description: 'Congresos y conferencias médicas',
    facultyId: 'facmed',
    icon: 'Stethoscope',
    color: '#10b981',
    count: 19,
    isActive: true,
    order: 2,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'facmed-practicas',
    name: 'Prácticas Clínicas',
    slug: 'practicas-clinicas',
    description: 'Documentación de prácticas clínicas',
    facultyId: 'facmed',
    icon: 'Heart',
    color: '#ef4444',
    count: 35,
    isActive: true,
    order: 3,
    createdAt: '2024-01-15T08:00:00Z'
  },
  {
    id: 'facmed-investigacion',
    name: 'Investigación Médica',
    slug: 'investigacion-medica',
    description: 'Presentaciones de investigación médica',
    facultyId: 'facmed',
    icon: 'Microscope',
    color: '#8b5cf6',
    count: 14,
    isActive: true,
    order: 4,
    createdAt: '2024-01-15T08:00:00Z'
  }
]

export const mockFaculties: Faculty[] = [
  {
    id: 'fisicc',
    name: 'FISICC',
    fullName: 'Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación',
    description: 'Formando profesionales en tecnología, sistemas de información y ciencias computacionales con excelencia académica y visión innovadora.',
    slug: 'fisicc',
    color: '#3b82f6',
    thumbnail: 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=400&h=300&fit=crop',
    coverImage: 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=1200&h=400&fit=crop',
    stats: {
      totalVideos: 67,
      totalGalleries: 26,
      totalViews: 15420,
      totalSubscribers: 1248
    },
    categories: fisiccCategories,
    socialLinks: {
      website: 'https://fisicc.galileo.edu',
      facebook: 'https://facebook.com/fisicc.galileo',
      instagram: 'https://instagram.com/fisicc_galileo',
      youtube: 'https://youtube.com/@fisicc-galileo'
    },
    createdAt: '2024-01-01T08:00:00Z',
    updatedAt: '2024-06-15T14:30:00Z'
  },
  {
    id: 'fing',
    name: 'FING',
    fullName: 'Facultad de Ingeniería',
    description: 'Excelencia en formación de ingenieros con sólidos conocimientos técnicos, científicos y humanísticos para el desarrollo sostenible.',
    slug: 'fing',
    color: '#10b981',
    thumbnail: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=300&fit=crop',
    coverImage: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&h=400&fit=crop',
    stats: {
      totalVideos: 89,
      totalGalleries: 38,
      totalViews: 22150,
      totalSubscribers: 1856
    },
    categories: fingCategories,
    socialLinks: {
      website: 'https://fing.galileo.edu',
      facebook: 'https://facebook.com/fing.galileo',
      instagram: 'https://instagram.com/fing_galileo'
    },
    createdAt: '2024-01-01T08:00:00Z',
    updatedAt: '2024-06-14T16:45:00Z'
  },
  {
    id: 'facmed',
    name: 'FACMED',
    fullName: 'Facultad de Medicina',
    description: 'Formación integral de profesionales médicos comprometidos con la salud, la investigación y el servicio a la comunidad.',
    slug: 'facmed',
    color: '#ef4444',
    thumbnail: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=300&fit=crop',
    coverImage: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200&h=400&fit=crop',
    stats: {
      totalVideos: 78,
      totalGalleries: 42,
      totalViews: 31280,
      totalSubscribers: 2134
    },
    categories: facmedCategories,
    socialLinks: {
      website: 'https://facmed.galileo.edu',
      facebook: 'https://facebook.com/facmed.galileo',
      instagram: 'https://instagram.com/facmed_galileo'
    },
    createdAt: '2024-01-01T08:00:00Z',
    updatedAt: '2024-06-13T11:20:00Z'
  },
  {
    id: 'facom',
    name: 'FACOM',
    fullName: 'Facultad de Comunicación',
    description: 'Profesionales en comunicación integral con dominio de medios tradicionales y digitales, creatividad e innovación.',
    slug: 'facom',
    color: '#f59e0b',
    thumbnail: 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=300&fit=crop',
    coverImage: 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1200&h=400&fit=crop',
    stats: {
      totalVideos: 45,
      totalGalleries: 29,
      totalViews: 18750,
      totalSubscribers: 892
    },
    categories: [
      {
        id: 'facom-graduaciones',
        name: 'Graduaciones',
        slug: 'graduaciones',
        description: 'Ceremonias de graduación de comunicación',
        facultyId: 'facom',
        icon: 'GraduationCap',
        color: '#3b82f6',
        count: 18,
        isActive: true,
        order: 1,
        createdAt: '2024-01-15T08:00:00Z'
      },
      {
        id: 'facom-produccion',
        name: 'Producción Audiovisual',
        slug: 'produccion-audiovisual',
        description: 'Proyectos y producciones estudiantiles',
        facultyId: 'facom',
        icon: 'Video',
        color: '#10b981',
        count: 32,
        isActive: true,
        order: 2,
        createdAt: '2024-01-15T08:00:00Z'
      },
      {
        id: 'facom-eventos',
        name: 'Eventos',
        slug: 'eventos',
        description: 'Festivales, concursos y eventos especiales',
        facultyId: 'facom',
        icon: 'Camera',
        color: '#f59e0b',
        count: 24,
        isActive: true,
        order: 3,
        createdAt: '2024-01-15T08:00:00Z'
      }
    ],
    socialLinks: {
      website: 'https://facom.galileo.edu',
      facebook: 'https://facebook.com/facom.galileo',
      instagram: 'https://instagram.com/facom_galileo'
    },
    createdAt: '2024-01-01T08:00:00Z',
    updatedAt: '2024-06-12T09:15:00Z'
  }
]

// Helper functions
export const getFacultyById = (id: string): Faculty | undefined => {
  return mockFaculties.find(faculty => faculty.id === id)
}

export const getFacultyBySlug = (slug: string): Faculty | undefined => {
  return mockFaculties.find(faculty => faculty.slug === slug)
}

export const getCategoriesByFaculty = (facultyId: string): Category[] => {
  const faculty = getFacultyById(facultyId)
  return faculty?.categories || []
}

export const getCategoryById = (categoryId: string): Category | undefined => {
  for (const faculty of mockFaculties) {
    const category = faculty.categories.find(cat => cat.id === categoryId)
    if (category) return category
  }
  return undefined
}

export const getAllCategories = (): Category[] => {
  return mockFaculties.flatMap(faculty => faculty.categories)
}

export const getFacultyStats = () => {
  return mockFaculties.reduce((stats, faculty) => ({
    totalFaculties: stats.totalFaculties + 1,
    totalVideos: stats.totalVideos + faculty.stats.totalVideos,
    totalGalleries: stats.totalGalleries + faculty.stats.totalGalleries,
    totalViews: stats.totalViews + faculty.stats.totalViews,
    totalSubscribers: stats.totalSubscribers + faculty.stats.totalSubscribers
  }), {
    totalFaculties: 0,
    totalVideos: 0,
    totalGalleries: 0,
    totalViews: 0,
    totalSubscribers: 0
  })
}