from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, ExerciseType
from ..core.validation import validate_request_data
from sqlalchemy.exc import IntegrityError

bp = Blueprint('exercise_types', __name__, url_prefix='/api/exercise-types')

@bp.route('', methods=['GET'])
def get_exercise_types():
    """Get all exercise types.
    
    Returns:
        List of exercise types
    """
    exercise_types = db.session.execute(
        db.select(ExerciseType)
        .order_by(db.text('name'))
    ).scalars().all()
    return jsonify([{
        'id': ex.id,
        'name': ex.name,
        'category': ex.category,
        'description': ex.description,
        'created_at': ex.created_at.isoformat(),
        'updated_at': ex.updated_at.isoformat()
    } for ex in exercise_types])

@bp.route('', methods=['POST'])
def create_exercise_type():
    """Create a new exercise type.
    
    Required fields:
        - name: Exercise name
        - category: Exercise category (e.g., Strength, Cardio)
    
    Optional fields:
        - description: Detailed description of the exercise
        
    Returns:
        Exercise type data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['name', 'category'])
        
        exercise_type = ExerciseType(
            name=data['name'],
            category=data['category'],
            description=data.get('description')
        )
        
        db.session.add(exercise_type)
        db.session.commit()
        
        return jsonify({
            'id': exercise_type.id,
            'name': exercise_type.name,
            'category': exercise_type.category,
            'description': exercise_type.description,
            'created_at': exercise_type.created_at.isoformat(),
            'updated_at': exercise_type.updated_at.isoformat()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Exercise type already exists")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:type_id>', methods=['GET'])
def get_exercise_type(type_id):
    """Get exercise type by ID.
    
    Args:
        type_id: Exercise type ID
        
    Returns:
        Exercise type data or 404 if not found
    """
    exercise_type = ExerciseType.query.get_or_404(type_id)
    
    return jsonify({
        'id': exercise_type.id,
        'name': exercise_type.name,
        'category': exercise_type.category,
        'description': exercise_type.description,
        'created_at': exercise_type.created_at.isoformat(),
        'updated_at': exercise_type.updated_at.isoformat()
    })

@bp.route('/<int:type_id>', methods=['DELETE'])
def delete_exercise_type(type_id):
    """Delete exercise type by ID.
    
    Args:
        type_id: Exercise type ID
        
    Returns:
        204 No Content on success
    """
    exercise_type = ExerciseType.query.get_or_404(type_id)
    
    try:
        db.session.delete(exercise_type)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e)) 