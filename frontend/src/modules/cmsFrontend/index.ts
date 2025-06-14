// src/modules/cmsFrontend/index.ts

/**
 * CMS Frontend Module - Public-facing content display and browsing
 * 
 * Features:
 * - Intelligent HomePage with adaptive layout
 * - Live streaming with chat integration
 * - Faculty-based content organization
 * - Dark/light mode with persistence
 * - Responsive design mobile-first
 * - Modern UI with Framer Motion animations
 */

// Main Router - Entry point
export { CMSRouter } from './CMSRouter'

// Pages
export { HomePage } from './pages/HomePage'

// Layout System
export { 
  Layout, 
  LandingLayout, 
  ContentLayout, 
  FullScreenLayout 
} from './components/layout/Layout'

// Context Providers
export { ThemeProvider, useTheme } from './context/ThemeContext'

// UI Components
export * from './components/ui'

// Section Components
export * from './components/sections'

// Data & Types
export * from './data'

// Utils
export { cn } from './utils/cn'
export { tokens } from './utils/tokens'