import { config } from '../lib/config';

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
  const url = `${config.api.baseUrl}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}

/**
 * Fetches the API health status
 * @returns Promise containing the health check response
 * @throws Error if the request fails
 */
export async function getHealthStatus(): Promise<HealthCheckResponse> {
  return apiCall<HealthCheckResponse>('/api/health');
} 