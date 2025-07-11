# URL Shortener API Documentation

## Base URL
```
https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod
```

## Authentication
No authentication required for public endpoints.

## Endpoints

### 1. Create Short URL

**Endpoint:** `POST /`

**Description:** Creates a short URL from a long URL.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "long_url": "https://example.com/very-long-url-that-needs-shortening"
}
```

**Response (Success - 200):**
```json
{
  "short_url": "https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod/abc123",
  "short_code": "abc123",
  "long_url": "https://example.com/very-long-url-that-needs-shortening",
  "created_at": "2024-01-01T12:00:00.000Z"
}
```

**Response (Error - 400):**
```json
{
  "error": "Invalid URL format"
}
```

**Response (Error - 500):**
```json
{
  "error": "Internal server error"
}
```

**Example cURL:**
```bash
curl -X POST https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very-long-url"}'
```

### 2. Redirect Short URL

**Endpoint:** `GET /{short_code}`

**Description:** Redirects to the original long URL.

**Path Parameters:**
- `short_code` (string): The short code identifier

**Response (Success - 301):**
```
HTTP/1.1 301 Moved Permanently
Location: https://example.com/original-url
```

**Response (Error - 404):**
```json
{
  "error": "Short URL not found",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Response (Error - 400):**
```json
{
  "error": "Invalid short code format",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Example Usage:**
```bash
# Direct browser access
https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod/abc123

# cURL (will show redirect)
curl -I https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod/abc123
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 301 | Redirect (for short URL access) |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (short URL doesn't exist) |
| 500 | Internal Server Error |

## Rate Limiting

- Default API Gateway limits apply
- Consider implementing custom rate limiting for production use

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) with the following configuration:

- **Allowed Origins:** `*` (all origins)
- **Allowed Methods:** `POST, GET, OPTIONS`
- **Allowed Headers:** `Content-Type, Authorization`

## Data Storage

### DynamoDB Schema

**Table Name:** `URLShortenerTable`

**Primary Key:** `short_code` (String)

**Attributes:**
```json
{
  "short_code": "abc123",
  "long_url": "https://example.com/original-url",
  "created_at": "2024-01-01T12:00:00.000Z",
  "click_count": 42,
  "last_accessed": "2024-01-01T15:30:00.000Z"
}
```

## Analytics (Future Enhancement)

### Get URL Analytics

**Endpoint:** `GET /analytics/{short_code}` (Not implemented yet)

**Response:**
```json
{
  "short_code": "abc123",
  "long_url": "https://example.com/original-url",
  "click_count": 42,
  "created_at": "2024-01-01T12:00:00.000Z",
  "last_accessed": "2024-01-01T15:30:00.000Z"
}
```

## SDK Examples

### JavaScript/Node.js

```javascript
// Create short URL
async function createShortUrl(longUrl) {
  const response = await fetch('https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ long_url: longUrl })
  });
  
  return await response.json();
}

// Usage
createShortUrl('https://example.com/long-url')
  .then(data => console.log(data.short_url))
  .catch(error => console.error('Error:', error));
```

### Python

```python
import requests
import json

def create_short_url(long_url):
    url = "https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod"
    payload = {"long_url": long_url}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Usage
result = create_short_url("https://example.com/long-url")
print(result["short_url"])
```

### PHP

```php
<?php
function createShortUrl($longUrl) {
    $url = "https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod";
    $data = json_encode(["long_url" => $longUrl]);
    
    $options = [
        "http" => [
            "header" => "Content-Type: application/json\r\n",
            "method" => "POST",
            "content" => $data
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    return json_decode($result, true);
}

// Usage
$result = createShortUrl("https://example.com/long-url");
echo $result["short_url"];
?>
```

## Testing

### Unit Tests

Run the included tests:
```bash
python -m pytest tests/
```

### Integration Tests

Test the live API:
```bash
# Test URL creation
curl -X POST https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://httpbin.org/get"}'

# Test redirection (replace abc123 with actual short code)
curl -I https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod/abc123
```

## Monitoring

### CloudWatch Metrics

Monitor these key metrics:
- Lambda function duration
- Lambda function errors
- API Gateway 4XX/5XX errors
- DynamoDB read/write capacity

### Custom Metrics

The application tracks:
- URL creation count
- Redirect count
- Error rates

## Security Considerations

1. **Input Validation:** All URLs are validated before processing
2. **Rate Limiting:** Consider implementing rate limiting for production
3. **HTTPS Only:** All communications use HTTPS
4. **No Sensitive Data:** Short codes don't contain sensitive information

## Troubleshooting

### Common Issues

1. **CORS Errors:** Ensure proper headers are set
2. **Invalid URL:** Check URL format (must include protocol)
3. **Short Code Not Found:** Verify the short code exists
4. **Timeout Errors:** Check Lambda function logs

### Debug Information

Enable debug logging by setting environment variables in Lambda functions.
