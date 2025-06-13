// src/shared/components/LoadingScreen.tsx
import React from 'react';

export const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
      <div className="text-center space-y-4">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 text-zinc-50 mb-8">
          <div className="w-12 h-12 bg-lime-400 rounded-lg flex items-center justify-center">
            <svg className="w-7 h-7 text-zinc-950" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <span className="text-2xl font-bold">MediaLab</span>
        </div>

        {/* Spinner */}
        <div className="relative">
          <div className="w-16 h-16 border-4 border-zinc-800 border-t-lime-400 rounded-full animate-spin mx-auto" />
        </div>

        {/* Texto */}
        <div className="space-y-2">
          <p className="text-zinc-50 text-lg font-medium">
            Cargando MediaLab
          </p>
          <p className="text-zinc-400 text-sm">
            Universidad Galileo
          </p>
        </div>

        {/* Dots loading animation */}
        <div className="flex justify-center gap-1">
          <div className="w-2 h-2 bg-lime-400 rounded-full animate-pulse" style={{animationDelay: '0ms'}} />
          <div className="w-2 h-2 bg-lime-400 rounded-full animate-pulse" style={{animationDelay: '150ms'}} />
          <div className="w-2 h-2 bg-lime-400 rounded-full animate-pulse" style={{animationDelay: '300ms'}} />
        </div>
      </div>
    </div>
  );
};