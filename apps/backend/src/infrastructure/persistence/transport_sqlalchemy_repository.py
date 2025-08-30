"""
SQLAlchemy implementation of TransportRepository
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.entities.transport import Transport
from src.domain.repositories.transport_repository import TransportRepository
from src.domain.exceptions import NotFoundError, DuplicateCodeError
from src.infrastructure.persistence.models import TransportModel


class SQLAlchemyTransportRepository(TransportRepository):
    """SQLAlchemy implementation of TransportRepository"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, transport: Transport) -> None:
        """Save a transport entity"""
        # Generate ID if not present
        if not transport.id:
            transport.id = str(uuid.uuid4())

        # Check for existing transport by ID
        existing_model = self.session.query(TransportModel).filter(
            TransportModel.id == transport.id
        ).first()

        if existing_model:
            # Update existing
            existing_model.code = transport.code
            existing_model.capacity = transport.capacity
            existing_model.active = transport.active
        else:
            # Create new
            transport_model = TransportModel(
                id=transport.id,
                code=transport.code,
                capacity=transport.capacity,
                active=transport.active
            )
            self.session.add(transport_model)

        try:
            self.session.flush()  # Flush to check constraints but don't commit
        except IntegrityError as e:
            self.session.rollback()
            if "code" in str(e).lower():
                raise DuplicateCodeError(f"Transport with code '{transport.code}' already exists")
            raise

    def get(self, transport_id: str) -> Transport:
        """Get a transport by ID, raises NotFoundError if not found"""
        transport = self.find_by_id(transport_id)
        if not transport:
            raise NotFoundError(f"Transport with ID '{transport_id}' not found")
        return transport

    def find_by_id(self, transport_id: str) -> Optional[Transport]:
        """Find a transport by ID, returns None if not found"""
        model = self.session.query(TransportModel).filter(
            TransportModel.id == transport_id
        ).first()
        
        if model:
            return self._model_to_entity(model)
        return None

    def find_by_code(self, code: str) -> Optional[Transport]:
        """Find a transport by code, returns None if not found"""
        model = self.session.query(TransportModel).filter(
            TransportModel.code == code
        ).first()
        
        if model:
            return self._model_to_entity(model)
        return None

    def find_all(self, active: Optional[bool] = None) -> List[Transport]:
        """Find all transports, optionally filtered by active status"""
        query = self.session.query(TransportModel)
        
        if active is not None:
            query = query.filter(TransportModel.active == active)
        
        models = query.all()
        return [self._model_to_entity(model) for model in models]

    def delete(self, transport_id: str) -> None:
        """Delete a transport by ID"""
        model = self.session.query(TransportModel).filter(
            TransportModel.id == transport_id
        ).first()
        
        if model:
            self.session.delete(model)
            self.session.flush()

    def _model_to_entity(self, model: TransportModel) -> Transport:
        """Convert SQLAlchemy model to domain entity"""
        return Transport(
            id=model.id,
            code=model.code,
            capacity=model.capacity,
            active=model.active
        )