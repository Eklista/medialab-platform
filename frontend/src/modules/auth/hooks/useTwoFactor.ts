// modules/auth/hooks/useTwoFactor.ts
import { useState, useCallback, useEffect } from 'react';
import { authService } from '../../../shared/services/authService';
import type { TwoFactorRequest, TwoFactorResponse } from '../../../shared/types/auth.types';

interface UseTwoFactorOptions {
  tempSessionId?: string;
  expiresIn?: number;
  onSuccess?: (response: TwoFactorResponse) => void;
  onError?: (error: string) => void;
  onExpired?: () => void;
}

export const useTwoFactor = (options: UseTwoFactorOptions = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(options.expiresIn || 600);

  useEffect(() => {
    if (timeLeft <= 0) {
      options.onExpired?.();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          options.onExpired?.();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, options]);

  const verify2FA = useCallback(async (code: string) => {
    if (!options.tempSessionId) {
      setError('No hay sesión temporal disponible');
      return { success: false, error: 'No hay sesión temporal disponible' };
    }

    if (code.length !== 6) {
      setError('El código debe tener 6 dígitos');
      return { success: false, error: 'El código debe tener 6 dígitos' };
    }

    setIsLoading(true);
    setError(null);

    try {
      const request: TwoFactorRequest = {
        temp_session_id: options.tempSessionId,
        code,
      };

      const response = await authService.verify2FA(request);

      if (response.success) {
        options.onSuccess?.(response);
        return { success: true, response };
      } else {
        setError(response.message);
        options.onError?.(response.message);
        return { success: false, error: response.message };
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Código inválido';
      setError(errorMessage);
      options.onError?.(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, [options.tempSessionId, options]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const formatTime = useCallback((seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }, []);

  return {
    verify2FA,
    isLoading,
    error,
    timeLeft,
    isExpired: timeLeft <= 0,
    formattedTime: formatTime(timeLeft),
    clearError,
  };
};