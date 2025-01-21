import { Workout, CreateWorkout, UpdateWorkout } from '../types/workout'

const API_BASE = '/api/workouts'

export async function createWorkout(workout: CreateWorkout): Promise<Workout> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(workout),
  })

  if (!response.ok) {
    throw new Error('Failed to create workout')
  }

  return response.json()
}

export async function updateWorkout(id: number, workout: UpdateWorkout): Promise<Workout> {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(workout),
  })

  if (!response.ok) {
    throw new Error('Failed to update workout')
  }

  return response.json()
}

export async function deleteWorkout(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error('Failed to delete workout')
  }
}

export async function getPlanWorkouts(planId: number): Promise<Workout[]> {
  const response = await fetch(`${API_BASE}/plan/${planId}`)

  if (!response.ok) {
    throw new Error('Failed to fetch workouts')
  }

  return response.json()
} 