// src/modules/cmsFrontend/data/mockLiveStream.ts
import type { LiveStream, ChatConfig } from './types'

export const mockLiveStream: LiveStream = {
  id: 'live-stream-main',
  title: 'Conferencia Magistral: Innovación en Ingeniería Biomédica',
  description: `Transmisión en vivo de la conferencia magistral "Innovación en Ingeniería Biomédica: Tecnologías Emergentes para el Futuro de la Medicina".

Ponente: Dr. María Fernández, Ph.D. en Ingeniería Biomédica
Instituto Tecnológico de Massachusetts (MIT)

Temas a tratar:
• Inteligencia Artificial en Diagnóstico Médico
• Nanotecnología en Medicina Regenerativa  
• Dispositivos Médicos Inteligentes
• Bioimpresión 3D y Órganos Artificiales
• Ética en la Innovación Biomédica

La conferencia incluye sesión de preguntas y respuestas al final.`,
  isLive: true,
  status: 'live',
  embedUrl: 'https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1&mute=1',
  provider: 'youtube',
  streamKey: 'live_stream_key_2024',
  viewerCount: 1456,
  maxViewers: 2134,
  thumbnail: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&h=450&fit=crop',
  facultyId: 'fing',
  categoryId: 'fing-simposiums',
  tags: ['live', 'conferencia', 'ingenieria', 'biomedica', 'innovacion', 'mit'],
  scheduledStart: '2024-06-15T14:00:00Z',
  actualStart: '2024-06-15T14:05:00Z',
  actualEnd: undefined,
  chat: {
    enabled: true,
    moderationLevel: 'moderate',
    allowGuests: true
  },
  recording: {
    enabled: true,
    autoPublish: true,
    retentionDays: 365
  }
}

export const mockChatConfig: ChatConfig = {
  enabled: true,
  maxMessageLength: 200,
  rateLimitMessages: 3,
  rateLimitWindow: 60,
  slowMode: false,
  slowModeDelay: 30,
  autoModeration: true,
  bannedWords: [
    'spam',
    'promocion',
    'venta',
    'enlace',
    'link',
    'http',
    'www',
    'compra',
    'descuento'
  ]
}

// Streams programados para el futuro
export const scheduledStreams: LiveStream[] = [
  {
    id: 'scheduled-1',
    title: 'Graduación FISICC 2024 - Ceremonia de Grado',
    description: 'Transmisión en vivo de la ceremonia de graduación de la Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación.',
    isLive: false,
    status: 'scheduled',
    embedUrl: 'https://www.youtube.com/embed/placeholder',
    provider: 'youtube',
    viewerCount: 0,
    maxViewers: 0,
    thumbnail: 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=800&h=450&fit=crop',
    facultyId: 'fisicc',
    categoryId: 'fisicc-graduaciones',
    tags: ['graduacion', 'fisicc', 'ceremonia', 'diploma'],
    scheduledStart: '2024-06-20T09:00:00Z',
    actualStart: undefined,
    actualEnd: undefined,
    chat: {
      enabled: true,
      moderationLevel: 'moderate',
      allowGuests: true
    },
    recording: {
      enabled: true,
      autoPublish: true,
      retentionDays: 365
    }
  },
  {
    id: 'scheduled-2',
    title: 'Simposium Internacional de Medicina',
    description: 'Simposium internacional con especialistas médicos de reconocimiento mundial presentando los últimos avances en medicina.',
    isLive: false,
    status: 'scheduled',
    embedUrl: 'https://www.youtube.com/embed/placeholder',
    provider: 'youtube',
    viewerCount: 0,
    maxViewers: 0,
    thumbnail: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=800&h=450&fit=crop',
    facultyId: 'facmed',
    categoryId: 'facmed-congresos',
    tags: ['simposium', 'medicina', 'internacional', 'especialistas'],
    scheduledStart: '2024-06-25T08:00:00Z',
    actualStart: undefined,
    actualEnd: undefined,
    chat: {
      enabled: true,
      moderationLevel: 'strict',
      allowGuests: false
    },
    recording: {
      enabled: true,
      autoPublish: true,
      retentionDays: 365
    }
  },
  {
    id: 'scheduled-3',
    title: 'Mesa Redonda: Futuro de la Comunicación Digital',
    description: 'Mesa redonda con expertos en comunicación digital y nuevas tecnologías mediáticas.',
    isLive: false,
    status: 'scheduled',
    embedUrl: 'https://www.youtube.com/embed/placeholder',
    provider: 'youtube',
    viewerCount: 0,
    maxViewers: 0,
    thumbnail: 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=450&fit=crop',
    facultyId: 'facom',
    categoryId: 'facom-eventos',
    tags: ['mesa-redonda', 'comunicacion', 'digital', 'tecnologia'],
    scheduledStart: '2024-06-18T15:00:00Z',
    actualStart: undefined,
    actualEnd: undefined,
    chat: {
      enabled: true,
      moderationLevel: 'relaxed',
      allowGuests: true
    },
    recording: {
      enabled: true,
      autoPublish: true,
      retentionDays: 180
    }
  }
]

