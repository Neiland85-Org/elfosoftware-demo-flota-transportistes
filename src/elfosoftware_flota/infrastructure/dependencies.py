"""Dependencies

Funciones de dependencia para inyección de dependencias.
Permite cambiar fácilmente entre implementaciones de repositorios.
"""

from typing import Optional

from elfosoftware_flota.domain.repositories.i_vehiculo_repository import IVehiculoRepository
from elfosoftware_flota.infrastructure.repositories.inmemory_vehicle_repository import InMemoryVehiculoRepository


# Instancia global del repositorio (en producción usaríamos un contenedor de DI)
_vehiculo_repository: Optional[IVehiculoRepository] = None


async def get_vehiculo_repository() -> IVehiculoRepository:
    """Obtiene la instancia del repositorio de vehículos."""
    global _vehiculo_repository

    if _vehiculo_repository is None:
        _vehiculo_repository = InMemoryVehiculoRepository()
        # Inicializar con datos de prueba
        await _vehiculo_repository._initialize_test_data()

    return _vehiculo_repository
