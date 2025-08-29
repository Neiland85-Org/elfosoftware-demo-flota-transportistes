"""IFlotaRepository Interface

Interfaz del repositorio para la entidad Flota.
Define las operaciones de persistencia para el Aggregate Root Flota.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.flota import Flota


class IFlotaRepository(ABC):
    """Interfaz para el repositorio de Flota."""

    @abstractmethod
    async def save(self, flota: Flota) -> None:
        """Guarda una flota en el repositorio."""
        pass

    @abstractmethod
    async def find_by_id(self, flota_id: UUID) -> Optional[Flota]:
        """Busca una flota por su ID."""
        pass

    @abstractmethod
    async def find_by_nombre(self, nombre: str) -> Optional[Flota]:
        """Busca una flota por su nombre."""
        pass

    @abstractmethod
    async def find_all_activas(self) -> List[Flota]:
        """Retorna todas las flotas activas."""
        pass

    @abstractmethod
    async def find_by_transportista_id(self, transportista_id: UUID) -> List[Flota]:
        """Busca flotas que contengan un transportista específico."""
        pass

    @abstractmethod
    async def find_by_vehiculo_id(self, vehiculo_id: UUID) -> List[Flota]:
        """Busca flotas que contengan un vehículo específico."""
        pass

    @abstractmethod
    async def delete(self, flota_id: UUID) -> None:
        """Elimina una flota del repositorio."""
        pass

    @abstractmethod
    async def exists(self, flota_id: UUID) -> bool:
        """Verifica si existe una flota con el ID dado."""
        pass

    @abstractmethod
    async def count_activas(self) -> int:
        """Cuenta el número de flotas activas."""
        pass
