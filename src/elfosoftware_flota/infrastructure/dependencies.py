"""Dependencies

Funciones de dependencia para inyección de dependencias.
Permite cambiar fácilmente entre implementaciones de repositorios.
"""

from typing import Optional

from elfosoftware_flota.domain.repositories.i_vehiculo_repository import IVehiculoRepository
from elfosoftware_flota.domain.repositories.i_transportista_repository import ITransportistaRepository
from elfosoftware_flota.infrastructure.repositories.inmemory_vehicle_repository import InMemoryVehiculoRepository
from elfosoftware_flota.infrastructure.repositories.inmemory_transportista_repository import InMemoryTransportistaRepository


# Instancias globales de repositorios (en producción usaríamos un contenedor de DI)
_vehiculo_repository: Optional[IVehiculoRepository] = None
_transportista_repository: Optional[ITransportistaRepository] = None


async def get_vehiculo_repository() -> IVehiculoRepository:
    """Obtiene la instancia del repositorio de vehículos."""
    global _vehiculo_repository

    if _vehiculo_repository is None:
        _vehiculo_repository = InMemoryVehiculoRepository()
        # Inicializar con datos de prueba
        await _vehiculo_repository._initialize_test_data()

    return _vehiculo_repository


async def get_transportista_repository() -> ITransportistaRepository:
    """Obtiene la instancia del repositorio de transportistas."""
    global _transportista_repository

    if _transportista_repository is None:
        _transportista_repository = InMemoryTransportistaRepository()
        # Inicializar con datos de prueba
        await _transportista_repository._initialize_test_data()

    return _transportista_repository
