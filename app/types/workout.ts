export type WorkoutStatus = 'planned' | 'completed' | 'skipped'

export interface WorkoutExercise {
  id: number
  exercise_type_id: number
  exercise_name: string
  sets: number
  reps: number
  weight?: number
  notes?: string
  order: number
}

export interface Workout {
  id: number
  training_plan_id: number
  name: string
  planned_date: string
  status: WorkoutStatus
  exercises: WorkoutExercise[]
}

export interface CreateWorkoutExercise {
  exercise_type_id: number
  sets: number
  reps: number
  weight?: number
  notes?: string
}

export interface CreateWorkout {
  training_plan_id: number
  name: string
  planned_date: string
  status?: WorkoutStatus
  exercises: CreateWorkoutExercise[]
}

export interface UpdateWorkout {
  name?: string
  planned_date?: string
  status?: WorkoutStatus
  exercises?: CreateWorkoutExercise[]
} 