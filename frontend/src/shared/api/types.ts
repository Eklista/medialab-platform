// shared/api/types.ts
export interface ApiResponse<T = any> {
  data: T;
  status: number;
  message?: string;
}

export interface ApiError {
  error: string;
  message: string;
  path?: string;
  detail?: any;
}

export interface RequestConfig {
  skipAuth?: boolean;
  timeout?: number;
}