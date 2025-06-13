// shared/api/endpoints.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

export const ENDPOINTS = {
  // Base
  BASE_URL: API_BASE_URL,
  API_VERSION: API_VERSION,
  
  // Auth endpoints
  AUTH: {
    LOGIN: `${API_VERSION}/auth/login`,
    VERIFY_2FA: `${API_VERSION}/auth/verify-2fa`,
    LOGOUT: `${API_VERSION}/auth/logout`,
    LOGOUT_ALL: `${API_VERSION}/auth/logout-all`,
    VALIDATE_SESSION: (sessionId: string) => `${API_VERSION}/auth/session/${sessionId}/validate`,
    ACTIVE_SESSIONS: `${API_VERSION}/auth/sessions/active`,
    SECURITY_STATS: `${API_VERSION}/auth/security/stats`,
    LOGIN_HISTORY: (userId: number) => `${API_VERSION}/auth/user/${userId}/login-history`,
  },

  // Users endpoints (para futuro)
  USERS: {
    PROFILE: `${API_VERSION}/users/profile`,
    LIST: `${API_VERSION}/users`,
    DETAIL: (id: number) => `${API_VERSION}/users/${id}`,
  },

  // Health
  HEALTH: '/health',
} as const;