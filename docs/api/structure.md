# API Structure Documentation

## Directory Structure

```
api/
├── core/               # Core application components
│   ├── config.py      # Database and app configuration
│   └── models.py      # SQLAlchemy models
├── routes/            # API route definitions
│   └── api.py        # Main API endpoints
├── scripts/          # Development and maintenance scripts
│   └── check_db.py   # Database connection verification
├── migrations/       # Alembic database migrations
├── __init__.py      # Package initialization
├── index.py         # Application entry point
└── alembic.ini      # Alembic configuration
```

## Component Details

### Core Components

#### config.py
- Database configuration using SQLAlchemy
- Environment variable loading
- Database connection initialization

#### models.py
- SQLAlchemy model definitions
- Database schema representation
- Relationship definitions between models:
  - User -> Training Plans (one-to-many)
  - Training Plan -> Workouts (one-to-many)
  - Workout -> Exercise Types (many-to-many via workout_exercises)
  - Exercise Types (referenced by workout_exercises)

### Routes

#### api.py
Implements RESTful endpoints for:
- Users management
- Training plans CRUD
- Exercise types management
- Workout management with exercises
  - Create/update workouts with exercises
  - Status management
  - Exercise selection and configuration

### Development Scripts

#### check_db.py
Database verification script that:
- Validates database connection
- Lists available schemas
- Shows current tables
- Helps in development debugging

### Database Migrations

The `migrations/` directory contains Alembic-managed database migrations:
- Version-controlled schema changes
- Upgrade and downgrade paths
- Migration history tracking

## Environment Setup

The application requires:
- Python 3.12+
- PostgreSQL (via Neon.tech)
- Environment variables in `.env.development.local`:
  - DATABASE_URL
  - Other configuration variables

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   cd api
   alembic upgrade head
   ```

3. Start the server:
   ```bash
   python api/index.py
   ```

## Development Guidelines

1. **Database Changes**
   - Always use Alembic migrations
   - Create new migration: `alembic revision --autogenerate -m "description"`
   - Apply migrations: `alembic upgrade head`

2. **Adding New Routes**
   - Place in appropriate file under `routes/`
   - Follow RESTful principles
   - Include proper error handling
   - Document in OpenAPI/Swagger format

3. **Model Changes**
   - Update `models.py`
   - Create corresponding migration
   - Update related routes
   - Update documentation 