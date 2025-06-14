// src/modules/cmsFrontend/components/layout/Layout.tsx
import React from 'react'
import { useTheme } from '../../context/ThemeContext'
import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { MobileMenu } from './MobileMenu'
import { cn } from '../../utils/cn'

interface LayoutProps {
  children: React.ReactNode
  showSidebar?: boolean
  showHeader?: boolean
  sidebarCollapsed?: boolean
  className?: string
}

export const Layout: React.FC<LayoutProps> = ({
  children,
  showSidebar = true,
  showHeader = true,
  sidebarCollapsed: controlledCollapsed,
  className
}) => {
  useTheme()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = React.useState(false)

  // Use controlled or internal state for sidebar collapse
  const isCollapsed = controlledCollapsed !== undefined 
    ? controlledCollapsed 
    : isSidebarCollapsed

  const handleMenuToggle = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  const handleSidebarToggle = () => {
    if (controlledCollapsed === undefined) {
      setIsSidebarCollapsed(!isSidebarCollapsed)
    }
  }

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false)
  }

  return (
    <div className={cn(
      'min-h-screen bg-zinc-50 dark:bg-zinc-900 transition-colors duration-200',
      className
    )}>
      {/* Header */}
      {showHeader && (
        <Header
          onMenuToggle={handleMenuToggle}
          isMenuOpen={isMobileMenuOpen}
        />
      )}

      <div className="flex">
        {/* Desktop Sidebar */}
        {showSidebar && (
          <div className="hidden lg:block">
            <Sidebar
              isOpen={true}
              isCollapsed={isCollapsed}
              onToggleCollapse={handleSidebarToggle}
            />
          </div>
        )}

        {/* Main Content */}
        <main className={cn(
          'flex-1 min-h-[calc(100vh-4rem)]',
          showSidebar && !isCollapsed && 'lg:ml-0', // Sidebar handles its own width
          showSidebar && isCollapsed && 'lg:ml-0'
        )}>
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </div>
        </main>
      </div>

      {/* Mobile Menu */}
      {showSidebar && (
        <MobileMenu
          isOpen={isMobileMenuOpen}
          onClose={closeMobileMenu}
        />
      )}
    </div>
  )
}

// Specialized layouts for different page types
export const LandingLayout: React.FC<{ children: React.ReactNode }> = ({ 
  children 
}) => (
  <Layout showSidebar={false}>
    {children}
  </Layout>
)

export const ContentLayout: React.FC<{ 
  children: React.ReactNode
  sidebarCollapsed?: boolean 
}> = ({ 
  children, 
  sidebarCollapsed 
}) => (
  <Layout 
    showSidebar={true}
    sidebarCollapsed={sidebarCollapsed}
  >
    {children}
  </Layout>
)

export const FullScreenLayout: React.FC<{ children: React.ReactNode }> = ({ 
  children 
}) => (
  <Layout 
    showSidebar={false}
    showHeader={false}
    className="bg-black"
  >
    {children}
  </Layout>
)