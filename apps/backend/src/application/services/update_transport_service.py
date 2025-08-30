"""
Service for updating transport entities
"""
from typing import Optional
from src.domain.entities.transport import Transport
from src.domain.exceptions import NotFoundError, DuplicateCodeError, ValidationError
from src.infrastructure.persistence.uow import UnitOfWork


class UpdateTransportService:
    """Service for updating transport entities with partial updates"""

    def execute(
        self,
        uow: UnitOfWork,
        transport_id: str,
        code: Optional[str] = None,
        capacity: Optional[float] = None,
        active: Optional[bool] = None
    ) -> Transport:
        """
        Update a transport entity with partial data
        
        Args:
            uow: Unit of Work instance
            transport_id: ID of the transport to update
            code: New transport code (optional)
            capacity: New transport capacity in kg (optional)
            active: New active status (optional)
            
        Returns:
            Transport: The updated transport entity
            
        Raises:
            NotFoundError: If transport with given ID doesn't exist
            DuplicateCodeError: If trying to update to an existing code
            ValidationError: If validation fails or no fields provided
        """
        # Validate at least one field is provided
        if code is None and capacity is None and active is None:
            raise ValidationError("At least one field must be provided for update")
        
        with uow:
            # Get existing transport
            transport = uow.transport_repository.get(transport_id)
            
            # Check for duplicate code if code is being updated
            if code is not None and code != transport.code:
                existing_transport = uow.transport_repository.find_by_code(code)
                if existing_transport:
                    raise DuplicateCodeError(f"Transport with code '{code}' already exists")
            
            # Update fields
            if code is not None:
                transport.code = code
            if capacity is not None:
                transport.capacity = capacity
            if active is not None:
                transport.active = active
            
            # Validate updated entity
            transport.ensure_valid()
            
            # Save transport
            uow.transport_repository.save(transport)
            uow.commit()
            
            return transport