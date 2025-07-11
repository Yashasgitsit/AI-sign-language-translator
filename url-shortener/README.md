# AWS Serverless URL Shortener

A serverless URL shortener built with AWS Lambda, API Gateway, and DynamoDB. This application allows users to create short URLs that redirect to longer URLs, similar to bit.ly or tinyurl.

## 🏗️ Architecture

```
Frontend (S3) → API Gateway → Lambda Functions → DynamoDB
```

### Components:
- **Frontend**: Static HTML/CSS/JS hosted on S3
- **API Gateway**: RESTful API endpoints
- **Lambda Functions**: 
  - `shortenr.py`: Creates short URLs
  - `redirector.py`: Handles redirections
- **DynamoDB**: Stores URL mappings
- **CloudWatch**: Logging and monitoring

## 🚀 Features

- ✅ Create short URLs from long URLs
- ✅ Automatic redirection to original URLs
- ✅ Click tracking and analytics
- ✅ Duplicate URL detection
- ✅ CORS support for web frontend
- ✅ Error handling and validation
- ✅ Serverless architecture (pay-per-use)
- ✅ Auto-scaling capabilities

## 📁 Project Structure

```
url-shortener/
├── lambda/
│   ├── shortenr.py          # URL shortening function
│   ├── redirector.py        # URL redirection function
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html          # Web interface
├── infrastructure/
│   └── template.yaml       # AWS SAM template
├── docs/
│   └── API.md             # API documentation
└── README.md              # This file
```

## 🛠️ Deployment

### Prerequisites

1. **AWS CLI** configured with appropriate permissions
2. **AWS SAM CLI** installed
3. **Python 3.9+** installed

### Quick Deployment

1. **Clone and navigate to the project:**
```bash
cd url-shortener
```

2. **Build the SAM application:**
```bash
sam build
```

3. **Deploy the application:**
```bash
sam deploy --guided
```

4. **Upload frontend to S3:**
```bash
aws s3 cp frontend/index.html s3://your-frontend-bucket/
```

### Manual Deployment Steps

1. **Create DynamoDB Table:**
```bash
aws dynamodb create-table \
    --table-name URLShortenerTable \
    --attribute-definitions AttributeName=short_code,AttributeType=S \
    --key-schema AttributeName=short_code,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

2. **Package Lambda functions:**
```bash
zip -r shortenr.zip lambda/shortenr.py
zip -r redirector.zip lambda/redirector.py
```

3. **Create Lambda functions via AWS Console or CLI**

4. **Set up API Gateway endpoints**

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DYNAMODB_TABLE` | DynamoDB table name | `URLShortenerTable` |
| `BASE_URL` | Base URL for short links | API Gateway URL |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/` | Create short URL |
| `GET` | `/{short_code}` | Redirect to original URL |

## 📖 API Usage

### Create Short URL

**Request:**
```bash
curl -X POST https://your-api-gateway-url/ \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very-long-url"}'
```

**Response:**
```json
{
  "short_url": "https://your-api-gateway-url/abc123",
  "short_code": "abc123",
  "long_url": "https://example.com/very-long-url",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Use Short URL

Simply visit the short URL in a browser:
```
https://your-api-gateway-url/abc123
```

## 🔍 Monitoring

### CloudWatch Metrics
- Lambda function invocations
- API Gateway requests
- DynamoDB read/write operations
- Error rates and latency

### Logs
- Lambda function logs in CloudWatch
- API Gateway access logs
- DynamoDB operation logs

## 💰 Cost Estimation

For 1000 URL shortenings and 10,000 redirects per month:

- **Lambda**: ~$0.20
- **API Gateway**: ~$3.50
- **DynamoDB**: ~$1.25
- **S3**: ~$0.50
- **Total**: ~$5.45/month

## 🔒 Security

- CORS configured for web access
- Input validation on all endpoints
- Rate limiting via API Gateway
- IAM roles with least privilege
- No sensitive data in URLs

## 🚀 Performance

- **Cold start**: ~100-200ms
- **Warm requests**: ~10-50ms
- **DynamoDB**: Single-digit millisecond latency
- **Auto-scaling**: Handles traffic spikes automatically

## 🔄 Future Enhancements

- [ ] Custom short codes
- [ ] Expiration dates for URLs
- [ ] Analytics dashboard
- [ ] Bulk URL creation
- [ ] QR code generation
- [ ] User authentication
- [ ] Custom domains

## 🐛 Troubleshooting

### Common Issues

1. **CORS errors**: Check API Gateway CORS configuration
2. **Lambda timeouts**: Increase timeout in template.yaml
3. **DynamoDB errors**: Verify IAM permissions
4. **Frontend not loading**: Check S3 bucket policy

### Debug Commands

```bash
# Check Lambda logs
sam logs -n ShortenUrlFunction --tail

# Test API locally
sam local start-api

# Validate SAM template
sam validate
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in this repository
- Check AWS documentation for service-specific issues
