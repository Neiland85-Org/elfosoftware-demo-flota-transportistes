"""ITransportistaRepository Interface

Interfaz del repositorio para la entidad Transportista.
Define las operaciones de persistencia para Transportista.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.transportista import Transportista


class ITransportistaRepository(ABC):
    """Interfaz para el repositorio de Transportista."""

    @abstractmethod
    async def save(self, transportista: Transportista) -> None:
        """Guarda un transportista en el repositorio."""
        pass

    @abstractmethod
    async def find_by_id(self, transportista_id: UUID) -> Optional[Transportista]:
        """Busca un transportista por su ID."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Transportista]:
        """Busca un transportista por su email."""
        pass

    @abstractmethod
    async def find_by_numero_licencia(self, numero_licencia: str) -> Optional[Transportista]:
        """Busca un transportista por su número de licencia."""
        pass

    @abstractmethod
    async def find_all_activos(self) -> List[Transportista]:
        """Retorna todos los transportistas activos."""
        pass

    @abstractmethod
    async def find_by_licencia_vigente(self, vigente: bool = True) -> List[Transportista]:
        """Busca transportistas con licencia vigente o expirada."""
        pass

    @abstractmethod
    async def find_by_edad_rango(self, edad_min: int, edad_max: int) -> List[Transportista]:
        """Busca transportistas dentro de un rango de edad."""
        pass

    @abstractmethod
    async def delete(self, transportista_id: UUID) -> None:
        """Elimina un transportista del repositorio."""
        pass

    @abstractmethod
    async def exists(self, transportista_id: UUID) -> bool:
        """Verifica si existe un transportista con el ID dado."""
        pass

    @abstractmethod
    async def count_activos(self) -> int:
        """Cuenta el número de transportistas activos."""
        pass
