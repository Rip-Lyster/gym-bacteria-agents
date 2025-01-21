'use client';

import { useState, useEffect } from 'react';
import { Calendar, Plus, Trash2, Loader2, ChevronRight } from 'lucide-react';
import { format } from 'date-fns';
import { getPlanWorkouts, updateWorkout, deleteWorkout } from '../../services/workouts';
import { Workout } from '../../types/workout';
import { WorkoutDetails } from './workout-details';

interface Props {
  planId: number;
  onCreateClick: () => void;
}

export default function WorkoutList({ planId, onCreateClick }: Props) {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingWorkoutId, setUpdatingWorkoutId] = useState<number | null>(null);
  const [deletingWorkoutId, setDeletingWorkoutId] = useState<number | null>(null);
  const [selectedWorkout, setSelectedWorkout] = useState<Workout | null>(null);

  useEffect(() => {
    async function fetchWorkouts() {
      try {
        const data = await getPlanWorkouts(planId);
        setWorkouts(data);
      } catch (err) {
        console.error('Failed to fetch workouts:', err);
        setError('Failed to load workouts. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchWorkouts();
  }, [planId]);

  const handleStatusUpdate = async (workoutId: number, newStatus: 'planned' | 'completed' | 'skipped') => {
    setUpdatingWorkoutId(workoutId);
    setError(null);

    try {
      const updatedWorkout = await updateWorkout(workoutId, { status: newStatus });
      setWorkouts(workouts.map(w => w.id === workoutId ? updatedWorkout : w));
      // Update the selected workout if it's currently being viewed
      if (selectedWorkout?.id === workoutId) {
        setSelectedWorkout(updatedWorkout);
      }
    } catch (err) {
      console.error('Failed to update workout status:', err);
      setError('Failed to update workout status. Please try again.');
    } finally {
      setUpdatingWorkoutId(null);
    }
  };

  const handleDelete = async (workoutId: number) => {
    if (!confirm('Are you sure you want to delete this workout?')) {
      return;
    }

    setDeletingWorkoutId(workoutId);
    setError(null);

    try {
      await deleteWorkout(workoutId);
      setWorkouts(workouts.filter(w => w.id !== workoutId));
      if (selectedWorkout?.id === workoutId) {
        setSelectedWorkout(null);
      }
    } catch (err) {
      console.error('Failed to delete workout:', err);
      setError('Failed to delete workout. Please try again.');
    } finally {
      setDeletingWorkoutId(null);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 p-4 text-destructive">
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">Workouts</h2>
        <button
          onClick={onCreateClick}
          className="inline-flex items-center justify-center rounded-md text-sm font-medium bg-primary text-primary-foreground h-9 px-4 py-2 hover:bg-primary/90"
        >
          <Plus className="mr-2 h-4 w-4" />
          Add Workout
        </button>
      </div>

      {workouts.length === 0 ? (
        <p className="text-muted-foreground">No workouts added yet.</p>
      ) : (
        <div className="space-y-4">
          {workouts.map(workout => (
            <div
              key={workout.id}
              className="rounded-lg border p-4 hover:border-accent transition-colors cursor-pointer"
              onClick={() => setSelectedWorkout(workout)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium">{workout.name}</h3>
                  <div className="flex items-center text-sm text-muted-foreground mt-1">
                    <Calendar className="mr-1 h-4 w-4" />
                    <span>{format(new Date(workout.planned_date), 'PPP')}</span>
                  </div>
                  <div className="mt-2 text-sm text-muted-foreground">
                    {workout.exercises.length} exercise{workout.exercises.length !== 1 ? 's' : ''}
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    workout.status === 'completed' ? 'bg-green-50 text-green-600' :
                    workout.status === 'skipped' ? 'bg-red-50 text-red-600' :
                    'bg-blue-50 text-blue-600'
                  }`}>
                    {workout.status.charAt(0).toUpperCase() + workout.status.slice(1)}
                  </div>
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedWorkout && (
        <WorkoutDetails
          workout={selectedWorkout}
          isOpen={true}
          onClose={() => setSelectedWorkout(null)}
          onStatusChange={(status) => handleStatusUpdate(selectedWorkout.id, status)}
        />
      )}
    </div>
  );
} 