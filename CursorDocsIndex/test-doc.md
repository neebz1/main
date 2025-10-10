# Test Documentation for Docs-Agent

## Introduction

This is a sample documentation file to test the Docs-Agent module.

## Authentication

To authenticate with the API, use an API key in the request headers:

```python
headers = {
    "Authorization": f"Bearer {api_key}"
}
```

## API Endpoints

### GET /users

Retrieve a list of users.

**Parameters:**
- `limit` (integer): Maximum number of users to return
- `offset` (integer): Number of users to skip

**Response:**
```json
{
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
}
```

### POST /users

Create a new user.

**Request Body:**
```json
{
    "name": "Charlie",
    "email": "charlie@example.com"
}
```

## Rate Limiting

The API enforces rate limits of 100 requests per minute. If you exceed this limit, you'll receive a 429 status code.

## Error Handling

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

