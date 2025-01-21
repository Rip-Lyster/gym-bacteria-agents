import { apiCall } from './api';

export interface TrainingPlan {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  user_id: number;
}

export interface CreateTrainingPlanData {
  name: string;
  start_date: string;
  end_date: string;
  user_id: number;
}

export interface UpdateTrainingPlanData extends Partial<CreateTrainingPlanData> {
  id: number;
}

/**
 * Fetches all training plans for a user
 * @param userId - The ID of the user
 * @returns Promise containing the list of training plans
 */
export async function getTrainingPlans(userId: number): Promise<TrainingPlan[]> {
  return apiCall<TrainingPlan[]>(`/api/users/${userId}/training-plans`);
}

/**
 * Fetches a specific training plan
 * @param planId - The ID of the training plan
 * @returns Promise containing the training plan details
 */
export async function getTrainingPlan(planId: number): Promise<TrainingPlan> {
  return apiCall<TrainingPlan>(`/api/training-plans/${planId}`);
}

/**
 * Creates a new training plan
 * @param data - The training plan data
 * @returns Promise containing the created training plan
 */
export async function createTrainingPlan(data: CreateTrainingPlanData): Promise<TrainingPlan> {
  return apiCall<TrainingPlan>('/api/training-plans', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Updates an existing training plan
 * @param data - The training plan data to update
 * @returns Promise containing the updated training plan
 */
export async function updateTrainingPlan(data: UpdateTrainingPlanData): Promise<TrainingPlan> {
  return apiCall<TrainingPlan>(`/api/training-plans/${data.id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

/**
 * Deletes a training plan
 * @param planId - The ID of the training plan to delete
 * @returns Promise that resolves when the plan is deleted
 */
export async function deleteTrainingPlan(planId: number): Promise<void> {
  return apiCall<void>(`/api/training-plans/${planId}`, {
    method: 'DELETE',
  });
} 