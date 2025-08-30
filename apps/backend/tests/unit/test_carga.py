"""
Unit tests for Carga entity
"""
import pytest
from datetime import datetime
from src.domain.entities.carga import Carga, TipoCarga, EstadoCarga

class TestCarga:
    """Test cases for Carga entity"""

    def test_carga_creation(self):
        """Test basic load creation"""
        carga = Carga(
            id="CAR001",
            descripcion="Electrónicos varios",
            tipo=TipoCarga.FRAGIL,
            peso=500.0,
            origen="Madrid",
            destino="Barcelona"
        )

        assert carga.id == "CAR001"
        assert carga.descripcion == "Electrónicos varios"
        assert carga.tipo == TipoCarga.FRAGIL
        assert carga.peso == 500.0
        assert carga.origen == "Madrid"
        assert carga.destino == "Barcelona"
        assert carga.estado == EstadoCarga.PENDIENTE

    def test_carga_creation_with_valor(self):
        """Test load creation with declared value"""
        carga = Carga(
            id="CAR002",
            descripcion="Mercancía valiosa",
            tipo=TipoCarga.GENERAL,
            peso=1000.0,
            valor_declarado=50000.0,
            origen="Madrid",
            destino="Barcelona"
        )

        assert carga.valor_declarado == 50000.0

    def test_asignar_vehiculo(self):
        """Test assigning load to vehicle"""
        carga = self._crear_carga_basica()
        carga.asignar_vehiculo("VEH001")

        assert carga.vehiculo_id == "VEH001"

    def test_asignar_transportista(self):
        """Test assigning load to transporter"""
        carga = self._crear_carga_basica()
        carga.asignar_transportista("TRP001")

        assert carga.transportista_id == "TRP001"

    def test_asignar_flota(self):
        """Test assigning load to fleet"""
        carga = self._crear_carga_basica()
        carga.asignar_flota("FLT001")

        assert carga.flota_id == "FLT001"

    def test_cambiar_estado_a_en_transito(self):
        """Test changing status to in transit"""
        carga = self._crear_carga_basica()
        carga.cambiar_estado(EstadoCarga.EN_TRANSITO)

        assert carga.estado == EstadoCarga.EN_TRANSITO
        assert carga.fecha_salida is not None
        assert carga.ultima_actualizacion is not None

    def test_cambiar_estado_a_entregada(self):
        """Test changing status to delivered"""
        carga = self._crear_carga_basica()
        carga.cambiar_estado(EstadoCarga.EN_TRANSITO)
        carga.cambiar_estado(EstadoCarga.ENTREGADA)

        assert carga.estado == EstadoCarga.ENTREGADA
        assert carga.fecha_entrega is not None

    def test_actualizar_ubicacion(self):
        """Test updating current location"""
        carga = self._crear_carga_basica()
        coordenadas = "40.4168,-3.7038"

        carga.actualizar_ubicacion(coordenadas)

        assert carga.coordenadas_actuales == coordenadas
        assert carga.ultima_actualizacion is not None

    def test_calcular_tiempo_transito(self):
        """Test calculating transit time"""
        carga = self._crear_carga_basica()
        carga.fecha_salida = datetime(2024, 1, 1, 10, 0, 0)
        carga.fecha_entrega = datetime(2024, 1, 1, 14, 0, 0)

        tiempo = carga.calcular_tiempo_transito()

        assert tiempo == 4  # 4 horas

    def test_calcular_tiempo_transito_sin_fechas(self):
        """Test calculating transit time without dates"""
        carga = self._crear_carga_basica()

        tiempo = carga.calcular_tiempo_transito()

        assert tiempo is None

    def test_esta_en_transito(self):
        """Test checking if load is in transit"""
        carga = self._crear_carga_basica()
        assert carga.esta_en_transito() is False

        carga.cambiar_estado(EstadoCarga.EN_TRANSITO)
        assert carga.esta_en_transito() is True

    def test_esta_entregada(self):
        """Test checking if load is delivered"""
        carga = self._crear_carga_basica()
        assert carga.esta_entregada() is False

        carga.cambiar_estado(EstadoCarga.ENTREGADA)
        assert carga.esta_entregada() is True

    def _crear_carga_basica(self) -> Carga:
        """Helper method to create a basic load for testing"""
        return Carga(
            id="CAR001",
            descripcion="Electrónicos varios",
            tipo=TipoCarga.FRAGIL,
            peso=500.0,
            origen="Madrid",
            destino="Barcelona"
        )