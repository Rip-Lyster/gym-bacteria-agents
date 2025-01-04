/**
 * API service for handling backend communication
 * Contains all API endpoints and their respective TypeScript interfaces
 */

// Response type for health check endpoint
interface HealthCheckResponse {
  status: string;
}

/**
 * Fetches the API health status
 * @returns Promise containing the health check response
 * @throws Error if the request fails
 */
export async function getHealthStatus(): Promise<HealthCheckResponse> {
  const response = await fetch('/api/health');
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
} 