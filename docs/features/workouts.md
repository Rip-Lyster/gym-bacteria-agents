# Workout Management

## Overview
The workout management system allows users to create, track, and manage their workouts within training plans. It provides a comprehensive interface for scheduling workouts, selecting exercises, and tracking workout completion status.

## Features

### Calendar View
- Interactive calendar using FullCalendar
- Color-coded workout status display:
  - Blue: Planned workouts
  - Green: Completed workouts
  - Red: Skipped workouts
- Click-to-update status functionality
- Date selection for new workouts

### Workout Creation
- Intuitive workout creation form
- Date picker for scheduling
- Exercise selector with:
  - Categorized exercise listing
  - Real-time search functionality
  - Selected exercise management
- Form validation and error handling

### Workout List
- Comprehensive workout listing
- Status controls for each workout:
  - Mark as planned
  - Mark as completed
  - Mark as skipped
- Delete functionality
- Loading states and error handling

### Exercise Browser
- Complete exercise type listing
- Categorized display
- Real-time search functionality
- Integration with workout creation

## Technical Implementation

### Database Schema
```sql
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    training_plan_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    planned_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (training_plan_id) REFERENCES training_plans(id) ON DELETE CASCADE
);

CREATE TABLE workout_exercises (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER NOT NULL,
    exercise_type_id INTEGER NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight FLOAT,
    notes TEXT,
    order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_type_id) REFERENCES exercise_types(id) ON DELETE CASCADE
);
```

### API Endpoints
- `POST /api/workouts`: Create workout with exercises
- `PATCH /api/workouts/<id>`: Update workout details and exercises
- `GET /api/workouts/plan/<id>`: Get all workouts for a plan
- `DELETE /api/workouts/<id>`: Delete workout and exercises

### Frontend Components
- `WorkoutCalendar`: FullCalendar integration
- `CreateWorkoutForm`: Workout creation interface
- `WorkoutList`: List view with status controls
- `ExerciseSelector`: Exercise browsing and selection

## Usage

### Creating a Workout
1. Navigate to training plan
2. Click "Add Workout" or select a date
3. Fill in workout details:
   - Name
   - Planned date
   - Select exercises
4. Submit the form

### Managing Workouts
- Use calendar view for scheduling overview
- Use list view for detailed management
- Update status by clicking in calendar or using controls
- Delete workouts as needed

### Exercise Selection
1. Click "Add Exercise" in workout form
2. Use search to find exercises
3. Click exercise to select
4. Remove selected exercises if needed

## Future Enhancements
- Exercise details modal
- Exercise history tracking
- Parameter configuration UI
- Exercise variation system 