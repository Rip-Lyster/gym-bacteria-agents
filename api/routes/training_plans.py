from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, TrainingPlan
from ..core.validation import validate_request_data, validate_date_format, validate_date_range
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import Dict, Any

def validate_request_data(data: Dict[str, Any], required_fields: list) -> None:
    """Validate that all required fields are present in the request data."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

bp = Blueprint('training_plans', __name__, url_prefix='/api/training-plans')

@bp.route('', methods=['POST'])
def create_training_plan():
    """Create a new training plan.
    
    Required fields:
        - user_id: ID of the user creating the plan
        - name: Name of the training plan
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        
    Returns:
        Training plan data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['user_id', 'name', 'start_date', 'end_date'])
        
        # Validate dates
        start_date = validate_date_format(data['start_date'])
        end_date = validate_date_format(data['end_date'])
        validate_date_range(start_date, end_date)
        
        plan = TrainingPlan(
            user_id=data['user_id'],
            name=data['name'],
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(plan)
        db.session.commit()
        
        return jsonify({
            'id': plan.id,
            'name': plan.name,
            'user_id': plan.user_id,
            'start_date': plan.start_date.isoformat(),
            'end_date': plan.end_date.isoformat()
        }), HTTPStatus.CREATED
        
    except ValueError as e:
        abort(400, description=str(e))
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('/<int:plan_id>', methods=['GET'])
def get_training_plan(plan_id):
    """Get training plan by ID.
    
    Args:
        plan_id: Training plan ID
        
    Returns:
        Training plan data or 404 if not found
    """
    plan = TrainingPlan.query.get_or_404(plan_id)
    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'user_id': plan.user_id,
        'start_date': plan.start_date.isoformat(),
        'end_date': plan.end_date.isoformat()
    })

@bp.route('/<int:plan_id>', methods=['DELETE'])
def delete_training_plan(plan_id):
    """Delete a training plan by ID.
    
    Args:
        plan_id: Training plan ID
        
    Returns:
        204 No Content on success
    """
    plan = TrainingPlan.query.get_or_404(plan_id)
    
    try:
        db.session.delete(plan)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception:
        db.session.rollback()
        abort(500)

@bp.route('/<int:plan_id>', methods=['PATCH'])
def update_training_plan(plan_id):
    """Update a training plan by ID.
    
    Required fields in request body:
        - name: Name of the training plan
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        
    Args:
        plan_id: Training plan ID
        
    Returns:
        Updated training plan data
    """
    try:
        plan = TrainingPlan.query.get_or_404(plan_id)
        data = request.get_json()
        validate_request_data(data, ['name', 'start_date', 'end_date'])
        
        # Validate dates
        start_date = validate_date_format(data['start_date'])
        end_date = validate_date_format(data['end_date'])
        validate_date_range(start_date, end_date)
        
        plan.name = data['name']
        plan.start_date = start_date
        plan.end_date = end_date
        
        db.session.commit()
        
        return jsonify({
            'id': plan.id,
            'name': plan.name,
            'user_id': plan.user_id,
            'start_date': plan.start_date.isoformat(),
            'end_date': plan.end_date.isoformat()
        })
        
    except ValueError as e:
        abort(400, description=str(e))
    except Exception:
        db.session.rollback()
        abort(500) 