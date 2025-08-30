"""
Transportista entity
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class Transportista(BaseModel):
    """Entity representing a transporter/driver"""
    id: str = Field(..., description="Unique identifier for the transporter")
    nombre: str = Field(..., description="Transporter's full name")
    email: EmailStr = Field(..., description="Transporter's email address")
    telefono: Optional[str] = Field(None, description="Transporter's phone number")
    licencia: str = Field(..., description="Driver's license number")
    fecha_nacimiento: Optional[datetime] = Field(None, description="Birth date")
    fecha_contratacion: datetime = Field(default_factory=datetime.now, description="Hiring date")
    activo: bool = Field(default=True, description="Whether the transporter is active")
    flota_id: Optional[str] = Field(None, description="ID of the fleet this transporter belongs to")

    def asignar_a_flota(self, flota_id: str) -> None:
        """Assign transporter to a fleet"""
        self.flota_id = flota_id

    def remover_de_flota(self) -> None:
        """Remove transporter from current fleet"""
        self.flota_id = None

    def esta_disponible(self) -> bool:
        """Check if transporter is available for assignments"""
        return self.activo and self.flota_id is not None