'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useUser } from '../contexts/user-context';
import { createUser } from '../services/auth';

export default function SignupPage() {
  const { login } = useUser();
  const [nickname, setNickname] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [accessKey, setAccessKey] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nickname.trim()) {
      setError('Please enter your nickname');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // Generate a random access key
      const newAccessKey = Math.random().toString(36).substring(2, 15);
      const user = await createUser(nickname.trim(), newAccessKey);
      setAccessKey(newAccessKey);
    } catch (err) {
      console.error('Failed to create user:', err);
      setError('Failed to create account. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleContinue = async () => {
    if (!accessKey) return;
    
    try {
      await login(accessKey);
    } catch (err) {
      setError('Failed to log in with new account. Please try again.');
    }
  };

  if (accessKey) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md text-center">
          <h1 className="text-3xl font-bold mb-4">Account Created!</h1>
          <p className="mb-8 text-muted-foreground">
            Here's your access key. Make sure to save it somewhere safe - you'll need it to log in.
          </p>

          <div className="mb-8 p-4 bg-muted rounded-lg">
            <p className="font-mono text-lg break-all">{accessKey}</p>
          </div>

          <button
            onClick={handleContinue}
            className="w-full rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90"
          >
            Continue to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Create Account</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Get started with your training journey
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {error && (
            <div className="rounded-lg border border-destructive/50 p-4 text-destructive text-sm">
              <p>{error}</p>
            </div>
          )}

          <div>
            <label htmlFor="nickname" className="block text-sm font-medium mb-2">
              Nickname
            </label>
            <input
              id="nickname"
              type="text"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              className="w-full rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              placeholder="Enter your nickname"
              disabled={isSubmitting}
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-50"
          >
            {isSubmitting ? 'Creating account...' : 'Create Account'}
          </button>

          <div className="text-center text-sm">
            <p className="text-muted-foreground">
              Already have an access key?{' '}
              <Link href="/login" className="font-semibold text-primary hover:text-primary/90">
                Sign in
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
} 