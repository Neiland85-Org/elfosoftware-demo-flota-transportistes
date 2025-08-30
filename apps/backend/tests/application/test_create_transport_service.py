"""
Tests for CreateTransportService
"""
import pytest
from typing import Dict, List, Optional
from src.domain.entities.transport import Transport
from src.domain.repositories.transport_repository import TransportRepository
from src.domain.exceptions import NotFoundError, DuplicateCodeError, ValidationError
from src.infrastructure.persistence.uow import UnitOfWork
from src.application.services.create_transport_service import CreateTransportService


class InMemoryTransportRepository(TransportRepository):
    """In-memory implementation of TransportRepository for testing"""
    
    def __init__(self):
        self.transports: Dict[str, Transport] = {}
        self.next_id = 1

    def save(self, transport: Transport) -> None:
        """Save a transport entity"""
        if not transport.id:
            transport.id = str(self.next_id)
            self.next_id += 1
        
        # Check for duplicate code
        for existing_id, existing_transport in self.transports.items():
            if existing_transport.code == transport.code and existing_id != transport.id:
                raise DuplicateCodeError(f"Transport with code '{transport.code}' already exists")
        
        self.transports[transport.id] = transport

    def get(self, transport_id: str) -> Transport:
        """Get a transport by ID, raises NotFoundError if not found"""
        from src.domain.exceptions import NotFoundError
        transport = self.find_by_id(transport_id)
        if not transport:
            raise NotFoundError(f"Transport with ID '{transport_id}' not found")
        return transport

    def find_by_id(self, transport_id: str) -> Optional[Transport]:
        """Find a transport by ID, returns None if not found"""
        return self.transports.get(transport_id)

    def find_by_code(self, code: str) -> Optional[Transport]:
        """Find a transport by code, returns None if not found"""
        for transport in self.transports.values():
            if transport.code == code:
                return transport
        return None

    def find_all(self, active: Optional[bool] = None) -> List[Transport]:
        """Find all transports, optionally filtered by active status"""
        transports = list(self.transports.values())
        if active is not None:
            transports = [t for t in transports if t.active == active]
        return transports

    def delete(self, transport_id: str) -> None:
        """Delete a transport by ID"""
        if transport_id in self.transports:
            del self.transports[transport_id]


class DummyUnitOfWork(UnitOfWork):
    """Dummy Unit of Work for testing"""
    
    def __init__(self):
        self.transport_repository = InMemoryTransportRepository()
        self.committed = False
        self.rolled_back = False

    def commit(self):
        """Commit the current transaction"""
        self.committed = True

    def rollback(self):
        """Rollback the current transaction"""
        self.rolled_back = True


class TestCreateTransportService:
    """Test cases for CreateTransportService"""

    def setup_method(self):
        """Set up test fixtures"""
        self.uow = DummyUnitOfWork()
        self.service = CreateTransportService()

    def test_create_transport_success(self):
        """Test successful transport creation"""
        transport = self.service.execute(
            self.uow,
            code="TST001",
            capacity=1000.0
        )

        assert transport.code == "TST001"
        assert transport.capacity == 1000.0
        assert transport.active is True
        assert transport.id is not None
        assert self.uow.committed

    def test_create_transport_duplicate_code_raises_error(self):
        """Test creation with duplicate code raises DuplicateCodeError"""
        # Create first transport
        self.service.execute(
            self.uow,
            code="TST001",
            capacity=1000.0
        )

        # Try to create another with same code
        with pytest.raises(DuplicateCodeError) as exc_info:
            self.service.execute(
                self.uow,
                code="TST001",
                capacity=2000.0
            )
        
        assert "already exists" in str(exc_info.value)

    def test_create_transport_invalid_capacity_raises_validation_error(self):
        """Test creation with invalid capacity raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.execute(
                self.uow,
                code="TST001",
                capacity=-100.0
            )
        
        assert "greater than 0" in str(exc_info.value)

    def test_create_transport_invalid_code_raises_validation_error(self):
        """Test creation with invalid code raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.execute(
                self.uow,
                code="A",  # Too short
                capacity=1000.0
            )
        
        assert "at least 2 characters" in str(exc_info.value)