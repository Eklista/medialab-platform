// src/modules/cmsFrontend/components/layout/Sidebar.tsx
import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronRight } from 'lucide-react'
import { Badge } from '../ui/Badge'
import { cn } from '../../utils/cn'
import { 
  primaryNavigation, 
  facultyNavigation,
  updateNavigationBadges 
} from '../../data/mockNavigation'
import type { NavigationItem } from '../../data/types'

// Helper para obtener el icono de Lucide
const getIcon = (iconName: string) => {
  const icons: { [key: string]: React.ComponentType<{ className?: string }> } = {
    Home: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    ),
    Radio: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2z" />
      </svg>
    ),
    Video: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
    ),
    Images: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
    Search: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    ),
    GraduationCap: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
      </svg>
    ),
    Calendar: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
    Users: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    ),
    Trophy: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
      </svg>
    ),
    Lightbulb: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
    Beaker: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547A1.99 1.99 0 004 17.5V18a2 2 0 002 2h12a2 2 0 002-2v-.5a1.99 1.99 0 00-.572-1.072zM14 11V6a2 2 0 00-2-2H8a2 2 0 00-2 2v5M4 15h16a1 1 0 000-2H4a1 1 0 000 2z" />
      </svg>
    ),
    Presentation: ({ className }) => (
      <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m0 0V3a1 1 0 011 1v10a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1V4z M8 7h8 M8 11h8 M8 15h8" />
      </svg>
    )
  }

  const IconComponent = icons[iconName]
  return IconComponent ? <IconComponent className="h-4 w-4" /> : <div className="h-4 w-4" />
}

interface SidebarProps {
  isOpen?: boolean
  isCollapsed?: boolean
  onToggleCollapse?: () => void
  className?: string
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen = true,
  isCollapsed = false,
  onToggleCollapse,
  className
}) => {
  const [expandedItems, setExpandedItems] = React.useState<string[]>(['fisicc'])

  // Actualizar badges cuando se monta el componente
  React.useEffect(() => {
    updateNavigationBadges()
  }, [])

  const toggleExpanded = (itemId: string) => {
    if (isCollapsed) return
    
    setExpandedItems(prev =>
      prev.includes(itemId)
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    )
  }

  const getBadgeVariant = (item: NavigationItem) => {
    if (item.badgeVariant) return item.badgeVariant
    if (item.badge === 'LIVE') return 'live'
    if (typeof item.badge === 'number') return 'secondary'
    return 'default'
  }

  const NavItemComponent: React.FC<{ 
    item: NavigationItem
    level?: number
  }> = ({ item, level = 0 }) => {
    const hasChildren = item.children && item.children.length > 0
    const isItemExpanded = expandedItems.includes(item.id)

    return (
      <div>
        <button
          onClick={() => hasChildren ? toggleExpanded(item.id) : undefined}
          className={cn(
            'w-full flex items-center gap-3 px-3 py-2.5 text-left rounded-lg transition-all duration-200',
            'hover:bg-zinc-100 dark:hover:bg-zinc-800',
            item.isActive && 'bg-primary-50 text-primary-700 dark:bg-primary-950 dark:text-primary-300',
            level > 0 && 'ml-4 text-sm',
            isCollapsed && 'justify-center px-2'
          )}
        >
          <div className="flex-shrink-0">
            {getIcon(item.icon)}
          </div>
          
          {!isCollapsed && (
            <>
              <span className="flex-1 font-medium">
                {item.label}
              </span>
              
              {item.badge && (
                <Badge 
                  variant={getBadgeVariant(item)}
                  size="sm"
                >
                  {item.badge}
                </Badge>
              )}
              
              {hasChildren && (
                <motion.div
                  animate={{ rotate: isItemExpanded ? 90 : 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <ChevronRight className="h-4 w-4 text-zinc-400" />
                </motion.div>
              )}
            </>
          )}
        </button>

        {/* Children */}
        {hasChildren && !isCollapsed && (
          <AnimatePresence>
            {isItemExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="ml-4 space-y-1 border-l border-zinc-200 dark:border-zinc-700 pl-4 py-2">
                  {item.children?.map(child => (
                    <NavItemComponent
                      key={child.id}
                      item={child}
                      level={level + 1}
                    />
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        )}
      </div>
    )
  }

  return (
    <AnimatePresence mode="wait">
      {isOpen && (
        <motion.aside
          initial={{ x: -280, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -280, opacity: 0 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className={cn(
            'fixed left-0 top-14 h-[calc(100vh-3.5rem)] bg-white dark:bg-zinc-950 border-r border-zinc-200 dark:border-zinc-800 z-30',
            'lg:relative lg:top-0 lg:h-full lg:z-0',
            isCollapsed ? 'w-16' : 'w-64',
            className
          )}
        >
          <div className="flex flex-col h-full">
            {/* Collapse Toggle */}
            <div className="hidden lg:flex items-center justify-end p-4 border-b border-zinc-200 dark:border-zinc-800">
              <button
                onClick={onToggleCollapse}
                className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
              >
                <motion.div
                  animate={{ rotate: isCollapsed ? 180 : 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <ChevronRight className="h-4 w-4 text-zinc-500" />
                </motion.div>
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
              {/* Navegación Principal */}
              <div className="space-y-1">
                {!isCollapsed && (
                  <h3 className="px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Navegación
                  </h3>
                )}
                {primaryNavigation.map(item => (
                  <NavItemComponent key={item.id} item={item} />
                ))}
              </div>

              {/* Facultades */}
              <div className="space-y-1">
                {!isCollapsed && (
                  <h3 className="px-3 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Facultades
                  </h3>
                )}
                {facultyNavigation.map(item => (
                  <NavItemComponent key={item.id} item={item} />
                ))}
              </div>
            </div>

            {/* Footer */}
            {!isCollapsed && (
              <div className="p-4 border-t border-zinc-200 dark:border-zinc-800">
                <div className="text-xs text-zinc-500 dark:text-zinc-400">
                  <p className="font-medium">Universidad Galileo</p>
                  <p>MediaLab © 2024</p>
                </div>
              </div>
            )}
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  )
}