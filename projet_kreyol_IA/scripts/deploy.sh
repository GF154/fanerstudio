#!/bin/bash
# Deployment script for Pwojè Kreyòl IA
# Usage: ./deploy.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  🇭🇹 Pwojè Kreyòl IA - Deployment Script${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Get environment
ENVIRONMENT=${1:-development}

print_header
print_info "Deploying to: $ENVIRONMENT"
echo ""

# Step 1: Validate environment
print_info "Step 1: Validating environment..."

if [ "$ENVIRONMENT" != "development" ] && [ "$ENVIRONMENT" != "production" ]; then
    print_error "Invalid environment: $ENVIRONMENT"
    echo "Usage: ./deploy.sh [development|production]"
    exit 1
fi

print_success "Environment validated"

# Step 2: Check dependencies
print_info "Step 2: Checking dependencies..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi

print_success "Dependencies checked"

# Step 3: Build Docker image
print_info "Step 3: Building Docker image..."

docker build -t kreyol-ai:latest . || {
    print_error "Docker build failed"
    exit 1
}

print_success "Docker image built"

# Step 4: Stop existing containers
print_info "Step 4: Stopping existing containers..."

docker-compose down || true

print_success "Containers stopped"

# Step 5: Start services
print_info "Step 5: Starting services..."

if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose up -d --build
else
    docker-compose up -d
fi

print_success "Services started"

# Step 6: Wait for services to be healthy
print_info "Step 6: Waiting for services to be ready..."

sleep 10

# Check API health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "API service is healthy"
else
    print_error "API service is not responding"
    docker-compose logs api
    exit 1
fi

# Step 7: Run post-deployment tasks
print_info "Step 7: Running post-deployment tasks..."

# Download model if not present
docker-compose exec -T api python download_model.py || print_info "Model already downloaded"

print_success "Post-deployment tasks completed"

# Step 8: Display status
echo ""
print_header
print_success "Deployment completed successfully!"
echo ""
print_info "Services:"
echo "  📡 API:        http://localhost:8000"
echo "  📚 API Docs:   http://localhost:8000/docs"
echo "  🖥️  GUI:        http://localhost:8501"
echo ""
print_info "Management commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart:       docker-compose restart"
echo ""
print_success "Deployment finished! 🚀"

