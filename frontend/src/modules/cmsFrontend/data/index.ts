// src/modules/cmsFrontend/data/index.ts

// Types - Export all interfaces
export * from './types'

// Mock Data - Export main data arrays
export { 
  mockFaculties,
  fisiccCategories,
  fingCategories, 
  facmedCategories 
} from './mockFaculties'

export { 
  mockContent,
  graduationPhotos,
  conferencePhotos 
} from './mockContent'

export { 
  mockLiveStream,
  mockChatConfig,
  scheduledStreams,
  recentEndedStreams 
} from './mockLiveStream'

export { 
  primaryNavigation,
  facultyNavigation,
  footerNavigation,
  socialNavigation,
  mockGlobalStats 
} from './mockNavigation'

// Helper Functions - Export commonly used functions
export {
  // Faculty helpers
  getFacultyById,
  getFacultyBySlug,
  getCategoriesByFaculty,
  getCategoryById,
  getAllCategories,
  getFacultyStats
} from './mockFaculties'

export {
  // Content helpers
  getContentById,
  getContentBySlug,
  getContentByFaculty,
  getContentByCategory,
  getContentByType,
  getFeaturedContent,
  getRecentContent,
  getPopularContent,
  searchContent,
  getContentStats
} from './mockContent'

export {
  // Live stream helpers
  getCurrentLiveStream,
  getScheduledStreams,
  getUpcomingStream,
  getStreamsByFaculty,
  getRecentStreams,
  getLiveStreamStats,
  updateViewerCount,
  simulateViewerCountChanges
} from './mockLiveStream'

export {
  // Navigation helpers
  getNavigationByRole,
  getFacultyNavigation,
  getNavigationItem,
  updateNavigationBadges,
  setActiveNavigation,
  getBreadcrumbs,
  searchNavigation
} from './mockNavigation'