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
    <div className="min-h-screen bg-zinc-950 flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-lime-400 to-lime-500 p-12 flex-col justify-between">
        <div>
          {showLogo && (
            <div className="flex items-center gap-3 text-zinc-950">
              <div className="w-10 h-10 bg-zinc-950 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-lime-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
              </div>
              <span className="text-xl font-bold">MediaLab</span>
            </div>
          )}
        </div>
        
        <div className="text-zinc-950">
          <h1 className="text-4xl font-bold mb-4">
            Universidad Galileo
          </h1>
          <p className="text-xl opacity-80 leading-relaxed">
            Plataforma integral para la gestión de proyectos creativos y comunicación institucional.
          </p>
        </div>

        <div className="text-zinc-950/60 text-sm">
          © 2025 Universidad Galileo. Todos los derechos reservados.
        </div>
      </div>

      {/* Right side - Auth Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            {/* Mobile logo */}
            <div className="lg:hidden flex items-center justify-center gap-3 text-zinc-50 mb-8">
              <div className="w-10 h-10 bg-lime-400 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-zinc-950" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
              </div>
              <span className="text-xl font-bold">MediaLab</span>
            </div>

            <h2 className="text-3xl font-bold text-zinc-50">
              {title}
            </h2>
            {subtitle && (
              <p className="mt-2 text-zinc-400">
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
