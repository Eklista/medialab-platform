// src/modules/cmsFrontend/components/layout/Header.tsx
import React from 'react'
import { Search, Sun, Moon, Menu, X } from 'lucide-react'
import { motion } from 'framer-motion'
import { useTheme } from '../../context/ThemeContext'
import { Button } from '../ui/Button'
import { SearchInput } from '../ui/Input'
import { cn } from '../../utils/cn'

interface HeaderProps {
  onMenuToggle?: () => void
  isMenuOpen?: boolean
  showSearch?: boolean
  className?: string
}

export const Header: React.FC<HeaderProps> = ({
  onMenuToggle,
  isMenuOpen = false,
  showSearch = true,
  className
}) => {
  const { isDark, toggleTheme } = useTheme()
  const [searchQuery, setSearchQuery] = React.useState('')
  const [isSearchFocused, setIsSearchFocused] = React.useState(false)

  const handleSearch = (value: string) => {
    setSearchQuery(value)
    console.log('Searching for:', value)
  }

  return (
    <header className={cn(
      'sticky top-0 z-40 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:bg-zinc-950/95 dark:supports-[backdrop-filter]:bg-zinc-950/60',
      'border-zinc-200 dark:border-zinc-800',
      className
    )}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">
          {/* Logo y Menu Mobile */}
          <div className="flex items-center gap-4">
            {/* Menu Toggle (Mobile) */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden h-8 w-8"
              onClick={onMenuToggle}
            >
              <motion.div
                initial={false}
                animate={{ rotate: isMenuOpen ? 180 : 0 }}
                transition={{ duration: 0.2 }}
              >
                {isMenuOpen ? (
                  <X className="h-4 w-4" />
                ) : (
                  <Menu className="h-4 w-4" />
                )}
              </motion.div>
            </Button>

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary-600">
                <span className="text-xs font-bold text-white">ML</span>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
                  MediaLab
                </h1>
              </div>
            </div>
          </div>

          {/* Search Bar (Desktop) */}
          {showSearch && (
            <div className="hidden md:flex flex-1 max-w-sm mx-8">
              <SearchInput
                placeholder="Buscar contenido..."
                value={searchQuery}
                onSearch={handleSearch}
                className="w-full h-9"
              />
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-2">
            {/* Search Mobile */}
            {showSearch && (
              <Button
                variant="ghost"
                size="icon"
                className="md:hidden h-8 w-8"
              >
                <Search className="h-4 w-4" />
              </Button>
            )}

            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="relative h-8 w-8"
            >
              <Sun className={cn(
                "h-4 w-4 transition-all",
                isDark ? "rotate-90 scale-0" : "rotate-0 scale-100"
              )} />
              <Moon className={cn(
                "absolute h-4 w-4 transition-all",
                isDark ? "rotate-0 scale-100" : "-rotate-90 scale-0"
              )} />
              <span className="sr-only">Toggle theme</span>
            </Button>

            {/* Live Indicator */}
            <div className="hidden sm:flex items-center gap-2 px-2 py-1 bg-red-500/10 border border-red-500/20 rounded-full">
              <div className="h-1.5 w-1.5 bg-red-500 rounded-full animate-pulse" />
              <span className="text-xs font-medium text-red-600 dark:text-red-400">
                EN VIVO
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}