// shared/api/interceptors.ts
import type { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

export const requestInterceptor = (config: AxiosRequestConfig) => {
  // Add request ID for debugging
  config.headers = {
    ...config.headers,
    'X-Request-ID': crypto.randomUUID(),
  };

  return config;
};

export const responseInterceptor = (response: AxiosResponse) => {
  // Log successful responses in development
  if (import.meta.env.DEV) {
    console.log(`[API Success] ${response.config.method?.toUpperCase()} ${response.config.url}`, {
      status: response.status,
      data: response.data,
    });
  }

  return response;
};

export const errorInterceptor = (error: AxiosError) => {
  // Log errors in development
  if (import.meta.env.DEV) {
    console.error(`[API Error] ${error.config?.method?.toUpperCase()} ${error.config?.url}`, {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    });
  }

  return Promise.reject(error);
};