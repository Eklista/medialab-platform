// modules/auth/hooks/useLogin.ts
import { useState, useCallback } from 'react';
import { authService } from '../../../shared/services/authService';
import type { LoginRequest, LoginResponse } from '../../../shared/types/auth.types';

interface UseLoginOptions {
  onSuccess?: (response: LoginResponse) => void;
  onError?: (error: string) => void;
  onRequires2FA?: (tempSessionId: string, expiresIn: number) => void;
}

export const useLogin = (options: UseLoginOptions = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (credentials: LoginRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await authService.login(credentials);

      if (response.success) {
        if (response.requires_2fa) {
          options.onRequires2FA?.(
            response.temp_session_id!,
            response.expires_in || 600
          );
        } else {
          options.onSuccess?.(response);
        }
        return { success: true, response };
      } else {
        setError(response.message);
        options.onError?.(response.message);
        return { success: false, error: response.message };
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail?.message || 'Error de conexión';
      setError(errorMessage);
      options.onError?.(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, [options]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    login,
    isLoading,
    error,
    clearError,
  };
};