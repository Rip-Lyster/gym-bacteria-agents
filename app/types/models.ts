export interface User {
  id: number;
  access_key: string;
  nickname: string;
  created_at: string;
  updated_at: string;
  last_access?: string;
}

export interface TrainingPlan {
  id: number;
  user_id: number;
  name: string;
  progression_type?: string;
  target_weekly_hours?: number;
  start_date?: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TrainingBlock {
  id: number;
  plan_id: number;
  name: string;
  primary_focus: string;
  duration_weeks: number;
  sequence_order: number;
  created_at: string;
  updated_at: string;
}

export interface ExerciseType {
  id: number;
  name: string;
  category: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface ExerciseSet {
  reps: number;
  weight: string;
  rpe?: number;
}

export interface ExerciseLog {
  timestamp: string;
  sets: ExerciseSet[];
  notes?: string;
  perceived_effort?: number;
  completed: boolean;
}

export interface PlannedExercise {
  sets: number;
  reps: string;
  weight?: string;
  rest?: string;
  notes?: string;
}

export interface WorkoutExercise {
  exercise_type_id: number;
  name: string;
  sequence: number;
  planned: PlannedExercise;
  logs?: ExerciseLog[];
}

export interface Workout {
  id: number;
  block_id: number;
  name: string;
  planned_date: string;
  actual_date?: string;
  status: 'planned' | 'completed' | 'skipped';
  sequence_order: number;
  exercises: {
    exercises: WorkoutExercise[];
  };
  created_at: string;
  updated_at: string;
} 