'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { User, authenticateUser, getSavedAccessKey, getSavedUser, saveAccessKey, saveUser, clearAuth } from '../services/auth';

interface UserContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (accessKey: string) => Promise<void>;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

const PUBLIC_PATHS = ['/login', '/signup'];

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    async function initializeAuth() {
      const savedUser = getSavedUser();
      const savedAccessKey = getSavedAccessKey();

      if (savedUser) {
        setUser(savedUser);
        setIsLoading(false);
        return;
      }

      if (savedAccessKey) {
        try {
          const userData = await authenticateUser(savedAccessKey);
          setUser(userData);
          saveUser(userData);
        } catch (err) {
          console.error('Failed to authenticate with saved access key:', err);
          clearAuth();
          setError('Your session has expired. Please log in again.');
        }
      }

      setIsLoading(false);
    }

    initializeAuth();
  }, []);

  useEffect(() => {
    if (!isLoading && !user && !PUBLIC_PATHS.includes(pathname)) {
      router.push('/login');
    }
  }, [isLoading, user, pathname, router]);

  const login = async (accessKey: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const userData = await authenticateUser(accessKey);
      setUser(userData);
      saveAccessKey(accessKey);
      saveUser(userData);
      router.push('/training-plans');
    } catch (err) {
      console.error('Login failed:', err);
      setError('Invalid access key. Please try again.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    clearAuth();
    router.push('/login');
  };

  return (
    <UserContext.Provider value={{ user, isLoading, error, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
} 