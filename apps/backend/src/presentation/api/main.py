"""
Main FastAPI application for Elfosoftware Demo Flota Transportistes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(
    title="Elfosoftware Demo - Flota Transportistes API",
    description="API REST para gestión de flota de transportistas",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Elfosoftware Demo - Flota Transportistes API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/api/v1/")
async def api_root():
    """API root endpoint"""
    return {"message": "API v1", "version": "0.1.0"}

# Add your API routes here
from .routes.flota_routes import router as flota_router

# Include routers
app.include_router(flota_router)
