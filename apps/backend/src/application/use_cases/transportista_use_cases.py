"""
Use cases for transporter management
"""
from typing import List, Optional
from src.domain.entities.transportista import Transportista
from src.domain.repositories.interfaces import TransportistaRepository

class CrearTransportistaUseCase:
    """Use case for creating a new transporter"""

    def __init__(self, transportista_repository: TransportistaRepository):
        self.transportista_repository = transportista_repository

    def execute(self, nombre: str, email: str, licencia: str, telefono: Optional[str] = None) -> Transportista:
        """Create a new transporter"""
        # Generate a simple ID (in production, use UUID or similar)
        transportista_id = f"TRP{len(self.transportista_repository.find_all()) + 1:03d}"

        transportista = Transportista(
            id=transportista_id,
            nombre=nombre,
            email=email,
            licencia=licencia,
            telefono=telefono
        )

        self.transportista_repository.save(transportista)
        return transportista

class ObtenerTransportistaUseCase:
    """Use case for getting a transporter by ID"""

    def __init__(self, transportista_repository: TransportistaRepository):
        self.transportista_repository = transportista_repository

    def execute(self, transportista_id: str) -> Optional[Transportista]:
        """Get a transporter by ID"""
        return self.transportista_repository.find_by_id(transportista_id)

class ListarTransportistasUseCase:
    """Use case for listing transporters"""

    def __init__(self, transportista_repository: TransportistaRepository):
        self.transportista_repository = transportista_repository

    def execute(self, flota_id: Optional[str] = None, solo_activos: bool = True) -> List[Transportista]:
        """List transporters"""
        if flota_id:
            return self.transportista_repository.find_by_flota(flota_id)
        elif solo_activos:
            return self.transportista_repository.find_by_activo(True)
        return self.transportista_repository.find_all()

class AsignarTransportistaAFlotaUseCase:
    """Use case for assigning a transporter to a fleet"""

    def __init__(self, transportista_repository: TransportistaRepository):
        self.transportista_repository = transportista_repository

    def execute(self, transportista_id: str, flota_id: str) -> bool:
        """Assign a transporter to a fleet"""
        transportista = self.transportista_repository.find_by_id(transportista_id)
        if not transportista:
            return False

        transportista.asignar_a_flota(flota_id)
        self.transportista_repository.save(transportista)
        return True

class VerificarDisponibilidadTransportistaUseCase:
    """Use case for checking transporter availability"""

    def __init__(self, transportista_repository: TransportistaRepository):
        self.transportista_repository = transportista_repository

    def execute(self, transportista_id: str) -> bool:
        """Check if a transporter is available"""
        transportista = self.transportista_repository.find_by_id(transportista_id)
        if not transportista:
            return False

        return transportista.esta_disponible()