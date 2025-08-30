"""
Domain entities for Flota Transportistes
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Flota(BaseModel):
    """Aggregate root for fleet management"""
    id: str = Field(..., description="Unique identifier for the fleet")
    nombre: str = Field(..., description="Fleet name")
    descripcion: Optional[str] = Field(None, description="Fleet description")
    transportistas: List[str] = Field(default_factory=list, description="List of transporter IDs")
    vehiculos: List[str] = Field(default_factory=list, description="List of vehicle IDs")
    fecha_creacion: datetime = Field(default_factory=datetime.now, description="Creation date")
    activo: bool = Field(default=True, description="Whether the fleet is active")

    def agregar_transportista(self, transportista_id: str) -> None:
        """Add a transporter to the fleet"""
        if transportista_id not in self.transportistas:
            self.transportistas.append(transportista_id)

    def remover_transportista(self, transportista_id: str) -> None:
        """Remove a transporter from the fleet"""
        if transportista_id in self.transportistas:
            self.transportistas.remove(transportista_id)

    def agregar_vehiculo(self, vehiculo_id: str) -> None:
        """Add a vehicle to the fleet"""
        if vehiculo_id not in self.vehiculos:
            self.vehiculos.append(vehiculo_id)

    def remover_vehiculo(self, vehiculo_id: str) -> None:
        """Remove a vehicle from the fleet"""
        if vehiculo_id in self.vehiculos:
            self.vehiculos.remove(vehiculo_id)

    def obtener_estadisticas(self) -> dict:
        """Get fleet statistics"""
        return {
            "total_transportistas": len(self.transportistas),
            "total_vehiculos": len(self.vehiculos),
            "activo": self.activo
        }