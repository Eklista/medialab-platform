// src/modules/auth/components/TwoFactorCard.tsx
import React, { useState, useEffect } from 'react';
import { CodeInput } from '../ui/inputs/CodeInput';
import { LoginButton } from '../ui/buttons/LoginButton';

interface TwoFactorCardProps {
  onSubmit: (code: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
  expiresIn?: number; // segundos
}

export const TwoFactorCard: React.FC<TwoFactorCardProps> = ({
  onSubmit,
  isLoading = false,
  error,
  expiresIn = 600
}) => {
  const [code, setCode] = useState('');
  const [timeLeft, setTimeLeft] = useState(expiresIn);

  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          // Redirigir al login cuando expire
          window.location.reload();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

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
        <div className={`text-sm font-medium ${timeLeft < 60 ? 'text-red-400' : 'text-orange-400'}`}>
          Tiempo restante: {formatTime(timeLeft)}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-lg bg-red-950/50 border border-red-900 text-red-400 text-sm">
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
        <p className="text-sm text-zinc-400">
          Ingresa el código de 6 dígitos de tu aplicación autenticadora
        </p>
        
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="text-sm text-lime-400 hover:text-lime-300 transition-colors"
        >
          Volver al inicio de sesión
        </button>
      </div>

      {/* Backup codes help */}
      <div className="text-center">
        <button
          type="button"
          className="text-xs text-zinc-500 hover:text-zinc-400 transition-colors"
        >
          ¿No tienes acceso a tu dispositivo? Usa un código de respaldo
        </button>
      </div>
    </div>
  );
};
