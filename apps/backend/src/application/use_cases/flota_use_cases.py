"""
Use cases for fleet management
"""
from typing import List, Optional
from src.domain.entities.flota import Flota
from src.domain.repositories.interfaces import FlotaRepository

class CrearFlotaUseCase:
    """Use case for creating a new fleet"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, nombre: str, descripcion: Optional[str] = None) -> Flota:
        """Create a new fleet"""
        # Generate a simple ID (in production, use UUID or similar)
        flota_id = f"FLT{len(self.flota_repository.find_all()) + 1:03d}"

        flota = Flota(
            id=flota_id,
            nombre=nombre,
            descripcion=descripcion
        )

        self.flota_repository.save(flota)
        return flota

class ObtenerFlotaUseCase:
    """Use case for getting a fleet by ID"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, flota_id: str) -> Optional[Flota]:
        """Get a fleet by ID"""
        return self.flota_repository.find_by_id(flota_id)

class ListarFlotasUseCase:
    """Use case for listing all fleets"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, solo_activas: bool = True) -> List[Flota]:
        """List all fleets"""
        if solo_activas:
            return self.flota_repository.find_by_activa(True)
        return self.flota_repository.find_all()

class AgregarTransportistaAFlotaUseCase:
    """Use case for adding a transporter to a fleet"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, flota_id: str, transportista_id: str) -> bool:
        """Add a transporter to a fleet"""
        flota = self.flota_repository.find_by_id(flota_id)
        if not flota:
            return False

        flota.agregar_transportista(transportista_id)
        self.flota_repository.save(flota)
        return True

class AgregarVehiculoAFlotaUseCase:
    """Use case for adding a vehicle to a fleet"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, flota_id: str, vehiculo_id: str) -> bool:
        """Add a vehicle to a fleet"""
        flota = self.flota_repository.find_by_id(flota_id)
        if not flota:
            return False

        flota.agregar_vehiculo(vehiculo_id)
        self.flota_repository.save(flota)
        return True

class ObtenerEstadisticasFlotaUseCase:
    """Use case for getting fleet statistics"""

    def __init__(self, flota_repository: FlotaRepository):
        self.flota_repository = flota_repository

    def execute(self, flota_id: str) -> Optional[dict]:
        """Get statistics for a fleet"""
        flota = self.flota_repository.find_by_id(flota_id)
        if not flota:
            return None

        return flota.obtener_estadisticas()