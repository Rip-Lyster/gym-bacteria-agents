"""Routes package for the API.

This package contains all the route blueprints for the API.
Each blueprint is responsible for a specific resource or group of related resources.
"""

from . import users, training_plans, exercise_types, workouts

__all__ = ['users', 'training_plans', 'exercise_types', 'workouts'] 