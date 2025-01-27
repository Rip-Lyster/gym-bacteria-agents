'use client';

import { WorkoutExercise } from '@/types/models';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ClipboardIcon, PencilIcon } from '@heroicons/react/24/outline';

interface ExerciseListProps {
  exercises: WorkoutExercise[];
  onLogClick: (exerciseId: number) => void;
}

export function ExerciseList({ exercises, onLogClick }: ExerciseListProps) {
  if (!exercises.length) {
    return (
      <div className="text-center p-6 text-muted-foreground">
        No exercises added yet
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {exercises.map((exercise) => (
        <Card key={exercise.exercise_type_id}>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>{exercise.name}</span>
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onLogClick(exercise.exercise_type_id)}
                >
                  <ClipboardIcon className="h-4 w-4 mr-1" />
                  Log
                </Button>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-sm">
                <span className="font-medium">Sets:</span> {exercise.planned.sets}
              </div>
              <div className="text-sm">
                <span className="font-medium">Reps:</span> {exercise.planned.reps}
              </div>
              {exercise.planned.weight && (
                <div className="text-sm">
                  <span className="font-medium">Weight:</span> {exercise.planned.weight}
                </div>
              )}
              {exercise.planned.rest && (
                <div className="text-sm">
                  <span className="font-medium">Rest:</span> {exercise.planned.rest}
                </div>
              )}
              {exercise.planned.notes && (
                <div className="text-sm text-muted-foreground">
                  {exercise.planned.notes}
                </div>
              )}
              
              {exercise.logs && exercise.logs.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium mb-2">Recent Logs</h4>
                  <div className="space-y-2">
                    {exercise.logs.slice(-3).map((log, index) => (
                      <div key={index} className="text-sm">
                        <div className="flex justify-between text-muted-foreground">
                          <span>{new Date(log.timestamp).toLocaleDateString()}</span>
                          <span>RPE: {log.perceived_effort}</span>
                        </div>
                        <div className="space-y-1">
                          {log.sets.map((set, setIndex) => (
                            <div key={setIndex} className="flex space-x-4">
                              <span>{set.reps} reps</span>
                              <span>{set.weight}</span>
                              {set.rpe && <span>RPE: {set.rpe}</span>}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
} 