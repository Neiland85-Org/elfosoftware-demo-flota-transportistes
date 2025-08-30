"""
Repository interface for Transport entity
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.transport import Transport


class TransportRepository(ABC):
    """Repository interface for Transport entity"""

    @abstractmethod
    def save(self, transport: Transport) -> None:
        """Save a transport entity"""
        pass

    @abstractmethod
    def get(self, transport_id: str) -> Transport:
        """Get a transport by ID, raises NotFoundError if not found"""
        pass

    @abstractmethod
    def find_by_id(self, transport_id: str) -> Optional[Transport]:
        """Find a transport by ID, returns None if not found"""
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Transport]:
        """Find a transport by code, returns None if not found"""
        pass

    @abstractmethod
    def find_all(self, active: Optional[bool] = None) -> List[Transport]:
        """Find all transports, optionally filtered by active status"""
        pass

    @abstractmethod
    def delete(self, transport_id: str) -> None:
        """Delete a transport by ID"""
        pass