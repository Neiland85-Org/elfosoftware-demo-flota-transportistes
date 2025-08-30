"""
Repository interfaces for domain entities
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.flota import Flota
from src.domain.entities.transportista import Transportista
from src.domain.entities.vehiculo import Vehiculo
from src.domain.entities.carga import Carga

class FlotaRepository(ABC):
    """Repository interface for Flota entity"""

    @abstractmethod
    def save(self, flota: Flota) -> None:
        """Save a fleet"""
        pass

    @abstractmethod
    def find_by_id(self, flota_id: str) -> Optional[Flota]:
        """Find a fleet by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Flota]:
        """Find all fleets"""
        pass

    @abstractmethod
    def find_by_activa(self, activa: bool = True) -> List[Flota]:
        """Find fleets by active status"""
        pass

    @abstractmethod
    def delete(self, flota_id: str) -> None:
        """Delete a fleet by ID"""
        pass

class TransportistaRepository(ABC):
    """Repository interface for Transportista entity"""

    @abstractmethod
    def save(self, transportista: Transportista) -> None:
        """Save a transporter"""
        pass

    @abstractmethod
    def find_by_id(self, transportista_id: str) -> Optional[Transportista]:
        """Find a transporter by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Transportista]:
        """Find all transporters"""
        pass

    @abstractmethod
    def find_by_flota(self, flota_id: str) -> List[Transportista]:
        """Find transporters by fleet ID"""
        pass

    @abstractmethod
    def find_by_activo(self, activo: bool = True) -> List[Transportista]:
        """Find transporters by active status"""
        pass

    @abstractmethod
    def delete(self, transportista_id: str) -> None:
        """Delete a transporter by ID"""
        pass

class VehiculoRepository(ABC):
    """Repository interface for Vehiculo entity"""

    @abstractmethod
    def save(self, vehiculo: Vehiculo) -> None:
        """Save a vehicle"""
        pass

    @abstractmethod
    def find_by_id(self, vehiculo_id: str) -> Optional[Vehiculo]:
        """Find a vehicle by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Vehiculo]:
        """Find all vehicles"""
        pass

    @abstractmethod
    def find_by_flota(self, flota_id: str) -> List[Vehiculo]:
        """Find vehicles by fleet ID"""
        pass

    @abstractmethod
    def find_by_estado(self, estado: str) -> List[Vehiculo]:
        """Find vehicles by status"""
        pass

    @abstractmethod
    def find_disponibles(self) -> List[Vehiculo]:
        """Find available vehicles"""
        pass

    @abstractmethod
    def delete(self, vehiculo_id: str) -> None:
        """Delete a vehicle by ID"""
        pass

class CargaRepository(ABC):
    """Repository interface for Carga entity"""

    @abstractmethod
    def save(self, carga: Carga) -> None:
        """Save a load"""
        pass

    @abstractmethod
    def find_by_id(self, carga_id: str) -> Optional[Carga]:
        """Find a load by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Carga]:
        """Find all loads"""
        pass

    @abstractmethod
    def find_by_estado(self, estado: str) -> List[Carga]:
        """Find loads by status"""
        pass

    @abstractmethod
    def find_by_flota(self, flota_id: str) -> List[Carga]:
        """Find loads by fleet ID"""
        pass

    @abstractmethod
    def find_by_transportista(self, transportista_id: str) -> List[Carga]:
        """Find loads by transporter ID"""
        pass

    @abstractmethod
    def find_en_transito(self) -> List[Carga]:
        """Find loads currently in transit"""
        pass

    @abstractmethod
    def delete(self, carga_id: str) -> None:
        """Delete a load by ID"""
        pass