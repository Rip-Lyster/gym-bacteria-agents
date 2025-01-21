import os
import sys
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.models import User, TrainingPlan, Workout, ExerciseType, WorkoutExercise, db

# Load development environment
load_dotenv('.env.development.local')

def create_session():
    """Create a database session using the development database."""
    # Use non-pooling URL for scripts
    database_url = os.getenv('POSTGRES_URL_NON_POOLING')
    if not database_url:
        print("Error: POSTGRES_URL_NON_POOLING not set in .env.development.local")
        print("Get this from Vercel Dashboard -> Storage -> Postgres -> .env.local tab")
        sys.exit(1)
    
    # Convert postgres:// to postgresql:// if needed
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()

def create_sample_users(session):
    """Create sample users."""
    users = [
        User(access_key='dev_user_1', nickname='John Doe'),
        User(access_key='dev_user_2', nickname='Jane Smith'),
        User(access_key='dev_user_3', nickname='Bob Johnson')
    ]
    
    for user in users:
        try:
            session.add(user)
            print(f"Created user: {user.nickname}")
        except Exception as e:
            print(f"Error creating user {user.nickname}: {str(e)}")
            session.rollback()
    
    session.commit()
    return users

def create_exercise_types(session):
    """Create sample exercise types."""
    exercise_types = [
        ExerciseType(
            name='Bench Press',
            category='Strength',
            parameters={'sets': 3, 'reps': '8-12', 'rest': '90s'}
        ),
        ExerciseType(
            name='Squats',
            category='Strength',
            parameters={'sets': 4, 'reps': '6-8', 'rest': '120s'}
        ),
        ExerciseType(
            name='Pull-ups',
            category='Bodyweight',
            parameters={'sets': 3, 'reps': 'max', 'rest': '60s'}
        ),
        ExerciseType(
            name='Running',
            category='Cardio',
            parameters={'duration': '30min', 'intensity': 'moderate'}
        )
    ]
    
    for ex_type in exercise_types:
        try:
            session.add(ex_type)
            print(f"Created exercise type: {ex_type.name}")
        except Exception as e:
            print(f"Error creating exercise type {ex_type.name}: {str(e)}")
            session.rollback()
    
    session.commit()
    return exercise_types

def create_training_plans(session, users):
    """Create sample training plans for users."""
    plans = []
    for user in users:
        start_date = datetime.now().date()
        plan = TrainingPlan(
            user_id=user.id,
            name=f"{user.nickname}'s Training Plan",
            start_date=start_date,
            end_date=start_date + timedelta(weeks=12)
        )
        try:
            session.add(plan)
            plans.append(plan)
            print(f"Created training plan for: {user.nickname}")
        except Exception as e:
            print(f"Error creating plan for {user.nickname}: {str(e)}")
            session.rollback()
    
    session.commit()
    return plans

def create_workouts(session, plans, exercise_types):
    """Create sample workouts for training plans."""
    workout_templates = {
        'Push Day': [
            {'name': 'Bench Press', 'sets': 4, 'reps': 8, 'weight': 60},
            {'name': 'Pull-ups', 'sets': 3, 'reps': 12, 'notes': 'Focus on form'},
        ],
        'Pull Day': [
            {'name': 'Pull-ups', 'sets': 4, 'reps': 8, 'notes': 'Wide grip'},
            {'name': 'Bench Press', 'sets': 3, 'reps': 12, 'weight': 50},
        ],
        'Leg Day': [
            {'name': 'Squats', 'sets': 5, 'reps': 5, 'weight': 80},
            {'name': 'Running', 'sets': 1, 'reps': 1, 'notes': '10 min cooldown'},
        ],
        'Cardio': [
            {'name': 'Running', 'sets': 1, 'reps': 1, 'notes': '30 min steady state'},
        ],
        'Full Body': [
            {'name': 'Squats', 'sets': 3, 'reps': 10, 'weight': 60},
            {'name': 'Bench Press', 'sets': 3, 'reps': 10, 'weight': 45},
            {'name': 'Pull-ups', 'sets': 3, 'reps': 8},
        ],
    }
    
    # Create a lookup for exercise types by name
    exercise_lookup = {ex.name: ex for ex in exercise_types}
    
    for plan in plans:
        # Create 3 workouts per plan
        for i in range(3):
            workout_date = plan.start_date + timedelta(days=i*2)
            workout_name = random.choice(list(workout_templates.keys()))
            workout = Workout(
                training_plan_id=plan.id,
                name=workout_name,
                planned_date=workout_date,
                status=random.choice(['planned', 'completed', 'skipped'])
            )
            try:
                session.add(workout)
                session.flush()  # Get the workout ID
                
                # Add exercises from the template
                for order, exercise in enumerate(workout_templates[workout_name]):
                    exercise_type = exercise_lookup[exercise['name']]
                    workout_exercise = WorkoutExercise(
                        workout_id=workout.id,
                        exercise_type_id=exercise_type.id,
                        sets=exercise['sets'],
                        reps=exercise['reps'],
                        weight=exercise.get('weight'),
                        notes=exercise.get('notes'),
                        order=order
                    )
                    session.add(workout_exercise)
                
                print(f"Created workout: {workout.name} for plan {plan.id}")
            except Exception as e:
                print(f"Error creating workout: {str(e)}")
                session.rollback()
    
    session.commit()

def main():
    """Main function to populate the development database."""
    print("Starting development database population...")
    session = create_session()
    
    try:
        # Create sample data in order
        users = create_sample_users(session)
        exercise_types = create_exercise_types(session)
        plans = create_training_plans(session, users)
        create_workouts(session, plans, exercise_types)
        
        print("\nDatabase population completed successfully!")
        
    except Exception as e:
        print(f"Error populating database: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main() 