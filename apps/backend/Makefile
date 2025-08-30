.PHONY: help install dev-install test test-cov test-verbose lint format clean run dev docs build

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	@echo "Installing production dependencies..."
	pip install -e .

dev-install: ## Install development dependencies
	@echo "Installing development dependencies..."
	pip install -e ".[dev]"
	pre-commit install

# Testing
test: ## Run tests
	@echo "Running tests..."
	pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

test-verbose: ## Run tests with verbose output
	@echo "Running tests with verbose output..."
	pytest tests/ -vv -s

# Code Quality
lint: ## Run linting tools
	@echo "Running linting tools..."
	ruff check src/ tests/
	mypy src/

format: ## Format code with black and isort
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

# Development
run: ## Run the FastAPI application
	@echo "Starting FastAPI application..."
	python -m src.presentation.api.main

dev: ## Run the FastAPI application in development mode
	@echo "Starting FastAPI application in development mode..."
	uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000

# Cleanup
clean: ## Clean up generated files
	@echo "Cleaning up generated files..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	mkdocs build

# Build
build: ## Build the package
	@echo "Building package..."
	python -m build

# Health check
health: ## Check API health
	@echo "Checking API health..."
	curl -s http://localhost:8000/health | jq . || echo "API not running"

# Docker (if needed in future)
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t elfosoftware-backend .

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run -p 8000:8000 elfosoftware-backend
