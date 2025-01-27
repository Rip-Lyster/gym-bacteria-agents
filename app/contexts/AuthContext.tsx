'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { type User, authenticateUser, getSavedAccessKey, saveAccessKey, clearAuth } from '@/services/auth';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (accessKey: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check for saved access key on mount
  useEffect(() => {
    const initAuth = async () => {
      const savedKey = getSavedAccessKey();
      if (savedKey) {
        try {
          const userData = await authenticateUser(savedKey);
          setUser(userData);
          router.push('/dashboard');
        } catch (err) {
          clearAuth();
          setError('Session expired. Please login again.');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, [router]);

  const login = async (accessKey: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const userData = await authenticateUser(accessKey);
      setUser(userData);
      saveAccessKey(accessKey);
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid access key. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    clearAuth();
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 