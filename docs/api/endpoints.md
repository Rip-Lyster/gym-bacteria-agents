# API Reference

This document describes the API endpoints available in the Gym Bacteria Agents project.

## Backend API Endpoints

The Flask backend runs on `http://localhost:5328` in development.

### Base URL

- Development: `http://localhost:5328`
- Production: [Your production URL]

### Authentication

[To be documented: Authentication methods and requirements]

### Endpoints

#### GET /api/health
Health check endpoint to verify the API is running.

**Response**
```json
{
    "status": "ok"
}
```

[Additional endpoints to be documented as they are implemented]

## Frontend Components

The Next.js frontend runs on `http://localhost:3000` in development.

### Pages

- `/` - Home page
- [Additional pages to be documented as they are implemented]

### Components

[To be documented: Reusable components and their props] 

# API Endpoints

## Health Check Endpoint

### Overview
**Endpoint:** `GET /api/health`
**Description:** Simple health check endpoint to verify the API is running and responsive.

### Authentication
- **Required:** No
- **Type:** None

### Request
No parameters required.

### Response

#### Success Response
**Status Code:** `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2024-01-04T12:00:00Z",
  "version": "1.0.0"
}
```

#### Error Responses
| Status Code | Description | Example |
|-------------|-------------|---------|
| `500` | Server Error | `{"error": "Internal server error"}` |

### Examples

#### cURL
```bash
curl 'http://localhost:5000/api/health'
```

#### TypeScript/JavaScript
```typescript
const response = await fetch('http://localhost:5000/api/health');
const health = await response.json();
```

#### Python
```python
import requests

response = requests.get('http://localhost:5000/api/health')
health = response.json()
```

### Notes
- Use this endpoint for monitoring and health checks
- The endpoint is unauthenticated to allow for simple monitoring
- Response includes API version and timestamp for tracking

### Changelog
| Date | Changes |
|------|---------|
| 2024-01-04 | Initial implementation | 

# API Documentation

## Architecture
For details on how API communication is structured in the frontend, see [ADR 002: API Service Layer Architecture](../adr/002-api-service-layer.md).

## Endpoints

### Health Check
- **URL**: `/api/health`
- **Method**: `GET`
- **Response**:
  ```typescript
  interface HealthCheckResponse {
    status: string;
  }
  ```
- **Usage**:
  ```typescript
  import { getHealthStatus } from '@/services/api';
  
  const status = await getHealthStatus();
  ``` 

# API Endpoints Documentation

## Users

### Create User
- **POST** `/api/users`
- Creates a new user
- **Request Body**:
  ```json
  {
    "access_key": "string",
    "nickname": "string"
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "integer",
    "nickname": "string"
  }
  ```

### Get User
- **GET** `/api/users/<access_key>`
- Retrieves user information by access key
- **Response** (200):
  ```json
  {
    "id": "integer",
    "nickname": "string"
  }
  ```
- **Error** (404):
  ```json
  {
    "error": "User not found"
  }
  ```

## Training Plans

### Create Training Plan
- **POST** `/api/training-plans`
- Creates a new training plan
- **Request Body**:
  ```json
  {
    "user_id": "integer",
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "integer",
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }
  ```

### Get Training Plan
- **GET** `/api/training-plans/<plan_id>`
- Retrieves a specific training plan
- **Response** (200):
  ```json
  {
    "id": "integer",
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }
  ```
- **Error** (404): Not Found

### Get User's Training Plans
- **GET** `/api/users/<user_id>/training-plans`
- Lists all training plans for a user
- **Response** (200):
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD"
    }
  ]
  ```

## Exercise Types

### Create Exercise Type
- **POST** `/api/exercise-types`
- Creates a new exercise type
- **Request Body**:
  ```json
  {
    "name": "string",
    "category": "string",
    "parameters": {
      // Optional JSON object with exercise parameters
    }
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "integer",
    "name": "string",
    "category": "string",
    "parameters": "object"
  }
  ```

### List Exercise Types
- **GET** `/api/exercise-types`
- Retrieves all exercise types
- **Response** (200):
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "category": "string",
      "parameters": "object"
    }
  ]
  ```

## Workouts

### Create Workout
- **POST** `/api/workouts`
- Creates a new workout with exercises
- **Request Body**:
  ```json
  {
    "training_plan_id": "integer",
    "name": "string",
    "planned_date": "YYYY-MM-DD",
    "exercises": [
      {
        "exercise_type_id": "integer",
        "sets": "integer",
        "reps": "integer",
        "weight": "float?",
        "notes": "string?"
      }
    ],
    "status": "string (planned|completed|skipped)?"
  }
  ```
- **Response** (201):
  ```json
  {
    "id": "integer",
    "name": "string",
    "training_plan_id": "integer",
    "planned_date": "YYYY-MM-DD",
    "status": "string",
    "exercises": [
      {
        "id": "integer",
        "exercise_type_id": "integer",
        "exercise_name": "string",
        "sets": "integer",
        "reps": "integer",
        "weight": "float?",
        "notes": "string?",
        "order": "integer"
      }
    ]
  }
  ```

### Update Workout
- **PATCH** `/api/workouts/<workout_id>`
- Updates workout details and status
- **Request Body**:
  ```json
  {
    "name": "string?",
    "planned_date": "YYYY-MM-DD?",
    "status": "string (planned|completed|skipped)?",
    "exercises": [
      {
        "exercise_type_id": "integer",
        "sets": "integer",
        "reps": "integer",
        "weight": "float?",
        "notes": "string?"
      }
    ]?
  }
  ```
- **Response** (200):
  ```json
  {
    "id": "integer",
    "name": "string",
    "planned_date": "YYYY-MM-DD",
    "status": "string",
    "exercises": [
      {
        "id": "integer",
        "exercise_type_id": "integer",
        "exercise_name": "string",
        "sets": "integer",
        "reps": "integer",
        "weight": "float?",
        "notes": "string?",
        "order": "integer"
      }
    ]
  }
  ```

### Get Plan Workouts
- **GET** `/api/workouts/plan/<plan_id>`
- Lists all workouts for a training plan
- **Response** (200):
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "planned_date": "YYYY-MM-DD",
      "status": "string",
      "exercises": [
        {
          "id": "integer",
          "exercise_type_id": "integer",
          "exercise_name": "string",
          "sets": "integer",
          "reps": "integer",
          "weight": "float?",
          "notes": "string?",
          "order": "integer"
        }
      ]
    }
  ]
  ```

### Delete Workout
- **DELETE** `/api/workouts/<workout_id>`
- Deletes a workout and its exercises
- **Response** (204): No Content 