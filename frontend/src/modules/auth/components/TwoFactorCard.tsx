// src/modules/auth/components/TwoFactorCard.tsx
import React, { useState, useEffect } from 'react';
import { CodeInput } from '../ui/inputs/CodeInput';
import { LoginButton } from '../ui/buttons/LoginButton';
import { useAuthNavigation } from '../context/AuthNavigationContext';

interface TwoFactorCardProps {
  onSubmit: (code: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
  expiresIn?: number;
}

export const TwoFactorCard: React.FC<TwoFactorCardProps> = ({
  onSubmit,
  isLoading = false,
  error,
  expiresIn = 600
}) => {
  const [code, setCode] = useState('');
  const [timeLeft, setTimeLeft] = useState(expiresIn);
  const { navigateToLogin } = useAuthNavigation();

  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          navigateToLogin();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, navigateToLogin]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (code.length !== 6) {
      return;
    }

    await onSubmit(code);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      {/* Timer */}
      <div className="text-center">
        <div className={`text-sm font-medium ${timeLeft < 60 ? 'text-red-600' : 'text-amber-600'}`}>
          Tiempo restante: {formatTime(timeLeft)}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* 2FA Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <CodeInput
          value={code}
          onChange={setCode}
          error={error}
          length={6}
          autoFocus
        />

        <LoginButton
          type="submit"
          className="w-full"
          isLoading={isLoading}
          disabled={code.length !== 6 || timeLeft <= 0}
        >
          {isLoading ? 'Verificando...' : 'Verificar Código'}
        </LoginButton>
      </form>

      {/* Help text */}
      <div className="text-center space-y-2">
        <p className="text-sm text-slate-500">
          Ingresa el código de 6 dígitos de tu aplicación autenticadora
        </p>
        
        <button
          type="button"
          onClick={navigateToLogin}
          className="text-sm text-zinc-800 hover:text-zinc-600 transition-colors font-medium"
        >
          Volver al inicio de sesión
        </button>
      </div>

      {/* Backup codes help */}
      <div className="text-center">
        <button
          type="button"
          className="text-xs text-slate-400 hover:text-slate-500 transition-colors"
        >
          ¿No tienes acceso a tu dispositivo? Usa un código de respaldo
        </button>
      </div>
    </div>
  );
};