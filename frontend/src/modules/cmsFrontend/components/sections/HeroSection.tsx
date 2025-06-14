// src/modules/cmsFrontend/components/sections/HeroSection.tsx
import React from 'react'
import { motion } from 'framer-motion'
import { Play, Users, TrendingUp } from 'lucide-react'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { Card, CardContent } from '../ui/Card'
import { cn } from '../../utils/cn'
import { getCurrentLiveStream } from '../../data/mockLiveStream'
import { getFacultyStats } from '../../data/mockFaculties'
import { getContentStats } from '../../data/mockContent'

interface HeroSectionProps {
  className?: string
}

export const HeroSection: React.FC<HeroSectionProps> = ({ className }) => {
  const currentLive = getCurrentLiveStream()
  const facultyStats = getFacultyStats()
  const contentStats = getContentStats()

  const handleExploreContent = () => {
    console.log('Navigate to content explorer')
  }

  const handleWatchLive = () => {
    console.log('Navigate to live stream')
  }

  return (
    <section className={cn('py-6', className)}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Main Hero Card */}
        <Card className="overflow-hidden mb-6">
          <div className="relative h-48 md:h-56">
            {/* Background Gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-emerald-600" />
            
            {/* Content */}
            <div className="relative h-full flex items-center justify-between p-6 md:p-8">
              <div className="space-y-4 text-white max-w-lg">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                >
                  <h1 className="text-2xl md:text-3xl font-bold mb-2">
                    MediaLab Universidad Galileo
                  </h1>
                  <p className="text-primary-100">
                    Explora contenido multimedia de todas las facultades
                  </p>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                  className="flex gap-3"
                >
                  <Button 
                    onClick={handleExploreContent}
                    className="bg-white text-primary-700 hover:bg-white/90"
                  >
                    Explorar Contenido
                  </Button>
                  
                  {currentLive && (
                    <Button 
                      onClick={handleWatchLive}
                      variant="outline"
                      className="border-white/30 text-white hover:bg-white/10"
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Ver En Vivo
                    </Button>
                  )}
                </motion.div>
              </div>

              {/* Stats Grid */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="hidden md:grid grid-cols-2 gap-4 text-white text-right"
              >
                <div>
                  <div className="text-2xl font-bold">{facultyStats.totalFaculties}</div>
                  <div className="text-primary-100 text-sm">Facultades</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{contentStats.videos}</div>
                  <div className="text-primary-100 text-sm">Videos</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{contentStats.galleries}</div>
                  <div className="text-primary-100 text-sm">Galerías</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">{Math.round(contentStats.totalViews / 1000)}K</div>
                  <div className="text-primary-100 text-sm">Vistas</div>
                </div>
              </motion.div>
            </div>

            {/* Decorative Elements */}
            <div className="absolute top-4 right-4 w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm" />
            <div className="absolute bottom-4 left-4 w-6 h-6 rounded-full bg-emerald-400/30" />
          </div>
        </Card>

        {/* Secondary Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          {/* Live Stream Card */}
          {currentLive && (
            <Card variant="interactive" onClick={handleWatchLive} className="cursor-pointer">
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Badge variant="live" className="animate-pulse">
                    ● EN VIVO
                  </Badge>
                  <div className="flex items-center gap-1 text-sm text-zinc-600 dark:text-zinc-400">
                    <Users className="w-3 h-3" />
                    <span>{currentLive.viewerCount.toLocaleString()}</span>
                  </div>
                </div>
                
                <div className="relative aspect-video rounded-lg overflow-hidden mb-3">
                  <img 
                    src={currentLive.thumbnail} 
                    alt={currentLive.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                    <Play className="w-6 h-6 text-white" fill="currentColor" />
                  </div>
                </div>
                
                <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 text-sm line-clamp-2">
                  {currentLive.title}
                </h3>
              </CardContent>
            </Card>
          )}

          {/* Quick Stats Cards */}
          <Card>
            <CardContent className="p-4 text-center">
              <div className="flex items-center justify-center mb-2">
                <TrendingUp className="w-5 h-5 text-emerald-600 mr-2" />
                <span className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
                  +12%
                </span>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Crecimiento este mes
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-lg font-bold text-zinc-900 dark:text-zinc-100 mb-1">
                {contentStats.featured}
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Contenido destacado
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}