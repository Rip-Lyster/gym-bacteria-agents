from flask import Blueprint, jsonify, request, abort
from http import HTTPStatus
from ..core.models import db, TrainingBlock, TrainingPlan
from ..core.validation import validate_request_data
from sqlalchemy.exc import IntegrityError

bp = Blueprint('training_blocks', __name__, url_prefix='/api/training-blocks')

@bp.route('', methods=['GET'])
def get_training_blocks():
    """Get all training blocks for a training plan.
    
    Query parameters:
        - plan_id: Training plan ID (required)
        
    Returns:
        List of training blocks in sequence order
    """
    plan_id = request.args.get('plan_id', type=int)
    if not plan_id:
        abort(400, description="plan_id query parameter is required")
        
    plan = TrainingPlan.query.get_or_404(plan_id)
    blocks = db.session.execute(
        db.select(TrainingBlock)
        .filter_by(plan_id=plan_id)
        .order_by(db.text('sequence_order'))
    ).scalars().all()
    
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'plan_id': b.plan_id,
        'primary_focus': b.primary_focus,
        'duration_weeks': b.duration_weeks,
        'sequence_order': b.sequence_order,
        'created_at': b.created_at.isoformat(),
        'updated_at': b.updated_at.isoformat()
    } for b in blocks])

@bp.route('', methods=['POST'])
def create_training_block():
    """Create a new training block.
    
    Required fields:
        - name: Block name
        - plan_id: Training plan ID
        - primary_focus: Primary training focus
        - duration_weeks: Duration in weeks
        - sequence_order: Order within the plan
        
    Returns:
        Training block data and 201 status code on success
    """
    try:
        data = request.get_json()
        validate_request_data(data, ['name', 'plan_id', 'primary_focus', 'duration_weeks', 'sequence_order'])
        
        plan = TrainingPlan.query.get_or_404(data['plan_id'])
        
        block = TrainingBlock(
            name=data['name'],
            plan_id=data['plan_id'],
            primary_focus=data['primary_focus'],
            duration_weeks=data['duration_weeks'],
            sequence_order=data['sequence_order']
        )
        
        db.session.add(block)
        db.session.commit()
        
        return jsonify({
            'id': block.id,
            'name': block.name,
            'plan_id': block.plan_id,
            'primary_focus': block.primary_focus,
            'duration_weeks': block.duration_weeks,
            'sequence_order': block.sequence_order,
            'created_at': block.created_at.isoformat(),
            'updated_at': block.updated_at.isoformat()
        }), HTTPStatus.CREATED
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Training block with this sequence order already exists in plan")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:block_id>', methods=['GET'])
def get_training_block(block_id):
    """Get training block by ID.
    
    Args:
        block_id: Training block ID
        
    Returns:
        Training block data or 404 if not found
    """
    block = TrainingBlock.query.get_or_404(block_id)
    
    return jsonify({
        'id': block.id,
        'name': block.name,
        'plan_id': block.plan_id,
        'primary_focus': block.primary_focus,
        'duration_weeks': block.duration_weeks,
        'sequence_order': block.sequence_order,
        'created_at': block.created_at.isoformat(),
        'updated_at': block.updated_at.isoformat()
    })

@bp.route('/<int:block_id>', methods=['PUT'])
def update_training_block(block_id):
    """Update training block by ID.
    
    Args:
        block_id: Training block ID
        
    Optional fields:
        - name: Block name
        - primary_focus: Primary training focus
        - duration_weeks: Duration in weeks
        - sequence_order: Order within the plan
        
    Returns:
        Updated training block data
    """
    block = TrainingBlock.query.get_or_404(block_id)
    
    try:
        data = request.get_json()
        
        if 'name' in data:
            block.name = data['name']
        if 'primary_focus' in data:
            block.primary_focus = data['primary_focus']
        if 'duration_weeks' in data:
            block.duration_weeks = data['duration_weeks']
        if 'sequence_order' in data:
            block.sequence_order = data['sequence_order']
            
        db.session.commit()
        
        return jsonify({
            'id': block.id,
            'name': block.name,
            'plan_id': block.plan_id,
            'primary_focus': block.primary_focus,
            'duration_weeks': block.duration_weeks,
            'sequence_order': block.sequence_order,
            'created_at': block.created_at.isoformat(),
            'updated_at': block.updated_at.isoformat()
        })
        
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Training block with this sequence order already exists in plan")
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))

@bp.route('/<int:block_id>', methods=['DELETE'])
def delete_training_block(block_id):
    """Delete training block by ID.
    
    Args:
        block_id: Training block ID
        
    Returns:
        204 No Content on success
    """
    block = TrainingBlock.query.get_or_404(block_id)
    
    try:
        db.session.delete(block)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e)) 