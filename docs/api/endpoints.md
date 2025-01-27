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

## Overview
This document details the available endpoints in the Gym Bacteria API. All endpoints are prefixed with `/api`.

## Authentication
Currently using simple access key authentication. Each user has a unique `access_key` that must be provided for user-specific operations.

## Users

### Create User
```http
POST /users
Content-Type: application/json

{
    "access_key": "string",
    "nickname": "string"
}
```

### Get User
```http
GET /users/{access_key}
```

### Delete User
```http
DELETE /users/{access_key}
```

## Training Plans

### Get User's Training Plans
```http
GET /users/{user_id}/training-plans
```

### Create Training Plan
```http
POST /training-plans
Content-Type: application/json

{
    "user_id": "integer",
    "name": "string",
    "progression_type": "string",     // optional
    "target_weekly_hours": "integer", // optional
    "start_date": "YYYY-MM-DD",      // optional
    "end_date": "YYYY-MM-DD"         // optional
}
```

## Training Blocks

### Create Training Block
```http
POST /training-blocks
Content-Type: application/json

{
    "plan_id": "integer",
    "name": "string",
    "primary_focus": "string",
    "duration_weeks": "integer",
    "sequence_order": "integer"
}
```

### Get Training Block
```http
GET /training-blocks/{block_id}
```

### Delete Training Block
```http
DELETE /training-blocks/{block_id}
```

## Exercise Types

### Get All Exercise Types
```http
GET /exercise-types
```

### Create Exercise Type
```http
POST /exercise-types
Content-Type: application/json

{
    "name": "string",
    "category": "string",
    "description": "string"  // optional
}
```

## Workouts

### Create Workout
```http
POST /workouts
Content-Type: application/json

{
    "block_id": "integer",
    "name": "string",
    "planned_date": "YYYY-MM-DD",
    "sequence_order": "integer",
    "actual_date": "YYYY-MM-DD",     // optional
    "status": "string",              // optional, default: "planned"
    "exercises": {
        "exercises": [
            {
                "exercise_type_id": "integer",
                "name": "string",
                "sequence": "integer",
                "planned": {
                    "sets": "integer",
                    "reps": "string or integer",
                    "rpe": "integer (1-10)",
                    "rest_minutes": "integer",
                    "notes": "string"
                }
            }
        ]
    }
}
```

## Data Structures

### Exercise JSON Structure
The exercise data is stored as JSONB in the database. Here's the structure:

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
                        {
                            "reps": 5,
                            "weight": "100kg",
                            "rpe": 8
                        },
                        {
                            "reps": 5,
                            "weight": "100kg",
                            "rpe": 8.5
                        },
                        {
                            "reps": 5,
                            "weight": "100kg",
                            "rpe": 9
                        }
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

## Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request
- `404` - Not Found

## Rate Limiting
Currently no rate limiting implemented.

## Error Responses
All error responses follow this format:
```json
{
    "error": "Error message describing what went wrong"
}
``` 