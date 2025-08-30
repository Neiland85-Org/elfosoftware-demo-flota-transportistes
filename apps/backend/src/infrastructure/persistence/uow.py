"""
Unit of Work pattern implementation for managing database transactions
"""
from abc import ABC, abstractmethod
from typing import Generator
from sqlalchemy.orm import Session
from src.infrastructure.persistence.session import SessionLocal
from src.domain.repositories.transport_repository import TransportRepository


class UnitOfWork(ABC):
    """Abstract Unit of Work interface"""
    
    transport_repository: TransportRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        """Commit the current transaction"""
        pass

    @abstractmethod
    def rollback(self):
        """Rollback the current transaction"""
        pass


class SqlAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy implementation of Unit of Work"""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory
        self.session: Session = None

    def __enter__(self):
        self.session = self.session_factory()
        # Import here to avoid circular import
        from src.infrastructure.persistence.transport_sqlalchemy_repository import SQLAlchemyTransportRepository
        self.transport_repository = SQLAlchemyTransportRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        if self.session:
            self.session.close()

    def commit(self):
        """Commit the current transaction"""
        if self.session:
            self.session.commit()

    def rollback(self):
        """Rollback the current transaction"""
        if self.session:
            self.session.rollback()