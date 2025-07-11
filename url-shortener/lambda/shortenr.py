"""
AWS Lambda function for URL shortening
Creates short URLs and stores them in DynamoDB
"""

import json
import boto3
import random
import string
import os
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'URLShortenerTable')
table = dynamodb.Table(table_name)

# Base URL for short URLs
BASE_URL = os.environ.get('BASE_URL', 'https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod')

def lambda_handler(event, context):
    """
    Main Lambda handler for URL shortening
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    
    # Handle CORS preflight requests
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})
    
    try:
        # Parse request body
        if 'body' not in event or not event['body']:
            return cors_response(400, {'error': 'Request body is required'})
        
        body = json.loads(event['body'])
        long_url = body.get('long_url', '').strip()
        
        # Validate URL
        if not long_url:
            return cors_response(400, {'error': 'long_url is required'})
        
        if not is_valid_url(long_url):
            return cors_response(400, {'error': 'Invalid URL format'})
        
        # Check if URL already exists
        existing_short_code = check_existing_url(long_url)
        if existing_short_code:
            short_url = f"{BASE_URL}/{existing_short_code}"
            logger.info(f"Returning existing short URL: {short_url}")
            return cors_response(200, {
                'short_url': short_url,
                'short_code': existing_short_code,
                'message': 'URL already exists'
            })
        
        # Generate a unique short code
        short_code = generate_unique_short_code()
        
        # Store the mapping in DynamoDB
        store_url_mapping(short_code, long_url)
        
        # Construct the full short URL
        short_url = f"{BASE_URL}/{short_code}"
        
        logger.info(f"Created short URL: {short_url} for {long_url}")
        
        return cors_response(200, {
            'short_url': short_url,
            'short_code': short_code,
            'long_url': long_url,
            'created_at': datetime.utcnow().isoformat()
        })

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return cors_response(400, {'error': 'Invalid JSON in request body'})
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return cors_response(500, {'error': 'Internal server error'})

def generate_short_code(length=None):
    """
    Generate a random short code
    
    Args:
        length: Length of the short code (default: random between 3-8)
        
    Returns:
        Random short code string
    """
    if length is None:
        length = random.randint(3, 8)
    
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_unique_short_code(max_attempts=10):
    """
    Generate a unique short code that doesn't exist in the database
    
    Args:
        max_attempts: Maximum number of attempts to generate unique code
        
    Returns:
        Unique short code
        
    Raises:
        Exception: If unable to generate unique code after max_attempts
    """
    for attempt in range(max_attempts):
        short_code = generate_short_code()
        
        # Check if this code already exists
        try:
            response = table.get_item(Key={'short_code': short_code})
            if 'Item' not in response:
                return short_code
        except Exception as e:
            logger.error(f"Error checking existing short code: {str(e)}")
            continue
    
    raise Exception("Unable to generate unique short code")

def store_url_mapping(short_code, long_url):
    """
    Store URL mapping in DynamoDB
    
    Args:
        short_code: Short code identifier
        long_url: Original long URL
    """
    table.put_item(
        Item={
            'short_code': short_code,
            'long_url': long_url,
            'created_at': datetime.utcnow().isoformat(),
            'click_count': 0
        }
    )

def check_existing_url(long_url):
    """
    Check if a long URL already has a short code
    
    Args:
        long_url: URL to check
        
    Returns:
        Existing short code or None
    """
    try:
        # Note: This requires a GSI on long_url for efficient querying
        # For now, we'll skip this optimization
        return None
    except Exception as e:
        logger.error(f"Error checking existing URL: {str(e)}")
        return None

def is_valid_url(url):
    """
    Basic URL validation
    
    Args:
        url: URL to validate
        
    Returns:
        Boolean indicating if URL is valid
    """
    import re
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def cors_response(status_code, body):
    """
    Create a CORS-enabled response
    
    Args:
        status_code: HTTP status code
        body: Response body
        
    Returns:
        API Gateway response with CORS headers
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
