"""
Service for listing transport entities
"""
from typing import List, Optional
from src.domain.entities.transport import Transport
from src.infrastructure.persistence.uow import UnitOfWork


class ListTransportService:
    """Service for listing transport entities"""

    def execute(self, uow: UnitOfWork, active: Optional[bool] = None) -> List[Transport]:
        """
        List transport entities
        
        Args:
            uow: Unit of Work instance
            active: Filter by active status (optional)
            
        Returns:
            List[Transport]: List of transport entities
        """
        with uow:
            transports = uow.transport_repository.find_all(active=active)
            return transports