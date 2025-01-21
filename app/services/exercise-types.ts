import { apiCall } from './api';

export interface ExerciseType {
  id: number;
  name: string;
  category: string;
  parameters?: Record<string, any>;
}

/**
 * Fetches all exercise types
 * @returns Promise containing the list of exercise types
 */
export async function getExerciseTypes(): Promise<ExerciseType[]> {
  return apiCall<ExerciseType[]>('/api/exercise-types');
}

/**
 * Creates a new exercise type
 * @param data - The exercise type data
 * @returns Promise containing the created exercise type
 */
export async function createExerciseType(data: Omit<ExerciseType, 'id'>): Promise<ExerciseType> {
  return apiCall<ExerciseType>('/api/exercise-types', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Deletes an exercise type
 * @param typeId - The ID of the exercise type to delete
 * @returns Promise that resolves when the exercise type is deleted
 */
export async function deleteExerciseType(typeId: number): Promise<void> {
  return apiCall<void>(`/api/exercise-types/${typeId}`, {
    method: 'DELETE',
  });
} 