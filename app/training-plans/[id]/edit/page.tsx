'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { CalendarIcon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { TrainingPlan, getTrainingPlan, updateTrainingPlan } from '../../../services/training-plans';
import { useUser } from '../../../contexts/user-context';

interface Props {
  params: {
    id: string;
  };
}

interface FormData {
  name: string;
  start_date: string;
  end_date: string;
}

export default function EditTrainingPlanPage({ params }: Props) {
  const router = useRouter();
  const { user } = useUser();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>();

  useEffect(() => {
    async function fetchPlan() {
      if (!user) return;

      try {
        const data = await getTrainingPlan(parseInt(params.id));
        // Verify the plan belongs to the current user
        if (data.user_id !== user.id) {
          setError('You do not have permission to edit this training plan.');
          return;
        }
        // Pre-fill the form with existing data
        reset({
          name: data.name,
          start_date: data.start_date,
          end_date: data.end_date,
        });
      } catch (err) {
        console.error('Failed to fetch training plan:', err);
        setError('Failed to load training plan. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchPlan();
  }, [params.id, user, reset]);

  const onSubmit = async (data: FormData) => {
    if (!user) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await updateTrainingPlan({
        id: parseInt(params.id),
        ...data,
        user_id: user.id,
      });
      router.push(`/training-plans/${params.id}`);
    } catch (err) {
      console.error('Failed to update training plan:', err);
      setError('Failed to update training plan. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container py-10">
        <div className="flex justify-center items-center min-h-[200px]">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-muted rounded w-[250px]" />
            <div className="h-4 bg-muted rounded w-[200px]" />
            <div className="h-4 bg-muted rounded w-[150px]" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-10">
        <div className="rounded-lg border border-destructive/50 p-4 text-destructive">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-10">
      <div className="mx-auto max-w-2xl">
        <Link
          href={`/training-plans/${params.id}`}
          className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-8"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Plan Details
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Edit Training Plan</h1>
          <p className="text-muted-foreground">Update your training plan details</p>
        </div>

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
            <Link
              href={`/training-plans/${params.id}`}
              className="rounded-md px-4 py-2 text-sm font-medium border border-input hover:bg-accent hover:text-accent-foreground"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              {isSubmitting ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 