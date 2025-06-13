// shared/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
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

interface AuthContextType extends AuthState {
  login: (credentials: LoginRequest) => Promise<{ success: boolean; requires_2fa?: boolean; error?: string; expires_in?: number }>;
  verify2FA: (code: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  clearError: () => void;
  isInternalUser: boolean;
  isInstitutionalUser: boolean;
  canAccessDashboard: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>(initialState);

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      console.log('AuthContext - Initializing auth...');
      const { sessionId, user } = authService.getAuthData();
      
      if (sessionId && user) {
        const isValid = await authService.validateSession(sessionId);
        if (isValid) {
          console.log('AuthContext - Valid session found, setting authenticated');
          setState(prev => ({
            ...prev,
            user,
            session_id: sessionId,
            is_authenticated: true,
            is_loading: false,
          }));
          return;
        } else {
          authService.clearAuthData();
        }
      }
      
      console.log('AuthContext - No valid session, setting not authenticated');
      setState(prev => ({ ...prev, is_loading: false }));
    };

    initAuth();
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    console.log('AuthContext - Starting login...');
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
          
          console.log('AuthContext - Login successful, setting authenticated state');
          
          setState({
            user,
            session_id: response.session_id!,
            is_authenticated: true,
            requires_2fa: false,
            temp_session_id: null,
            is_loading: false,
            error: null,
          });
          
          console.log('AuthContext - State updated to authenticated');

          return { success: true, requires_2fa: false };
        }
      } else {
        // Error en login
        setState(prev => ({
          ...prev,
          error: response.message,
          is_loading: false,
        }));

        return { success: false, error: response.message };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail?.message || 'Error de conexión';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        is_loading: false,
      }));

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

        setState({
          user,
          session_id: response.session_id!,
          temp_session_id: null,
          requires_2fa: false,
          is_authenticated: true,
          is_loading: false,
          error: null,
        });

        return { success: true };
      } else {
        setState(prev => ({
          ...prev,
          error: response.message,
          is_loading: false,
        }));

        return { success: false, error: response.message };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Código inválido';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        is_loading: false,
      }));

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
  }, [state.session_id]);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  console.log('AuthContext - Current state:', {
    isAuthenticated: state.is_authenticated,
    isLoading: state.is_loading,
    hasUser: !!state.user
  });

  const contextValue: AuthContextType = {
    ...state,
    login,
    verify2FA,
    logout,
    clearError,
    isInternalUser: state.user?.user_type === 'internal_user',
    isInstitutionalUser: state.user?.user_type === 'institutional_user',
    canAccessDashboard: state.user?.can_access_dashboard || false,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};