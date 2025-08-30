"""
Dependency injection for FastAPI
"""
from fastapi import Depends
from src.infrastructure.persistence.uow import SqlAlchemyUnitOfWork, UnitOfWork
from src.application.services.create_transport_service import CreateTransportService
from src.application.services.update_transport_service import UpdateTransportService
from src.application.services.list_transport_service import ListTransportService


def get_uow() -> UnitOfWork:
    """Get Unit of Work instance"""
    return SqlAlchemyUnitOfWork()


def get_create_transport_service() -> CreateTransportService:
    """Get CreateTransportService instance"""
    return CreateTransportService()


def get_update_transport_service() -> UpdateTransportService:
    """Get UpdateTransportService instance"""
    return UpdateTransportService()


def get_list_transport_service() -> ListTransportService:
    """Get ListTransportService instance"""
    return ListTransportService()