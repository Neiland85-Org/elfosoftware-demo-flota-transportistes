"""Tests for Domain Entities

Unit tests for domain entities following DDD principles.
"""

import pytest
from datetime import date, datetime
from uuid import uuid4

from elfosoftware_flota.domain.entities.flota import Flota
from elfosoftware_flota.domain.entities.transportista import Transportista
from elfosoftware_flota.domain.entities.vehiculo import Vehiculo
from elfosoftware_flota.domain.value_objects.matricula import Matricula


class TestFlota:
    """Test cases for Flota entity."""

    def test_crear_flota(self):
        """Test creating a new Flota."""
        flota = Flota(
            nombre="Flota Norte",
            descripcion="Flota para zona norte"
        )

        assert flota.nombre == "Flota Norte"
        assert flota.descripcion == "Flota para zona norte"
        assert flota.activo is True
        assert len(flota.transportistas_ids) == 0
        assert len(flota.vehiculos_ids) == 0

    def test_agregar_transportista(self):
        """Test adding a transportista to flota."""
        flota = Flota(nombre="Flota Test")
        transportista_id = uuid4()

        flota.agregar_transportista(transportista_id)

        assert transportista_id in flota.transportistas_ids
        assert flota.cantidad_transportistas == 1

    def test_remover_transportista(self):
        """Test removing a transportista from flota."""
        flota = Flota(nombre="Flota Test")
        transportista_id = uuid4()

        flota.agregar_transportista(transportista_id)
        flota.remover_transportista(transportista_id)

        assert transportista_id not in flota.transportistas_ids
        assert flota.cantidad_transportistas == 0


class TestTransportista:
    """Test cases for Transportista entity."""

    def test_crear_transportista(self):
        """Test creating a new Transportista."""
        transportista = Transportista(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@email.com",
            telefono="+34123456789",
            fecha_nacimiento=date(1985, 5, 15),
            numero_licencia="LIC123456",
            fecha_expiracion_licencia=date(2025, 12, 31)
        )

        assert transportista.nombre_completo == "Juan Pérez"
        assert transportista.edad == datetime.now().year - 1985
        assert transportista.licencia_vigente is True
        assert transportista.activo is True

    def test_licencia_expirada(self):
        """Test transportista with expired license."""
        transportista = Transportista(
            nombre="Ana",
            apellido="García",
            email="ana.garcia@email.com",
            telefono="+34987654321",
            fecha_nacimiento=date(1990, 3, 20),
            numero_licencia="LIC654321",
            fecha_expiracion_licencia=date(2020, 1, 1)  # Fecha pasada
        )

        assert transportista.licencia_vigente is False


class TestVehiculo:
    """Test cases for Vehiculo entity."""

    def test_crear_vehiculo(self):
        """Test creating a new Vehiculo."""
        matricula = Matricula(valor="1234ABC")
        vehiculo = Vehiculo(
            matricula=matricula,
            marca="Mercedes",
            modelo="Actros",
            anio=2020,
            capacidad_carga_kg=24000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2020, 6, 15)
        )

        assert vehiculo.matricula == matricula
        assert vehiculo.marca == "Mercedes"
        assert vehiculo.antiguedad_anios == datetime.now().year - 2020
        assert vehiculo.activo is True

    def test_actualizar_kilometraje(self):
        """Test updating vehicle mileage."""
        matricula = Matricula(valor="5678DEF")
        vehiculo = Vehiculo(
            matricula=matricula,
            marca="Volvo",
            modelo="FH",
            anio=2019,
            capacidad_carga_kg=22000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2019, 4, 10)
        )

        vehiculo.actualizar_kilometraje(150000.0)

        assert vehiculo.kilometraje_actual == 150000.0

    def test_kilometraje_invalido(self):
        """Test invalid mileage update."""
        matricula = Matricula(valor="9012GHI")
        vehiculo = Vehiculo(
            matricula=matricula,
            marca="Scania",
            modelo="R450",
            anio=2021,
            capacidad_carga_kg=25000.0,
            tipo_vehiculo="Camión",
            fecha_matriculacion=date(2021, 8, 20),
            kilometraje_actual=100000.0
        )

        with pytest.raises(ValueError):
            vehiculo.actualizar_kilometraje(50000.0)  # Menor que el actual


class TestMatricula:
    """Test cases for Matricula value object."""

    def test_matricula_valida(self):
        """Test creating valid matricula."""
        matricula = Matricula(valor="1234ABC")

        assert str(matricula) == "1234ABC"
        assert matricula.numero == "1234"
        assert matricula.letras == "ABC"

    def test_matricula_formato_invalido(self):
        """Test invalid matricula format."""
        with pytest.raises(ValueError):
            Matricula(valor="123ABC")  # Faltan números

        with pytest.raises(ValueError):
            Matricula(valor="12345ABC")  # Demasiados números

        with pytest.raises(ValueError):
            Matricula(valor="1234AB")  # Faltan letras

    def test_matricula_minusculas(self):
        """Test matricula with lowercase letters."""
        matricula = Matricula(valor="1234abc")

        assert str(matricula) == "1234ABC"  # Se convierte a mayúsculas

    def test_matricula_igualdad(self):
        """Test matricula equality."""
        matricula1 = Matricula(valor="1234ABC")
        matricula2 = Matricula(valor="1234ABC")
        matricula3 = Matricula(valor="5678DEF")

        assert matricula1 == matricula2
        assert matricula1 != matricula3
