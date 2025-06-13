// shared/types/auth.types.ts
export interface LoginRequest {
  identifier: string;
  password: string;
  remember_me?: boolean;
  device_name?: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  user_id?: number;
  user_type?: 'internal_user' | 'institutional_user';
  session_id?: string;
  expires_at?: string;
  requires_2fa?: boolean;
  temp_session_id?: string;
  expires_in?: number;
  response_time_ms?: number;
}

export interface TwoFactorRequest {
  temp_session_id: string;
  code: string;
}

export interface TwoFactorResponse {
  success: boolean;
  message: string;
  user_id?: number;
  user_type?: string;
  session_id?: string;
  expires_at?: string;
}

export interface AuthUser {
  id: number;
  user_type: 'internal_user' | 'institutional_user';
  first_name: string;
  last_name: string;
  email: string;
  username: string;
  is_active: boolean;
  can_access_dashboard?: boolean;  // internal_user
  is_faculty?: boolean;           // institutional_user
}

export interface AuthState {
  user: AuthUser | null;
  session_id: string | null;
  temp_session_id: string | null;
  requires_2fa: boolean;
  is_authenticated: boolean;
  is_loading: boolean;
  error: string | null;
}