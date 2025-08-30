#!/bin/bash

# Script to start development environment with Docker

echo "🛠️  Starting Development Environment"
echo "==================================="
echo "Arquitectura DELFOS - Development Mode"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  backend    Start only backend services (API + Database)"
    echo "  full       Start full stack (Backend + Frontend + Database)"
    echo "  stop       Stop all running services"
    echo "  logs       Show logs from running services"
    echo "  help       Show this help message"
    echo ""
}

# Parse command line arguments
case "${1:-full}" in
    "backend")
        echo "📦 Starting backend services only..."
        cd infra
        docker compose up --build db backend
        ;;
    "full")
        echo "📦 Starting full stack..."
        cd infra
        docker compose up --build
        ;;
    "stop")
        echo "🛑 Stopping all services..."
        cd infra
        docker compose down
        echo "✅ Services stopped"
        ;;
    "logs")
        echo "📋 Showing logs..."
        cd infra
        docker compose logs -f
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo "❌ Invalid option: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
