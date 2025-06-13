// modules/auth/hooks/useRecovery.ts
import { useState, useCallback } from 'react';
import { apiClient } from '../../../shared/api/apiClient';

interface RecoveryRequest {
  email: string;
}

interface RecoveryResponse {
  success: boolean;
  message: string;
}

interface UseRecoveryOptions {
  onSuccess?: (response: RecoveryResponse) => void;
  onError?: (error: string) => void;
}

export const useRecovery = (options: UseRecoveryOptions = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const requestRecovery = useCallback(async (email: string) => {
    setIsLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const request: RecoveryRequest = { email };
      const response = await apiClient.post<RecoveryResponse>('/api/v1/auth/recovery', request);

      if (response.data.success) {
        setSuccess(true);
        options.onSuccess?.(response.data);
        return { success: true, response: response.data };
      } else {
        setError(response.data.message);
        options.onError?.(response.data.message);
        return { success: false, error: response.data.message };
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail?.message || 'Error al enviar correo de recuperación';
      setError(errorMessage);
      options.onError?.(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, [options]);

  const resetRecovery = useCallback(() => {
    setSuccess(false);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    requestRecovery,
    isLoading,
    error,
    success,
    resetRecovery,
    clearError,
  };
};