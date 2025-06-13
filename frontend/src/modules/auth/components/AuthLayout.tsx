// modules/auth/components/AuthLayout.tsx
import React from 'react';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  showLogo?: boolean;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title,
  subtitle,
  showLogo = true
}) => {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Panel izquierdo - Imagen y contenido */}
      <div className="hidden lg:flex lg:w-1/2">
        <div className="w-full relative overflow-hidden rounded-r-3xl">
          {/* Imagen de fondo */}
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style={{
              backgroundImage: 'url(/background.webp)'
            }}
          />
          
          {/* Overlay oscuro para legibilidad */}
          <div className="absolute inset-0 bg-black/40" />
          
          {/* Contenido sobre la imagen */}
          <div className="relative z-10 p-12 flex flex-col justify-between h-full text-white">
            <div>
              {showLogo && (
                <div className="flex items-center gap-3">
                  <img
                    src="/logo-white.png"
                    alt="MediaLab Logo"
                    className="w-10 h-10 object-contain"
                  />
                  <span className="text-xl font-bold">MediaLab</span>
                </div>
              )}
            </div>
            
            <div className="flex-1 flex items-end pb-16">
              <div className="max-w-lg">
                <h1 className="text-5xl font-bold mb-6 leading-tight">
                  MediaLab
                </h1>
                <p className="text-lg opacity-90 leading-relaxed">
                  Plataforma integral para la gestión de proyectos creativos y comunicación multimedia.
                </p>
              </div>
            </div>
            
            <div className="text-white/60 text-sm">
              © 2025 MediaLab. Todos los derechos reservados.
            </div>
          </div>
        </div>
      </div>

      {/* Panel derecho - Formulario */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          {/* Logo móvil */}
          <div className="lg:hidden flex items-center justify-center gap-3 text-gray-900 mb-8">
            <img
              src="/logo.png"
              alt="MediaLab Logo"
              className="w-10 h-10 object-contain"
            />
            <span className="text-xl font-bold">MediaLab</span>
          </div>
          
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {title}
            </h2>
            {subtitle && (
              <p className="text-gray-600">
                {subtitle}
              </p>
            )}
          </div>
          
          {children}
        </div>
      </div>
    </div>
  );
};