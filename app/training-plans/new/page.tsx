'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { CalendarIcon } from 'lucide-react';
import { format } from 'date-fns';
import { CreateTrainingPlanData, createTrainingPlan } from '../../services/training-plans';
import { useUser } from '../../contexts/user-context';

interface FormData extends Omit<CreateTrainingPlanData, 'user_id'> {}

export default function NewTrainingPlanPage() {
  const router = useRouter();
  const { user } = useUser();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    defaultValues: {
      name: '',
      start_date: format(new Date(), 'yyyy-MM-dd'),
      end_date: format(new Date(), 'yyyy-MM-dd'),
    },
  });

  const onSubmit = async (data: FormData) => {
    if (!user) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await createTrainingPlan({
        ...data,
        user_id: user.id,
      });
      router.push('/training-plans');
    } catch (err) {
      console.error('Failed to create training plan:', err);
      setError('Failed to create training plan. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container py-10">
      <div className="mx-auto max-w-2xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Create New Training Plan</h1>
          <p className="text-muted-foreground">Create a new training plan to organize your workouts</p>
        </div>

        {error && (
          <div className="mb-6 rounded-lg border border-destructive/50 p-4 text-destructive">
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium mb-2">
              Plan Name
            </label>
            <input
              type="text"
              id="name"
              className="w-full rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              placeholder="e.g., Summer Strength Training"
              {...register('name', { required: 'Plan name is required' })}
            />
            {errors.name && (
              <p className="mt-1 text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <label htmlFor="start_date" className="block text-sm font-medium mb-2">
                Start Date
              </label>
              <div className="relative">
                <input
                  type="date"
                  id="start_date"
                  className="w-full rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  {...register('start_date', { required: 'Start date is required' })}
                />
                <CalendarIcon className="absolute right-3 top-2.5 h-4 w-4 text-muted-foreground" />
              </div>
              {errors.start_date && (
                <p className="mt-1 text-sm text-destructive">{errors.start_date.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="end_date" className="block text-sm font-medium mb-2">
                End Date
              </label>
              <div className="relative">
                <input
                  type="date"
                  id="end_date"
                  className="w-full rounded-md border border-input px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                  {...register('end_date', { required: 'End date is required' })}
                />
                <CalendarIcon className="absolute right-3 top-2.5 h-4 w-4 text-muted-foreground" />
              </div>
              {errors.end_date && (
                <p className="mt-1 text-sm text-destructive">{errors.end_date.message}</p>
              )}
            </div>
          </div>

          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={() => router.back()}
              className="rounded-md px-4 py-2 text-sm font-medium border border-input hover:bg-accent hover:text-accent-foreground"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              {isSubmitting ? 'Creating...' : 'Create Plan'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 