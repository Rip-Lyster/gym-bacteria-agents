'use client';

import { useState, useEffect } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { ExerciseType, getExerciseTypes } from '../../services/exercise-types';

interface Props {
  onSelect: (exercise: ExerciseType) => void;
}

export default function ExerciseSelector({ onSelect }: Props) {
  const [exercises, setExercises] = useState<ExerciseType[]>([]);
  const [filteredExercises, setFilteredExercises] = useState<ExerciseType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function fetchExercises() {
      try {
        const data = await getExerciseTypes();
        setExercises(data);
        setFilteredExercises(data);
      } catch (err) {
        console.error('Failed to fetch exercises:', err);
        setError('Failed to load exercises. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchExercises();
  }, []);

  useEffect(() => {
    const query = searchQuery.toLowerCase();
    const filtered = exercises.filter(
      exercise =>
        exercise.name.toLowerCase().includes(query) ||
        exercise.category.toLowerCase().includes(query)
    );
    setFilteredExercises(filtered);
  }, [searchQuery, exercises]);

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
    <div className="space-y-4">
      <div className="relative">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search exercises..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full rounded-md border border-input pl-9 pr-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>

      <div className="grid gap-2">
        {filteredExercises.length === 0 ? (
          <p className="text-center text-muted-foreground py-4">
            No exercises found
          </p>
        ) : (
          filteredExercises.map(exercise => (
            <button
              key={exercise.id}
              onClick={() => onSelect(exercise)}
              className="flex flex-col items-start rounded-lg border p-3 hover:bg-accent text-left transition-colors"
            >
              <span className="font-medium">{exercise.name}</span>
              <span className="text-sm text-muted-foreground">
                {exercise.category}
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  );
} 