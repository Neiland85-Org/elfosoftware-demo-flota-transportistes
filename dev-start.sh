#!/bin/bash
echo "🚀 Starting Development Environment - Flota Transportistes"
echo "Architecture: DELFOS (Domain-driven Enterprise Layered Framework for Optimal Solutions)"
echo ""

# Function to start backend
start_backend() {
    echo "🔧 Starting Backend (FastAPI)..."
    cd apps/backend
    if [ -f "../../requirements.txt" ]; then
        pip install -r ../../requirements.txt
    fi
    python -m uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ../..
    echo "✅ Backend started (PID: $BACKEND_PID) - http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
}

# Function to start frontend
start_frontend() {
    echo "🌐 Starting Frontend (Next.js)..."
    cd apps/web
    npm install
    npm run dev &
    FRONTEND_PID=$!
    cd ../..
    echo "✅ Frontend started (PID: $FRONTEND_PID) - http://localhost:3000"
}

# Function to stop all services
stop_services() {
    echo "🛑 Stopping all services..."
    pkill -f "uvicorn src.presentation.api.main:app" || true
    pkill -f "next dev" || true
    echo "✅ Services stopped"
}

# Parse arguments
case "$1" in
    "backend")
        start_backend
        ;;
    "frontend")
        start_frontend
        ;;
    "stop")
        stop_services
        ;;
    "full"|*)
        echo "Starting full development environment..."
        start_backend
        echo ""
        start_frontend
        echo ""
        echo "🎉 Development environment ready!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "🔧 Backend: http://localhost:8000"
        echo "📚 API Docs: http://localhost:8000/docs"
        echo ""
        echo "Press Ctrl+C to stop all services"
        wait
        ;;
esac
