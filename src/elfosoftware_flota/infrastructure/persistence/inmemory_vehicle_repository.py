"""InMemoryVehicleRepository

Implementación en memoria del repositorio de Vehiculo para desarrollo y testing.
"""

from typing import Dict, List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.vehiculo import Vehiculo
from elfosoftware_flota.domain.repositories.i_vehiculo_repository import IVehiculoRepository
from elfosoftware_flota.domain.value_objects.matricula import Matricula


class InMemoryVehicleRepository(IVehiculoRepository):
    """Implementación en memoria del repositorio de Vehiculo."""

    def __init__(self) -> None:
        """Inicializa el repositorio con un diccionario vacío."""
        self._vehicles: Dict[UUID, Vehiculo] = {}
        self._matricula_index: Dict[str, UUID] = {}

    async def save(self, vehiculo: Vehiculo) -> None:
        """Guarda un vehículo en el repositorio."""
        self._vehicles[vehiculo.id] = vehiculo
        self._matricula_index[str(vehiculo.matricula)] = vehiculo.id

    async def find_by_id(self, vehiculo_id: UUID) -> Optional[Vehiculo]:
        """Busca un vehículo por su ID."""
        return self._vehicles.get(vehiculo_id)

    async def find_by_matricula(self, matricula: Matricula) -> Optional[Vehiculo]:
        """Busca un vehículo por su matrícula."""
        vehicle_id = self._matricula_index.get(str(matricula))
        if vehicle_id:
            return self._vehicles.get(vehicle_id)
        return None

    async def find_all_activos(self) -> List[Vehiculo]:
        """Retorna todos los vehículos activos."""
        return [v for v in self._vehicles.values() if v.activo]

    async def find_by_marca(self, marca: str) -> List[Vehiculo]:
        """Busca vehículos por marca."""
        return [v for v in self._vehicles.values() if v.marca.lower() == marca.lower()]

    async def find_by_tipo(self, tipo_vehiculo: str) -> List[Vehiculo]:
        """Busca vehículos por tipo."""
        return [v for v in self._vehicles.values() if v.tipo_vehiculo.lower() == tipo_vehiculo.lower()]

    async def find_necesitan_revision(self) -> List[Vehiculo]:
        """Busca vehículos que necesitan revisión."""
        return [v for v in self._vehicles.values() if v.necesita_revision]

    async def find_by_capacidad_minima(self, capacidad_minima: float) -> List[Vehiculo]:
        """Busca vehículos con capacidad de carga mínima."""
        return [v for v in self._vehicles.values() if v.capacidad_carga_kg >= capacidad_minima]

    async def find_by_anio_rango(self, anio_min: int, anio_max: int) -> List[Vehiculo]:
        """Busca vehículos dentro de un rango de años."""
        return [v for v in self._vehicles.values() if anio_min <= v.anio <= anio_max]

    async def delete(self, vehiculo_id: UUID) -> None:
        """Elimina un vehículo del repositorio."""
        if vehiculo_id in self._vehicles:
            matricula = str(self._vehicles[vehiculo_id].matricula)
            del self._vehicles[vehiculo_id]
            if matricula in self._matricula_index:
                del self._matricula_index[matricula]

    async def exists(self, vehiculo_id: UUID) -> bool:
        """Verifica si existe un vehículo con el ID dado."""
        return vehiculo_id in self._vehicles

    async def exists_by_matricula(self, matricula: Matricula) -> bool:
        """Verifica si existe un vehículo con la matrícula dada."""
        return str(matricula) in self._matricula_index

    async def count_activos(self) -> int:
        """Cuenta el número de vehículos activos."""
        return len([v for v in self._vehicles.values() if v.activo])

    # Métodos adicionales para testing y desarrollo
    async def clear(self) -> None:
        """Limpia todos los datos del repositorio (útil para testing)."""
        self._vehicles.clear()
        self._matricula_index.clear()

    async def get_all(self) -> List[Vehiculo]:
        """Retorna todos los vehículos (incluyendo inactivos)."""
        return list(self._vehicles.values())
