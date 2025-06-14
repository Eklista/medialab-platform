// src/modules/cmsFrontend/components/sections/StatsSection.tsx
import React from 'react'
import { motion, useMotionValue, animate } from 'framer-motion'
import { Users, Video, Images, Eye, Clock, GraduationCap, TrendingUp, Calendar } from 'lucide-react'
import { Card, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { cn } from '../../utils/cn'
import { getContentStats } from '../../data/mockContent'
import { getLiveStreamStats } from '../../data/mockLiveStream'
import { getFacultyStats } from '../../data/mockFaculties'

interface StatsItemProps {
  icon: React.ReactNode
  label: string
  value: number
  suffix?: string
  prefix?: string
  color?: string
  description?: string
  delay?: number
}

interface StatsSectionProps {
  className?: string
}

const StatsItem: React.FC<StatsItemProps> = ({ 
  icon, 
  label, 
  value, 
  suffix = '', 
  prefix = '',
  color = 'text-primary-600',
  description,
  delay = 0
}) => {
  const count = useMotionValue(0)
  const [displayValue, setDisplayValue] = React.useState(0)

  React.useEffect(() => {
    const controls = animate(count, value, {
      duration: 2,
      delay: delay,
      ease: 'easeOut',
      onUpdate: (latest) => {
        setDisplayValue(Math.round(latest))
      }
    })

    return controls.stop
  }, [count, value, delay])

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
      whileHover={{ y: -4 }}
    >
      <Card variant="elevated" className="text-center h-full group hover:shadow-xl transition-all duration-300">
        <CardContent className="p-6">
          <div className={cn('inline-flex p-3 rounded-full mb-4 group-hover:scale-110 transition-transform', 
            color.includes('primary') ? 'bg-primary-100 dark:bg-primary-900/30' :
            color.includes('emerald') ? 'bg-emerald-100 dark:bg-emerald-900/30' :
            color.includes('amber') ? 'bg-amber-100 dark:bg-amber-900/30' :
            color.includes('red') ? 'bg-red-100 dark:bg-red-900/30' :
            'bg-zinc-100 dark:bg-zinc-800'
          )}>
            <div className={cn('w-6 h-6', color)}>
              {icon}
            </div>
          </div>
          
          <div className="space-y-2">
            <div className={cn('text-3xl lg:text-4xl font-bold', color)}>
              {prefix}{formatNumber(displayValue)}{suffix}
            </div>
            
            <div className="font-medium text-zinc-900 dark:text-zinc-100">
              {label}
            </div>
            
            {description && (
              <div className="text-sm text-zinc-500 dark:text-zinc-400">
                {description}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export const StatsSection: React.FC<StatsSectionProps> = ({ className }) => {
  const contentStats = getContentStats()
  const liveStats = getLiveStreamStats()
  const facultyStats = getFacultyStats()

  // Calculate additional stats
  const totalContent = contentStats.videos + contentStats.galleries
  const averageViewsPerContent = Math.round(contentStats.totalViews / totalContent)
  const estimatedHours = Math.round(contentStats.videos * 35 / 60) // Assuming avg 35min per video

  const mainStats = [
    {
      icon: <GraduationCap className="w-6 h-6" />,
      label: 'Facultades',
      value: facultyStats.totalFaculties,
      color: 'text-primary-600 dark:text-primary-400',
      description: 'Universidad Galileo'
    },
    {
      icon: <Video className="w-6 h-6" />,
      label: 'Videos',
      value: contentStats.videos,
      color: 'text-blue-600 dark:text-blue-400',
      description: 'Contenido audiovisual'
    },
    {
      icon: <Images className="w-6 h-6" />,
      label: 'Galerías',
      value: contentStats.galleries,
      color: 'text-emerald-600 dark:text-emerald-400',
      description: 'Colecciones fotográficas'
    },
    {
      icon: <Eye className="w-6 h-6" />,
      label: 'Visualizaciones',
      value: contentStats.totalViews,
      color: 'text-purple-600 dark:text-purple-400',
      description: 'Total de reproducciones'
    }
  ]

  const secondaryStats = [
    {
      icon: <Users className="w-6 h-6" />,
      label: 'Suscriptores',
      value: facultyStats.totalSubscribers,
      color: 'text-orange-600 dark:text-orange-400',
      description: 'Comunidad activa'
    },
    {
      icon: <Clock className="w-6 h-6" />,
      label: 'Horas de Contenido',
      value: estimatedHours,
      suffix: 'h',
      color: 'text-indigo-600 dark:text-indigo-400',
      description: 'Tiempo total estimado'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      label: 'Promedio de Vistas',
      value: averageViewsPerContent,
      color: 'text-green-600 dark:text-green-400',
      description: 'Por contenido'
    },
    {
      icon: <Calendar className="w-6 h-6" />,
      label: 'Este Mes',
      value: 45892, // Mock monthly views
      color: 'text-cyan-600 dark:text-cyan-400',
      description: 'Visualizaciones mensuales'
    }
  ]

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
            MediaLab en Números
          </h2>
          <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
            Descubre el impacto y alcance de nuestro contenido multimedia universitario
          </p>
        </motion.div>

        {/* Live Stream Status */}
        {liveStats.isLive && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-12"
          >
            <Card variant="elevated" className="bg-gradient-to-r from-red-500 to-pink-600 text-white overflow-hidden">
              <CardContent className="p-6 text-center relative">
                <div className="absolute inset-0 bg-black/10" />
                <div className="relative z-10">
                  <Badge variant="live" className="bg-white/20 text-white border-white/30 mb-3">
                    ● EN VIVO AHORA
                  </Badge>
                  <div className="flex items-center justify-center gap-6">
                    <div>
                      <div className="text-2xl font-bold">{liveStats.currentViewers.toLocaleString()}</div>
                      <div className="text-sm opacity-90">Viendo ahora</div>
                    </div>
                    <div className="w-px h-8 bg-white/30" />
                    <div>
                      <div className="text-2xl font-bold">{liveStats.maxViewersEver.toLocaleString()}</div>
                      <div className="text-sm opacity-90">Récord de audiencia</div>
                    </div>
                    <div className="w-px h-8 bg-white/30" />
                    <div>
                      <div className="text-2xl font-bold">{liveStats.totalStreamsThisMonth}</div>
                      <div className="text-sm opacity-90">Streams este mes</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Main Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {mainStats.map((stat, index) => (
            <StatsItem
              key={stat.label}
              {...stat}
              delay={index * 0.1}
            />
          ))}
        </div>

        {/* Secondary Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {secondaryStats.map((stat, index) => (
            <StatsItem
              key={stat.label}
              {...stat}
              delay={0.4 + index * 0.1}
            />
          ))}
        </div>

        {/* Achievement Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <Card variant="elevated" className="text-center group hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="inline-flex p-3 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 mb-4 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                Contenido Más Visto
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3">
                {contentStats.mostViewed.title}
              </p>
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {contentStats.mostViewed.stats.views.toLocaleString()} vistas
              </div>
            </CardContent>
          </Card>

          <Card variant="elevated" className="text-center group hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="inline-flex p-3 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 mb-4 group-hover:scale-110 transition-transform">
                <Video className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                Promedio de Calidad
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3">
                Contenido en alta definición
              </p>
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                1080p HD
              </div>
            </CardContent>
          </Card>

          <Card variant="elevated" className="text-center group hover:shadow-xl transition-all duration-300">
            <CardContent className="p-6">
              <div className="inline-flex p-3 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 mb-4 group-hover:scale-110 transition-transform">
                <Users className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                Engagement Rate
              </h3>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3">
                Interacción promedio
              </p>
              <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                {Math.round((contentStats.totalLikes / contentStats.totalViews) * 100 * 100)}%
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 1 }}
          className="text-center mt-16"
        >
          <div className="max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
              Sé Parte de Nuestra Comunidad
            </h3>
            <p className="text-zinc-600 dark:text-zinc-400 mb-6">
              Únete a miles de estudiantes, profesores y profesionales que confían en MediaLab 
              para mantenerse conectados con el contenido académico de la Universidad Galileo.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                Explorar Contenido
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-3 border border-zinc-300 dark:border-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-lg font-medium hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
              >
                Ver Transmisión en Vivo
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}