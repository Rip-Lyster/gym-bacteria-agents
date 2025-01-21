'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { CalendarIcon, Pencil, Trash2, ArrowLeft, LayoutList, CalendarDays } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';
import { TrainingPlan, getTrainingPlan, deleteTrainingPlan } from '../../services/training-plans';
import { useUser } from '../../contexts/user-context';
import WorkoutList from '../../components/workouts/workout-list';
import WorkoutCalendar from '../../components/workouts/workout-calendar';
import CreateWorkoutForm from '../../components/workouts/create-workout-form';

interface Props {
  params: {
    id: string;
  };
}

type ViewMode = 'list' | 'calendar';

export default function TrainingPlanDetailsPage({ params }: Props) {
  const router = useRouter();
  const { user } = useUser();
  const [plan, setPlan] = useState<TrainingPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [showCreateWorkout, setShowCreateWorkout] = useState(false);
  const [viewMode, setViewMode] = useState<ViewMode>('calendar');
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  useEffect(() => {
    async function fetchPlan() {
      if (!user) return;

      try {
        const data = await getTrainingPlan(parseInt(params.id));
        // Verify the plan belongs to the current user
        if (data.user_id !== user.id) {
          setError('You do not have permission to view this training plan.');
          return;
        }
        setPlan(data);
      } catch (err) {
        console.error('Failed to fetch training plan:', err);
        setError('Failed to load training plan. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchPlan();
  }, [params.id, user]);

  const handleDelete = async () => {
    if (!plan || !confirm('Are you sure you want to delete this training plan?')) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTrainingPlan(plan.id);
      router.push('/training-plans');
    } catch (err) {
      console.error('Failed to delete training plan:', err);
      setError('Failed to delete training plan. Please try again.');
      setIsDeleting(false);
    }
  };

  const handleCreateClick = (date?: Date) => {
    setSelectedDate(date ?? null);
    setShowCreateWorkout(true);
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

  if (!plan) {
    return (
      <div className="container py-10">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Training Plan Not Found</h1>
          <p className="mt-2 text-muted-foreground">
            The training plan you're looking for doesn't exist.
          </p>
          <Link
            href="/training-plans"
            className="mt-4 inline-flex items-center text-sm font-medium text-primary"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Training Plans
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-10">
      <div className="mb-8">
        <Link
          href="/training-plans"
          className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Training Plans
        </Link>

        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{plan.name}</h1>
            <div className="mt-2 flex items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center">
                <CalendarIcon className="mr-1 h-4 w-4" />
                <span>
                  {new Date(plan.start_date).toLocaleDateString()} -{' '}
                  {new Date(plan.end_date).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <Link
              href={`/training-plans/${plan.id}/edit`}
              className="inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium border border-input hover:bg-accent hover:text-accent-foreground"
            >
              <Pencil className="mr-2 h-4 w-4" />
              Edit
            </Link>
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium bg-destructive text-destructive-foreground hover:bg-destructive/90 disabled:opacity-50"
            >
              <Trash2 className="mr-2 h-4 w-4" />
              {isDeleting ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>
      </div>

      <div className="rounded-lg border p-6">
        {showCreateWorkout ? (
          <div className="max-w-2xl mx-auto">
            <h2 className="text-lg font-semibold mb-4">Add New Workout</h2>
            <CreateWorkoutForm
              planId={plan.id}
              initialDate={selectedDate ? selectedDate : undefined}
              onSuccess={() => {
                setShowCreateWorkout(false);
                setSelectedDate(null);
              }}
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setViewMode('calendar')}
                  className={`inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    viewMode === 'calendar'
                      ? 'bg-primary text-primary-foreground'
                      : 'border border-input hover:bg-accent hover:text-accent-foreground'
                  }`}
                >
                  <CalendarDays className="mr-2 h-4 w-4" />
                  Calendar
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                    viewMode === 'list'
                      ? 'bg-primary text-primary-foreground'
                      : 'border border-input hover:bg-accent hover:text-accent-foreground'
                  }`}
                >
                  <LayoutList className="mr-2 h-4 w-4" />
                  List
                </button>
              </div>
            </div>

            {viewMode === 'calendar' ? (
              <WorkoutCalendar
                planId={plan.id}
                onDateSelect={date => handleCreateClick(date)}
              />
            ) : (
              <WorkoutList
                planId={plan.id}
                onCreateClick={() => handleCreateClick()}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
} 