"""
Service for creating transport entities
"""
from src.domain.entities.transport import Transport
from src.domain.exceptions import DuplicateCodeError
from src.infrastructure.persistence.uow import UnitOfWork


class CreateTransportService:
    """Service for creating new transport entities"""

    def execute(self, uow: UnitOfWork, code: str, capacity: float) -> Transport:
        """
        Create a new transport entity
        
        Args:
            uow: Unit of Work instance
            code: Unique transport code 
            capacity: Transport capacity in kg
            
        Returns:
            Transport: The created transport entity
            
        Raises:
            DuplicateCodeError: If a transport with the same code already exists
            ValidationError: If validation fails
        """
        with uow:
            # Check if transport with this code already exists
            existing_transport = uow.transport_repository.find_by_code(code)
            if existing_transport:
                raise DuplicateCodeError(f"Transport with code '{code}' already exists")
            
            # Create new transport
            transport = Transport(
                code=code,
                capacity=capacity,
                active=True
            )
            
            # Validate entity
            transport.ensure_valid()
            
            # Save transport
            uow.transport_repository.save(transport)
            uow.commit()
            
            return transport