from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, Workout, TrainingBlock
from ..core.validation import validate_request_data, validate_date_format
from sqlalchemy.exc import IntegrityError
from typing import List

bp = Blueprint('workouts', __name__, url_prefix='/api/workouts')

@bp.route('', methods=['GET'])
def get_workouts():
    """Get all workouts for a training block.
    
    Query parameters:
        - block_id: Training block ID (required)
        
    Returns:
        List of workouts in sequence order
    """
    block_id = request.args.get('block_id', type=int)
    if not block_id:
        abort(400, description="block_id query parameter is required")
        
    block = TrainingBlock.query.get_or_404(block_id)
    workouts = db.session.execute(
        db.select(Workout)
        .filter_by(block_id=block_id)
        .order_by(db.text('sequence_order'))
    ).scalars().all()
    
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'block_id': w.block_id,
        'sequence_order': w.sequence_order,
        'status': w.status,
        'planned_date': w.planned_date.isoformat() if w.planned_date else None,
        'actual_date': w.actual_date.isoformat() if w.actual_date else None,
        'exercises': w.exercises,
        'created_at': w.created_at.isoformat(),
        'updated_at': w.updated_at.isoformat()
    } for w in workouts])

@bp.route('', methods=['POST'])
def create_workout():
    """Create a new workout.
    
    Required fields:
        - name: Workout name
        - block_id: Training block ID
        - sequence_order: Order within the block
        - exercises: List of exercise objects with:
            - exercise_type_id: Exercise type ID
            - planned: Object with planned parameters
              (sets, reps, weight, etc. based on exercise type)
    
    Optional fields:
        - planned_date: ISO format date string
        - status: Workout status (default: 'pending')
        
    Returns:
        Workout data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['name', 'block_id', 'sequence_order', 'exercises'])
        
        block = TrainingBlock.query.get_or_404(data['block_id'])
        
        workout = Workout(
            name=data['name'],
            block_id=data['block_id'],
            sequence_order=data['sequence_order'],
            exercises=data['exercises'],
            planned_date=data.get('planned_date'),
            status=data.get('status', 'pending')
        )
        
        db.session.add(workout)
        db.session.commit()
        
        return jsonify({
            'id': workout.id,
            'name': workout.name,
            'block_id': workout.block_id,
            'sequence_order': workout.sequence_order,
            'status': workout.status,
            'planned_date': workout.planned_date.isoformat() if workout.planned_date else None,
            'actual_date': workout.actual_date.isoformat() if workout.actual_date else None,
            'exercises': workout.exercises,
            'created_at': workout.created_at.isoformat(),
            'updated_at': workout.updated_at.isoformat()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Workout with this sequence order already exists in block")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Get workout by ID.
    
    Args:
        workout_id: Workout ID
        
    Returns:
        Workout data or 404 if not found
    """
    workout = Workout.query.get_or_404(workout_id)
    
    return jsonify({
        'id': workout.id,
        'name': workout.name,
        'block_id': workout.block_id,
        'sequence_order': workout.sequence_order,
        'status': workout.status,
        'planned_date': workout.planned_date.isoformat() if workout.planned_date else None,
        'actual_date': workout.actual_date.isoformat() if workout.actual_date else None,
        'exercises': workout.exercises,
        'created_at': workout.created_at.isoformat(),
        'updated_at': workout.updated_at.isoformat()
    })

@bp.route('/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    """Update workout by ID.
    
    Args:
        workout_id: Workout ID
        
    Optional fields:
        - name: Workout name
        - sequence_order: Order within the block
        - planned_date: ISO format date string
        - actual_date: ISO format date string
        - status: Workout status
        - exercises: List of exercise objects with:
            - exercise_type_id: Exercise type ID
            - planned: Object with planned parameters
            - actual: Object with actual performance data (optional)
            
    Returns:
        Updated workout data
    """
    workout = Workout.query.get_or_404(workout_id)
    
    try:
        data = request.get_json()
        
        if 'name' in data:
            workout.name = data['name']
        if 'sequence_order' in data:
            workout.sequence_order = data['sequence_order']
        if 'planned_date' in data:
            workout.planned_date = data['planned_date']
        if 'actual_date' in data:
            workout.actual_date = data['actual_date']
        if 'status' in data:
            workout.status = data['status']
        if 'exercises' in data:
            workout.exercises = data['exercises']
            
        db.session.commit()
        
        return jsonify({
            'id': workout.id,
            'name': workout.name,
            'block_id': workout.block_id,
            'sequence_order': workout.sequence_order,
            'status': workout.status,
            'planned_date': workout.planned_date.isoformat() if workout.planned_date else None,
            'actual_date': workout.actual_date.isoformat() if workout.actual_date else None,
            'exercises': workout.exercises,
            'created_at': workout.created_at.isoformat(),
            'updated_at': workout.updated_at.isoformat()
        })
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Workout with this sequence order already exists in block")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete workout by ID.
    
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
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/block/<int:block_id>', methods=['GET'])
def get_block_workouts(block_id):
    """Get all workouts for a training block.
    
    Args:
        block_id: Training block ID
        
    Returns:
        List of workout data
    """
    # Verify block exists
    block = TrainingBlock.query.get_or_404(block_id)
    
    workouts = db.session.execute(
        db.select(Workout)
        .filter_by(block_id=block_id)
        .order_by(db.text('sequence_order'))
    ).scalars().all()
    
    return jsonify([{
        'id': workout.id,
        'block_id': workout.block_id,
        'name': workout.name,
        'planned_date': workout.planned_date.isoformat(),
        'actual_date': workout.actual_date.isoformat() if workout.actual_date else None,
        'status': workout.status,
        'sequence_order': workout.sequence_order,
        'exercises': workout.exercises,
        'created_at': workout.created_at.isoformat(),
        'updated_at': workout.updated_at.isoformat()
    } for workout in workouts]) 