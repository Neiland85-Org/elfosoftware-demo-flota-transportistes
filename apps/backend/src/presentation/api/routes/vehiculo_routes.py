"""
API routes for vehicle management
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Domain imports
from src.domain.entities.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo

# Application imports
from src.application.use_cases.vehiculo_use_cases import (
    CrearVehiculoUseCase,
    ObtenerVehiculoUseCase,
    ListarVehiculosUseCase,
    ActualizarVehiculoUseCase,
    CambiarEstadoVehiculoUseCase,
    AsignarVehiculoAFlotaUseCase,
    RemoverVehiculoDeFlotaUseCase,
    EliminarVehiculoUseCase
)

# Infrastructure imports
from src.infrastructure.repositories.vehiculo_repository import SQLAlchemyVehiculoRepository
from src.infrastructure.persistence.session import get_db

# Dependency injection
def get_vehiculo_repository(db = Depends(get_db)) -> SQLAlchemyVehiculoRepository:
    return SQLAlchemyVehiculoRepository(db)

def get_crear_vehiculo_use_case(repo = Depends(get_vehiculo_repository)) -> CrearVehiculoUseCase:
    return CrearVehiculoUseCase(repo)

def get_obtener_vehiculo_use_case(repo = Depends(get_vehiculo_repository)) -> ObtenerVehiculoUseCase:
    return ObtenerVehiculoUseCase(repo)

def get_listar_vehiculos_use_case(repo = Depends(get_vehiculo_repository)) -> ListarVehiculosUseCase:
    return ListarVehiculosUseCase(repo)

def get_actualizar_vehiculo_use_case(repo = Depends(get_vehiculo_repository)) -> ActualizarVehiculoUseCase:
    return ActualizarVehiculoUseCase(repo)

def get_cambiar_estado_use_case(repo = Depends(get_vehiculo_repository)) -> CambiarEstadoVehiculoUseCase:
    return CambiarEstadoVehiculoUseCase(repo)

def get_asignar_flota_use_case(repo = Depends(get_vehiculo_repository)) -> AsignarVehiculoAFlotaUseCase:
    return AsignarVehiculoAFlotaUseCase(repo)

def get_remover_flota_use_case(repo = Depends(get_vehiculo_repository)) -> RemoverVehiculoDeFlotaUseCase:
    return RemoverVehiculoDeFlotaUseCase(repo)

def get_eliminar_vehiculo_use_case(repo = Depends(get_vehiculo_repository)) -> EliminarVehiculoUseCase:
    return EliminarVehiculoUseCase(repo)

# Pydantic models for API
class CrearVehiculoRequest(BaseModel):
    matricula: str = Field(..., description="Vehicle license plate", min_length=1, max_length=20)
    marca: str = Field(..., description="Vehicle brand", min_length=1, max_length=50)
    modelo: str = Field(..., description="Vehicle model", min_length=1, max_length=50)
    tipo: TipoVehiculo = Field(..., description="Vehicle type")
    capacidad_carga: float = Field(..., description="Load capacity in kg", gt=0)
    fecha_matriculacion: datetime = Field(..., description="Registration date")
    fecha_ultimo_mantenimiento: Optional[datetime] = Field(None, description="Last maintenance date")
    kilometraje: int = Field(default=0, description="Current mileage in km", ge=0)

class ActualizarVehiculoRequest(BaseModel):
    matricula: Optional[str] = Field(None, description="Vehicle license plate", min_length=1, max_length=20)
    marca: Optional[str] = Field(None, description="Vehicle brand", min_length=1, max_length=50)
    modelo: Optional[str] = Field(None, description="Vehicle model", min_length=1, max_length=50)
    tipo: Optional[TipoVehiculo] = Field(None, description="Vehicle type")
    capacidad_carga: Optional[float] = Field(None, description="Load capacity in kg", gt=0)
    fecha_ultimo_mantenimiento: Optional[datetime] = Field(None, description="Last maintenance date")
    kilometraje: Optional[int] = Field(None, description="Current mileage in km", ge=0)

class CambiarEstadoRequest(BaseModel):
    estado: EstadoVehiculo = Field(..., description="New vehicle status")

class AsignarFlotaRequest(BaseModel):
    flota_id: str = Field(..., description="Fleet ID to assign the vehicle to")

# Router
router = APIRouter(prefix="/api/v1/vehiculos", tags=["vehículos"])

@router.post("/", response_model=Vehiculo, status_code=201)
async def crear_vehiculo(
    request: CrearVehiculoRequest,
    use_case: CrearVehiculoUseCase = Depends(get_crear_vehiculo_use_case)
):
    """Create a new vehicle"""
    try:
        vehiculo = use_case.execute(
            matricula=request.matricula,
            marca=request.marca,
            modelo=request.modelo,
            tipo=request.tipo,
            capacidad_carga=request.capacidad_carga,
            fecha_matriculacion=request.fecha_matriculacion,
            fecha_ultimo_mantenimiento=request.fecha_ultimo_mantenimiento,
            kilometraje=request.kilometraje
        )
        return vehiculo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating vehicle: {str(e)}")

@router.get("/{vehiculo_id}", response_model=Vehiculo)
async def obtener_vehiculo(
    vehiculo_id: str,
    use_case: ObtenerVehiculoUseCase = Depends(get_obtener_vehiculo_use_case)
):
    """Get a vehicle by ID"""
    vehiculo = use_case.execute(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehiculo

@router.get("/", response_model=List[Vehiculo])
async def listar_vehiculos(
    flota_id: Optional[str] = None,
    estado: Optional[str] = None,
    disponibles: bool = False,
    use_case: ListarVehiculosUseCase = Depends(get_listar_vehiculos_use_case)
):
    """List vehicles with optional filters"""
    vehiculos = use_case.execute(
        flota_id=flota_id,
        estado=estado,
        solo_disponibles=disponibles
    )
    return vehiculos

@router.put("/{vehiculo_id}", response_model=Vehiculo)
async def actualizar_vehiculo(
    vehiculo_id: str,
    request: ActualizarVehiculoRequest,
    use_case: ActualizarVehiculoUseCase = Depends(get_actualizar_vehiculo_use_case)
):
    """Update a vehicle"""
    # Convert request to dict, excluding None values
    update_data = {k: v for k, v in request.dict().items() if v is not None}

    vehiculo = use_case.execute(vehiculo_id, **update_data)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehiculo

@router.patch("/{vehiculo_id}/estado", response_model=Vehiculo)
async def cambiar_estado_vehiculo(
    vehiculo_id: str,
    request: CambiarEstadoRequest,
    use_case: CambiarEstadoVehiculoUseCase = Depends(get_cambiar_estado_use_case)
):
    """Change vehicle status"""
    vehiculo = use_case.execute(vehiculo_id, request.estado)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehiculo

@router.patch("/{vehiculo_id}/flota", response_model=Vehiculo)
async def asignar_vehiculo_a_flota(
    vehiculo_id: str,
    request: AsignarFlotaRequest,
    use_case: AsignarVehiculoAFlotaUseCase = Depends(get_asignar_flota_use_case)
):
    """Assign vehicle to a fleet"""
    vehiculo = use_case.execute(vehiculo_id, request.flota_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehiculo

@router.delete("/{vehiculo_id}/flota", response_model=Vehiculo)
async def remover_vehiculo_de_flota(
    vehiculo_id: str,
    use_case: RemoverVehiculoDeFlotaUseCase = Depends(get_remover_flota_use_case)
):
    """Remove vehicle from its current fleet"""
    vehiculo = use_case.execute(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehiculo

@router.delete("/{vehiculo_id}", status_code=204)
async def eliminar_vehiculo(
    vehiculo_id: str,
    use_case: EliminarVehiculoUseCase = Depends(get_eliminar_vehiculo_use_case)
):
    """Delete a vehicle"""
    success = use_case.execute(vehiculo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
