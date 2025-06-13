// modules/auth/components/TwoFactorForm.tsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../shared/hooks/useAuth';

export const TwoFactorForm: React.FC = () => {
  const { verify2FA, isLoading, error, clearError } = useAuth();
  const [code, setCode] = useState('');
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutos

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          // Redirigir al login
          window.location.href = '/login';
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (code.length !== 6) {
      return;
    }

    clearError();
    const result = await verify2FA(code);
    
    if (result.success) {
      window.location.href = '/dashboard';
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Autenticación de Dos Factores
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ingresa el código de 6 dígitos de tu aplicación autenticadora
          </p>
          <p className="mt-1 text-center text-sm text-orange-600">
            Tiempo restante: {formatTime(timeLeft)}
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="code" className="block text-sm font-medium text-gray-700">
              Código de verificación
            </label>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              className="mt-1 block w-full px-3 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-center text-2xl font-mono"
              placeholder="123456"
              maxLength={6}
              autoFocus
            />
          </div>

          <button
            type="submit"
            disabled={isLoading || code.length !== 6 || timeLeft <= 0}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Verificando...' : 'Verificar Código'}
          </button>

          <div className="text-center">
            <button
              type="button"
              onClick={() => window.location.href = '/login'}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Volver al login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
