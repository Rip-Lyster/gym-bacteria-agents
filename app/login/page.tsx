'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useUser } from '../contexts/user-context';

export default function LoginPage() {
  const { login, error: contextError } = useUser();
  const [accessKey, setAccessKey] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!accessKey.trim()) {
      setError('Please enter your access key');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await login(accessKey.trim());
    } catch (err) {
      // Error is handled by the context
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Welcome Back</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Enter your access key to continue
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {(error || contextError) && (
            <div className="rounded-lg border border-destructive/50 p-4 text-destructive text-sm">
              <p>{error || contextError}</p>
            </div>
          )}

          <div>
            <label htmlFor="access-key" className="block text-sm font-medium mb-2">
              Access Key
            </label>
            <input
              id="access-key"
              type="text"
              value={accessKey}
              onChange={(e) => setAccessKey(e.target.value)}
              className="w-full rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              placeholder="Enter your access key"
              disabled={isSubmitting}
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-50"
          >
            {isSubmitting ? 'Signing in...' : 'Sign in'}
          </button>

          <div className="text-center text-sm">
            <p className="text-muted-foreground">
              Don't have an access key?{' '}
              <Link href="/signup" className="font-semibold text-primary hover:text-primary/90">
                Create one
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
} 