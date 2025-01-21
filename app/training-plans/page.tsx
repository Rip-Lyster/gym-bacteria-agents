'use client';

import { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import Link from 'next/link';
import { TrainingPlan, getTrainingPlans } from '../services/training-plans';
import { useUser } from '../contexts/user-context';

export default function TrainingPlansPage() {
  const { user } = useUser();
  const [plans, setPlans] = useState<TrainingPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPlans() {
      if (!user) return;

      try {
        const data = await getTrainingPlans(user.id);
        setPlans(data);
      } catch (err) {
        console.error('Failed to fetch training plans:', err);
        setError('Failed to load training plans. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchPlans();
  }, [user]);

  return (
    <div className="container py-10">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Training Plans</h1>
          <p className="text-muted-foreground">Manage and track your training plans</p>
        </div>
        <Link
          href="/training-plans/new"
          className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          <Plus className="mr-2 h-4 w-4" />
          New Plan
        </Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center min-h-[200px]">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-muted rounded w-[250px]" />
            <div className="h-4 bg-muted rounded w-[200px]" />
            <div className="h-4 bg-muted rounded w-[150px]" />
          </div>
        </div>
      ) : error ? (
        <div className="rounded-lg border border-destructive/50 p-4 text-destructive">
          <p>{error}</p>
        </div>
      ) : plans.length === 0 ? (
        <div className="rounded-lg border border-dashed p-8 text-center">
          <h3 className="font-semibold mb-1">No training plans</h3>
          <p className="text-muted-foreground mb-4">Get started by creating a new training plan.</p>
          <Link
            href="/training-plans/new"
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            <Plus className="mr-2 h-4 w-4" />
            Create your first plan
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {plans.map((plan) => (
            <Link
              key={plan.id}
              href={`/training-plans/${plan.id}`}
              className="group relative rounded-lg border p-6 hover:border-primary transition-colors"
            >
              <h3 className="font-semibold mb-2">{plan.name}</h3>
              <div className="text-sm text-muted-foreground">
                <p>Start: {new Date(plan.start_date).toLocaleDateString()}</p>
                <p>End: {new Date(plan.end_date).toLocaleDateString()}</p>
              </div>
              <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="text-primary text-sm">View details →</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
} 