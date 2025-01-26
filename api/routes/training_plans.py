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

@bp.route('', methods=['GET'])
def get_training_plans():
    """Get all training plans for the current user.
    
    Returns:
        List of training plans
    """
    # TODO: Get current user from auth context
    user_id = 1  # Temporary until auth is implemented
    
    plans = TrainingPlan.query.filter_by(user_id=user_id).order_by(TrainingPlan.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'user_id': p.user_id,
        'progression_type': p.progression_type,
        'target_weekly_hours': p.target_weekly_hours,
        'start_date': p.start_date.isoformat() if p.start_date else None,
        'end_date': p.end_date.isoformat() if p.end_date else None,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat()
    } for p in plans])

@bp.route('', methods=['POST'])
def create_training_plan():
    """Create a new training plan.
    
    Required fields:
        - name: Plan name
        - progression_type: Type of progression (linear, undulating, etc.)
        - target_weekly_hours: Target training hours per week
        
    Optional fields:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        
    Returns:
        Training plan data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['name', 'progression_type', 'target_weekly_hours'])
        
        # Validate dates if provided
        start_date = None
        end_date = None
        if 'start_date' in data:
            start_date = validate_date_format(data['start_date'])
        if 'end_date' in data:
            end_date = validate_date_format(data['end_date'])
        if start_date and end_date:
            validate_date_range(start_date, end_date)
        
        # TODO: Get current user from auth context
        user_id = 1  # Temporary until auth is implemented
        
        plan = TrainingPlan(
            name=data['name'],
            user_id=user_id,
            progression_type=data['progression_type'],
            target_weekly_hours=data['target_weekly_hours'],
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(plan)
        db.session.commit()
        
        return jsonify({
            'id': plan.id,
            'name': plan.name,
            'user_id': plan.user_id,
            'progression_type': plan.progression_type,
            'target_weekly_hours': plan.target_weekly_hours,
            'start_date': plan.start_date.isoformat() if plan.start_date else None,
            'end_date': plan.end_date.isoformat() if plan.end_date else None,
            'created_at': plan.created_at.isoformat(),
            'updated_at': plan.updated_at.isoformat()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Training plan with this name already exists")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:plan_id>', methods=['GET'])
def get_training_plan(plan_id):
    """Get training plan by ID.
    
    Args:
        plan_id: Training plan ID
        
    Returns:
        Training plan data or 404 if not found
    """
    plan = TrainingPlan.query.get_or_404(plan_id)
    
    # TODO: Check if user has access to this plan
    
    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'user_id': plan.user_id,
        'progression_type': plan.progression_type,
        'target_weekly_hours': plan.target_weekly_hours,
        'start_date': plan.start_date.isoformat() if plan.start_date else None,
        'end_date': plan.end_date.isoformat() if plan.end_date else None,
        'created_at': plan.created_at.isoformat(),
        'updated_at': plan.updated_at.isoformat()
    })

@bp.route('/<int:plan_id>', methods=['PUT'])
def update_training_plan(plan_id):
    """Update training plan by ID.
    
    Args:
        plan_id: Training plan ID
        
    Optional fields:
        - name: Plan name
        - progression_type: Type of progression
        - target_weekly_hours: Target training hours per week
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        
    Returns:
        Updated training plan data
    """
    plan = TrainingPlan.query.get_or_404(plan_id)
    
    # TODO: Check if user has permission to update this plan
    
    try:
        data = request.get_json()
        
        if 'name' in data:
            plan.name = data['name']
        if 'progression_type' in data:
            plan.progression_type = data['progression_type']
        if 'target_weekly_hours' in data:
            plan.target_weekly_hours = data['target_weekly_hours']
        
        # Validate and update dates if provided
        if 'start_date' in data:
            plan.start_date = validate_date_format(data['start_date'])
        if 'end_date' in data:
            plan.end_date = validate_date_format(data['end_date'])
        if plan.start_date and plan.end_date:
            validate_date_range(plan.start_date, plan.end_date)
            
        db.session.commit()
        
        return jsonify({
            'id': plan.id,
            'name': plan.name,
            'user_id': plan.user_id,
            'progression_type': plan.progression_type,
            'target_weekly_hours': plan.target_weekly_hours,
            'start_date': plan.start_date.isoformat() if plan.start_date else None,
            'end_date': plan.end_date.isoformat() if plan.end_date else None,
            'created_at': plan.created_at.isoformat(),
            'updated_at': plan.updated_at.isoformat()
        })
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Training plan with this name already exists")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:plan_id>', methods=['DELETE'])
def delete_training_plan(plan_id):
    """Delete training plan by ID.
    
    Args:
        plan_id: Training plan ID
        
    Returns:
        204 No Content on success
    """
    plan = TrainingPlan.query.get_or_404(plan_id)
    
    # TODO: Check if user has permission to delete this plan
    
    try:
        db.session.delete(plan)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e)) 