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