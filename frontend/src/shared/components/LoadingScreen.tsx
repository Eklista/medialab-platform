// src/shared/components/LoadingScreen.tsx
import React from 'react';

export const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="text-center space-y-4">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 text-slate-800 mb-8">
          <div className="w-12 h-12 bg-zinc-950 rounded-lg flex items-center justify-center">
            <img
              src="/logo-white.png"
              alt="MediaLab Logo"
              className="w-7 h-7 object-contain"
            />
          </div>
          <span className="text-2xl font-bold">MediaLab</span>
        </div>

        {/* Spinner */}
        <div className="relative">
          <div className="w-16 h-16 border-4 border-slate-200 border-t-zinc-800 rounded-full animate-spin mx-auto" />
        </div>

        {/* Texto */}
        <div className="space-y-2">
          <p className="text-slate-800 text-lg font-medium">
            Cargando MediaLab
          </p>
          <p className="text-slate-500 text-sm">
            Universidad Galileo
          </p>
        </div>

        {/* Dots loading animation */}
        <div className="flex justify-center gap-1">
          <div className="w-2 h-2 bg-zinc-800 rounded-full animate-pulse" style={{animationDelay: '0ms'}} />
          <div className="w-2 h-2 bg-zinc-800 rounded-full animate-pulse" style={{animationDelay: '150ms'}} />
          <div className="w-2 h-2 bg-zinc-800 rounded-full animate-pulse" style={{animationDelay: '300ms'}} />
        </div>
      </div>
    </div>
  );
};