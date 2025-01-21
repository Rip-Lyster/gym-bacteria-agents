'use client';

import { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { getPlanWorkouts, updateWorkout } from '../../services/workouts';
import { Workout } from '../../types/workout';
import { WorkoutDetails } from './workout-details';

interface Props {
  planId: number;
  onDateSelect: (date: Date) => void;
}

export default function WorkoutCalendar({ planId, onDateSelect }: Props) {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
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

  const handleEventClick = (info: { event: any }) => {
    const workout = workouts.find(w => w.id === parseInt(info.event.id));
    if (workout) {
      setSelectedWorkout(workout);
    }
  };

  const handleStatusUpdate = async (workoutId: number, newStatus: 'planned' | 'completed' | 'skipped') => {
    try {
      const updatedWorkout = await updateWorkout(workoutId, { status: newStatus });
      setWorkouts(workouts.map(w => w.id === workoutId ? updatedWorkout : w));
      // Update the selected workout if it's currently being viewed
      if (selectedWorkout?.id === workoutId) {
        setSelectedWorkout(updatedWorkout);
      }
    } catch (err) {
      console.error('Failed to update workout status:', err);
    }
  };

  const events = workouts.map(workout => ({
    id: workout.id.toString(),
    title: workout.name,
    start: workout.planned_date,
    backgroundColor: workout.status === 'completed' ? '#22c55e' :
                    workout.status === 'skipped' ? '#ef4444' : '#3b82f6',
    borderColor: workout.status === 'completed' ? '#16a34a' :
                workout.status === 'skipped' ? '#dc2626' : '#2563eb',
    classNames: ['cursor-pointer hover:opacity-80'],
  }));

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 p-4 text-destructive">
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-card">
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        eventClick={handleEventClick}
        selectable={true}
        select={info => onDateSelect(info.start)}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,dayGridWeek'
        }}
        height="auto"
        eventTimeFormat={{
          hour: 'numeric',
          minute: '2-digit',
          meridiem: 'short'
        }}
      />

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