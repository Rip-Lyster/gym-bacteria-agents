import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Calendar } from './ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover'
import { format } from 'date-fns'
import { CalendarIcon, Plus, Trash2 } from 'lucide-react'
import { cn } from '../lib/utils'
import { CreateWorkout, UpdateWorkout, Workout } from '../types/workout'

const workoutSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  planned_date: z.date(),
  exercises: z.array(z.object({
    exercise_type_id: z.number(),
    sets: z.number().min(1, 'Sets must be at least 1'),
    reps: z.number().min(1, 'Reps must be at least 1'),
    weight: z.number().optional(),
    notes: z.string().optional(),
  })).min(1, 'At least one exercise is required'),
})

type WorkoutFormData = z.infer<typeof workoutSchema>

interface WorkoutFormProps {
  planId: number
  initialData?: Workout
  onSubmit: (data: CreateWorkout | UpdateWorkout) => Promise<void>
  exerciseTypes: Array<{ id: number; name: string }>
}

export function WorkoutForm({ planId, initialData, onSubmit, exerciseTypes }: WorkoutFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)

  const form = useForm<WorkoutFormData>({
    resolver: zodResolver(workoutSchema),
    defaultValues: initialData ? {
      name: initialData.name,
      planned_date: new Date(initialData.planned_date),
      exercises: initialData.exercises.map(e => ({
        exercise_type_id: e.exercise_type_id,
        sets: e.sets,
        reps: e.reps,
        weight: e.weight,
        notes: e.notes,
      })),
    } : {
      name: '',
      planned_date: new Date(),
      exercises: [{
        exercise_type_id: exerciseTypes[0]?.id || 0,
        sets: 3,
        reps: 10,
      }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'exercises',
  })

  const handleSubmit = async (data: WorkoutFormData) => {
    try {
      setIsSubmitting(true)
      await onSubmit({
        ...data,
        training_plan_id: planId,
        planned_date: format(data.planned_date, 'yyyy-MM-dd'),
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-8">
      <div className="space-y-4">
        <div>
          <Label htmlFor="name">Workout Name</Label>
          <Input
            id="name"
            {...form.register('name')}
            placeholder="e.g., Upper Body Strength"
          />
          {form.formState.errors.name && (
            <p className="mt-1 text-sm text-red-500">{form.formState.errors.name.message}</p>
          )}
        </div>

        <div>
          <Label>Planned Date</Label>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className={cn(
                  'w-full justify-start text-left font-normal',
                  !form.getValues('planned_date') && 'text-muted-foreground'
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {form.getValues('planned_date') ? (
                  format(form.getValues('planned_date'), 'PPP')
                ) : (
                  <span>Pick a date</span>
                )}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={form.getValues('planned_date')}
                onSelect={(date: Date | undefined) => form.setValue('planned_date', date || new Date())}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Label>Exercises</Label>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => append({
              exercise_type_id: exerciseTypes[0]?.id || 0,
              sets: 3,
              reps: 10,
            })}
          >
            <Plus className="mr-2 h-4 w-4" />
            Add Exercise
          </Button>
        </div>

        {fields.map((field, index) => (
          <div key={field.id} className="rounded-lg border p-4">
            <div className="mb-4 flex items-center justify-between">
              <h4 className="text-sm font-medium">Exercise {index + 1}</h4>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => remove(index)}
                disabled={fields.length === 1}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <Label>Exercise Type</Label>
                <select
                  {...form.register(`exercises.${index}.exercise_type_id`, {
                    valueAsNumber: true,
                  })}
                  className="w-full rounded-md border p-2"
                >
                  {exerciseTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <Label>Sets</Label>
                <Input
                  type="number"
                  {...form.register(`exercises.${index}.sets`, {
                    valueAsNumber: true,
                  })}
                  min={1}
                />
              </div>

              <div>
                <Label>Reps</Label>
                <Input
                  type="number"
                  {...form.register(`exercises.${index}.reps`, {
                    valueAsNumber: true,
                  })}
                  min={1}
                />
              </div>

              <div>
                <Label>Weight (optional)</Label>
                <Input
                  type="number"
                  {...form.register(`exercises.${index}.weight`, {
                    valueAsNumber: true,
                  })}
                  step={0.5}
                  min={0}
                />
              </div>

              <div className="sm:col-span-2">
                <Label>Notes (optional)</Label>
                <Input
                  {...form.register(`exercises.${index}.notes`)}
                  placeholder="Any special instructions or notes"
                />
              </div>
            </div>
          </div>
        ))}

        {form.formState.errors.exercises && (
          <p className="text-sm text-red-500">{form.formState.errors.exercises.message}</p>
        )}
      </div>

      <Button type="submit" disabled={isSubmitting} className="w-full">
        {isSubmitting ? 'Saving...' : initialData ? 'Update Workout' : 'Create Workout'}
      </Button>
    </form>
  )
} 