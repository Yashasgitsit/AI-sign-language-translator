"""
AWS Lambda function for URL redirection
Retrieves original URLs from DynamoDB and redirects users
"""

import json
import boto3
import os
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'URLShortenerTable')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    Main Lambda handler for URL redirection
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        HTTP redirect response or 404 error
    """
    
    try:
        # Extract short code from path parameters
        path_parameters = event.get('pathParameters', {})
        if not path_parameters or 'short_code' not in path_parameters:
            logger.error("No short_code in path parameters")
            return error_response(400, 'Invalid request: missing short code')
        
        short_code = path_parameters['short_code']
        
        # Validate short code format
        if not is_valid_short_code(short_code):
            logger.error(f"Invalid short code format: {short_code}")
            return error_response(400, 'Invalid short code format')
        
        # Retrieve URL mapping from DynamoDB
        url_data = get_url_mapping(short_code)
        
        if not url_data:
            logger.info(f"Short code not found: {short_code}")
            return error_response(404, 'Short URL not found')
        
        long_url = url_data['long_url']
        
        # Update click count (fire and forget)
        try:
            update_click_count(short_code)
        except Exception as e:
            logger.warning(f"Failed to update click count: {str(e)}")
        
        logger.info(f"Redirecting {short_code} to {long_url}")
        
        # Return redirect response
        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url,
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            'body': ''
        }

    except Exception as e:
        logger.error(f"Unexpected error in redirector: {str(e)}")
        return error_response(500, 'Internal server error')

def get_url_mapping(short_code):
    """
    Retrieve URL mapping from DynamoDB
    
    Args:
        short_code: Short code to look up
        
    Returns:
        URL data dictionary or None if not found
    """
    try:
        response = table.get_item(
            Key={'short_code': short_code}
        )
        
        if 'Item' in response:
            return response['Item']
        else:
            return None
            
    except Exception as e:
        logger.error(f"Error retrieving URL mapping for {short_code}: {str(e)}")
        return None

def update_click_count(short_code):
    """
    Increment the click count for a short URL
    
    Args:
        short_code: Short code to update
    """
    try:
        table.update_item(
            Key={'short_code': short_code},
            UpdateExpression='ADD click_count :inc SET last_accessed = :timestamp',
            ExpressionAttributeValues={
                ':inc': 1,
                ':timestamp': datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error updating click count for {short_code}: {str(e)}")
        raise

def is_valid_short_code(short_code):
    """
    Validate short code format
    
    Args:
        short_code: Short code to validate
        
    Returns:
        Boolean indicating if short code is valid
    """
    import re
    
    # Allow alphanumeric characters, 3-8 characters long
    pattern = re.compile(r'^[a-zA-Z0-9]{3,8}$')
    return pattern.match(short_code) is not None

def error_response(status_code, message):
    """
    Create an error response
    
    Args:
        status_code: HTTP status code
        message: Error message
        
    Returns:
        API Gateway error response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': message,
            'timestamp': datetime.utcnow().isoformat()
        })
    }

def get_analytics_data(short_code):
    """
    Get analytics data for a short URL (future enhancement)
    
    Args:
        short_code: Short code to get analytics for
        
    Returns:
        Analytics data dictionary
    """
    try:
        response = table.get_item(
            Key={'short_code': short_code}
        )
        
        if 'Item' in response:
            item = response['Item']
            return {
                'short_code': short_code,
                'long_url': item.get('long_url'),
                'click_count': item.get('click_count', 0),
                'created_at': item.get('created_at'),
                'last_accessed': item.get('last_accessed')
            }
        else:
            return None
            
    except Exception as e:
        logger.error(f"Error retrieving analytics for {short_code}: {str(e)}")
        return None
