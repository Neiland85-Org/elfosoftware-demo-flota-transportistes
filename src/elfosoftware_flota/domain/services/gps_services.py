"""GPS and distance calculation services.

Servicios de dominio para cálculos GPS y distancias.
Arquitectura DELFOS - Domain Services.
"""

import math
from typing import Tuple


def calcular_distancia_haversine(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calcula la distancia aproximada entre dos puntos GPS usando la fórmula de Haversine.
    
    La fórmula de Haversine es una ecuación importante en navegación que proporciona
    distancias de gran círculo entre dos puntos en una esfera a partir de sus latitudes
    y longitudes.
    
    Args:
        lat1: Latitud del primer punto en grados decimales (-90 a 90)
        lon1: Longitud del primer punto en grados decimales (-180 a 180)
        lat2: Latitud del segundo punto en grados decimales (-90 a 90)
        lon2: Longitud del segundo punto en grados decimales (-180 a 180)
        
    Returns:
        float: Distancia en kilómetros entre los dos puntos
        
    Raises:
        ValueError: Si las coordenadas están fuera de los rangos válidos
        
    Examples:
        >>> # Madrid a Barcelona
        >>> distancia = calcular_distancia_haversine(40.4168, -3.7038, 41.3851, 2.1734)
        >>> print(f"{distancia:.2f} km")
        505.44 km
    """
    # Validar rangos de coordenadas
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError("Las latitudes deben estar entre -90 y 90 grados")
    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError("Las longitudes deben estar entre -180 y 180 grados")
    
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula de Haversine
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distancia
    distancia = R * c
    
    return distancia


def calcular_distancia_entre_coordenadas(
    coordenadas1: Tuple[float, float], coordenadas2: Tuple[float, float]
) -> float:
    """Calcula la distancia entre dos tuplas de coordenadas usando Haversine.
    
    Args:
        coordenadas1: Tupla (latitud, longitud) del primer punto
        coordenadas2: Tupla (latitud, longitud) del segundo punto
        
    Returns:
        float: Distancia en kilómetros
        
    Examples:
        >>> madrid = (40.4168, -3.7038)
        >>> barcelona = (41.3851, 2.1734)
        >>> distancia = calcular_distancia_entre_coordenadas(madrid, barcelona)
        >>> print(f"{distancia:.2f} km")
        505.44 km
    """
    lat1, lon1 = coordenadas1
    lat2, lon2 = coordenadas2
    return calcular_distancia_haversine(lat1, lon1, lat2, lon2)


def validar_coordenadas_gps(latitud: float, longitud: float) -> bool:
    """Valida si las coordenadas GPS están en rangos válidos.
    
    Args:
        latitud: Latitud en grados decimales
        longitud: Longitud en grados decimales
        
    Returns:
        bool: True si las coordenadas son válidas, False en caso contrario
    """
    return (-90 <= latitud <= 90) and (-180 <= longitud <= 180)