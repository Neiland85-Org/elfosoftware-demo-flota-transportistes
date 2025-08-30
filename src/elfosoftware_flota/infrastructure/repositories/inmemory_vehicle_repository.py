"""InMemoryVehiculoRepository

Implementación en memoria del repositorio de Vehiculo para desarrollo y testing.
"""

from typing import Dict, List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.vehiculo import Vehiculo
from elfosoftware_flota.domain.repositories.i_vehiculo_repository import IVehiculoRepository
from elfosoftware_flota.domain.value_objects.matricula import Matricula


class InMemoryVehiculoRepository(IVehiculoRepository):
    """Repositorio en memoria para Vehiculo."""

    def __init__(self):
        """Inicializa el repositorio con datos de ejemplo."""
        self._vehiculos: Dict[UUID, Vehiculo] = {}
        self._vehiculos_por_matricula: Dict[str, UUID] = {}

    async def save(self, vehiculo: Vehiculo) -> None:
        """Guarda un vehículo en el repositorio."""
        self._vehiculos[vehiculo.id] = vehiculo
        self._vehiculos_por_matricula[str(vehiculo.matricula)] = vehiculo.id

    async def find_by_id(self, vehiculo_id: UUID) -> Optional[Vehiculo]:
        """Busca un vehículo por su ID."""
        return self._vehiculos.get(vehiculo_id)

    async def find_by_matricula(self, matricula: Matricula) -> Optional[Vehiculo]:
        """Busca un vehículo por su matrícula."""
        vehiculo_id = self._vehiculos_por_matricula.get(str(matricula))
        if vehiculo_id:
            return self._vehiculos.get(vehiculo_id)
        return None

    async def find_all_activos(self) -> List[Vehiculo]:
        """Retorna todos los vehículos activos."""
        return [v for v in self._vehiculos.values() if v.activo]

    async def find_by_marca(self, marca: str) -> List[Vehiculo]:
        """Busca vehículos por marca."""
        return [v for v in self._vehiculos.values() if v.marca.lower() == marca.lower()]

    async def find_by_tipo(self, tipo_vehiculo: str) -> List[Vehiculo]:
        """Busca vehículos por tipo."""
        return [v for v in self._vehiculos.values() if v.tipo_vehiculo.lower() == tipo_vehiculo.lower()]

    async def find_necesitan_revision(self) -> List[Vehiculo]:
        """Busca vehículos que necesitan revisión."""
        return [v for v in self._vehiculos.values() if v.necesita_revision]

    async def find_by_capacidad_minima(self, capacidad_minima: float) -> List[Vehiculo]:
        """Busca vehículos con capacidad de carga mínima."""
        return [v for v in self._vehiculos.values() if v.capacidad_carga_kg >= capacidad_minima]

    async def find_by_anio_rango(self, anio_min: int, anio_max: int) -> List[Vehiculo]:
        """Busca vehículos dentro de un rango de años."""
        return [v for v in self._vehiculos.values() if anio_min <= v.anio <= anio_max]

    async def delete(self, vehiculo_id: UUID) -> None:
        """Elimina un vehículo del repositorio."""
        vehiculo = self._vehiculos.get(vehiculo_id)
        if vehiculo:
            del self._vehiculos[vehiculo_id]
            del self._vehiculos_por_matricula[str(vehiculo.matricula)]

    async def exists(self, vehiculo_id: UUID) -> bool:
        """Verifica si existe un vehículo con el ID dado."""
        return vehiculo_id in self._vehiculos

    async def exists_by_matricula(self, matricula: Matricula) -> bool:
        """Verifica si existe un vehículo con la matrícula dada."""
        return str(matricula) in self._vehiculos_por_matricula

    async def count_activos(self) -> int:
        """Cuenta el número de vehículos activos."""
        return len([v for v in self._vehiculos.values() if v.activo])

    # Método auxiliar para inicializar datos de prueba
    async def _initialize_test_data(self) -> None:
        """Inicializa datos de prueba."""
        from datetime import date

        # Crear algunos vehículos de ejemplo
        vehiculo1 = Vehiculo(
            matricula=Matricula("ABC123"),
            marca="Mercedes-Benz",
            modelo="Actros",
            anio=2020,
            capacidad_carga_kg=25000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2020, 1, 15),
            fecha_ultima_revision=date(2023, 6, 15),
            kilometraje_actual=150000.0
        )

        vehiculo2 = Vehiculo(
            matricula=Matricula("XYZ789"),
            marca="Volvo",
            modelo="FH16",
            anio=2019,
            capacidad_carga_kg=30000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2019, 3, 20),
            fecha_ultima_revision=date(2023, 8, 10),
            kilometraje_actual=180000.0
        )

        vehiculo3 = Vehiculo(
            matricula=Matricula("DEF456"),
            marca="Iveco",
            modelo="Stralis",
            anio=2021,
            capacidad_carga_kg=20000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2021, 5, 10),
            fecha_ultima_revision=date(2023, 4, 5),
            kilometraje_actual=120000.0
        )

        await self.save(vehiculo1)
        await self.save(vehiculo2)
        await self.save(vehiculo3)
