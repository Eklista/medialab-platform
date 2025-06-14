// src/modules/cmsFrontend/components/sections/FacultiesGrid.tsx
import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, Video, Images, Users, TrendingUp } from 'lucide-react'
import { Card, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { cn } from '../../utils/cn'
import { mockFaculties } from '../../data/mockFaculties'
import type { Faculty } from '../../data/types'

interface FacultiesGridProps {
  className?: string
  onFacultyClick?: (faculty: Faculty) => void
}

export const FacultiesGrid: React.FC<FacultiesGridProps> = ({ 
  className,
  onFacultyClick 
}) => {
  const handleFacultyClick = (faculty: Faculty) => {
    onFacultyClick?.(faculty)
    // TODO: Navigate to faculty page
    console.log('Navigate to faculty:', faculty.slug)
  }

  const formatNumber = (num: number): string => {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`
    }
    return num.toString()
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: 'easeOut'
      }
    }
  }

  return (
    <section className={cn('py-16 lg:py-24', className)}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12 lg:mb-16"
        >
          <h2 className="text-3xl lg:text-4xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
            Explora por Facultad
          </h2>
          <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            Descubre contenido multimedia organizado por cada facultad de la Universidad Galileo
          </p>
        </motion.div>

        {/* Faculties Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-6"
        >
          {mockFaculties.map((faculty) => (
            <motion.div key={faculty.id} variants={cardVariants}>
              <Card 
                variant="interactive"
                className="group h-full overflow-hidden border-2 hover:border-primary-200 dark:hover:border-primary-800 transition-all duration-300"
              >
                {/* Faculty Cover */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={faculty.thumbnail}
                    alt={faculty.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div 
                    className="absolute inset-0 opacity-60 group-hover:opacity-40 transition-opacity duration-300"
                    style={{ backgroundColor: faculty.color }}
                  />
                  
                  {/* Faculty Badge */}
                  <div className="absolute top-4 left-4">
                    <Badge 
                      variant="secondary" 
                      className="bg-white/90 text-zinc-900 font-semibold"
                    >
                      {faculty.name}
                    </Badge>
                  </div>

                  {/* Content Count */}
                  <div className="absolute top-4 right-4">
                    <div className="bg-black/70 text-white px-2 py-1 rounded-full text-xs font-medium">
                      {faculty.stats.totalVideos + faculty.stats.totalGalleries} contenidos
                    </div>
                  </div>
                </div>

                <CardContent className="p-6">
                  {/* Faculty Info */}
                  <div className="mb-4">
                    <h3 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {faculty.name}
                    </h3>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 font-medium mb-2">
                      {faculty.fullName}
                    </p>
                    <p className="text-sm text-zinc-500 dark:text-zinc-500 line-clamp-2">
                      {faculty.description}
                    </p>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="text-center p-3 rounded-lg bg-zinc-50 dark:bg-zinc-800">
                      <div className="flex items-center justify-center mb-1">
                        <Video className="w-4 h-4 text-blue-600 mr-1" />
                        <span className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
                          {faculty.stats.totalVideos}
                        </span>
                      </div>
                      <div className="text-xs text-zinc-500 dark:text-zinc-400">Videos</div>
                    </div>
                    
                    <div className="text-center p-3 rounded-lg bg-zinc-50 dark:bg-zinc-800">
                      <div className="flex items-center justify-center mb-1">
                        <Images className="w-4 h-4 text-emerald-600 mr-1" />
                        <span className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
                          {faculty.stats.totalGalleries}
                        </span>
                      </div>
                      <div className="text-xs text-zinc-500 dark:text-zinc-400">Galerías</div>
                    </div>
                  </div>

                  {/* Additional Stats */}
                  <div className="flex items-center justify-between mb-4 text-sm text-zinc-600 dark:text-zinc-400">
                    <div className="flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      <span>{formatNumber(faculty.stats.totalViews)} vistas</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="w-4 h-4" />
                      <span>{formatNumber(faculty.stats.totalSubscribers)} suscriptores</span>
                    </div>
                  </div>

                  {/* Categories Preview */}
                  <div className="mb-4">
                    <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-2">
                      Categorías principales:
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {faculty.categories.slice(0, 3).map((category) => (
                        <Badge 
                          key={category.id}
                          variant="outline"
                          className="text-xs"
                        >
                          {category.name}
                        </Badge>
                      ))}
                      {faculty.categories.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{faculty.categories.length - 3} más
                        </Badge>
                      )}
                    </div>
                  </div>

                  {/* Action Button */}
                  <Button
                    onClick={() => handleFacultyClick(faculty)}
                    variant="outline"
                    size="sm"
                    className="w-full group-hover:bg-primary-600 group-hover:text-white group-hover:border-primary-600 transition-all duration-300"
                  >
                    <span>Explorar {faculty.name}</span>
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* View All Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center mt-12"
        >
          <Button variant="outline" size="lg">
            Ver Todas las Facultades
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </motion.div>
      </div>
    </section>
  )
}