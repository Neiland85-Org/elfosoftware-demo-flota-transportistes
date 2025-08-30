"""Tests para GPS Services.

Tests unitarios para servicios de GPS y cálculos de distancia.
"""

import pytest
import math

from elfosoftware_flota.domain.services.gps_services import (
    calcular_distancia_haversine,
    calcular_distancia_entre_coordenadas,
    validar_coordenadas_gps
)


class TestCalcularDistanciaHaversine:
    """Tests para la función calcular_distancia_haversine."""

    def test_distancia_madrid_barcelona(self):
        """Test del cálculo de distancia Madrid-Barcelona."""
        # Coordenadas reales
        madrid_lat, madrid_lon = 40.4168, -3.7038
        barcelona_lat, barcelona_lon = 41.3851, 2.1734
        
        distancia = calcular_distancia_haversine(
            madrid_lat, madrid_lon, barcelona_lat, barcelona_lon
        )
        
        # La distancia real es aproximadamente 505 km
        assert 500 <= distancia <= 510
        assert abs(distancia - 505.44) < 1  # Tolerancia de 1 km

    def test_distancia_misma_ubicacion(self):
        """Test del cálculo de distancia en la misma ubicación."""
        lat, lon = 40.4168, -3.7038
        
        distancia = calcular_distancia_haversine(lat, lon, lat, lon)
        
        assert distancia == 0.0

    def test_distancia_nueva_york_londres(self):
        """Test del cálculo de distancia Nueva York-Londres."""
        # Nueva York
        ny_lat, ny_lon = 40.7128, -74.0060
        # Londres
        london_lat, london_lon = 51.5074, -0.1278
        
        distancia = calcular_distancia_haversine(ny_lat, ny_lon, london_lat, london_lon)
        
        # La distancia real es aproximadamente 5585 km
        assert 5580 <= distancia <= 5590

    def test_validacion_latitud_invalida(self):
        """Test de validación con latitud inválida."""
        with pytest.raises(ValueError, match="Las latitudes deben estar entre -90 y 90 grados"):
            calcular_distancia_haversine(91, 0, 0, 0)
        
        with pytest.raises(ValueError, match="Las latitudes deben estar entre -90 y 90 grados"):
            calcular_distancia_haversine(-91, 0, 0, 0)

    def test_validacion_longitud_invalida(self):
        """Test de validación con longitud inválida."""
        with pytest.raises(ValueError, match="Las longitudes deben estar entre -180 y 180 grados"):
            calcular_distancia_haversine(0, 181, 0, 0)
        
        with pytest.raises(ValueError, match="Las longitudes deben estar entre -180 y 180 grados"):
            calcular_distancia_haversine(0, -181, 0, 0)

    def test_coordenadas_limite(self):
        """Test con coordenadas en los límites."""
        # Coordenadas válidas en los límites
        distancia = calcular_distancia_haversine(90, 180, -90, -180)
        
        # Debe ser una distancia válida (mitad de la circunferencia de la Tierra)
        assert distancia > 0
        assert distancia <= 20015  # Aproximadamente media circunferencia terrestre

    def test_precision_calculo(self):
        """Test de precisión del cálculo."""
        # Distancia pequeña (aproximadamente 1 km)
        lat1, lon1 = 40.4168, -3.7038
        lat2, lon2 = 40.4258, -3.7038  # Aproximadamente 1 km al norte
        
        distancia = calcular_distancia_haversine(lat1, lon1, lat2, lon2)
        
        # Debería ser aproximadamente 1 km
        assert 0.9 <= distancia <= 1.1


class TestCalcularDistanciaEntreCoordenadas:
    """Tests para la función calcular_distancia_entre_coordenadas."""

    def test_con_tuplas(self):
        """Test usando tuplas de coordenadas."""
        madrid = (40.4168, -3.7038)
        barcelona = (41.3851, 2.1734)
        
        distancia = calcular_distancia_entre_coordenadas(madrid, barcelona)
        
        assert 500 <= distancia <= 510

    def test_misma_ubicacion_tuplas(self):
        """Test con la misma ubicación usando tuplas."""
        ubicacion = (40.4168, -3.7038)
        
        distancia = calcular_distancia_entre_coordenadas(ubicacion, ubicacion)
        
        assert distancia == 0.0


class TestValidarCoordenadasGps:
    """Tests para la función validar_coordenadas_gps."""

    def test_coordenadas_validas(self):
        """Test con coordenadas válidas."""
        assert validar_coordenadas_gps(40.4168, -3.7038) is True
        assert validar_coordenadas_gps(0, 0) is True
        assert validar_coordenadas_gps(90, 180) is True
        assert validar_coordenadas_gps(-90, -180) is True

    def test_latitud_invalida(self):
        """Test con latitud inválida."""
        assert validar_coordenadas_gps(91, 0) is False
        assert validar_coordenadas_gps(-91, 0) is False

    def test_longitud_invalida(self):
        """Test con longitud inválida."""
        assert validar_coordenadas_gps(0, 181) is False
        assert validar_coordenadas_gps(0, -181) is False

    def test_ambas_coordenadas_invalidas(self):
        """Test con ambas coordenadas inválidas."""
        assert validar_coordenadas_gps(91, 181) is False
        assert validar_coordenadas_gps(-91, -181) is False


class TestConsistenciaImplementaciones:
    """Tests para verificar consistencia entre implementaciones."""

    def test_consistencia_con_implementacion_existente(self):
        """Test para verificar que la nueva implementación es consistente con la existente."""
        # Importar la implementación existente
        from apps.backend.src.domain.value_objects.direccion import Coordenadas
        
        # Coordenadas de prueba
        lat1, lon1 = 40.4168, -3.7038
        lat2, lon2 = 41.3851, 2.1734
        
        # Cálculo con nueva implementación
        distancia_nueva = calcular_distancia_haversine(lat1, lon1, lat2, lon2)
        
        # Cálculo con implementación existente
        coord1 = Coordenadas(latitud=lat1, longitud=lon1)
        coord2 = Coordenadas(latitud=lat2, longitud=lon2)
        distancia_existente = coord1.calcular_distancia(coord2)
        
        # Deben ser prácticamente iguales (tolerancia de 0.01 km)
        assert abs(distancia_nueva - distancia_existente) < 0.01