/**
 * Shared API - HTTP client and backend communication
 * Centralizes: axios config, interceptors, endpoints, error handling
 */

export { apiClient } from './apiClient';
export { ENDPOINTS } from './endpoints';
export * from './types';
export * from './interceptors';