"""
Vehiculo entity
"""
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class TipoVehiculo(Enum):
    """Vehicle type enumeration"""
    CAMION = "camion"
    FURGONETA = "furgoneta"
    MOTOCICLETA = "motocicleta"
    TRAILER = "trailer"

class EstadoVehiculo(Enum):
    """Vehicle status enumeration"""
    DISPONIBLE = "disponible"
    EN_USO = "en_uso"
    EN_MANTENIMIENTO = "en_mantenimiento"
    FUERA_DE_SERVICIO = "fuera_de_servicio"

class Vehiculo(BaseModel):
    """Entity representing a vehicle"""
    id: str = Field(..., description="Unique identifier for the vehicle")
    matricula: str = Field(..., description="Vehicle license plate")
    marca: str = Field(..., description="Vehicle brand")
    modelo: str = Field(..., description="Vehicle model")
    tipo: TipoVehiculo = Field(..., description="Vehicle type")
    capacidad_carga: float = Field(..., description="Load capacity in kg")
    estado: EstadoVehiculo = Field(default=EstadoVehiculo.DISPONIBLE, description="Current vehicle status")
    fecha_matriculacion: datetime = Field(..., description="Registration date")
    fecha_ultimo_mantenimiento: Optional[datetime] = Field(None, description="Last maintenance date")
    kilometraje: int = Field(default=0, description="Current mileage in km")
    flota_id: Optional[str] = Field(None, description="ID of the fleet this vehicle belongs to")
    transportista_id: Optional[str] = Field(None, description="ID of the current driver")

    def asignar_a_flota(self, flota_id: str) -> None:
        """Assign vehicle to a fleet"""
        self.flota_id = flota_id

    def remover_de_flota(self) -> None:
        """Remove vehicle from current fleet"""
        self.flota_id = None

    def asignar_transportista(self, transportista_id: str) -> None:
        """Assign vehicle to a transporter"""
        self.transportista_id = transportista_id
        if self.estado == EstadoVehiculo.DISPONIBLE:
            self.estado = EstadoVehiculo.EN_USO

    def liberar_transportista(self) -> None:
        """Release vehicle from current transporter"""
        self.transportista_id = None
        if self.estado == EstadoVehiculo.EN_USO:
            self.estado = EstadoVehiculo.DISPONIBLE

    def cambiar_estado(self, nuevo_estado: EstadoVehiculo) -> None:
        """Change vehicle status"""
        self.estado = nuevo_estado

    def actualizar_kilometraje(self, nuevo_kilometraje: int) -> None:
        """Update vehicle mileage"""
        if nuevo_kilometraje >= self.kilometraje:
            self.kilometraje = nuevo_kilometraje

    def necesita_mantenimiento(self) -> bool:
        """Check if vehicle needs maintenance (simplified logic)"""
        if self.fecha_ultimo_mantenimiento:
            dias_desde_mantenimiento = (datetime.now() - self.fecha_ultimo_mantenimiento).days
            return dias_desde_mantenimiento > 90 or self.kilometraje > 50000
        return True

    def esta_disponible(self) -> bool:
        """Check if vehicle is available for use"""
        return (self.estado == EstadoVehiculo.DISPONIBLE and
                self.flota_id is not None and
                not self.necesita_mantenimiento())