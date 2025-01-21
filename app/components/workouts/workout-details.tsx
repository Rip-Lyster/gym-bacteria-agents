'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { format } from "date-fns";
import { Calendar, CheckCircle2, XCircle, Clock } from "lucide-react";
import { Workout } from "../../types/workout";
import { Button } from "../ui/button";

interface Props {
  workout: Workout;
  isOpen: boolean;
  onClose: () => void;
  onStatusChange: (status: 'planned' | 'completed' | 'skipped') => void;
}

export function WorkoutDetails({ workout, isOpen, onClose, onStatusChange }: Props) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{workout.name}</DialogTitle>
          <div className="flex items-center text-sm text-muted-foreground mt-1">
            <Calendar className="mr-1 h-4 w-4" />
            <span>{format(new Date(workout.planned_date), 'PPP')}</span>
          </div>
        </DialogHeader>

        <div className="mt-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Exercises</h3>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => onStatusChange('completed')}
                className={workout.status === 'completed' ? 'bg-green-50 text-green-600' : ''}
              >
                <CheckCircle2 className="mr-2 h-4 w-4" />
                Completed
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onStatusChange('skipped')}
                className={workout.status === 'skipped' ? 'bg-red-50 text-red-600' : ''}
              >
                <XCircle className="mr-2 h-4 w-4" />
                Skipped
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onStatusChange('planned')}
                className={workout.status === 'planned' ? 'bg-blue-50 text-blue-600' : ''}
              >
                <Clock className="mr-2 h-4 w-4" />
                Planned
              </Button>
            </div>
          </div>

          <div className="space-y-4">
            {workout.exercises.map((exercise) => (
              <div
                key={exercise.id}
                className="rounded-lg border p-4 hover:border-accent transition-colors"
              >
                <div className="font-medium text-lg">{exercise.exercise_name}</div>
                <div className="mt-2 grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Sets:</span>{" "}
                    <span className="font-medium">{exercise.sets}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Reps:</span>{" "}
                    <span className="font-medium">{exercise.reps}</span>
                  </div>
                  {exercise.weight && (
                    <div>
                      <span className="text-muted-foreground">Weight:</span>{" "}
                      <span className="font-medium">{exercise.weight}kg</span>
                    </div>
                  )}
                </div>
                {exercise.notes && (
                  <div className="mt-2 text-sm text-muted-foreground">
                    <span className="font-medium">Notes: </span>
                    {exercise.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
} 