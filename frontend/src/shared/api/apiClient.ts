// shared/api/apiClient.ts
import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { ENDPOINTS } from './endpoints';
import type { ApiError, RequestConfig } from './types';

class ApiClient {
  private instance: AxiosInstance;
  private isRefreshing = false;
  private refreshSubscribers: Array<(token: string) => void> = [];

  constructor() {
    this.instance = axios.create({
      baseURL: ENDPOINTS.BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.instance.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const sessionId = localStorage.getItem('session_id');
        if (sessionId && !config.headers['skip-auth']) {
          config.headers.Authorization = `Bearer ${sessionId}`;
        }

        // Add device info
        config.headers['X-Device-Info'] = this.getDeviceInfo();
        
        // Add timestamp for security
        config.headers['X-Request-Time'] = new Date().toISOString();

        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`, {
          headers: config.headers,
          data: config.data,
        });

        return config;
      },
      (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`[API] Response ${response.status}:`, response.data);
        return response;
      },
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        console.error('[API] Response error:', {
          status: error.response?.status,
          data: error.response?.data,
          url: originalRequest?.url,
        });

        // Handle 401 Unauthorized
        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            // If already refreshing, wait for it
            return new Promise((resolve) => {
              this.refreshSubscribers.push((sessionId: string) => {
                if (originalRequest.headers) {
                  originalRequest.headers.Authorization = `Bearer ${sessionId}`;
                }
                resolve(this.instance(originalRequest));
              });
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          try {
            // Try to refresh session or redirect to login
            const sessionId = localStorage.getItem('session_id');
            if (sessionId) {
              // Validate current session
              const isValid = await this.validateSession(sessionId);
              if (isValid) {
                this.processRefreshQueue(sessionId);
                return this.instance(originalRequest);
              }
            }

            // Session invalid, redirect to login
            this.handleAuthError();
            return Promise.reject(error);

          } catch (refreshError) {
            this.handleAuthError();
            return Promise.reject(refreshError);
          } finally {
            this.isRefreshing = false;
            this.refreshSubscribers = [];
          }
        }

        // Handle other errors
        return Promise.reject(this.normalizeError(error));
      }
    );
  }

  private async validateSession(sessionId: string): Promise<boolean> {
    try {
      const response = await this.instance.get(
        ENDPOINTS.AUTH.VALIDATE_SESSION(sessionId),
        { headers: { 'skip-auth': 'true' } }
      );
      return response.data.valid;
    } catch {
      return false;
    }
  }

  private processRefreshQueue(sessionId: string): void {
    this.refreshSubscribers.forEach(callback => callback(sessionId));
    this.refreshSubscribers = [];
  }

  private handleAuthError(): void {
    // Clear auth data
    localStorage.removeItem('session_id');
    localStorage.removeItem('user');
    localStorage.removeItem('temp_session_id');
    
    // Redirect to login if not already there
    if (!window.location.pathname.includes('/login')) {
      window.location.href = '/login';
    }
  }

  private normalizeError(error: AxiosError): ApiError {
    const response = error.response;
    
    if (response?.data) {
      // Backend error format
      const data = response.data as any;
      return {
        error: data.error || 'API Error',
        message: data.message || data.detail?.message || error.message,
        path: data.path,
        detail: data.detail,
      };
    }

    // Network or other error
    return {
      error: 'Network Error',
      message: error.message || 'Error de conexión',
    };
  }

  private getDeviceInfo(): string {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const platform = navigator.platform || 'Unknown';
    
    return JSON.stringify({
      type: isMobile ? 'mobile' : 'desktop',
      platform,
      userAgent: navigator.userAgent,
      language: navigator.language,
    });
  }

  // ===================================
  // PUBLIC METHODS
  // ===================================

  async get<T = any>(url: string, config?: RequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.get(url, this.mergeConfig(config));
  }

  async post<T = any>(url: string, data?: any, config?: RequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.post(url, data, this.mergeConfig(config));
  }

  async put<T = any>(url: string, data?: any, config?: RequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.put(url, data, this.mergeConfig(config));
  }

  async patch<T = any>(url: string, data?: any, config?: RequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.patch(url, data, this.mergeConfig(config));
  }

  async delete<T = any>(url: string, config?: RequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.delete(url, this.mergeConfig(config));
  }

  private mergeConfig(config?: RequestConfig): AxiosRequestConfig {
    const baseConfig: AxiosRequestConfig = {};
    
    if (config?.skipAuth) {
      baseConfig.headers = { 'skip-auth': 'true' };
    }
    
    if (config?.timeout) {
      baseConfig.timeout = config.timeout;
    }

    return baseConfig;
  }

  // ===================================
  // UTILITY METHODS
  // ===================================

  setAuthToken(sessionId: string): void {
    this.instance.defaults.headers.common['Authorization'] = `Bearer ${sessionId}`;
  }

  clearAuthToken(): void {
    delete this.instance.defaults.headers.common['Authorization'];
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.get(ENDPOINTS.HEALTH, { skipAuth: true });
      return response.status === 200;
    } catch {
      return false;
    }
  }

  // Get current base URL
  getBaseURL(): string {
    return ENDPOINTS.BASE_URL;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();