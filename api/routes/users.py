from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, User, TrainingPlan
from ..core.validation import validate_request_data
from sqlalchemy.exc import IntegrityError
from typing import Dict, Any

def validate_request_data(data: Dict[str, Any], required_fields: list) -> None:
    """Validate that all required fields are present in the request data.
    
    Args:
        data: Request data dictionary
        required_fields: List of required field names
        
    Raises:
        ValueError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('', methods=['POST'])
def create_user():
    """Create a new user.
    
    Required fields:
        - access_key: Unique identifier for the user
        - nickname: User's display name
        
    Returns:
        User data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['access_key', 'nickname'])
        
        user = User(
            access_key=data['access_key'],
            nickname=data['nickname']
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'id': user.id,
            'nickname': user.nickname,
            'access_key': user.access_key
        }), HTTPStatus.CREATED
        
    except ValueError as e:
        abort(400, description=str(e))
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Access key already exists")
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('/<access_key>', methods=['GET'])
def get_user(access_key):
    """Get user by access key.
    
    Args:
        access_key: User's unique access key
        
    Returns:
        User data or 404 if not found
    """
    user = User.query.filter_by(access_key=access_key).first()
    if not user:
        abort(404)
        
    return jsonify({
        'id': user.id,
        'nickname': user.nickname,
        'access_key': user.access_key
    })

@bp.route('/<int:user_id>/training-plans', methods=['GET'])
def get_user_training_plans(user_id):
    """Get all training plans for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        List of training plans
    """
    User.query.get_or_404(user_id)  # Verify user exists
    plans = TrainingPlan.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': plan.id,
        'name': plan.name,
        'start_date': plan.start_date.isoformat(),
        'end_date': plan.end_date.isoformat()
    } for plan in plans])

@bp.route('/<access_key>', methods=['DELETE'])
def delete_user(access_key):
    """Delete a user by access key.
    
    Args:
        access_key: User's unique access key
        
    Returns:
        204 No Content on success
    """
    user = User.query.filter_by(access_key=access_key).first()
    if not user:
        abort(404)
        
    try:
        db.session.delete(user)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception:
        db.session.rollback()
        abort(500) 