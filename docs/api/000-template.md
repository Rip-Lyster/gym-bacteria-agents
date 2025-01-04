# API Endpoint: [Endpoint Name]

## Overview
**Endpoint:** `[HTTP Method] /api/path/to/endpoint`
**Description:** [Brief description of what this endpoint does]

## Authentication
- **Required:** [Yes/No]
- **Type:** [Bearer Token/API Key/etc.]

## Request

### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | `string` | Yes | Description |

### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `param1` | `string` | No | `null` | Description |

### Request Body
```json
{
  "field1": "string",
  "field2": {
    "nested": "value"
  }
}
```

#### Field Descriptions
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field1` | `string` | Yes | Description |
| `field2.nested` | `string` | No | Description |

## Response

### Success Response
**Status Code:** `200 OK`

```json
{
  "data": {
    "field": "value"
  },
  "meta": {
    "timestamp": "2024-01-04T12:00:00Z"
  }
}
```

### Error Responses
| Status Code | Description | Example |
|-------------|-------------|---------|
| `400` | Bad Request | `{"error": "Invalid parameters"}` |
| `401` | Unauthorized | `{"error": "Invalid token"}` |
| `403` | Forbidden | `{"error": "Insufficient permissions"}` |
| `404` | Not Found | `{"error": "Resource not found"}` |
| `500` | Server Error | `{"error": "Internal server error"}` |

## Rate Limiting
- **Limit:** [requests per time window]
- **Window:** [time window]
- **Header:** `X-RateLimit-Remaining`

## Examples

### cURL
```bash
curl -X POST \
  'https://api.example.com/endpoint' \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "field1": "value"
  }'
```

### TypeScript/JavaScript
```typescript
const response = await fetch('https://api.example.com/endpoint', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    field1: 'value',
  }),
});
```

### Python
```python
import requests

response = requests.post(
    'https://api.example.com/endpoint',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    },
    json={
        'field1': 'value',
    },
)
```

## Notes
- [Important considerations]
- [Edge cases]
- [Known limitations]

## Changelog
| Date | Changes |
|------|---------|
| YYYY-MM-DD | Initial documentation | 