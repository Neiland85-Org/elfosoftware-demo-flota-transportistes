#!/bin/bash

# Deployment script for Docker Compose
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-dev}
COMPOSE_FILE="docker-compose.prod.yml"

echo "🚀 Starting deployment to $ENVIRONMENT environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure your variables."
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Pull latest images
echo "📦 Pulling latest Docker images..."
docker-compose -f $COMPOSE_FILE pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down

# Start services
echo "▶️  Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check health
echo "🔍 Checking service health..."
if curl -f http://localhost:${BACKEND_PORT:-8000}/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    exit 1
fi

if curl -f http://localhost:${FRONTEND_PORT:-3000} > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Service URLs:"
echo "  Frontend: http://localhost:${FRONTEND_PORT:-3000}"
echo "  Backend:  http://localhost:${BACKEND_PORT:-8000}"
echo ""
echo "📊 To view logs: docker-compose -f $COMPOSE_FILE logs -f"
echo "🛑 To stop: docker-compose -f $COMPOSE_FILE down"
