// src/modules/cmsFrontend/data/types.ts

// Base types para toda la aplicación
export interface Faculty {
  id: string
  name: string          // "FISICC"
  fullName: string      // "Facultad de Ingeniería de Sistemas..."
  description: string
  slug: string
  color: string         // Brand color para la facultad
  thumbnail: string
  coverImage: string
  stats: {
    totalVideos: number
    totalGalleries: number
    totalViews: number
    totalSubscribers: number
  }
  categories: Category[]
  socialLinks?: {
    website?: string
    facebook?: string
    instagram?: string
    youtube?: string
  }
  createdAt: string
  updatedAt: string
}

export interface Category {
  id: string
  name: string          // "Graduaciones"
  slug: string
  description: string
  facultyId: string
  icon: string          // Lucide icon name
  color?: string
  count: number         // Total de contenido en esta categoría
  isActive: boolean
  order: number
  createdAt: string
}

export interface ContentItem {
  id: string
  type: 'video' | 'gallery'
  title: string
  slug: string
  description: string
  thumbnail: string
  facultyId: string
  categoryId: string
  tags: string[]
  status: 'published' | 'draft' | 'archived'
  visibility: 'public' | 'private' | 'unlisted'
  featured: boolean
  publishedAt: string
  createdAt: string
  updatedAt: string
  stats: {
    views: number
    likes: number
    shares: number
    comments: number
  }
  // Específico para videos
  video?: {
    duration: string      // "45:32"
    embedUrl: string
    provider: 'youtube' | 'vimeo' | 'local'
    videoId: string
    quality: string[]     // ["720p", "1080p"]
  }
  // Específico para galerías
  gallery?: {
    photoCount: number
    photos: Photo[]
    downloadUrl?: string
  }
  author?: {
    name: string
    email: string
    role: string
  }
}

export interface Photo {
  id: string
  url: string
  thumbnail: string
  caption?: string
  alt: string
  width: number
  height: number
  fileSize: number
  order: number
}

export interface LiveStream {
  id: string
  title: string
  description: string
  isLive: boolean
  status: 'live' | 'scheduled' | 'ended'
  embedUrl: string
  provider: 'youtube' | 'twitch' | 'local'
  streamKey?: string
  viewerCount: number
  maxViewers: number
  thumbnail: string
  facultyId?: string
  categoryId?: string
  tags: string[]
  scheduledStart?: string
  actualStart?: string
  actualEnd?: string
  chat: {
    enabled: boolean
    moderationLevel: 'strict' | 'moderate' | 'relaxed'
    allowGuests: boolean
  }
  recording: {
    enabled: boolean
    autoPublish: boolean
    retentionDays: number
  }
}

export interface NavigationItem {
  id: string
  label: string
  icon: string          // Lucide icon name
  href?: string
  badge?: string | number
  badgeVariant?: 'default' | 'live' | 'success' | 'warning'
  isActive?: boolean
  isExternal?: boolean
  order: number
  children?: NavigationItem[]
}

export interface GlobalStats {
  totalFaculties: number
  totalVideos: number
  totalGalleries: number
  totalViews: number
  totalHours: number       // Total de horas de contenido
  liveViewers: number
  monthlyViews: number
  topContent: ContentItem[]
  recentContent: ContentItem[]
}

// API Response types
export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
  meta?: {
    total: number
    page: number
    limit: number
    hasNext: boolean
    hasPrev: boolean
  }
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  meta: {
    total: number
    page: number
    limit: number
    hasNext: boolean
    hasPrev: boolean
  }
}

// Filter types para búsquedas y filtros
export interface ContentFilters {
  type?: 'video' | 'gallery' | 'all'
  facultyId?: string
  categoryId?: string
  tags?: string[]
  dateRange?: {
    start: string
    end: string
  }
  sortBy?: 'newest' | 'oldest' | 'popular' | 'title' | 'views'
  sortOrder?: 'asc' | 'desc'
  status?: 'published' | 'draft' | 'archived'
  featured?: boolean
  limit?: number
  page?: number
}

export interface SearchResults {
  content: ContentItem[]
  faculties: Faculty[]
  categories: Category[]
  totalResults: number
  searchTime: number
}

// Chat types (para el live stream)
export interface ChatMessage {
  id: string
  sessionId: string
  username: string
  message: string
  timestamp: number
  ipHash?: string
  isModerated?: boolean
  isModerator?: boolean
}

export interface ChatConfig {
  enabled: boolean
  maxMessageLength: number
  rateLimitMessages: number
  rateLimitWindow: number
  slowMode: boolean
  slowModeDelay: number
  autoModeration: boolean
  bannedWords: string[]
}