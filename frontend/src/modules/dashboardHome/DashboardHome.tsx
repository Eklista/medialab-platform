// src/modules/dashboardHome/DashboardHome.tsx
import React from 'react';
import type { AuthUser } from '../../shared/types/auth.types';

interface DashboardHomeProps {
  user: AuthUser | null;
  onLogout: () => void;
}

export const DashboardHome: React.FC<DashboardHomeProps> = ({ user, onLogout }) => {
  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Header */}
      <header className="bg-zinc-900 border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-lime-400 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-zinc-950" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
              </div>
              <span className="text-xl font-bold text-zinc-50">MediaLab</span>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-sm text-zinc-300">
                Hola, {user?.first_name || user?.email || 'Usuario'}
              </span>
              <button
                onClick={onLogout}
                className="px-4 py-2 text-sm bg-zinc-800 text-zinc-300 hover:bg-zinc-700 rounded-lg transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-8">
          <div>
            <h1 className="text-4xl font-bold text-zinc-50 mb-4">
              ¡Bienvenido a MediaLab!
            </h1>
            <p className="text-xl text-zinc-400">
              Dashboard en construcción...
            </p>
          </div>

          {/* User Info Card */}
          <div className="max-w-md mx-auto bg-zinc-900 border border-zinc-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-zinc-50 mb-4">
              Información de Usuario
            </h2>
            <div className="space-y-2 text-left">
              <div>
                <span className="text-sm font-medium text-zinc-400">ID:</span>
                <span className="ml-2 text-sm text-zinc-300">{user?.id}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-zinc-400">Tipo:</span>
                <span className="ml-2 text-sm text-zinc-300">{user?.user_type}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-zinc-400">Email:</span>
                <span className="ml-2 text-sm text-zinc-300">{user?.email}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-zinc-400">Estado:</span>
                <span className="ml-2 text-sm text-lime-400">Activo</span>
              </div>
            </div>
          </div>

          {/* Success Message */}
          <div className="p-4 bg-lime-950/50 border border-lime-900 rounded-lg text-lime-400 text-sm max-w-md mx-auto">
            🎉 ¡Autenticación exitosa! El sistema de 2FA está funcionando correctamente.
          </div>
        </div>
      </main>
    </div>
  );
};

