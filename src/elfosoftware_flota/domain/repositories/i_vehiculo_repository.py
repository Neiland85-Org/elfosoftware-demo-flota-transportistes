"""IVehiculoRepository Interface

Interfaz del repositorio para la entidad Vehiculo.
Define las operaciones de persistencia para Vehiculo.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.vehiculo import Vehiculo
from elfosoftware_flota.domain.value_objects.matricula import Matricula


class IVehiculoRepository(ABC):
    """Interfaz para el repositorio de Vehiculo."""

    @abstractmethod
    async def save(self, vehiculo: Vehiculo) -> None:
        """Guarda un vehículo en el repositorio."""
        pass

    @abstractmethod
    async def find_by_id(self, vehiculo_id: UUID) -> Optional[Vehiculo]:
        """Busca un vehículo por su ID."""
        pass

    @abstractmethod
    async def find_by_matricula(self, matricula: Matricula) -> Optional[Vehiculo]:
        """Busca un vehículo por su matrícula."""
        pass

    @abstractmethod
    async def find_all_activos(self) -> List[Vehiculo]:
        """Retorna todos los vehículos activos."""
        pass

    @abstractmethod
    async def find_by_marca(self, marca: str) -> List[Vehiculo]:
        """Busca vehículos por marca."""
        pass

    @abstractmethod
    async def find_by_tipo(self, tipo_vehiculo: str) -> List[Vehiculo]:
        """Busca vehículos por tipo."""
        pass

    @abstractmethod
    async def find_necesitan_revision(self) -> List[Vehiculo]:
        """Busca vehículos que necesitan revisión."""
        pass

    @abstractmethod
    async def find_by_capacidad_minima(self, capacidad_minima: float) -> List[Vehiculo]:
        """Busca vehículos con capacidad de carga mínima."""
        pass

    @abstractmethod
    async def find_by_anio_rango(self, anio_min: int, anio_max: int) -> List[Vehiculo]:
        """Busca vehículos dentro de un rango de años."""
        pass

    @abstractmethod
    async def delete(self, vehiculo_id: UUID) -> None:
        """Elimina un vehículo del repositorio."""
        pass

    @abstractmethod
    async def exists(self, vehiculo_id: UUID) -> bool:
        """Verifica si existe un vehículo con el ID dado."""
        pass

    @abstractmethod
    async def exists_by_matricula(self, matricula: Matricula) -> bool:
        """Verifica si existe un vehículo con la matrícula dada."""
        pass

    @abstractmethod
    async def count_activos(self) -> int:
        """Cuenta el número de vehículos activos."""
        pass
