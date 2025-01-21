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
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    access_key = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    training_plans = db.relationship('TrainingPlan', backref='user', lazy=True)
    
    def __init__(self, access_key, nickname):
        self.access_key = access_key
        self.nickname = nickname

class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workouts = db.relationship('Workout', backref='training_plan', lazy=True)
    
    def __init__(self, user_id, name, start_date, end_date):
        self.user_id = user_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

class ExerciseType(db.Model):
    __tablename__ = 'exercise_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise_type', lazy=True)
    
    def __init__(self, name, category, parameters=None):
        self.name = name
        self.category = category
        self.parameters = parameters

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    training_plan_id = db.Column(db.Integer, db.ForeignKey('training_plans.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    planned_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='planned')  # planned, completed, skipped
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', lazy=True, order_by='WorkoutExercise.order')
    
    def __init__(self, training_plan_id, name, planned_date, status='planned'):
        self.training_plan_id = training_plan_id
        self.name = name
        self.planned_date = planned_date
        self.status = status

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_types.id', ondelete='CASCADE'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise_type = db.relationship('ExerciseType', back_populates='workout_exercises')
    
    def __init__(self, workout_id, exercise_type_id, sets, reps, order, weight=None, notes=None):
        self.workout_id = workout_id
        self.exercise_type_id = exercise_type_id
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.notes = notes
        self.order = order 