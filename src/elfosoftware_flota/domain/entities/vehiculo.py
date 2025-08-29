"""Vehiculo Entity

Entidad que representa un vehículo en el sistema de flota.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from elfosoftware_flota.domain.value_objects.matricula import Matricula


class Vehiculo(BaseModel):
    """Entidad Vehiculo."""

    id: UUID = Field(default_factory=uuid4)
    matricula: Matricula
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    anio: int = Field(..., ge=1900, le=2030)
    capacidad_carga_kg: float = Field(..., gt=0)
    tipo_vehiculo: str = Field(..., min_length=1, max_length=50)  # camión, furgoneta, etc.
    fecha_matriculacion: date
    fecha_ultima_revision: Optional[date] = None
    kilometraje_actual: float = Field(default=0, ge=0)
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
    def necesita_revision(self) -> bool:
        """Verifica si el vehículo necesita revisión (cada 6 meses)."""
        if self.fecha_ultima_revision is None:
            return True

        # Calcular si han pasado más de 6 meses desde la última revisión
        from dateutil.relativedelta import relativedelta
        seis_meses_despues = self.fecha_ultima_revision + relativedelta(months=6)
        return date.today() > seis_meses_despues

    @property
    def antiguedad_anios(self) -> int:
        """Calcula la antigüedad del vehículo en años."""
        return date.today().year - self.fecha_matriculacion.year

    def actualizar_kilometraje(self, nuevo_kilometraje: float) -> None:
        """Actualiza el kilometraje del vehículo."""
        if nuevo_kilometraje < self.kilometraje_actual:
            raise ValueError("El nuevo kilometraje no puede ser menor al actual")

        self.kilometraje_actual = nuevo_kilometraje
        self.fecha_actualizacion = datetime.now()

    def registrar_revision(self, fecha_revision: date) -> None:
        """Registra una nueva revisión del vehículo."""
        if fecha_revision > date.today():
            raise ValueError("La fecha de revisión no puede ser futura")

        self.fecha_ultima_revision = fecha_revision
        self.fecha_actualizacion = datetime.now()

    def actualizar_datos(
        self,
        marca: Optional[str] = None,
        modelo: Optional[str] = None,
        capacidad_carga_kg: Optional[float] = None,
        tipo_vehiculo: Optional[str] = None
    ) -> None:
        """Actualiza los datos del vehículo."""
        if marca is not None:
            self.marca = marca
        if modelo is not None:
            self.modelo = modelo
        if capacidad_carga_kg is not None:
            self.capacidad_carga_kg = capacidad_carga_kg
        if tipo_vehiculo is not None:
            self.tipo_vehiculo = tipo_vehiculo

        self.fecha_actualizacion = datetime.now()

    def desactivar(self) -> None:
        """Desactiva el vehículo."""
        self.activo = False
        self.fecha_actualizacion = datetime.now()

    def activar(self) -> None:
        """Activa el vehículo."""
        self.activo = True
        self.fecha_actualizacion = datetime.now()
