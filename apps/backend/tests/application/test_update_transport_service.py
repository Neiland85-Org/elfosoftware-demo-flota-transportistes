"""
Tests for UpdateTransportService
"""
import pytest
from typing import Dict, List, Optional
from src.domain.entities.transport import Transport
from src.domain.repositories.transport_repository import TransportRepository
from src.domain.exceptions import NotFoundError, DuplicateCodeError, ValidationError
from src.infrastructure.persistence.uow import UnitOfWork
from src.application.services.update_transport_service import UpdateTransportService


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


class TestUpdateTransportService:
    """Test cases for UpdateTransportService"""

    def setup_method(self):
        """Set up test fixtures"""
        self.uow = DummyUnitOfWork()
        self.service = UpdateTransportService()
        
        # Create a test transport
        self.test_transport = Transport(
            id="test-id",
            code="TST001",
            capacity=1000.0,
            active=True
        )
        self.uow.transport_repository.save(self.test_transport)

    def test_update_code_success(self):
        """Test successful code update"""
        updated_transport = self.service.execute(
            self.uow,
            "test-id",
            code="TST002"
        )

        assert updated_transport.code == "TST002"
        assert updated_transport.capacity == 1000.0
        assert updated_transport.active is True
        assert self.uow.committed

    def test_update_capacity_success(self):
        """Test successful capacity update"""
        updated_transport = self.service.execute(
            self.uow,
            "test-id", 
            capacity=2000.0
        )

        assert updated_transport.code == "TST001"
        assert updated_transport.capacity == 2000.0
        assert updated_transport.active is True
        assert self.uow.committed

    def test_update_active_success(self):
        """Test successful active status update"""
        updated_transport = self.service.execute(
            self.uow,
            "test-id",
            active=False
        )

        assert updated_transport.code == "TST001"
        assert updated_transport.capacity == 1000.0
        assert updated_transport.active is False
        assert self.uow.committed

    def test_update_all_fields_success(self):
        """Test successful update of all fields"""
        updated_transport = self.service.execute(
            self.uow,
            "test-id",
            code="TST003",
            capacity=3000.0,
            active=False
        )

        assert updated_transport.code == "TST003"
        assert updated_transport.capacity == 3000.0
        assert updated_transport.active is False
        assert self.uow.committed

    def test_update_nonexistent_transport_raises_not_found(self):
        """Test update of non-existent transport raises NotFoundError"""
        with pytest.raises(NotFoundError) as exc_info:
            self.service.execute(
                self.uow,
                "nonexistent-id",
                code="TST002"
            )
        
        assert "not found" in str(exc_info.value)

    def test_update_duplicate_code_raises_error(self):
        """Test update to duplicate code raises DuplicateCodeError"""
        # Create another transport
        another_transport = Transport(
            id="another-id",
            code="TST999",
            capacity=500.0,
            active=True
        )
        self.uow.transport_repository.save(another_transport)

        # Try to update first transport to use existing code
        with pytest.raises(DuplicateCodeError) as exc_info:
            self.service.execute(
                self.uow,
                "test-id",
                code="TST999"
            )
        
        assert "already exists" in str(exc_info.value)

    def test_update_invalid_capacity_raises_validation_error(self):
        """Test update with invalid capacity raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.execute(
                self.uow,
                "test-id",
                capacity=-100.0
            )
        
        assert "greater than 0" in str(exc_info.value)

    def test_update_invalid_code_raises_validation_error(self):
        """Test update with invalid code raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.execute(
                self.uow,
                "test-id", 
                code="A"  # Too short
            )
        
        assert "at least 2 characters" in str(exc_info.value)

    def test_update_no_fields_raises_validation_error(self):
        """Test update with no fields raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.service.execute(
                self.uow,
                "test-id"
            )
        
        assert "At least one field must be provided" in str(exc_info.value)

    def test_update_same_code_success(self):
        """Test update with same code is allowed"""
        updated_transport = self.service.execute(
            self.uow,
            "test-id",
            code="TST001",  # Same code
            capacity=2000.0
        )

        assert updated_transport.code == "TST001"
        assert updated_transport.capacity == 2000.0
        assert self.uow.committed