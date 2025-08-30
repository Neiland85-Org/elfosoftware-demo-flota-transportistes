#!/bin/bash

# Script to start the demo environment using Docker Compose

echo "🚀 Starting Elfosoftware Demo - Flota Transportistes"
echo "=================================================="
echo "🏗️  Arquitectura DELFOS - Domain-Driven Design"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Navigate to infra directory
cd infra

# Start services with modern compose
echo "📦 Starting Docker Compose services..."
echo "  - PostgreSQL Database"
echo "  - FastAPI Backend (Python)"
echo "  - Next.js Frontend (Node.js)"
echo ""

docker compose up --build

echo ""
echo "✅ Demo environment started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432"
echo ""
echo "To stop the demo, press Ctrl+C"
