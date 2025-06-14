// src/modules/cmsFrontend/components/sections/LiveStreamCard.tsx
import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Play, 
  Users, 
  Calendar, 
  Clock, 
  Radio, 
  MessageCircle, 
  Share2, 
  Maximize,
  Volume2,
  VolumeX,
  Settings
} from 'lucide-react'
import { Card, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { cn } from '../../utils/cn'
import { 
  getCurrentLiveStream, 
  getUpcomingStream,
  simulateViewerCountChanges 
} from '../../data/mockLiveStream'
import { getFacultyById } from '../../data/mockFaculties'
import type { LiveStream } from '../../data/types'

interface LiveStreamCardProps {
  className?: string
  variant?: 'compact' | 'featured' | 'hero'
  onWatchClick?: (stream: LiveStream) => void
  onChatToggle?: () => void
  showChat?: boolean
}

export const LiveStreamCard: React.FC<LiveStreamCardProps> = ({
  className,
  variant = 'featured',
  onWatchClick,
  onChatToggle,
  showChat = false
}) => {
  const [currentStream, setCurrentStream] = React.useState<LiveStream | undefined>()
  const [upcomingStream, setUpcomingStream] = React.useState<LiveStream | undefined>()
  const [viewerCount, setViewerCount] = React.useState(0)
  const [isPlaying, setIsPlaying] = React.useState(false)
  const [isMuted, setIsMuted] = React.useState(true)
  const [showControls, setShowControls] = React.useState(false)

  React.useEffect(() => {
    const live = getCurrentLiveStream()
    const upcoming = getUpcomingStream()
    
    setCurrentStream(live || undefined)
    setUpcomingStream(upcoming || undefined)
    
    if (live) {
      setViewerCount(live.viewerCount)
      
      // Simular cambios en viewer count
      const interval = setInterval(() => {
        simulateViewerCountChanges()
        const updatedStream = getCurrentLiveStream()
        if (updatedStream) {
          setViewerCount(updatedStream.viewerCount)
        }
      }, 3000)

      return () => clearInterval(interval)
    }
  }, [])

  const handleWatchClick = () => {
    if (currentStream) {
      setIsPlaying(true)
      onWatchClick?.(currentStream)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.abs(date.getTime() - now.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 24) {
      return new Intl.DateTimeFormat('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }
    
    return new Intl.DateTimeFormat('es-ES', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }

  const getTimeUntilStream = (dateString: string) => {
    const streamTime = new Date(dateString)
    const now = new Date()
    const diffInMinutes = Math.floor((streamTime.getTime() - now.getTime()) / (1000 * 60))
    
    if (diffInMinutes < 60) {
      return `en ${diffInMinutes}min`
    }
    
    const diffInHours = Math.floor(diffInMinutes / 60)
    if (diffInHours < 24) {
      return `en ${diffInHours}h`
    }
    
    const diffInDays = Math.floor(diffInHours / 24)
    return `en ${diffInDays}d`
  }

  // Render para stream activo
  const renderLiveStream = () => {
    const faculty = currentStream ? getFacultyById(currentStream.facultyId || '') : null
    
    return (
      <Card 
        variant={variant === 'hero' ? 'elevated' : 'interactive'}
        className={cn(
          'overflow-hidden border-2 group',
          variant === 'hero' && 'border-red-500/20 bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-950/20 dark:to-pink-950/20',
          variant === 'featured' && 'hover:border-red-500/30',
          variant === 'compact' && 'border-red-500/30'
        )}
      >
        {/* Live Stream Video Area */}
        <div 
          className={cn(
            'relative overflow-hidden',
            variant === 'hero' ? 'aspect-video' : variant === 'featured' ? 'aspect-video' : 'aspect-[16/10]'
          )}
          onMouseEnter={() => setShowControls(true)}
          onMouseLeave={() => setShowControls(false)}
        >
          {/* Stream Thumbnail/Video */}
          <img
            src={currentStream?.thumbnail}
            alt={currentStream?.title}
            className="w-full h-full object-cover"
          />
          
          {/* Live Overlay */}
          <div className="absolute inset-0 bg-black/20" />
          
          {/* Live Indicator */}
          <div className="absolute top-4 left-4 z-10">
            <motion.div
              animate={{ opacity: [1, 0.5, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <Badge variant="live" className="bg-red-600 text-white border-0 font-semibold">
                <Radio className="w-3 h-3 mr-1" />
                EN VIVO
              </Badge>
            </motion.div>
          </div>

          {/* Viewer Count */}
          <div className="absolute top-4 right-4 z-10">
            <motion.div
              key={viewerCount}
              initial={{ scale: 1.1 }}
              animate={{ scale: 1 }}
              className="bg-black/70 text-white px-3 py-1 rounded-full text-sm font-medium"
            >
              <Users className="w-4 h-4 inline mr-1" />
              {viewerCount.toLocaleString()}
            </motion.div>
          </div>

          {/* Faculty Badge */}
          {faculty && (
            <div className="absolute bottom-4 left-4 z-10">
              <Badge 
                variant="secondary"
                className="bg-black/70 text-white border-0"
              >
                {faculty.name}
              </Badge>
            </div>
          )}

          {/* Play Button / Controls */}
          <div className="absolute inset-0 flex items-center justify-center">
            {!isPlaying ? (
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleWatchClick}
                className="w-20 h-20 bg-white/90 rounded-full flex items-center justify-center shadow-xl hover:bg-white transition-colors group"
              >
                <Play className="w-10 h-10 text-zinc-900 ml-1 group-hover:text-red-600" fill="currentColor" />
              </motion.button>
            ) : (
              <AnimatePresence>
                {showControls && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex items-center gap-4"
                  >
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setIsMuted(!isMuted)}
                      className="bg-black/50 text-white hover:bg-black/70"
                    >
                      {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="bg-black/50 text-white hover:bg-black/70"
                    >
                      <Settings className="w-5 h-5" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="bg-black/50 text-white hover:bg-black/70"
                    >
                      <Maximize className="w-5 h-5" />
                    </Button>
                  </motion.div>
                )}
              </AnimatePresence>
            )}
          </div>
        </div>

        <CardContent className={cn('p-6', variant === 'compact' && 'p-4')}>
          {/* Stream Info */}
          <div className="space-y-4">
            <div>
              <h3 className={cn(
                'font-bold text-zinc-900 dark:text-zinc-100 line-clamp-2',
                variant === 'hero' ? 'text-2xl' : variant === 'featured' ? 'text-xl' : 'text-lg'
              )}>
                {currentStream?.title}
              </h3>
              
              {variant !== 'compact' && (
                <p className="text-zinc-600 dark:text-zinc-400 mt-2 line-clamp-2">
                  {currentStream?.description}
                </p>
              )}
            </div>

            {/* Stream Actions */}
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <Button 
                  onClick={handleWatchClick}
                  className="bg-red-600 hover:bg-red-700"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Ver Ahora
                </Button>
                
                {variant !== 'compact' && (
                  <>
                    <Button 
                      variant="outline" 
                      size="icon"
                      onClick={onChatToggle}
                      className={showChat ? 'bg-primary-50 border-primary-300' : ''}
                    >
                      <MessageCircle className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="icon">
                      <Share2 className="w-4 h-4" />
                    </Button>
                  </>
                )}
              </div>

              {/* Live Stats */}
              <div className="text-right text-sm text-zinc-500 dark:text-zinc-400">
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>Iniciado hace 2h</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Render para stream programado
  const renderUpcomingStream = () => {
    const faculty = upcomingStream ? getFacultyById(upcomingStream.facultyId || '') : null
    
    return (
      <Card variant="outlined" className="overflow-hidden">
        <div className="relative aspect-video overflow-hidden">
          <img
            src={upcomingStream?.thumbnail}
            alt={upcomingStream?.title}
            className="w-full h-full object-cover opacity-75"
          />
          <div className="absolute inset-0 bg-black/40" />
          
          {/* Upcoming Badge */}
          <div className="absolute top-4 left-4">
            <Badge variant="warning">
              <Calendar className="w-3 h-3 mr-1" />
              PRÓXIMAMENTE
            </Badge>
          </div>

          {/* Time Until Stream */}
          <div className="absolute top-4 right-4">
            <div className="bg-black/70 text-white px-3 py-1 rounded-full text-sm font-medium">
              {getTimeUntilStream(upcomingStream?.scheduledStart || '')}
            </div>
          </div>

          {/* Faculty Badge */}
          {faculty && (
            <div className="absolute bottom-4 left-4">
              <Badge variant="secondary" className="bg-black/70 text-white border-0">
                {faculty.name}
              </Badge>
            </div>
          )}

          {/* Clock Icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-20 h-20 bg-white/90 rounded-full flex items-center justify-center">
              <Clock className="w-10 h-10 text-zinc-600" />
            </div>
          </div>
        </div>

        <CardContent className="p-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 line-clamp-2">
                {upcomingStream?.title}
              </h3>
              <p className="text-zinc-600 dark:text-zinc-400 mt-2 line-clamp-2">
                {upcomingStream?.description}
              </p>
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                  {formatDate(upcomingStream?.scheduledStart || '')}
                </div>
                <div className="text-xs text-zinc-500 dark:text-zinc-400">
                  {getTimeUntilStream(upcomingStream?.scheduledStart || '')}
                </div>
              </div>
              
              <Button variant="outline">
                <Calendar className="w-4 h-4 mr-2" />
                Recordar
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Render para no hay streams
  const renderNoStream = () => (
    <Card variant="outlined" className="text-center">
      <CardContent className="p-8">
        <div className="w-16 h-16 mx-auto mb-4 bg-zinc-100 dark:bg-zinc-800 rounded-full flex items-center justify-center">
          <Radio className="w-8 h-8 text-zinc-400" />
        </div>
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
          No hay transmisiones en vivo
        </h3>
        <p className="text-zinc-600 dark:text-zinc-400 mb-4">
          Mantente atento a nuestras próximas transmisiones
        </p>
        <Button variant="outline">
          <Calendar className="w-4 h-4 mr-2" />
          Ver Programación
        </Button>
      </CardContent>
    </Card>
  )

  return (
    <div className={className}>
      {currentStream ? renderLiveStream() : upcomingStream ? renderUpcomingStream() : renderNoStream()}
    </div>
  )
}