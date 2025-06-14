// src/modules/cmsFrontend/components/sections/FeaturedContent.tsx
import React from 'react'
import { motion } from 'framer-motion'
import { Play, Images, Eye, Calendar, Heart, ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react'
import { Card, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { cn } from '../../utils/cn'
import { getFeaturedContent, getPopularContent, getRecentContent } from '../../data/mockContent'
import { getFacultyById } from '../../data/mockFaculties'
import type { ContentItem } from '../../data/types'

interface FeaturedContentProps {
  className?: string
  onContentClick?: (content: ContentItem) => void
}

export const FeaturedContent: React.FC<FeaturedContentProps> = ({ 
  className,
  onContentClick 
}) => {
  const [activeTab, setActiveTab] = React.useState<'featured' | 'popular' | 'recent'>('featured')
  const [currentIndex, setCurrentIndex] = React.useState(0)
  const scrollContainerRef = React.useRef<HTMLDivElement>(null)

  // Get content based on active tab
  const getContent = () => {
    switch (activeTab) {
      case 'featured':
        return getFeaturedContent()
      case 'popular':
        return getPopularContent(8)
      case 'recent':
        return getRecentContent(8)
      default:
        return getFeaturedContent()
    }
  }

  const content = getContent()

  const handleContentClick = (item: ContentItem) => {
    onContentClick?.(item)
    // TODO: Navigate to content page
    console.log('Navigate to content:', item.slug)
  }

  const handlePrevious = () => {
    if (scrollContainerRef.current) {
      const container = scrollContainerRef.current
      const cardWidth = container.children[0]?.clientWidth || 0
      const gap = 24 // gap-6 = 24px
      const scrollAmount = cardWidth + gap
      
      container.scrollBy({ left: -scrollAmount * 2, behavior: 'smooth' })
      setCurrentIndex(Math.max(0, currentIndex - 2))
    }
  }

  const handleNext = () => {
    if (scrollContainerRef.current) {
      const container = scrollContainerRef.current
      const cardWidth = container.children[0]?.clientWidth || 0
      const gap = 24
      const scrollAmount = cardWidth + gap
      
      container.scrollBy({ left: scrollAmount * 2, behavior: 'smooth' })
      setCurrentIndex(Math.min(content.length - 2, currentIndex + 2))
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    }).format(date)
  }

  const formatDuration = (duration: string) => {
    return duration.split(':').slice(0, 2).join(':') // Remove seconds if present
  }

  const ContentCard: React.FC<{ item: ContentItem; index: number }> = ({ item, index }) => {
    const faculty = getFacultyById(item.facultyId)
    
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5, delay: index * 0.1 }}
        className="flex-shrink-0 w-80"
      >
        <Card 
          variant="interactive"
          className="group h-full overflow-hidden"
        >
          {/* Thumbnail */}
          <div className="relative aspect-video overflow-hidden">
            <img
              src={item.thumbnail}
              alt={item.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <div className="absolute inset-0 bg-black/20 group-hover:bg-black/30 transition-colors" />
            
            {/* Content Type Indicator */}
            <div className="absolute top-3 left-3">
              <Badge 
                variant={item.type === 'video' ? 'default' : 'success'}
                className="bg-black/70 text-white border-0"
              >
                {item.type === 'video' ? (
                  <>
                    <Play className="w-3 h-3 mr-1" />
                    Video
                  </>
                ) : (
                  <>
                    <Images className="w-3 h-3 mr-1" />
                    Galería
                  </>
                )}
              </Badge>
            </div>

            {/* Duration or Photo Count */}
            <div className="absolute bottom-3 right-3">
              <div className="bg-black/80 text-white px-2 py-1 rounded text-xs font-medium">
                {item.type === 'video' 
                  ? formatDuration(item.video?.duration || '0:00')
                  : `${item.gallery?.photoCount || 0} fotos`
                }
              </div>
            </div>

            {/* Play Button for Videos */}
            {item.type === 'video' && (
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 bg-white/90 rounded-full flex items-center justify-center shadow-lg">
                  <Play className="w-6 h-6 text-zinc-900 ml-1" fill="currentColor" />
                </div>
              </div>
            )}

            {/* Featured Badge */}
            {item.featured && (
              <div className="absolute top-3 right-3">
                <Badge variant="warning" className="bg-amber-500 text-white border-0">
                  Destacado
                </Badge>
              </div>
            )}
          </div>

          <CardContent className="p-4">
            {/* Faculty Badge */}
            <div className="flex items-center justify-between mb-2">
              <Badge 
                variant="outline" 
                className="text-xs"
                style={{ borderColor: faculty?.color, color: faculty?.color }}
              >
                {faculty?.name}
              </Badge>
              <div className="flex items-center gap-1 text-xs text-zinc-500 dark:text-zinc-400">
                <Calendar className="w-3 h-3" />
                {formatDate(item.publishedAt)}
              </div>
            </div>

            {/* Title */}
            <h3 
              onClick={() => handleContentClick(item)}
              className="font-semibold text-zinc-900 dark:text-zinc-100 mb-2 line-clamp-2 cursor-pointer group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors"
            >
              {item.title}
            </h3>

            {/* Description */}
            <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3 line-clamp-2">
              {item.description}
            </p>

            {/* Stats */}
            <div className="flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1">
                  <Eye className="w-3 h-3" />
                  <span>{item.stats.views.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Heart className="w-3 h-3" />
                  <span>{item.stats.likes}</span>
                </div>
              </div>
              
              {/* Author */}
              <div className="text-xs text-zinc-400 truncate max-w-[120px]">
                {item.author?.name}
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    )
  }

  const tabVariants = {
    inactive: { opacity: 0.6, scale: 0.95 },
    active: { opacity: 1, scale: 1 }
  }

  return (
    <section className={cn('py-16 lg:py-24 bg-zinc-50 dark:bg-zinc-900/50', className)}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl lg:text-4xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
            Contenido Destacado
          </h2>
          <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            Descubre los videos y galerías más populares de todas las facultades
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="flex justify-center mb-8"
        >
          <div className="flex items-center gap-1 p-1 bg-white dark:bg-zinc-800 rounded-lg shadow-sm border border-zinc-200 dark:border-zinc-700">
            {[
              { key: 'featured', label: 'Destacado', count: getFeaturedContent().length },
              { key: 'popular', label: 'Popular', count: getPopularContent().length },
              { key: 'recent', label: 'Reciente', count: getRecentContent().length }
            ].map((tab) => (
              <motion.button
                key={tab.key}
                variants={tabVariants}
                animate={activeTab === tab.key ? 'active' : 'inactive'}
                onClick={() => setActiveTab(tab.key as any)}
                className={cn(
                  'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200',
                  activeTab === tab.key
                    ? 'bg-primary-600 text-white shadow-sm'
                    : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100'
                )}
              >
                {tab.label}
                <span className="ml-2 text-xs opacity-75">({tab.count})</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Content Carousel */}
        <div className="relative">
          {/* Navigation Buttons */}
          <div className="hidden lg:flex justify-between absolute inset-y-0 -left-6 -right-6 items-center z-10 pointer-events-none">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handlePrevious}
              disabled={currentIndex === 0}
              className={cn(
                "w-12 h-12 rounded-full bg-white dark:bg-zinc-800 shadow-lg flex items-center justify-center pointer-events-auto transition-all",
                currentIndex === 0 
                  ? "opacity-50 cursor-not-allowed" 
                  : "hover:bg-zinc-50 dark:hover:bg-zinc-700"
              )}
            >
              <ChevronLeft className="w-6 h-6 text-zinc-600 dark:text-zinc-400" />
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={handleNext}
              disabled={currentIndex >= content.length - 2}
              className={cn(
                "w-12 h-12 rounded-full bg-white dark:bg-zinc-800 shadow-lg flex items-center justify-center pointer-events-auto transition-all",
                currentIndex >= content.length - 2
                  ? "opacity-50 cursor-not-allowed"
                  : "hover:bg-zinc-50 dark:hover:bg-zinc-700"
              )}
            >
              <ChevronRight className="w-6 h-6 text-zinc-600 dark:text-zinc-400" />
            </motion.button>
          </div>

          {/* Content Cards */}
          <div 
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {content.map((item, index) => (
              <ContentCard key={item.id} item={item} index={index} />
            ))}
          </div>
        </div>

        {/* View All Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center mt-12"
        >
          <Button variant="outline" size="lg">
            Ver Todo el Contenido
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </motion.div>
      </div>
    </section>
  )
}