// shared/services/authService.ts
import { apiClient } from '../api/apiClient';
import type { 
  LoginRequest, 
  LoginResponse, 
  TwoFactorRequest, 
  TwoFactorResponse,
  AuthUser
} from '../types/auth.types';

class AuthService {
  private readonly API_BASE = '/api/v1/auth';

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(`${this.API_BASE}/login`, credentials);
    return response.data;
  }

  async verify2FA(data: TwoFactorRequest): Promise<TwoFactorResponse> {
    const response = await apiClient.post<TwoFactorResponse>(`${this.API_BASE}/verify-2fa`, data);
    return response.data;
  }

  async logout(sessionId: string): Promise<void> {
    await apiClient.post(`${this.API_BASE}/logout`, { session_id: sessionId });
  }

  async validateSession(sessionId: string): Promise<boolean> {
    try {
      const response = await apiClient.get(`${this.API_BASE}/session/${sessionId}/validate`);
      return response.data.valid;
    } catch {
      return false;
    }
  }

  // Storage helpers
  setAuthData(sessionId: string, user: AuthUser): void {
    localStorage.setItem('session_id', sessionId);
    localStorage.setItem('user', JSON.stringify(user));
  }

  getAuthData(): { sessionId: string | null; user: AuthUser | null } {
    const sessionId = localStorage.getItem('session_id');
    const userStr = localStorage.getItem('user');
    const user = userStr ? JSON.parse(userStr) : null;
    return { sessionId, user };
  }

  clearAuthData(): void {
    localStorage.removeItem('session_id');
    localStorage.removeItem('user');
    localStorage.removeItem('temp_session_id');
  }

  setTempSession(tempSessionId: string): void {
    localStorage.setItem('temp_session_id', tempSessionId);
  }

  getTempSession(): string | null {
    return localStorage.getItem('temp_session_id');
  }

  clearTempSession(): void {
    localStorage.removeItem('temp_session_id');
  }
}

export const authService = new AuthService();