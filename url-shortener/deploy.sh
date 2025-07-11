#!/bin/bash

# AWS Serverless URL Shortener Deployment Script
# This script deploys the URL shortener using AWS SAM

set -e

echo "🚀 Starting URL Shortener Deployment..."

# Configuration
STACK_NAME="url-shortener-stack"
REGION="ap-south-1"
ENVIRONMENT="prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check SAM CLI
    if ! command -v sam &> /dev/null; then
        print_error "AWS SAM CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Please run 'aws configure'."
        exit 1
    fi
    
    print_status "Prerequisites check passed ✅"
}

# Build the SAM application
build_application() {
    print_status "Building SAM application..."
    
    if sam build; then
        print_status "Build completed successfully ✅"
    else
        print_error "Build failed ❌"
        exit 1
    fi
}

# Deploy the application
deploy_application() {
    print_status "Deploying application..."
    
    # Check if this is first deployment
    if aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION &> /dev/null; then
        print_status "Stack exists, updating..."
        sam deploy \
            --stack-name $STACK_NAME \
            --region $REGION \
            --parameter-overrides Environment=$ENVIRONMENT \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset
    else
        print_status "First deployment, using guided mode..."
        sam deploy \
            --guided \
            --stack-name $STACK_NAME \
            --region $REGION \
            --parameter-overrides Environment=$ENVIRONMENT
    fi
    
    if [ $? -eq 0 ]; then
        print_status "Deployment completed successfully ✅"
    else
        print_error "Deployment failed ❌"
        exit 1
    fi
}

# Get stack outputs
get_outputs() {
    print_status "Getting stack outputs..."
    
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayUrl`].OutputValue' \
        --output text)
    
    FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
        --output text)
    
    echo ""
    echo "🎉 Deployment Complete!"
    echo "========================"
    echo "API Gateway URL: $API_URL"
    echo "Frontend URL: $FRONTEND_BUCKET"
    echo ""
}

# Upload frontend to S3
upload_frontend() {
    print_status "Uploading frontend to S3..."
    
    # Get bucket name from stack outputs
    BUCKET_NAME=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
        --output text | sed 's|http://||' | sed 's|.s3-website.*||')
    
    if [ ! -z "$BUCKET_NAME" ]; then
        # Update API endpoint in HTML file
        sed -i.bak "s|https://81w6p4jdx7.execute-api.ap-south-1.amazonaws.com/prod|$API_URL|g" frontend/index.html
        
        # Upload to S3
        aws s3 cp frontend/index.html s3://$BUCKET_NAME/ --region $REGION
        
        # Restore original file
        mv frontend/index.html.bak frontend/index.html
        
        print_status "Frontend uploaded successfully ✅"
    else
        print_warning "Could not determine S3 bucket name"
    fi
}

# Test the deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Test URL shortening
    TEST_URL="https://example.com/test-url"
    
    RESPONSE=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "{\"long_url\": \"$TEST_URL\"}")
    
    if echo "$RESPONSE" | grep -q "short_url"; then
        print_status "API test passed ✅"
        echo "Test response: $RESPONSE"
    else
        print_warning "API test failed. Response: $RESPONSE"
    fi
}

# Main execution
main() {
    echo "URL Shortener Deployment Script"
    echo "==============================="
    echo ""
    
    check_prerequisites
    build_application
    deploy_application
    get_outputs
    upload_frontend
    test_deployment
    
    echo ""
    echo "🎉 All done! Your URL shortener is ready to use."
    echo ""
    echo "Next steps:"
    echo "1. Visit the frontend URL to test the interface"
    echo "2. Use the API URL to integrate with other applications"
    echo "3. Monitor the application in AWS CloudWatch"
    echo ""
}

# Run main function
main "$@"
