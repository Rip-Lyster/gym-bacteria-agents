# API Structure

## Overview
The Gym Bacteria API is built using Flask and follows a modular architecture. The API is organized around core entities: Users, Training Plans, Training Blocks, Exercise Types, and Workouts.

## Directory Structure
```
api/
├── __init__.py           # Flask app initialization
├── core/
│   ├── __init__.py
│   └── models.py         # SQLAlchemy models
├── routes/
│   ├── __init__.py
│   ├── users.py
│   ├── training_plans.py
│   ├── training_blocks.py
│   ├── exercise_types.py
│   └── workouts.py
├── scripts/
│   ├── check_db.py
│   ├── config_env.py
│   └── populate_dev_db.py
└── static/
    └── swagger.json      # OpenAPI specification
```

## Core Entities

### User
- Represents a user in the system
- Identified by unique access_key
- Can have multiple training plans
- Properties: id, access_key, nickname, timestamps

### Training Plan
- Top-level container for organizing training
- Belongs to a user
- Contains multiple training blocks
- Properties: name, progression_type, target_weekly_hours, dates

### Training Block
- Represents a specific phase in a training plan
- Examples: Hypertrophy, Strength, Peak
- Contains multiple workouts
- Properties: name, primary_focus, duration_weeks, sequence_order

### Exercise Type
- Template for exercises
- Properties: name, category, description
- Used as reference in workout exercises

### Workout
- Individual training session
- Contains exercises and their parameters
- Stores both planned and actual performance
- Properties: name, dates, status, sequence_order
- Exercises stored as JSONB with detailed structure

## Data Flow

1. User Authentication
   ```
   Client -> access_key -> API -> User Lookup
   ```

2. Training Plan Creation
   ```
   User -> Training Plan -> Training Blocks -> Workouts
   ```

3. Workout Flow
   ```
   Plan Selection -> Block Selection -> Workout Creation -> Exercise Logging
   ```

## Exercise Data Structure

### Planned Exercise
```json
{
    "exercise_type_id": 1,
    "name": "Squat",
    "sequence": 1,
    "planned": {
        "sets": 4,
        "reps": "5-5-5",
        "rpe": 8,
        "rest_minutes": 3,
        "notes": "Focus on depth"
    }
}
```

### Exercise Log
```json
{
    "timestamp": "2024-01-25T14:30:00",
    "sets": [
        {
            "reps": 5,
            "weight": "100kg",
            "rpe": 8
        }
    ],
    "notes": "Felt strong today",
    "perceived_effort": 8,
    "completed": true
}
```

## Authentication
- Simple access key authentication
- Access key required for all user-specific operations
- No rate limiting currently implemented

## Database
- PostgreSQL via Vercel
- SQLAlchemy ORM
- JSONB for flexible exercise data
- Separate development and production databases

## Best Practices

### Route Organization
- Routes grouped by entity
- Consistent error handling
- Clear parameter validation
- Proper HTTP method usage

### Data Validation
- Required fields enforced
- Type checking
- Relationship integrity
- Sequence ordering

### Response Format
- Consistent JSON structure
- Clear error messages
- Appropriate status codes
- Standardized timestamps 