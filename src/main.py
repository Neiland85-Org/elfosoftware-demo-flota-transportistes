"""Main FastAPI Application

Punto de entrada principal de la aplicación Elfosoftware Flota Transportistes.
Configura FastAPI con todas las rutas y middlewares necesarios.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from elfosoftware_flota.presentation.api import flota_router, transportista_router, vehiculo_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Elfosoftware Flota Transportistes API",
    description="API REST para gestión de flota de transportistas - Arquitectura DELFOS",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(flota_router, prefix="/api/v1/flota", tags=["Flota"])
app.include_router(transportista_router, prefix="/api/v1/transportista", tags=["Transportista"])
app.include_router(vehiculo_router, prefix="/api/v1/vehiculo", tags=["Vehiculo"])


@app.get("/")
async def root() -> dict:
    """Endpoint raíz de la API."""
    return {
        "message": "🚛 Elfosoftware Flota Transportistes API",
        "version": "0.1.0",
        "architecture": "DELFOS",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> dict:
    """Endpoint de health check."""
    return {"status": "healthy", "service": "flota-transportistes-api"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
