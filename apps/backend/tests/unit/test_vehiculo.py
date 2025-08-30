"""
Unit tests for Vehiculo entity
"""
import pytest
from datetime import datetime
from src.domain.entities.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo

class TestVehiculo:
    """Test cases for Vehiculo entity"""

    def test_vehiculo_creation(self):
        """Test basic vehicle creation"""
        fecha_matriculacion = datetime(2020, 1, 15)
        vehiculo = Vehiculo(
            id="VEH001",
            matricula="ABC123",
            marca="Mercedes",
            modelo="Actros",
            tipo=TipoVehiculo.CAMION,
            capacidad_carga=25000.0,
            fecha_matriculacion=fecha_matriculacion
        )

        assert vehiculo.id == "VEH001"
        assert vehiculo.matricula == "ABC123"
        assert vehiculo.marca == "Mercedes"
        assert vehiculo.modelo == "Actros"
        assert vehiculo.tipo == TipoVehiculo.CAMION
        assert vehiculo.capacidad_carga == 25000.0
        assert vehiculo.estado == EstadoVehiculo.DISPONIBLE
        assert vehiculo.kilometraje == 0

    def test_asignar_a_flota(self):
        """Test assigning vehicle to fleet"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.asignar_a_flota("FLT001")

        assert vehiculo.flota_id == "FLT001"

    def test_asignar_transportista(self):
        """Test assigning vehicle to transporter"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.asignar_a_flota("FLT001")
        vehiculo.asignar_transportista("TRP001")

        assert vehiculo.transportista_id == "TRP001"
        assert vehiculo.estado == EstadoVehiculo.EN_USO

    def test_liberar_transportista(self):
        """Test releasing vehicle from transporter"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.asignar_a_flota("FLT001")
        vehiculo.asignar_transportista("TRP001")

        vehiculo.liberar_transportista()

        assert vehiculo.transportista_id is None
        assert vehiculo.estado == EstadoVehiculo.DISPONIBLE

    def test_cambiar_estado(self):
        """Test changing vehicle status"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.cambiar_estado(EstadoVehiculo.EN_MANTENIMIENTO)

        assert vehiculo.estado == EstadoVehiculo.EN_MANTENIMIENTO

    def test_actualizar_kilometraje(self):
        """Test updating vehicle mileage"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.actualizar_kilometraje(50000)

        assert vehiculo.kilometraje == 50000

    def test_actualizar_kilometraje_invalido(self):
        """Test updating vehicle mileage with invalid value"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.actualizar_kilometraje(50000)

        # Intentar actualizar con un valor menor (debería ignorarse)
        vehiculo.actualizar_kilometraje(30000)

        assert vehiculo.kilometraje == 50000

    def test_necesita_mantenimiento_sin_mantenimiento(self):
        """Test maintenance check when no maintenance has been done"""
        vehiculo = self._crear_vehiculo_basico()

        assert vehiculo.necesita_mantenimiento() is True

    def test_necesita_mantenimiento_reciente(self):
        """Test maintenance check with recent maintenance"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.fecha_ultimo_mantenimiento = datetime.now()

        assert vehiculo.necesita_mantenimiento() is False

    def test_esta_disponible(self):
        """Test vehicle availability"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.asignar_a_flota("FLT001")
        vehiculo.fecha_ultimo_mantenimiento = datetime.now()

        assert vehiculo.esta_disponible() is True

    def test_no_esta_disponible_sin_flota(self):
        """Test vehicle not available when not assigned to fleet"""
        vehiculo = self._crear_vehiculo_basico()
        vehiculo.fecha_ultimo_mantenimiento = datetime.now()

        assert vehiculo.esta_disponible() is False

    def _crear_vehiculo_basico(self) -> Vehiculo:
        """Helper method to create a basic vehicle for testing"""
        return Vehiculo(
            id="VEH001",
            matricula="ABC123",
            marca="Mercedes",
            modelo="Actros",
            tipo=TipoVehiculo.CAMION,
            capacidad_carga=25000.0,
            fecha_matriculacion=datetime(2020, 1, 15)
        )