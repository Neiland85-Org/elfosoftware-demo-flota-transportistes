"""Flota Entity - Aggregate Root

Entidad principal del dominio Flota Transportistes.
Representa una flota completa de vehículos y transportistas.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Flota(BaseModel):
    """Entidad Flota - Aggregate Root del dominio."""

    id: UUID = Field(default_factory=uuid4)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    transportistas_ids: List[UUID] = Field(default_factory=list)
    vehiculos_ids: List[UUID] = Field(default_factory=list)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    }

    def agregar_transportista(self, transportista_id: UUID) -> None:
        """Agrega un transportista a la flota."""
        if transportista_id not in self.transportistas_ids:
            self.transportistas_ids.append(transportista_id)
            self.fecha_actualizacion = datetime.now()

    def remover_transportista(self, transportista_id: UUID) -> None:
        """Remueve un transportista de la flota."""
        if transportista_id in self.transportistas_ids:
            self.transportistas_ids.remove(transportista_id)
            self.fecha_actualizacion = datetime.now()

    def agregar_vehiculo(self, vehiculo_id: UUID) -> None:
        """Agrega un vehículo a la flota."""
        if vehiculo_id not in self.vehiculos_ids:
            self.vehiculos_ids.append(vehiculo_id)
            self.fecha_actualizacion = datetime.now()

    def remover_vehiculo(self, vehiculo_id: UUID) -> None:
        """Remueve un vehículo de la flota."""
        if vehiculo_id in self.vehiculos_ids:
            self.vehiculos_ids.remove(vehiculo_id)
            self.fecha_actualizacion = datetime.now()

    def desactivar(self) -> None:
        """Desactiva la flota."""
        self.activo = False
        self.fecha_actualizacion = datetime.now()

    def activar(self) -> None:
        """Activa la flota."""
        self.activo = True
        self.fecha_actualizacion = datetime.now()

    @property
    def cantidad_transportistas(self) -> int:
        """Retorna la cantidad de transportistas en la flota."""
        return len(self.transportistas_ids)

    @property
    def cantidad_vehiculos(self) -> int:
        """Retorna la cantidad de vehículos en la flota."""
        return len(self.vehiculos_ids)
