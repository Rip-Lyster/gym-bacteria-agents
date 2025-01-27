'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { ExerciseSet } from '@/types/models';
import { logExercise } from '@/services/workouts';
import { toast } from '@/components/ui/use-toast';

interface LogExerciseDialogProps {
  open: boolean;
  onClose: () => void;
  blockId: number;
  workoutId: number;
  exerciseId: number;
}

const setSchema = z.object({
  reps: z.number().min(1),
  weight: z.string().min(1),
  rpe: z.number().min(1).max(10).optional(),
});

const logSchema = z.object({
  sets: z.array(setSchema).min(1),
  notes: z.string().optional(),
  perceived_effort: z.number().min(1).max(10).optional(),
});

type LogFormData = z.infer<typeof logSchema>;

export function LogExerciseDialog({
  open,
  onClose,
  blockId,
  workoutId,
  exerciseId,
}: LogExerciseDialogProps) {
  const [sets, setSets] = useState<ExerciseSet[]>([{ reps: 0, weight: '', rpe: undefined }]);
  const { register, handleSubmit, formState: { errors } } = useForm<LogFormData>({
    resolver: zodResolver(logSchema),
  });

  const addSet = () => {
    setSets([...sets, { reps: 0, weight: '', rpe: undefined }]);
  };

  const removeSet = (index: number) => {
    setSets(sets.filter((_, i) => i !== index));
  };

  const onSubmit = async (data: LogFormData) => {
    try {
      await logExercise(blockId, workoutId, {
        exercise_type_id: exerciseId,
        log: {
          timestamp: new Date().toISOString(),
          sets: data.sets,
          notes: data.notes,
          perceived_effort: data.perceived_effort,
          completed: true,
        },
      });
      toast({
        title: 'Exercise logged successfully',
        variant: 'default',
      });
      onClose();
    } catch (error) {
      toast({
        title: 'Failed to log exercise',
        description: 'Please try again',
        variant: 'destructive',
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Log Exercise</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-4">
            {sets.map((_, index) => (
              <div key={index} className="grid grid-cols-3 gap-4 items-end">
                <div>
                  <Label>Reps</Label>
                  <Input
                    type="number"
                    {...register(`sets.${index}.reps` as const, { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Weight</Label>
                  <Input {...register(`sets.${index}.weight` as const)} />
                </div>
                <div className="flex items-center space-x-2">
                  <div className="flex-1">
                    <Label>RPE (optional)</Label>
                    <Input
                      type="number"
                      {...register(`sets.${index}.rpe` as const, { valueAsNumber: true })}
                    />
                  </div>
                  {sets.length > 1 && (
                    <Button
                      type="button"
                      variant="destructive"
                      size="sm"
                      onClick={() => removeSet(index)}
                    >
                      Remove
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>

          <Button type="button" variant="outline" onClick={addSet}>
            Add Set
          </Button>

          <div>
            <Label>Notes (optional)</Label>
            <Input {...register('notes')} />
          </div>

          <div>
            <Label>Overall RPE (optional)</Label>
            <Input
              type="number"
              {...register('perceived_effort', { valueAsNumber: true })}
            />
          </div>

          <div className="flex justify-end space-x-2">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">Save</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
} 