"""
Unit tests for Transportista entity
"""
import pytest
from datetime import datetime
from src.domain.entities.transportista import Transportista

class TestTransportista:
    """Test cases for Transportista entity"""

    def test_transportista_creation(self):
        """Test basic transporter creation"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456"
        )

        assert transportista.id == "TRP001"
        assert transportista.nombre == "Juan Pérez"
        assert transportista.email == "juan.perez@email.com"
        assert transportista.licencia == "LIC123456"
        assert transportista.activo is True
        assert transportista.flota_id is None

    def test_transportista_creation_with_phone(self):
        """Test transporter creation with phone number"""
        transportista = Transportista(
            id="TRP002",
            nombre="María García",
            email="maria.garcia@email.com",
            telefono="+1234567890",
            licencia="LIC789012"
        )

        assert transportista.telefono == "+1234567890"

    def test_asignar_a_flota(self):
        """Test assigning transporter to fleet"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456"
        )

        transportista.asignar_a_flota("FLT001")

        assert transportista.flota_id == "FLT001"

    def test_remover_de_flota(self):
        """Test removing transporter from fleet"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456"
        )

        transportista.asignar_a_flota("FLT001")
        transportista.remover_de_flota()

        assert transportista.flota_id is None

    def test_esta_disponible_sin_flota(self):
        """Test availability when not assigned to fleet"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456"
        )

        assert transportista.esta_disponible() is False

    def test_esta_disponible_con_flota(self):
        """Test availability when assigned to fleet"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456"
        )

        transportista.asignar_a_flota("FLT001")

        assert transportista.esta_disponible() is True

    def test_esta_disponible_inactivo(self):
        """Test availability when transporter is inactive"""
        transportista = Transportista(
            id="TRP001",
            nombre="Juan Pérez",
            email="juan.perez@email.com",
            licencia="LIC123456",
            activo=False
        )

        transportista.asignar_a_flota("FLT001")

        assert transportista.esta_disponible() is False

    def test_email_validation(self):
        """Test email validation"""
        with pytest.raises(ValueError):
            Transportista(
                id="TRP001",
                nombre="Juan Pérez",
                email="invalid-email",  # Invalid email format
                licencia="LIC123456"
            )