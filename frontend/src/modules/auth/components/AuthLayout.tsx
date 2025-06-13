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
    <div className="min-h-screen bg-slate-50 flex">
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
          
          {/* Overlay sutil para profundidad */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-transparent to-black/30" />
          
          {/* Contenido sobre la imagen */}
          <div className="relative z-10 p-12 flex flex-col justify-between h-full text-white">
            <div>
              {showLogo && (
                <div className="flex items-center gap-3 mb-8">
                  <img
                    src="/logo-white.png"
                    alt="MediaLab Logo"
                    className="w-10 h-10 object-contain"
                  />
                  <span className="text-xl font-semibold">MediaLab</span>
                </div>
              )}
            </div>
            
            <div className="flex-1 flex items-end pb-16">
              <div className="max-w-lg">
                <p className="text-lg text-white/80 leading-relaxed font-light">
                  Plataforma integral para la gestión de proyectos creativos y comunicación multimedia
                </p>
              </div>
            </div>
            
            <div className="text-white/50 text-sm font-light">
              © 2025 MediaLab. Todos los derechos reservados.
            </div>
          </div>
        </div>
      </div>

      {/* Panel derecho - Formulario */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white">
        <div className="w-full max-w-md">
          {/* Logo móvil */}
          <div className="lg:hidden flex items-center justify-center gap-3 text-slate-800 mb-12">
            <img
              src="/logo.png"
              alt="MediaLab Logo"
              className="w-10 h-10 object-contain"
            />
            <span className="text-xl font-semibold">MediaLab</span>
          </div>
          
          {/* Header del formulario - solo título principal */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-slate-800 mb-3">
              {title}
            </h2>
            {subtitle && (
              <p className="text-slate-500 text-sm font-light">
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