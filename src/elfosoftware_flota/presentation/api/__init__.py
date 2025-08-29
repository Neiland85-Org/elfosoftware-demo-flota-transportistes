"""API Layer

APIs REST con FastAPI:
- FlotaAPI: Endpoints para Flota
- TransportistaAPI: Endpoints para Transportista
- VehiculoAPI: Endpoints para Vehiculo
"""

from elfosoftware_flota.presentation.api.flota_api import flota_router
from elfosoftware_flota.presentation.api.transportista_api import transportista_router
from elfosoftware_flota.presentation.api.vehiculo_api import vehiculo_router

__all__ = ["flota_router", "transportista_router", "vehiculo_router"]
