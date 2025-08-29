"""VehiculoDTO - Data Transfer Object

DTO para transferir datos de Vehiculo entre capas.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class VehiculoDTO(BaseModel):
    """DTO para Vehiculo."""

    id: UUID
    matricula: str  # Representamos la matrícula como string para la API
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    anio: int = Field(..., ge=1900, le=datetime.now().year + 1)
    capacidad_carga_kg: float = Field(..., gt=0)
    tipo_vehiculo: str = Field(..., min_length=1, max_length=50)
    fecha_matriculacion: date
    fecha_ultima_revision: Optional[date] = None
    kilometraje_actual: float = Field(default=0, ge=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    necesita_revision: bool
    antiguedad_anios: int

    class Config:
        """Configuración Pydantic."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class CrearVehiculoDTO(BaseModel):
    """DTO para crear un nuevo vehículo."""

    matricula: str = Field(..., min_length=1, max_length=10)
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    anio: int = Field(..., ge=1900, le=datetime.now().year + 1)
    capacidad_carga_kg: float = Field(..., gt=0)
    tipo_vehiculo: str = Field(..., min_length=1, max_length=50)
    fecha_matriculacion: date
    fecha_ultima_revision: Optional[date] = None
    kilometraje_actual: Optional[float] = Field(default=0, ge=0)


class ActualizarVehiculoDTO(BaseModel):
    """DTO para actualizar un vehículo existente."""

    marca: Optional[str] = Field(None, min_length=1, max_length=50)
    modelo: Optional[str] = Field(None, min_length=1, max_length=50)
    capacidad_carga_kg: Optional[float] = Field(None, gt=0)
    tipo_vehiculo: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_ultima_revision: Optional[date] = None
    kilometraje_actual: Optional[float] = Field(None, ge=0)
    activo: Optional[bool] = None


class VehiculoResumenDTO(BaseModel):
    """DTO con información resumida de Vehiculo."""

    id: UUID
    matricula: str
    marca: str
    modelo: str
    tipo_vehiculo: str
    activo: bool
    necesita_revision: bool

    class Config:
        """Configuración Pydantic."""
        json_encoders = {
            UUID: lambda v: str(v)
        }


class ActualizarKilometrajeDTO(BaseModel):
    """DTO para actualizar el kilometraje del vehículo."""

    kilometraje_actual: float = Field(..., ge=0)


class RegistrarRevisionDTO(BaseModel):
    """DTO para registrar una revisión del vehículo."""

    fecha_revision: date
