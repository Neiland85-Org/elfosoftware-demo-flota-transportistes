#!/bin/bash

# Script to start the demo environment using Docker Compose

echo "🚀 Starting Elfosoftware Demo - Flota Transportistes"
echo "=================================================="

# Navigate to infra directory
cd infra

# Start services
echo "📦 Starting Docker Compose services..."
docker-compose up --build

echo "✅ Demo environment started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "🗄️  Database: localhost:5432"
echo ""
echo "To stop the demo, press Ctrl+C"
