import { useEffect, useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { Workout, WorkoutStatus } from '../types/workout'
import { getPlanWorkouts } from '../services/workouts'
import { useParams } from 'next/navigation'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { CalendarIcon, Plus } from 'lucide-react'
import Link from 'next/link'

const statusColors: Record<WorkoutStatus, string> = {
  planned: 'bg-blue-500',
  completed: 'bg-green-500',
  skipped: 'bg-gray-500',
}

interface WorkoutCalendarProps {
  planId: number
  onDateSelect?: (date: Date) => void
}

export function WorkoutCalendar({ planId, onDateSelect }: WorkoutCalendarProps) {
  const [workouts, setWorkouts] = useState<Workout[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadWorkouts = async () => {
      try {
        setIsLoading(true)
        const data = await getPlanWorkouts(planId)
        setWorkouts(data)
        setError(null)
      } catch (err) {
        setError('Failed to load workouts')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    loadWorkouts()
  }, [planId])

  const events = workouts.map(workout => ({
    id: workout.id.toString(),
    title: workout.name,
    start: workout.planned_date,
    className: statusColors[workout.status],
    extendedProps: {
      status: workout.status,
      exercises: workout.exercises,
    },
  }))

  const handleDateSelect = (info: { start: Date }) => {
    if (onDateSelect) {
      onDateSelect(info.start)
    }
  }

  if (isLoading) {
    return <div className="flex items-center justify-center p-8">Loading...</div>
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-red-500">
        <p>{error}</p>
        <Button onClick={() => window.location.reload()} variant="outline" className="mt-4">
          Retry
        </Button>
      </div>
    )
  }

  return (
    <div className="p-4">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <CalendarIcon className="h-5 w-5" />
          <h2 className="text-xl font-semibold">Workout Calendar</h2>
        </div>
        <Link href={`/training-plans/${planId}/workouts/new`}>
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Workout
          </Button>
        </Link>
      </div>

      <div className="mb-4 flex space-x-2">
        {Object.entries(statusColors).map(([status, color]) => (
          <Badge key={status} className={color}>
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </Badge>
        ))}
      </div>

      <div className="rounded-lg border bg-card">
        <FullCalendar
          plugins={[dayGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          selectable={true}
          select={handleDateSelect}
          events={events}
          eventContent={renderEventContent}
          height="auto"
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek',
          }}
        />
      </div>
    </div>
  )
}

function renderEventContent(eventInfo: any) {
  return (
    <div className="p-1">
      <div className="font-semibold">{eventInfo.event.title}</div>
      <div className="text-xs">
        {eventInfo.event.extendedProps.exercises.length} exercise
        {eventInfo.event.extendedProps.exercises.length !== 1 ? 's' : ''}
      </div>
    </div>
  )
} 