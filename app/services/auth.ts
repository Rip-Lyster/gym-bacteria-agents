import { apiCall } from './api';

export interface User {
  id: number;
  nickname: string;
  access_key: string;
}

/**
 * Authenticates a user with their access key
 * @param accessKey - The user's access key
 * @returns Promise containing the user data
 */
export async function authenticateUser(accessKey: string): Promise<User> {
  return apiCall<User>(`/api/users/${accessKey}`);
}

/**
 * Creates a new user
 * @param nickname - The user's display name
 * @param accessKey - The user's access key
 * @returns Promise containing the created user data
 */
export async function createUser(nickname: string, accessKey: string): Promise<User> {
  return apiCall<User>('/api/users', {
    method: 'POST',
    body: JSON.stringify({ nickname, access_key: accessKey }),
  });
}

// Local storage keys
const ACCESS_KEY_STORAGE_KEY = 'gym_bacteria_access_key';
const USER_STORAGE_KEY = 'gym_bacteria_user';

/**
 * Saves the user's access key to local storage
 * @param accessKey - The access key to save
 */
export function saveAccessKey(accessKey: string): void {
  localStorage.setItem(ACCESS_KEY_STORAGE_KEY, accessKey);
}

/**
 * Gets the saved access key from local storage
 * @returns The saved access key or null if not found
 */
export function getSavedAccessKey(): string | null {
  return localStorage.getItem(ACCESS_KEY_STORAGE_KEY);
}

/**
 * Saves the user data to local storage
 * @param user - The user data to save
 */
export function saveUser(user: User): void {
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
}

/**
 * Gets the saved user data from local storage
 * @returns The saved user data or null if not found
 */
export function getSavedUser(): User | null {
  const userData = localStorage.getItem(USER_STORAGE_KEY);
  return userData ? JSON.parse(userData) : null;
}

/**
 * Clears all saved authentication data
 */
export function clearAuth(): void {
  localStorage.removeItem(ACCESS_KEY_STORAGE_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
} 