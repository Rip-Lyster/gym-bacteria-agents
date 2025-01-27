import { apiConfig } from '../lib/config';

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
}

export class ApiError extends Error {
  constructor(message: string, public status?: number, public details?: any) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * API service for handling backend communication
 * Contains all API endpoints and their respective TypeScript interfaces
 */

// Response type for health check endpoint
interface HealthCheckResponse {
  status: string;
  timestamp?: string;
  version?: string;
}

/**
 * Base API call function with error handling
 * @param endpoint - API endpoint path
 * @param options - Fetch options
 * @returns Promise with the response data
 */
export async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${apiConfig.api.baseUrl}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new ApiError(
        data.message || 'An error occurred',
        response.status,
        data.details
      );
    }

    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    console.error('API call failed:', error);
    throw new ApiError('Network error or invalid JSON response');
  }
}

/**
 * Helper function for making GET requests
 */
export function get<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  return apiCall<T>(endpoint, { ...options, method: 'GET' });
}

/**
 * Helper function for making POST requests
 */
export function post<T>(endpoint: string, data: any, options: RequestInit = {}): Promise<T> {
  return apiCall<T>(endpoint, {
    ...options,
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Helper function for making PUT requests
 */
export function put<T>(endpoint: string, data: any, options: RequestInit = {}): Promise<T> {
  return apiCall<T>(endpoint, {
    ...options,
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Helper function for making DELETE requests
 */
export function del<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  return apiCall<T>(endpoint, { ...options, method: 'DELETE' });
}

/**
 * Fetches the API health status
 * @returns Promise containing the health check response
 * @throws Error if the request fails
 */
export async function getHealthStatus(): Promise<HealthCheckResponse> {
  return apiCall<HealthCheckResponse>('/api/health');
} 