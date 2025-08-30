"""
Integration tests for vehicle API endpoints
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Domain imports
from src.domain.entities.vehiculo import TipoVehiculo, EstadoVehiculo

# Infrastructure imports
from src.infrastructure.repositories.vehiculo_repository import SQLAlchemyVehiculoRepository

class TestVehiculoAPI:
    """Integration tests for vehicle API"""

    def test_crear_vehiculo(self, client: TestClient, db_session: Session):
        """Test creating a vehicle via API"""
        vehiculo_data = {
            "matricula": "ABC123",
            "marca": "Mercedes",
            "modelo": "Actros",
            "tipo": "camion",
            "capacidad_carga": 25000.0,
            "fecha_matriculacion": "2020-01-15T00:00:00",
            "kilometraje": 50000
        }

        response = client.post("/api/v1/vehiculos/", json=vehiculo_data)

        assert response.status_code == 201
        data = response.json()
        assert data["matricula"] == "ABC123"
        assert data["marca"] == "Mercedes"
        assert data["tipo"] == "camion"
        assert data["estado"] == "disponible"
        assert "id" in data

    def test_obtener_vehiculo_existente(self, client: TestClient, db_session: Session, sample_vehiculo):
        """Test getting an existing vehicle"""
        # First create the vehicle
        repo = SQLAlchemyVehiculoRepository(db_session)
        repo.save(sample_vehiculo)

        response = client.get(f"/api/v1/vehiculos/{sample_vehiculo.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_vehiculo.id
        assert data["matricula"] == sample_vehiculo.matricula

    def test_obtener_vehiculo_inexistente(self, client: TestClient):
        """Test getting a non-existent vehicle"""
        response = client.get("/api/v1/vehiculos/VEH999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_listar_vehiculos(self, client: TestClient, db_session: Session):
        """Test listing all vehicles"""
        # Create some test vehicles
        repo = SQLAlchemyVehiculoRepository(db_session)

        vehiculo1 = sample_vehiculo.__class__(
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

        vehiculo2 = sample_vehiculo.__class__(
            id="VEH002",
            matricula="XYZ789",
            marca="Volvo",
            modelo="FH",
            tipo=TipoVehiculo.CAMION,
            capacidad_carga=30000.0,
            estado=EstadoVehiculo.EN_USO,
            fecha_matriculacion=datetime(2019, 6, 10),
            kilometraje=80000
        )

        repo.save(vehiculo1)
        repo.save(vehiculo2)

        response = client.get("/api/v1/vehiculos/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(v["matricula"] == "ABC123" for v in data)
        assert any(v["matricula"] == "XYZ789" for v in data)

    def test_listar_vehiculos_disponibles(self, client: TestClient, db_session: Session):
        """Test listing only available vehicles"""
        # Create test vehicles with different statuses
        repo = SQLAlchemyVehiculoRepository(db_session)

        vehiculo_disponible = sample_vehiculo.__class__(
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

        vehiculo_en_uso = sample_vehiculo.__class__(
            id="VEH002",
            matricula="XYZ789",
            marca="Volvo",
            modelo="FH",
            tipo=TipoVehiculo.CAMION,
            capacidad_carga=30000.0,
            estado=EstadoVehiculo.EN_USO,
            fecha_matriculacion=datetime(2019, 6, 10),
            kilometraje=80000
        )

        repo.save(vehiculo_disponible)
        repo.save(vehiculo_en_uso)

        response = client.get("/api/v1/vehiculos/?disponibles=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["matricula"] == "ABC123"
        assert data[0]["estado"] == "disponible"

    def test_actualizar_vehiculo(self, client: TestClient, db_session: Session, sample_vehiculo):
        """Test updating a vehicle"""
        # First create the vehicle
        repo = SQLAlchemyVehiculoRepository(db_session)
        repo.save(sample_vehiculo)

        update_data = {
            "marca": "Mercedes-Benz",
            "kilometraje": 60000
        }

        response = client.put(f"/api/v1/vehiculos/{sample_vehiculo.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["marca"] == "Mercedes-Benz"
        assert data["kilometraje"] == 60000
        assert data["matricula"] == sample_vehiculo.matricula  # Unchanged

    def test_cambiar_estado_vehiculo(self, client: TestClient, db_session: Session, sample_vehiculo):
        """Test changing vehicle status"""
        # First create the vehicle
        repo = SQLAlchemyVehiculoRepository(db_session)
        repo.save(sample_vehiculo)

        status_data = {"estado": "en_mantenimiento"}

        response = client.patch(f"/api/v1/vehiculos/{sample_vehiculo.id}/estado", json=status_data)

        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "en_mantenimiento"

    def test_eliminar_vehiculo(self, client: TestClient, db_session: Session, sample_vehiculo):
        """Test deleting a vehicle"""
        # First create the vehicle
        repo = SQLAlchemyVehiculoRepository(db_session)
        repo.save(sample_vehiculo)

        # Delete the vehicle
        response = client.delete(f"/api/v1/vehiculos/{sample_vehiculo.id}")

        assert response.status_code == 204

        # Verify it's deleted
        response = client.get(f"/api/v1/vehiculos/{sample_vehiculo.id}")
        assert response.status_code == 404

    def test_crear_vehiculo_con_matricula_duplicada(self, client: TestClient, db_session: Session, sample_vehiculo):
        """Test creating vehicle with duplicate license plate should fail"""
        # First create the vehicle
        repo = SQLAlchemyVehiculoRepository(db_session)
        repo.save(sample_vehiculo)

        # Try to create another vehicle with same license plate
        vehiculo_data = {
            "matricula": sample_vehiculo.matricula,  # Same license plate
            "marca": "Volvo",
            "modelo": "FH",
            "tipo": "camion",
            "capacidad_carga": 30000.0,
            "fecha_matriculacion": "2019-06-10T00:00:00"
        }

        response = client.post("/api/v1/vehiculos/", json=vehiculo_data)

        # This should fail due to unique constraint on matricula
        assert response.status_code == 400

    def test_actualizar_vehiculo_inexistente(self, client: TestClient):
        """Test updating a non-existent vehicle"""
        update_data = {"marca": "NewBrand"}

        response = client.put("/api/v1/vehiculos/VEH999", json=update_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
