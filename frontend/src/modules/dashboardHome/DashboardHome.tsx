// src/modules/dashboardHome/DashboardHome.tsx
import React from 'react';
import type { AuthUser } from '../../shared/types/auth.types';

interface DashboardHomeProps {
  user: AuthUser | null;
  onLogout: () => void;
}

export const DashboardHome: React.FC<DashboardHomeProps> = ({ user, onLogout }) => {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-zinc-950 rounded-lg flex items-center justify-center">
                <img
                  src="/logo-white.png"
                  alt="MediaLab Logo"
                  className="w-5 h-5 object-contain"
                />
              </div>
              <span className="text-xl font-bold text-slate-800">MediaLab</span>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-sm text-slate-600">
                Hola, {user?.first_name || user?.email || 'Usuario'}
              </span>
              <button
                onClick={onLogout}
                className="px-4 py-2 text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-lg transition-colors border border-slate-200"
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
            <h1 className="text-4xl font-bold text-slate-800 mb-4">
              ¡Bienvenido a MediaLab!
            </h1>
            <p className="text-xl text-slate-500">
              Dashboard en construcción...
            </p>
          </div>

          {/* User Info Card */}
          <div className="max-w-md mx-auto bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">
              Información de Usuario
            </h2>
            <div className="space-y-2 text-left">
              <div>
                <span className="text-sm font-medium text-slate-500">ID:</span>
                <span className="ml-2 text-sm text-slate-700">{user?.id}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-slate-500">Tipo:</span>
                <span className="ml-2 text-sm text-slate-700">{user?.user_type}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-slate-500">Email:</span>
                <span className="ml-2 text-sm text-slate-700">{user?.email}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-slate-500">Estado:</span>
                <span className="ml-2 text-sm text-green-600 font-medium">Activo</span>
              </div>
            </div>
          </div>

          {/* Success Message */}
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm max-w-md mx-auto">
            🎉 ¡Autenticación exitosa! El sistema de 2FA está funcionando correctamente.
          </div>
        </div>
      </main>
    </div>
  );
};