'use client';
import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { getHealthStatus } from './services/api'
import { Dumbbell, Calendar, LineChart, AlertCircle } from 'lucide-react'

/**
 * Main Home component for the application.
 * Displays the application's landing page with health status monitoring and navigation links.
 * Features:
 * - Real-time API health status monitoring
 * - Responsive layout with mobile and desktop support
 * - Integration with Vercel deployment
 * - Quick access links to documentation and resources
 * @returns {JSX.Element} The rendered Home component
 */
export default function Home() {
  // State management for API health monitoring and error handling
  const [healthStatus, setHealthStatus] = useState<string>('Loading...');
  const [error, setError] = useState<string | null>(null);

  /**
   * Effect hook to fetch and monitor API health status
   * Runs once on component mount
   */
  useEffect(() => {
    getHealthStatus()
      .then(data => setHealthStatus(data.status))
      .catch(error => {
        console.error('Error fetching health check:', error);
        setError('Unable to connect to the server. Please try again later.');
        setHealthStatus('Error');
      });
  }, []);

  const features = [
    {
      name: 'Training Plans',
      description: 'Create and manage your training plans with ease. Track progress and adjust as needed.',
      href: '/training-plans',
      icon: Dumbbell,
    },
    {
      name: 'Workouts',
      description: 'Schedule and log your workouts. Keep track of sets, reps, and weights.',
      href: '/workouts',
      icon: Calendar,
    },
    {
      name: 'Progress Tracking',
      description: 'Visualize your progress over time with detailed charts and analytics.',
      href: '/progress',
      icon: LineChart,
    },
  ];

  return (
    <main className="flex-1">
      {error && (
        <div className="bg-destructive/15 text-destructive px-4 py-2 flex items-center justify-center gap-2">
          <AlertCircle className="h-4 w-4" />
          <span>{error}</span>
        </div>
      )}
      
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
              Your Training Journey Starts Here
            </h1>
            <p className="mt-6 text-lg leading-8 text-muted-foreground">
              Track your workouts, monitor progress, and achieve your fitness goals with our comprehensive training management system.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/training-plans"
                className="rounded-md bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
              >
                Get Started
              </Link>
              <Link href="/docs" className="text-sm font-semibold leading-6">
                Learn more <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-primary">Get Started</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
            Everything you need to manage your training
          </p>
          <p className="mt-6 text-lg leading-8 text-muted-foreground">
            Our platform provides all the tools you need to plan, track, and analyze your training journey.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
            {features.map((feature) => (
              <div key={feature.name} className="flex flex-col">
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7">
                  <feature.icon className="h-5 w-5 flex-none text-primary" aria-hidden="true" />
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-muted-foreground">
                  <p className="flex-auto">{feature.description}</p>
                  <p className="mt-6">
                    <Link href={feature.href} className="text-sm font-semibold leading-6 text-primary">
                      Learn more <span aria-hidden="true">→</span>
                    </Link>
                  </p>
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </main>
  )
}
