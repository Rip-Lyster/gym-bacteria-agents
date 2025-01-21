from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, Workout, TrainingPlan, WorkoutExercise, ExerciseType
from ..core.validation import validate_request_data, validate_date_format
from sqlalchemy.exc import IntegrityError
from typing import List

bp = Blueprint('workouts', __name__, url_prefix='/api/workouts')

@bp.route('', methods=['POST'])
def create_workout():
    """Create a new workout with exercises.
    
    Required fields:
        - training_plan_id: ID of the associated training plan
        - name: Workout name
        - planned_date: Planned date (YYYY-MM-DD)
        - exercises: List of exercises, each containing:
            - exercise_type_id: ID of the exercise type
            - sets: Number of sets
            - reps: Number of reps
            - weight: Weight (optional)
            - notes: Exercise notes (optional)
        
    Optional fields:
        - status: Workout status (default: 'planned')
        
    Returns:
        Workout data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['training_plan_id', 'name', 'planned_date', 'exercises'])
        
        if not isinstance(data['exercises'], list):
            abort(400, description="Exercises must be a list")
        
        planned_date = validate_date_format(data['planned_date'])
        
        # Verify training plan exists
        training_plan = TrainingPlan.query.get_or_404(data['training_plan_id'])
        
        # Create workout
        workout = Workout(
            training_plan_id=data['training_plan_id'],
            name=data['name'],
            planned_date=planned_date,
            status=data.get('status', 'planned')
        )
        
        if workout.status not in ['planned', 'completed', 'skipped']:
            abort(400, description="Invalid status. Must be one of: planned, completed, skipped")
        
        db.session.add(workout)
        
        # Add exercises
        for i, exercise_data in enumerate(data['exercises']):
            validate_request_data(exercise_data, ['exercise_type_id', 'sets', 'reps'])
            
            # Verify exercise type exists
            exercise_type = ExerciseType.query.get_or_404(exercise_data['exercise_type_id'])
            
            workout_exercise = WorkoutExercise(
                workout_id=workout.id,
                exercise_type_id=exercise_data['exercise_type_id'],
                sets=exercise_data['sets'],
                reps=exercise_data['reps'],
                weight=exercise_data.get('weight'),
                notes=exercise_data.get('notes'),
                order=i
            )
            db.session.add(workout_exercise)
        
        db.session.commit()
        
        # Get exercises after commit to ensure they're loaded
        workout_exercises = (
            db.session.query(WorkoutExercise)
            .filter_by(workout_id=workout.id)
            .order_by('order')
            .all()
        )
        
        return jsonify({
            'id': workout.id,
            'name': workout.name,
            'training_plan_id': workout.training_plan_id,
            'planned_date': workout.planned_date.isoformat(),
            'status': workout.status,
            'exercises': [{
                'id': we.id,
                'exercise_type_id': we.exercise_type_id,
                'exercise_name': we.exercise_type.name,
                'sets': we.sets,
                'reps': we.reps,
                'weight': we.weight,
                'notes': we.notes,
                'order': we.order
            } for we in workout_exercises]
        }), HTTPStatus.CREATED
        
    except ValueError as e:
        abort(400, description=str(e))
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('/<int:workout_id>', methods=['PATCH'])
def update_workout(workout_id):
    """Update workout details and status.
    
    Required fields:
        - status: New workout status ('planned', 'completed', or 'skipped')
        
    Optional fields:
        - name: New workout name
        - planned_date: New planned date (YYYY-MM-DD)
        - exercises: List of exercises to update
        
    Args:
        workout_id: Workout ID
        
    Returns:
        Updated workout data
    """
    try:
        workout = Workout.query.get_or_404(workout_id)
        data = request.get_json()
        
        # Update basic workout details
        if 'status' in data:
            if data['status'] not in ['planned', 'completed', 'skipped']:
                abort(400, description="Invalid status. Must be one of: planned, completed, skipped")
            workout.status = data['status']
            
        if 'name' in data:
            workout.name = data['name']
            
        if 'planned_date' in data:
            workout.planned_date = validate_date_format(data['planned_date'])
        
        # Update exercises if provided
        if 'exercises' in data:
            if not isinstance(data['exercises'], list):
                abort(400, description="Exercises must be a list")
            
            # Remove existing exercises
            db.session.query(WorkoutExercise).filter_by(workout_id=workout_id).delete()
            
            # Add new exercises
            for i, exercise_data in enumerate(data['exercises']):
                validate_request_data(exercise_data, ['exercise_type_id', 'sets', 'reps'])
                
                # Verify exercise type exists
                exercise_type = ExerciseType.query.get_or_404(exercise_data['exercise_type_id'])
                
                workout_exercise = WorkoutExercise(
                    workout_id=workout.id,
                    exercise_type_id=exercise_data['exercise_type_id'],
                    sets=exercise_data['sets'],
                    reps=exercise_data['reps'],
                    weight=exercise_data.get('weight'),
                    notes=exercise_data.get('notes'),
                    order=i
                )
                db.session.add(workout_exercise)
        
        db.session.commit()
        
        # Get exercises after commit to ensure they're loaded
        workout_exercises = (
            db.session.query(WorkoutExercise)
            .filter_by(workout_id=workout.id)
            .order_by('order')
            .all()
        )
        
        return jsonify({
            'id': workout.id,
            'name': workout.name,
            'planned_date': workout.planned_date.isoformat(),
            'status': workout.status,
            'exercises': [{
                'id': we.id,
                'exercise_type_id': we.exercise_type_id,
                'exercise_name': we.exercise_type.name,
                'sets': we.sets,
                'reps': we.reps,
                'weight': we.weight,
                'notes': we.notes,
                'order': we.order
            } for we in workout_exercises]
        })
        
    except ValueError as e:
        abort(400, description=str(e))
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('/plan/<int:plan_id>', methods=['GET'])
def get_plan_workouts(plan_id):
    """Get all workouts for a training plan.
    
    Args:
        plan_id: Training plan ID
        
    Returns:
        List of workouts with their exercises
    """
    training_plan = TrainingPlan.query.get_or_404(plan_id)  # Verify plan exists
    workouts = db.session.query(Workout).filter_by(training_plan_id=plan_id).all()
    return jsonify([{
        'id': workout.id,
        'name': workout.name,
        'planned_date': workout.planned_date.isoformat(),
        'status': workout.status,
        'exercises': [{
            'id': we.id,
            'exercise_type_id': we.exercise_type_id,
            'exercise_name': we.exercise_type.name,
            'sets': we.sets,
            'reps': we.reps,
            'weight': we.weight,
            'notes': we.notes,
            'order': we.order
        } for we in db.session.query(WorkoutExercise)
                      .filter_by(workout_id=workout.id)
                      .order_by('order')
                      .all()]
    } for workout in workouts])

@bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout by ID.
    
    Args:
        workout_id: Workout ID
        
    Returns:
        204 No Content on success
    """
    workout = Workout.query.get_or_404(workout_id)
    
    try:
        db.session.delete(workout)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception:
        db.session.rollback()
        abort(500) 