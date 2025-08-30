"""
Use cases for vehicle management
"""
from typing import List, Optional
from datetime import datetime
from src.domain.entities.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from src.domain.repositories.interfaces import VehiculoRepository

class CrearVehiculoUseCase:
    """Use case for creating a new vehicle"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, matricula: str, marca: str, modelo: str, tipo: TipoVehiculo,
                capacidad_carga: float, fecha_matriculacion: datetime,
                fecha_ultimo_mantenimiento: Optional[datetime] = None,
                kilometraje: int = 0) -> Vehiculo:
        """Create a new vehicle"""
        # Generate a simple ID (in production, use UUID or similar)
        vehiculo_id = f"VHC{len(self.vehiculo_repository.find_all()) + 1:03d}"

        vehiculo = Vehiculo(
            id=vehiculo_id,
            matricula=matricula,
            marca=marca,
            modelo=modelo,
            tipo=tipo,
            capacidad_carga=capacidad_carga,
            estado=EstadoVehiculo.DISPONIBLE,
            fecha_matriculacion=fecha_matriculacion,
            fecha_ultimo_mantenimiento=fecha_ultimo_mantenimiento,
            kilometraje=kilometraje
        )

        self.vehiculo_repository.save(vehiculo)
        return vehiculo

class ObtenerVehiculoUseCase:
    """Use case for getting a vehicle by ID"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str) -> Optional[Vehiculo]:
        """Get a vehicle by ID"""
        return self.vehiculo_repository.find_by_id(vehiculo_id)

class ListarVehiculosUseCase:
    """Use case for listing vehicles"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, flota_id: Optional[str] = None, estado: Optional[str] = None,
                solo_disponibles: bool = False) -> List[Vehiculo]:
        """List vehicles with optional filters"""
        if solo_disponibles:
            return self.vehiculo_repository.find_disponibles()
        elif flota_id:
            return self.vehiculo_repository.find_by_flota(flota_id)
        elif estado:
            return self.vehiculo_repository.find_by_estado(estado)
        else:
            return self.vehiculo_repository.find_all()

class ActualizarVehiculoUseCase:
    """Use case for updating a vehicle"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str, **kwargs) -> Optional[Vehiculo]:
        """Update a vehicle with the provided fields"""
        vehiculo = self.vehiculo_repository.find_by_id(vehiculo_id)
        if not vehiculo:
            return None

        # Update only provided fields
        for key, value in kwargs.items():
            if hasattr(vehiculo, key):
                setattr(vehiculo, key, value)

        self.vehiculo_repository.save(vehiculo)
        return vehiculo

class CambiarEstadoVehiculoUseCase:
    """Use case for changing vehicle status"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str, nuevo_estado: EstadoVehiculo) -> Optional[Vehiculo]:
        """Change vehicle status"""
        vehiculo = self.vehiculo_repository.find_by_id(vehiculo_id)
        if not vehiculo:
            return None

        vehiculo.estado = nuevo_estado
        self.vehiculo_repository.save(vehiculo)
        return vehiculo

class AsignarVehiculoAFlotaUseCase:
    """Use case for assigning a vehicle to a fleet"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str, flota_id: str) -> Optional[Vehiculo]:
        """Assign vehicle to a fleet"""
        vehiculo = self.vehiculo_repository.find_by_id(vehiculo_id)
        if not vehiculo:
            return None

        vehiculo.asignar_a_flota(flota_id)
        self.vehiculo_repository.save(vehiculo)
        return vehiculo

class RemoverVehiculoDeFlotaUseCase:
    """Use case for removing a vehicle from its fleet"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str) -> Optional[Vehiculo]:
        """Remove vehicle from its current fleet"""
        vehiculo = self.vehiculo_repository.find_by_id(vehiculo_id)
        if not vehiculo:
            return None

        vehiculo.remover_de_flota()
        self.vehiculo_repository.save(vehiculo)
        return vehiculo

class EliminarVehiculoUseCase:
    """Use case for deleting a vehicle"""

    def __init__(self, vehiculo_repository: VehiculoRepository):
        self.vehiculo_repository = vehiculo_repository

    def execute(self, vehiculo_id: str) -> bool:
        """Delete a vehicle by ID"""
        vehiculo = self.vehiculo_repository.find_by_id(vehiculo_id)
        if not vehiculo:
            return False

        self.vehiculo_repository.delete(vehiculo_id)
        return True
