"""
Carga entity
"""
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class TipoCarga(Enum):
    """Load type enumeration"""
    GENERAL = "general"
    FRAGIL = "fragil"
    PELIGROSA = "peligrosa"
    REFRIGERADA = "refrigerada"
    LIQUIDA = "liquida"
    A_GRANEL = "a_granel"

class EstadoCarga(Enum):
    """Load status enumeration"""
    PENDIENTE = "pendiente"
    EN_TRANSITO = "en_transito"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"
    PERDIDA = "perdida"

class Carga(BaseModel):
    """Entity representing a load/cargo"""
    id: str = Field(..., description="Unique identifier for the load")
    descripcion: str = Field(..., description="Load description")
    tipo: TipoCarga = Field(..., description="Load type")
    peso: float = Field(..., description="Load weight in kg")
    volumen: Optional[float] = Field(None, description="Load volume in m³")
    valor_declarado: Optional[float] = Field(None, description="Declared value in currency")
    estado: EstadoCarga = Field(default=EstadoCarga.PENDIENTE, description="Current load status")

    # Origen y destino
    origen: str = Field(..., description="Origin location")
    destino: str = Field(..., description="Destination location")

    # Fechas
    fecha_creacion: datetime = Field(default_factory=datetime.now, description="Creation date")
    fecha_salida: Optional[datetime] = Field(None, description="Departure date")
    fecha_entrega: Optional[datetime] = Field(None, description="Delivery date")

    # Asignaciones
    vehiculo_id: Optional[str] = Field(None, description="Assigned vehicle ID")
    transportista_id: Optional[str] = Field(None, description="Assigned transporter ID")
    flota_id: Optional[str] = Field(None, description="Assigned fleet ID")

    # Seguimiento
    coordenadas_actuales: Optional[str] = Field(None, description="Current GPS coordinates")
    ultima_actualizacion: Optional[datetime] = Field(None, description="Last status update")

    def asignar_vehiculo(self, vehiculo_id: str) -> None:
        """Assign load to a vehicle"""
        self.vehiculo_id = vehiculo_id

    def asignar_transportista(self, transportista_id: str) -> None:
        """Assign load to a transporter"""
        self.transportista_id = transportista_id

    def asignar_flota(self, flota_id: str) -> None:
        """Assign load to a fleet"""
        self.flota_id = flota_id

    def cambiar_estado(self, nuevo_estado: EstadoCarga) -> None:
        """Change load status"""
        self.estado = nuevo_estado
        self.ultima_actualizacion = datetime.now()

        if nuevo_estado == EstadoCarga.EN_TRANSITO and not self.fecha_salida:
            self.fecha_salida = datetime.now()
        elif nuevo_estado == EstadoCarga.ENTREGADA and not self.fecha_entrega:
            self.fecha_entrega = datetime.now()

    def actualizar_ubicacion(self, coordenadas: str) -> None:
        """Update current location"""
        self.coordenadas_actuales = coordenadas
        self.ultima_actualizacion = datetime.now()

    def calcular_tiempo_transito(self) -> Optional[int]:
        """Calculate transit time in hours"""
        if self.fecha_salida and self.fecha_entrega:
            tiempo = self.fecha_entrega - self.fecha_salida
            return int(tiempo.total_seconds() / 3600)
        return None

    def esta_en_transito(self) -> bool:
        """Check if load is in transit"""
        return self.estado == EstadoCarga.EN_TRANSITO

    def esta_entregada(self) -> bool:
        """Check if load has been delivered"""
        return self.estado == EstadoCarga.ENTREGADA