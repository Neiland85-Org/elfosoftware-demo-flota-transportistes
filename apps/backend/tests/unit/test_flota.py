"""
Unit tests for Flota entity
"""
import pytest
from datetime import datetime
from src.domain.entities.flota import Flota

class TestFlota:
    """Test cases for Flota entity"""

    def test_flota_creation(self):
        """Test basic fleet creation"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        assert flota.id == "FLT001"
        assert flota.nombre == "Flota Norte"
        assert flota.activo is True
        assert flota.transportistas == []
        assert flota.vehiculos == []

    def test_flota_creation_with_description(self):
        """Test fleet creation with description"""
        flota = Flota(
            id="FLT002",
            nombre="Flota Sur",
            descripcion="Flota dedicada al transporte del sur del país"
        )
        assert flota.descripcion == "Flota dedicada al transporte del sur del país"

    def test_agregar_transportista(self):
        """Test adding transporter to fleet"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_transportista("TRP001")

        assert "TRP001" in flota.transportistas
        assert len(flota.transportistas) == 1

    def test_agregar_transportista_duplicado(self):
        """Test adding duplicate transporter doesn't create duplicates"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_transportista("TRP001")
        flota.agregar_transportista("TRP001")  # Intentar agregar duplicado

        assert len(flota.transportistas) == 1

    def test_remover_transportista(self):
        """Test removing transporter from fleet"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_transportista("TRP001")
        flota.agregar_transportista("TRP002")

        flota.remover_transportista("TRP001")

        assert "TRP001" not in flota.transportistas
        assert "TRP002" in flota.transportistas
        assert len(flota.transportistas) == 1

    def test_agregar_vehiculo(self):
        """Test adding vehicle to fleet"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_vehiculo("VEH001")

        assert "VEH001" in flota.vehiculos
        assert len(flota.vehiculos) == 1

    def test_remover_vehiculo(self):
        """Test removing vehicle from fleet"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_vehiculo("VEH001")
        flota.agregar_vehiculo("VEH002")

        flota.remover_vehiculo("VEH001")

        assert "VEH001" not in flota.vehiculos
        assert "VEH002" in flota.vehiculos
        assert len(flota.vehiculos) == 1

    def test_obtener_estadisticas(self):
        """Test getting fleet statistics"""
        flota = Flota(id="FLT001", nombre="Flota Norte")
        flota.agregar_transportista("TRP001")
        flota.agregar_transportista("TRP002")
        flota.agregar_vehiculo("VEH001")

        stats = flota.obtener_estadisticas()

        assert stats["total_transportistas"] == 2
        assert stats["total_vehiculos"] == 1
        assert stats["activo"] is True