// Streams que han terminado recientemente
export const recentEndedStreams: LiveStream[] = [
  {
    id: 'ended-1',
    title: 'Hackathon FISICC 2024 - Presentaciones Finales',
    description: 'Presentaciones finales del Hackathon anual donde los equipos mostraron sus proyectos desarrollados.',
    isLive: false,
    status: 'ended',
    embedUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    provider: 'youtube',
    viewerCount: 0,
    maxViewers: 892,
    thumbnail: 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=450&fit=crop',
    facultyId: 'fisicc',
    categoryId: 'fisicc-eventos',
    tags: ['hackathon', 'presentaciones', 'proyectos', 'competencia'],
    scheduledStart: '2024-06-12T18:00:00Z',
    actualStart: '2024-06-12T18:05:00Z',
    actualEnd: '2024-06-12T21:30:00Z',
    chat: {
      enabled: true,
      moderationLevel: 'moderate',
      allowGuests: true
    },
    recording: {
      enabled: true,
      autoPublish: true,
      retentionDays: 365
    }
  }
]

// Helper functions
export const getCurrentLiveStream = (): LiveStream | undefined => {
  return mockLiveStream.isLive && mockLiveStream.status === 'live' ? mockLiveStream : undefined
}

export const getScheduledStreams = (): LiveStream[] => {
  return scheduledStreams.filter(stream => 
    stream.status === 'scheduled' && 
    new Date(stream.scheduledStart!) > new Date()
  ).sort((a, b) => 
    new Date(a.scheduledStart!).getTime() - new Date(b.scheduledStart!).getTime()
  )
}

export const getUpcomingStream = (): LiveStream | undefined => {
  const upcoming = getScheduledStreams()
  return upcoming.length > 0 ? upcoming[0] : undefined
}

export const getStreamsByFaculty = (facultyId: string): LiveStream[] => {
  return [...scheduledStreams, ...recentEndedStreams, mockLiveStream]
    .filter(stream => stream.facultyId === facultyId)
}

export const getRecentStreams = (limit: number = 5): LiveStream[] => {
  return recentEndedStreams
    .sort((a, b) => new Date(b.actualEnd!).getTime() - new Date(a.actualEnd!).getTime())
    .slice(0, limit)
}

export const getLiveStreamStats = () => {
  const totalScheduled = scheduledStreams.length
  const totalEnded = recentEndedStreams.length
  const isCurrentlyLive = mockLiveStream.isLive
  const currentViewers = isCurrentlyLive ? mockLiveStream.viewerCount : 0
  const maxViewersEver = Math.max(
    mockLiveStream.maxViewers,
    ...recentEndedStreams.map(s => s.maxViewers)
  )

  return {
    isLive: isCurrentlyLive,
    currentViewers,
    totalScheduled,
    totalEnded,
    maxViewersEver,
    totalStreamsThisMonth: totalEnded + (isCurrentlyLive ? 1 : 0),
    averageViewers: Math.round(
      (currentViewers + recentEndedStreams.reduce((sum, s) => sum + s.maxViewers, 0)) / 
      (recentEndedStreams.length + (isCurrentlyLive ? 1 : 0))
    )
  }
}

export const updateViewerCount = (streamId: string, newCount: number): void => {
  if (streamId === mockLiveStream.id) {
    mockLiveStream.viewerCount = newCount
    if (newCount > mockLiveStream.maxViewers) {
      mockLiveStream.maxViewers = newCount
    }
  }
}

export const simulateViewerCountChanges = (): void => {
  if (mockLiveStream.isLive) {
    // Simular cambios realistas en el número de viewers
    const baseCount = 1456
    const variation = Math.floor(Math.random() * 200) - 100 // ±100 viewers
    const newCount = Math.max(0, baseCount + variation)
    updateViewerCount(mockLiveStream.id, newCount)
  }
}