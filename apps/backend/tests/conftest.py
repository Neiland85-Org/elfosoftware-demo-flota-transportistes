"""
Test configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# Domain imports
from src.domain.entities.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from src.domain.repositories.interfaces import VehiculoRepository

# Infrastructure imports
from src.infrastructure.persistence.models import Base, VehiculoModel, FlotaModel, TransportistaModel
from src.infrastructure.repositories.vehiculo_repository import SQLAlchemyVehiculoRepository

# Application imports
from src.presentation.api.main import app

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """Create a test client for FastAPI"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def vehiculo_repository(db_session: Session):
    """Create a vehicle repository for testing"""
    return SQLAlchemyVehiculoRepository(db_session)

@pytest.fixture(scope="function")
def sample_vehiculo():
    """Create a sample vehicle for testing"""
    from datetime import datetime
    return Vehiculo(
        id="VEH001",
        matricula="ABC123",
        marca="Mercedes",
        modelo="Actros",
        tipo=TipoVehiculo.CAMION,
        capacidad_carga=25000.0,
        estado=EstadoVehiculo.DISPONIBLE,
        fecha_matriculacion=datetime(2020, 1, 15),
        kilometraje=50000
    )
