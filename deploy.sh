#!/bin/bash
echo "🚀 Starting Flota Transportistes Demo"

# Check if docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Docker detected - using Docker Compose"
    echo "Building and starting services..."

    # Check if docker-compose.yml exists in infra directory
    if [ -f "infra/docker-compose.yml" ]; then
        cd infra
        docker-compose up --build -d
        cd ..
        echo ""
        echo "✅ Services started!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "🔧 Backend API: http://localhost:8000"
        echo ""
        echo "To stop: cd infra && docker-compose down"
        echo "To view logs: cd infra && docker-compose logs -f"
    else
        echo "❌ docker-compose.yml not found in infra/ directory"
        echo "Please ensure you're in the project root directory"
        exit 1
    fi
else
    echo "🐳 Docker not available - manual setup required"
    echo ""
    echo "📦 Manual Setup Instructions:"
    echo "1. Backend: cd apps/backend && pip install -r requirements.txt && python -m uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000"
    echo "2. Frontend: cd apps/web && npm install && npm run dev"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo ""
    echo "💡 Quick commands:"
    echo "Backend only: cd apps/backend && python -m uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000"
    echo "Frontend only: cd apps/web && npm run dev"
fi
