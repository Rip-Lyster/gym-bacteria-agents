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

## Sample Data

### Populating the Database
To populate the development database with sample data:
```bash
python api/scripts/populate_dev_db.py
```

This script creates:
- Sample users
- Exercise types
- Training plans
- Sample workouts

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
```

#### Training Plans & Workouts
- Each user gets a 12-week training plan
- Each plan includes 3 sample workouts
- Workout types: Push Day, Pull Day, Leg Day, Cardio, Full Body

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

## Switching Environments
To switch between environments:
- Development: `cp .env.development.local .env`
- Production: `cp .env.production.local .env`

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