// shared/hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';
import type { AuthState, AuthUser, LoginRequest } from '../types/auth.types';

const initialState: AuthState = {
  user: null,
  session_id: null,
  temp_session_id: null,
  requires_2fa: false,
  is_authenticated: false,
  is_loading: true,
  error: null,
};

export const useAuth = () => {
  const [state, setState] = useState<AuthState>(initialState);
  const [renderVersion, setRenderVersion] = useState(0); // Forzar re-render

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      const { sessionId, user } = authService.getAuthData();
      
      if (sessionId && user) {
        const isValid = await authService.validateSession(sessionId);
        if (isValid) {
          setState(prev => ({
            ...prev,
            user,
            session_id: sessionId,
            is_authenticated: true,
            is_loading: false,
          }));
          setRenderVersion(v => v + 1);
          return;
        } else {
          authService.clearAuthData();
        }
      }
      
      setState(prev => ({ ...prev, is_loading: false }));
      setRenderVersion(v => v + 1);
    };

    initAuth();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    setState(prev => ({ ...prev, is_loading: true, error: null }));

    try {
      const response = await authService.login(credentials);

      if (response.success) {
        if (response.requires_2fa) {
          // Requiere 2FA
          authService.setTempSession(response.temp_session_id!);
          setState(prev => ({
            ...prev,
            temp_session_id: response.temp_session_id!,
            requires_2fa: true,
            is_loading: false,
          }));
          setRenderVersion(v => v + 1);

          return { success: true, requires_2fa: true, expires_in: response.expires_in };
        } else {
          // Login completo sin 2FA
          const user: AuthUser = {
            id: response.user_id!,
            user_type: response.user_type!,
            first_name: '', 
            last_name: '',
            email: credentials.identifier,
            username: credentials.identifier,
            is_active: true,
          };

          authService.setAuthData(response.session_id!, user);
          
          console.log('useAuth - Setting authenticated state with user:', user);
          
          // IMPORTANTE: Actualizar el estado inmediatamente
          setState({
            user,
            session_id: response.session_id!,
            is_authenticated: true,
            requires_2fa: false,
            temp_session_id: null,
            is_loading: false,
            error: null,
          });
          
          // Forzar re-render
          setRenderVersion(v => v + 1);
          
          console.log('useAuth - State updated, forcing re-render');

          return { success: true, requires_2fa: false };
        }
      } else {
        // Error en login
        setState(prev => ({
          ...prev,
          error: response.message,
          is_loading: false,
        }));
        setRenderVersion(v => v + 1);

        return { success: false, error: response.message };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail?.message || 'Error de conexión';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        is_loading: false,
      }));
      setRenderVersion(v => v + 1);

      return { success: false, error: errorMessage };
    }
  }, []);

  const verify2FA = useCallback(async (code: string) => {
    if (!state.temp_session_id) {
      return { success: false, error: 'No hay sesión temporal' };
    }

    setState(prev => ({ ...prev, is_loading: true, error: null }));

    try {
      const response = await authService.verify2FA({
        temp_session_id: state.temp_session_id,
        code,
      });

      if (response.success) {
        const user: AuthUser = {
          id: response.user_id!,
          user_type: response.user_type as any,
          first_name: '',
          last_name: '',
          email: '',
          username: '',
          is_active: true,
        };

        authService.setAuthData(response.session_id!, user);
        authService.clearTempSession();

        // IMPORTANTE: Actualizar el estado inmediatamente
        setState({
          user,
          session_id: response.session_id!,
          temp_session_id: null,
          requires_2fa: false,
          is_authenticated: true,
          is_loading: false,
          error: null,
        });
        
        setRenderVersion(v => v + 1);

        return { success: true };
      } else {
        setState(prev => ({
          ...prev,
          error: response.message,
          is_loading: false,
        }));
        setRenderVersion(v => v + 1);

        return { success: false, error: response.message };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Código inválido';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        is_loading: false,
      }));
      setRenderVersion(v => v + 1);

      return { success: false, error: errorMessage };
    }
  }, [state.temp_session_id]);

  const logout = useCallback(async () => {
    if (state.session_id) {
      try {
        await authService.logout(state.session_id);
      } catch (error) {
        console.error('Error during logout:', error);
      }
    }

    authService.clearAuthData();
    setState({
      ...initialState,
      is_loading: false,
    });
    setRenderVersion(v => v + 1);
  }, [state.session_id]);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
    setRenderVersion(v => v + 1);
  }, []);

  // Log para debug
  console.log('useAuth - Current state:', {
    isAuthenticated: state.is_authenticated,
    isLoading: state.is_loading,
    hasUser: !!state.user,
    renderVersion
  });

  return {
    // State
    user: state.user,
    isAuthenticated: state.is_authenticated,
    isLoading: state.is_loading,
    error: state.error,
    requires2FA: state.requires_2fa,
    
    // Actions
    login,
    verify2FA,
    logout,
    clearError,
    
    // Utils
    isInternalUser: state.user?.user_type === 'internal_user',
    isInstitutionalUser: state.user?.user_type === 'institutional_user',
    canAccessDashboard: state.user?.can_access_dashboard || false,
  };
};