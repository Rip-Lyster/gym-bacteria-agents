# Development Database Setup

## Overview
This document outlines how to set up and manage the development database environment for the Gym Bacteria project. We use Vercel Postgres for both development and production, with separate environments to keep data isolated.

## Development vs Production Data
The development and production environments use different connection URLs that point to separate database instances, ensuring complete data isolation:

- Development uses: `POSTGRES_URL_NON_POOLING` from `.env.development.local`
- Production uses: `POSTGRES_URL` from `.env.production.local`

This means:
- Data you add in development (like sample users) won't appear in production
- You can freely experiment with data in development without affecting production
- Each environment maintains its own separate state

### Data Isolation Example
```python
# Development data (only exists in development database)
dev_users = [
    User(access_key='dev_user_1', nickname='John Doe'),
    User(access_key='dev_user_2', nickname='Jane Smith')
]

# Production data (only exists in production database)
prod_users = [
    User(access_key='real_user_123', nickname='Real Customer')
]
```

## Environment Setup

### 1. Environment Files
The project uses three environment files:
- `.env.development.local` - Development environment variables
- `.env.production.local` - Production environment variables
- `.env` - Active environment (copy of either development or production)

To set up your environment:
```bash
python api/scripts/config_env.py
```

This script will create the necessary environment files if they don't exist.

### 2. Database Credentials
Get your development database credentials from Vercel:
1. Go to Vercel Dashboard
2. Select your project
3. Navigate to Storage -> Postgres
4. Click the '.env.local' tab
5. Copy all environment variables to your `.env.development.local` file

Required variables:
```env
POSTGRES_URL=
POSTGRES_PRISMA_URL=
POSTGRES_URL_NON_POOLING=
POSTGRES_USER=
POSTGRES_HOST=
POSTGRES_PASSWORD=
POSTGRES_DATABASE=
```

### 3. Dependencies
Make sure you have the required Python packages:
```bash
pip install psycopg2-binary requests
```

## Database Schema

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    access_key VARCHAR(64) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_access TIMESTAMP
);
```

### Training Plans
```sql
CREATE TABLE training_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    name VARCHAR(100) NOT NULL,
    progression_type VARCHAR(50),
    target_weekly_hours INTEGER,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Training Blocks
```sql
CREATE TABLE training_blocks (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES training_plans(id) NOT NULL,
    name VARCHAR(100) NOT NULL,
    primary_focus VARCHAR(50) NOT NULL,
    duration_weeks INTEGER NOT NULL,
    sequence_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Exercise Types
```sql
CREATE TABLE exercise_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Workouts
```sql
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    block_id INTEGER REFERENCES training_blocks(id) NOT NULL,
    name VARCHAR(100) NOT NULL,
    planned_date DATE NOT NULL,
    actual_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    sequence_order INTEGER NOT NULL,
    exercises JSONB NOT NULL DEFAULT '{"exercises": []}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Exercise JSON Structure
```json
{
    "exercises": [
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
            },
            "logs": [
                {
                    "timestamp": "2024-01-25T14:30:00",
                    "sets": [
                        {"reps": 5, "weight": "100kg", "rpe": 8},
                        {"reps": 5, "weight": "100kg", "rpe": 8.5},
                        {"reps": 5, "weight": "100kg", "rpe": 9}
                    ],
                    "notes": "Felt strong today",
                    "perceived_effort": 8,
                    "completed": true
                }
            ]
        }
    ]
}
```

## Sample Data

### Populating the Database
To populate the development database with sample data:
```bash
python api/scripts/populate_dev_db.py
```

This script creates:
- Sample users
- Exercise types
- Training plans with blocks
- Sample workouts with exercises

### Sample Data Details

#### Users
```python
users = [
    User(access_key='dev_user_1', nickname='John Doe'),
    User(access_key='dev_user_2', nickname='Jane Smith'),
    User(access_key='dev_user_3', nickname='Bob Johnson')
]
```

#### Exercise Types
```python
exercise_types = [
    ExerciseType(
        name='Squat',
        category='Strength',
        description='Compound lower body exercise targeting quads, hamstrings, and core'
    ),
    ExerciseType(
        name='Bench Press',
        category='Strength',
        description='Upper body push exercise for chest, shoulders, and triceps'
    ),
    ExerciseType(
        name='Deadlift',
        category='Strength',
        description='Full body compound exercise focusing on posterior chain'
    ),
    ExerciseType(
        name='Running',
        category='Cardio',
        description='Cardiovascular endurance training'
    )
]
```

#### Training Plans & Blocks
Each user gets:
- 12-week training plan
- 3 training blocks (4 weeks each):
  1. Hypertrophy Block (RPE 7-8)
  2. Strength Block (RPE 8-9)
  3. Peak Block (RPE 9-10)

## Development Scripts

### `config_env.py`
Sets up environment configuration files for development and production.
```python
python api/scripts/config_env.py
```

### `populate_dev_db.py`
Populates the development database with sample data.
```python
python api/scripts/populate_dev_db.py
```

### `check_db.py`
Verifies database connection and lists available schemas and tables.
```python
python api/scripts/check_db.py
```

## Best Practices
1. Never commit environment files (`.env*`) to version control
2. Use non-pooling connection URL for scripts (`POSTGRES_URL_NON_POOLING`)
3. Keep development and production data separate
4. Use sample data that's representative of real usage
5. Regularly refresh development data if needed

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify environment variables are correctly set
   - Check if database URL starts with `postgresql://` (not `postgres://`)
   - Ensure you have the required packages installed

2. **Missing Dependencies**
   ```bash
   pip install psycopg2-binary requests
   ```

3. **Environment File Issues**
   - Make sure `.env.development.local` exists and has all required variables
   - Verify you're using the correct environment file
   - Check file permissions 