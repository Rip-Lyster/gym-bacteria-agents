import os
import sys
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.models import User, TrainingPlan, TrainingBlock, Workout, ExerciseType, db

# Load development environment
load_dotenv('api/.env.development.local')

def create_session():
    """Create a database session using the development database."""
    # Use non-pooling URL for scripts
    database_url = os.getenv('DATABASE_URL_UNPOOLED')
    if not database_url:
        print("Error: DATABASE_URL_UNPOOLED not set in .env.development.local")
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
    """Create sample exercise types with descriptive text."""
    exercise_types = [
        ExerciseType(
            name='Squat',
            category='Strength',
            description="""
            A compound lower body exercise that targets the quadriceps, hamstrings, and glutes.
            
            Form cues:
            - Keep chest up and core braced
            - Push knees out in line with toes
            - Break at hips and knees simultaneously
            - Maintain neutral spine throughout
            - Drive through full foot, emphasizing heel
            
            Common variations:
            - Back squat (high/low bar)
            - Front squat
            - Box squat
            - Pause squat
            """
        ),
        ExerciseType(
            name='Bench Press',
            category='Strength',
            description="""
            A compound upper body push exercise targeting the chest, shoulders, and triceps.
            
            Form cues:
            - Set up with shoulders retracted and feet planted
            - Grip width typically 1.5-2x shoulder width
            - Lower bar with control to mid-chest
            - Tuck elbows ~45 degrees
            - Drive bar up and slightly back toward face
            
            Common variations:
            - Flat/Incline/Decline
            - Dumbbell/Barbell
            - Close grip
            - Pause press
            """
        ),
        ExerciseType(
            name='Deadlift',
            category='Strength',
            description="""
            A compound full body exercise emphasizing posterior chain development.
            
            Form cues:
            - Bar over mid-foot
            - Shoulders slightly in front of bar
            - Hips high, shoulders low
            - Brace core and pull slack out of bar
            - Drive through floor while maintaining bar contact
            
            Common variations:
            - Conventional
            - Sumo
            - Romanian
            - Deficit
            """
        ),
        ExerciseType(
            name='Running',
            category='Cardio',
            description="""
            Fundamental cardio exercise for building endurance and cardiovascular health.
            
            Key points:
            - Start with walk/run intervals for beginners
            - Gradually increase duration before intensity
            - Land mid-foot with feet under hips
            - Maintain relaxed upper body
            - Breathe rhythmically
            
            Types:
            - Easy/recovery runs
            - Tempo runs
            - Interval training
            - Long slow distance
            """
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
    """Create sample training plans with blocks."""
    plans = []
    current_date = datetime.now().date()
    
    for user in users:
        plan = TrainingPlan(
            user_id=user.id,
            name=f"{user.nickname}'s Training Plan",
            progression_type='linear',
            target_weekly_hours=6,
            start_date=current_date,
            end_date=current_date + timedelta(weeks=12)  # 12 weeks total duration
        )
        try:
            session.add(plan)
            session.flush()  # Get the plan ID
            
            # Create training blocks for the plan
            blocks = [
                TrainingBlock(
                    plan_id=plan.id,
                    name='Hypertrophy Block',
                    primary_focus='Build muscle mass and work capacity',
                    duration_weeks=4,
                    sequence_order=1
                ),
                TrainingBlock(
                    plan_id=plan.id,
                    name='Strength Block',
                    primary_focus='Increase maximal strength',
                    duration_weeks=6,
                    sequence_order=2
                ),
                TrainingBlock(
                    plan_id=plan.id,
                    name='Peak Block',
                    primary_focus='Peak strength and test maxes',
                    duration_weeks=2,
                    sequence_order=3
                )
            ]
            
            for block in blocks:
                session.add(block)
                print(f"Created training block: {block.name} for plan {plan.id}")
            
            plans.append(plan)
            print(f"Created training plan for: {user.nickname}")
            current_date += timedelta(days=7)  # Stagger plan start dates
        except Exception as e:
            print(f"Error creating plan for {user.nickname}: {str(e)}")
            session.rollback()
    
    session.commit()
    return plans

def create_workouts(session, plans, exercise_types):
    """Create sample workouts with exercises stored as JSON."""
    workout_templates = {
        'Hypertrophy Block': {
            'exercises': [
                {
                    'exercise_type_id': 1,  # Squat
                    'name': 'Squat',
                    'sequence': 1,
                    'planned': {
                        'sets': 4,
                        'reps': 10,
                        'rpe': 7,
                        'rest_minutes': 2
                    }
                },
                {
                    'exercise_type_id': 2,  # Bench Press
                    'name': 'Bench Press',
                    'sequence': 2,
                    'planned': {
                        'sets': 5,
                        'reps': 8,
                        'rpe': 7,
                        'rest_minutes': 2
                    }
                }
            ]
        },
        'Strength Block': {
            'exercises': [
                {
                    'exercise_type_id': 1,  # Squat
                    'name': 'Squat',
                    'sequence': 1,
                    'planned': {
                        'sets': 5,
                        'reps': 5,
                        'rpe': 8,
                        'rest_minutes': 3
                    }
                },
                {
                    'exercise_type_id': 3,  # Deadlift
                    'name': 'Deadlift',
                    'sequence': 2,
                    'planned': {
                        'sets': 5,
                        'reps': 5,
                        'rpe': 8,
                        'rest_minutes': 3
                    }
                }
            ]
        },
        'Peak Block': {
            'exercises': [
                {
                    'exercise_type_id': 2,  # Bench Press
                    'name': 'Bench Press',
                    'sequence': 1,
                    'planned': {
                        'sets': 1,
                        'reps': 1,
                        'rpe': 10,
                        'rest_minutes': 5
                    }
                },
                {
                    'exercise_type_id': 3,  # Deadlift
                    'name': 'Deadlift',
                    'sequence': 2,
                    'planned': {
                        'sets': 1,
                        'reps': 1,
                        'rpe': 10,
                        'rest_minutes': 5
                    }
                }
            ]
        }
    }
    
    # Get all training blocks
    blocks = []
    for plan in plans:
        blocks.extend(session.query(TrainingBlock).filter_by(plan_id=plan.id).all())
    
    current_date = datetime.now()
    for block in blocks:
        # Create 2 workouts per block
        for i in range(2):
            workout_date = current_date + timedelta(days=i*2)
            
            # Use the block's name to get the template
            template = workout_templates[block.name]
            
            workout = Workout(
                block_id=block.id,
                name=f"{block.name} Workout {i+1}",
                planned_date=workout_date,
                sequence_order=i+1,
                exercises=template,
                status=random.choice(['planned', 'completed', 'skipped'])
            )
            
            try:
                session.add(workout)
                print(f"Created workout: {workout.name} for block {block.id}")
            except Exception as e:
                print(f"Error creating workout: {str(e)}")
                session.rollback()
        
        current_date += timedelta(weeks=block.duration_weeks)
    
    session.commit()

def clear_existing_data(session):
    """Clear all existing data from the database."""
    try:
        session.execute(text('TRUNCATE TABLE workouts CASCADE'))
        session.execute(text('TRUNCATE TABLE training_blocks CASCADE'))
        session.execute(text('TRUNCATE TABLE training_plans CASCADE'))
        session.execute(text('TRUNCATE TABLE exercise_types CASCADE'))
        session.execute(text('TRUNCATE TABLE users CASCADE'))
        session.commit()
        print("Cleared existing data")
    except Exception as e:
        print(f"Error clearing data: {str(e)}")
        session.rollback()

def main():
    """Main function to populate the development database."""
    print("Starting development database population...")
    session = create_session()
    
    try:
        # Clear existing data first
        clear_existing_data(session)
        
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