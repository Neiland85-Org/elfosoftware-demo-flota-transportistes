"""
In-memory repository implementations
"""
from typing import List, Optional, Dict
from src.domain.entities.flota import Flota
from src.domain.repositories.interfaces import FlotaRepository

class InMemoryFlotaRepository(FlotaRepository):
    """In-memory implementation of FlotaRepository"""

    def __init__(self):
        self._flotas: Dict[str, Flota] = {}

    def save(self, flota: Flota) -> None:
        """Save a fleet"""
        self._flotas[flota.id] = flota

    def find_by_id(self, flota_id: str) -> Optional[Flota]:
        """Find a fleet by ID"""
        return self._flotas.get(flota_id)

    def find_all(self) -> List[Flota]:
        """Find all fleets"""
        return list(self._flotas.values())

    def find_by_activa(self, activa: bool = True) -> List[Flota]:
        """Find fleets by active status"""
        return [flota for flota in self._flotas.values() if flota.activo == activa]

    def delete(self, flota_id: str) -> None:
        """Delete a fleet by ID"""
        if flota_id in self._flotas:
            del self._flotas[flota_id]