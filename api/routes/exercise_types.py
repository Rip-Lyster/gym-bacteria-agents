from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, ExerciseType
from ..core.validation import validate_request_data
from sqlalchemy.exc import IntegrityError

bp = Blueprint('exercise_types', __name__, url_prefix='/api/exercise-types')

@bp.route('', methods=['POST'])
def create_exercise_type():
    """Create a new exercise type.
    
    Required fields:
        - name: Name of the exercise type
        - category: Exercise category
        
    Optional fields:
        - parameters: JSON object with exercise parameters
        
    Returns:
        Exercise type data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['name', 'category'])
        
        exercise_type = ExerciseType(
            name=data['name'],
            category=data['category'],
            parameters=data.get('parameters')
        )
        db.session.add(exercise_type)
        db.session.commit()
        
        return jsonify({
            'id': exercise_type.id,
            'name': exercise_type.name,
            'category': exercise_type.category,
            'parameters': exercise_type.parameters
        }), HTTPStatus.CREATED
        
    except ValueError as e:
        abort(400, description=str(e))
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Exercise type with this name already exists")
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('', methods=['GET'])
def get_exercise_types():
    """Get all exercise types.
    
    Returns:
        List of all exercise types
    """
    exercise_types = ExerciseType.query.all()
    return jsonify([{
        'id': et.id,
        'name': et.name,
        'category': et.category,
        'parameters': et.parameters
    } for et in exercise_types])

@bp.route('/<int:type_id>', methods=['DELETE'])
def delete_exercise_type(type_id):
    """Delete an exercise type by ID.
    
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
    except Exception:
        db.session.rollback()
        abort(500) 