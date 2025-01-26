"""
Database models for the Training System.

This module defines the SQLAlchemy models that represent the core entities in the training system.
The system is designed to help users track their training progress through a hierarchical structure:

Users create Training Plans, which are divided into Training Blocks (e.g., "Strength Phase", "Endurance Phase").
Each Training Block contains multiple Workouts. Workouts store their exercises and logs as JSON for maximum flexibility.

Model Hierarchy:
User
└── Training Plan
    └── Training Block
        └── Workout (includes exercises and logs as JSON)
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    # Create all database tables
    with app.app_context():
        db.create_all()

class User(db.Model):
    """
    Represents a user in the training system.
    
    Users are identified by their access key and can create multiple training plans.
    The system tracks when users were created, last updated, and their most recent access.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_access = db.Column(db.DateTime, nullable=True)
    
    training_plans = db.relationship('TrainingPlan', backref='user', lazy=True)
    
    def __init__(self, access_key, nickname):
        self.access_key = access_key
        self.nickname = nickname

class TrainingPlan(db.Model):
    """
    Represents a training plan created by a user.
    
    Training plans are the top-level container for organizing workouts. They:
    - Have a defined start and end date
    - Can specify a progression type (e.g., linear, undulating)
    - Can set target weekly training hours
    - Are divided into training blocks for different phases
    """
    __tablename__ = 'training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    progression_type = db.Column(db.String(50), nullable=True)
    target_weekly_hours = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    training_blocks = db.relationship('TrainingBlock', backref='training_plan', lazy=True, order_by='TrainingBlock.sequence_order')
    
    def __init__(self, user_id, name, progression_type=None, target_weekly_hours=None, start_date=None, end_date=None):
        self.user_id = user_id
        self.name = name
        self.progression_type = progression_type
        self.target_weekly_hours = target_weekly_hours
        self.start_date = start_date
        self.end_date = end_date

class TrainingBlock(db.Model):
    """
    Represents a specific phase or block within a training plan.
    
    Training blocks help organize workouts into focused periods, such as:
    - Strength blocks
    - Endurance blocks
    - Recovery blocks
    
    Each block has:
    - A primary training focus
    - A duration in weeks
    - An ordered sequence within the plan
    """
    __tablename__ = 'training_blocks'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('training_plans.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    primary_focus = db.Column(db.String(50), nullable=False)
    duration_weeks = db.Column(db.Integer, nullable=False)
    sequence_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    workouts = db.relationship('Workout', backref='training_block', lazy=True, order_by='Workout.sequence_order')
    
    def __init__(self, plan_id, name, primary_focus, duration_weeks, sequence_order):
        self.plan_id = plan_id
        self.name = name
        self.primary_focus = primary_focus
        self.duration_weeks = duration_weeks
        self.sequence_order = sequence_order

class ExerciseType(db.Model):
    """
    Defines a type of exercise that can be included in workouts.
    
    Exercise types are simple templates that define:
    - The name of the exercise
    - The category (e.g., Strength, Cardio, Flexibility)
    - A text description of how to perform the exercise
    
    Example:
    name: "Barbell Back Squat"
    category: "Strength"
    description: "A compound exercise targeting the legs and core. 
                 Stand with barbell across upper back, feet shoulder-width. 
                 Bend knees and hips to lower body, keeping chest up. 
                 Return to standing position."
    """
    __tablename__ = 'exercise_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, category, description=None):
        self.name = name
        self.category = category
        self.description = description

class Workout(db.Model):
    """
    Represents a planned workout session within a training block.
    
    Workouts track:
    - When they are planned vs actually performed
    - Their status (planned, completed, skipped)
    - Their sequence within the training block
    - The exercises to be performed and their parameters
    - The actual performance logs
    
    Example exercises JSON:
    {
        "exercises": [
            {
                "exercise_type_id": 1,
                "name": "Barbell Back Squat",
                "sequence": 1,
                "planned": {
                    "sets": 3,
                    "reps": "5-5-5",
                    "weight": "80kg",
                    "rest": "180s",
                    "notes": "Focus on depth"
                },
                "logs": [
                    {
                        "timestamp": "2024-01-21T14:30:00",
                        "sets": [
                            {"reps": 5, "weight": "82.5kg", "rpe": 8},
                            {"reps": 5, "weight": "82.5kg", "rpe": 8.5},
                            {"reps": 4, "weight": "82.5kg", "rpe": 9}
                        ],
                        "notes": "Last set was tough",
                        "perceived_effort": 8,
                        "completed": true
                    }
                ]
            }
        ]
    }
    """
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('training_blocks.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    planned_date = db.Column(db.Date, nullable=False)
    actual_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='planned')  # planned, completed, skipped
    sequence_order = db.Column(db.Integer, nullable=False)
    exercises = db.Column(db.JSON, nullable=False)  # Stores exercises, parameters, and logs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, block_id, name, planned_date, sequence_order, exercises=None, status='planned', actual_date=None):
        self.block_id = block_id
        self.name = name
        self.planned_date = planned_date
        self.actual_date = actual_date
        self.status = status
        self.sequence_order = sequence_order
        self.exercises = exercises or {"exercises": []} 