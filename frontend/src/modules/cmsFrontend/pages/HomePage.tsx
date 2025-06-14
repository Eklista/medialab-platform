// src/modules/cmsFrontend/pages/HomePage.tsx
import React from 'react'
import { ContentLayout } from '../components/layout/Layout'
import { 
  HeroSection, 
  FacultiesGrid, 
  FeaturedContent, 
  StatsSection,
  LiveStreamCard 
} from '../components/sections'
import { Card, CardContent } from '../components/ui/Card'
import { getCurrentLiveStream } from '../data/mockLiveStream'
import type { Faculty, ContentItem, LiveStream } from '../data/types'

export const HomePage: React.FC = () => {
  const [showChat, setShowChat] = React.useState(false)
  const [isFirstVisit] = React.useState(() => {
    // Check if it's user's first visit
    return !localStorage.getItem('cms-visited')
  })
  
  const currentLive = getCurrentLiveStream()

  React.useEffect(() => {
    // Mark as visited
    localStorage.setItem('cms-visited', 'true')
  }, [])

  const handleFacultyClick = (faculty: Faculty) => {
    console.log('Navigate to faculty:', faculty.slug)
    // TODO: Implement navigation
  }

  const handleContentClick = (content: ContentItem) => {
    console.log('Navigate to content:', content.slug, content.type)
    // TODO: Implement navigation
  }

  const handleLiveStreamClick = (stream: LiveStream) => {
    console.log('Watch live stream:', stream.id)
    // TODO: Implement live stream modal or navigation
  }

  const handleChatToggle = () => {
    setShowChat(!showChat)
  }

  // Intelligent layout based on context
  const shouldShowFullHero = isFirstVisit && !currentLive
  const shouldShowLiveFirst = currentLive && !isFirstVisit

  return (
    <ContentLayout>
      <div className="space-y-16">
        
        {/* Live Stream Priority Section - Show first if there's active stream and not first visit */}
        {shouldShowLiveFirst && (
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <LiveStreamCard
                variant="hero"
                onWatchClick={handleLiveStreamClick}
                onChatToggle={handleChatToggle}
                showChat={showChat}
              />
            </div>

            <div className="lg:col-span-1">
              {showChat ? (
                <Card className="h-full">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-zinc-900 dark:text-zinc-100">
                        Chat en Vivo
                      </h3>
                      <button
                        onClick={handleChatToggle}
                        className="text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-300 transition-colors"
                      >
                        ✕
                      </button>
                    </div>
                    
                    <div className="h-96 bg-zinc-50 dark:bg-zinc-800 rounded-lg flex items-center justify-center">
                      <div className="text-center text-zinc-500 dark:text-zinc-400">
                        <div className="text-2xl mb-2">💬</div>
                        <p className="text-sm font-medium">Chat Component</p>
                        <p className="text-xs">Por implementar</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card className="h-full">
                  <CardContent className="p-6">
                    <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 mb-4">
                      Acerca del Evento
                    </h3>
                    <div className="space-y-4 text-sm text-zinc-600 dark:text-zinc-400">
                      <p className="line-clamp-3">{currentLive.description}</p>
                      
                      <div className="border-t border-zinc-200 dark:border-zinc-700 pt-4">
                        <h4 className="font-medium text-zinc-900 dark:text-zinc-100 mb-2">
                          Detalles del Evento
                        </h4>
                        <ul className="space-y-2">
                          <li>📅 Iniciado: {new Date(currentLive.actualStart || currentLive.scheduledStart!).toLocaleString('es-ES')}</li>
                          <li>🏫 Facultad: {currentLive.facultyId?.toUpperCase()}</li>
                          <li>🎥 Grabación: {currentLive.recording.enabled ? 'Sí' : 'No'}</li>
                          <li>💬 Chat: {currentLive.chat.enabled ? 'Activo' : 'Deshabilitado'}</li>
                        </ul>
                      </div>

                      <div className="pt-4 border-t border-zinc-200 dark:border-zinc-700">
                        <button
                          onClick={handleChatToggle}
                          className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
                        >
                          Abrir Chat
                        </button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </section>
        )}

        {/* Hero Section - Full hero for first visits, compact if live stream active */}
        {shouldShowFullHero ? (
          <HeroSection />
        ) : !shouldShowLiveFirst && currentLive ? (
          <section>
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
                Transmisión en Vivo
              </h2>
            </div>
            <LiveStreamCard
              variant="featured"
              onWatchClick={handleLiveStreamClick}
              onChatToggle={handleChatToggle}
              showChat={showChat}
            />
          </section>
        ) : null}
        
        {/* Faculties Grid */}
        <FacultiesGrid onFacultyClick={handleFacultyClick} />
        
        {/* Featured Content */}
        <FeaturedContent onContentClick={handleContentClick} />
        
        {/* Stats Section */}
        <StatsSection />
      </div>
    </ContentLayout>
  )
}