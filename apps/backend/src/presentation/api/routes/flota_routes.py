"""
API routes for fleet management
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

# Domain imports
from src.domain.entities.flota import Flota

# Application imports
from src.application.use_cases.flota_use_cases import (
    CrearFlotaUseCase,
    ObtenerFlotaUseCase,
    ListarFlotasUseCase,
    AgregarTransportistaAFlotaUseCase,
    AgregarVehiculoAFlotaUseCase,
    ObtenerEstadisticasFlotaUseCase
)

# Infrastructure imports
from src.infrastructure.repositories.flota_repository import InMemoryFlotaRepository

# Dependency injection
def get_flota_repository() -> InMemoryFlotaRepository:
    return InMemoryFlotaRepository()

def get_crear_flota_use_case(repo: InMemoryFlotaRepository = Depends(get_flota_repository)) -> CrearFlotaUseCase:
    return CrearFlotaUseCase(repo)

def get_obtener_flota_use_case(repo: InMemoryFlotaRepository = Depends(get_flota_repository)) -> ObtenerFlotaUseCase:
    return ObtenerFlotaUseCase(repo)

def get_listar_flotas_use_case(repo: InMemoryFlotaRepository = Depends(get_flota_repository)) -> ListarFlotasUseCase:
    return ListarFlotasUseCase(repo)

# Pydantic models for API
class CrearFlotaRequest(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class AgregarTransportistaRequest(BaseModel):
    transportista_id: str

class AgregarVehiculoRequest(BaseModel):
    vehiculo_id: str

# Router
router = APIRouter(prefix="/api/v1/flota", tags=["flota"])

@router.post("/", response_model=Flota)
async def crear_flota(
    request: CrearFlotaRequest,
    use_case: CrearFlotaUseCase = Depends(get_crear_flota_use_case)
):
    """Create a new fleet"""
    return use_case.execute(request.nombre, request.descripcion)

@router.get("/{flota_id}", response_model=Flota)
async def obtener_flota(
    flota_id: str,
    use_case: ObtenerFlotaUseCase = Depends(get_obtener_flota_use_case)
):
    """Get a fleet by ID"""
    flota = use_case.execute(flota_id)
    if not flota:
        raise HTTPException(status_code=404, detail="Flota no encontrada")
    return flota

@router.get("/", response_model=List[Flota])
async def listar_flotas(
    solo_activas: bool = True,
    use_case: ListarFlotasUseCase = Depends(get_listar_flotas_use_case)
):
    """List all fleets"""
    return use_case.execute(solo_activas)

@router.post("/{flota_id}/transportista")
async def agregar_transportista_a_flota(
    flota_id: str,
    request: AgregarTransportistaRequest,
    use_case: AgregarTransportistaAFlotaUseCase = Depends(lambda: AgregarTransportistaAFlotaUseCase(InMemoryFlotaRepository()))
):
    """Add a transporter to a fleet"""
    success = use_case.execute(flota_id, request.transportista_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flota no encontrada")
    return {"message": "Transportista agregado exitosamente"}

@router.post("/{flota_id}/vehiculo")
async def agregar_vehiculo_a_flota(
    flota_id: str,
    request: AgregarVehiculoRequest,
    use_case: AgregarVehiculoAFlotaUseCase = Depends(lambda: AgregarVehiculoAFlotaUseCase(InMemoryFlotaRepository()))
):
    """Add a vehicle to a fleet"""
    success = use_case.execute(flota_id, request.vehiculo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flota no encontrada")
    return {"message": "Vehículo agregado exitosamente"}

@router.get("/{flota_id}/estadisticas")
async def obtener_estadisticas_flota(
    flota_id: str,
    use_case: ObtenerEstadisticasFlotaUseCase = Depends(lambda: ObtenerEstadisticasFlotaUseCase(InMemoryFlotaRepository()))
):
    """Get fleet statistics"""
    stats = use_case.execute(flota_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Flota no encontrada")
    return stats