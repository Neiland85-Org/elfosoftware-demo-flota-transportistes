"""Transportista Entity

Entidad que representa a un transportista (conductor) en el sistema.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr


class Transportista(BaseModel):
    """Entidad Transportista."""

    id: UUID = Field(default_factory=uuid4)
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: str = Field(..., min_length=1, max_length=20)
    fecha_nacimiento: date
    numero_licencia: str = Field(..., min_length=1, max_length=50)
    fecha_expiracion_licencia: date
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_actualizacion: datetime = Field(default_factory=datetime.now)

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    }

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del transportista."""
        return f"{self.nombre} {self.apellido}"

    @property
    def licencia_vigente(self) -> bool:
        """Verifica si la licencia del transportista está vigente."""
        return self.fecha_expiracion_licencia > date.today()

    @property
    def edad(self) -> int:
        """Calcula la edad del transportista."""
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def actualizar_datos(
        self,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        email: Optional[EmailStr] = None,
        telefono: Optional[str] = None,
        numero_licencia: Optional[str] = None,
        fecha_expiracion_licencia: Optional[date] = None
    ) -> None:
        """Actualiza los datos del transportista."""
        if nombre is not None:
            self.nombre = nombre
        if apellido is not None:
            self.apellido = apellido
        if email is not None:
            self.email = email
        if telefono is not None:
            self.telefono = telefono
        if numero_licencia is not None:
            self.numero_licencia = numero_licencia
        if fecha_expiracion_licencia is not None:
            self.fecha_expiracion_licencia = fecha_expiracion_licencia

        self.fecha_actualizacion = datetime.now()

    def desactivar(self) -> None:
        """Desactiva al transportista."""
        self.activo = False
        self.fecha_actualizacion = datetime.now()

    def activar(self) -> None:
        """Activa al transportista."""
        self.activo = True
        self.fecha_actualizacion = datetime.now()
