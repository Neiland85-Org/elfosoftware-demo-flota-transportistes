"""FlotaDTO - Data Transfer Object

DTO para transferir datos de Flota entre capas.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FlotaDTO(BaseModel):
    """DTO para Flota."""

    id: UUID
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    transportistas_ids: List[UUID] = Field(default_factory=list)
    vehiculos_ids: List[UUID] = Field(default_factory=list)
    activo: bool = Field(default=True)
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        """Configuración Pydantic."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class CrearFlotaDTO(BaseModel):
    """DTO para crear una nueva flota."""

    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)


class ActualizarFlotaDTO(BaseModel):
    """DTO para actualizar una flota existente."""

    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    activo: Optional[bool] = None


class FlotaResumenDTO(BaseModel):
    """DTO con información resumida de Flota."""

    id: UUID
    nombre: str
    descripcion: Optional[str]
    cantidad_transportistas: int
    cantidad_vehiculos: int
    activo: bool
    fecha_creacion: datetime

    class Config:
        """Configuración Pydantic."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
