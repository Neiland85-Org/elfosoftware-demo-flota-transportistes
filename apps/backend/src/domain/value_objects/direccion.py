"""
Value objects for domain
"""
from pydantic import BaseModel, Field, validator
from typing import Optional

class Direccion(BaseModel):
    """Value object representing an address"""
    calle: str = Field(..., description="Street name and number")
    ciudad: str = Field(..., description="City")
    codigo_postal: str = Field(..., description="Postal code")
    pais: str = Field(default="España", description="Country")
    provincia: Optional[str] = Field(None, description="Province/State")
    coordenadas: Optional[str] = Field(None, description="GPS coordinates (lat,lng)")

    @validator('codigo_postal')
    def validar_codigo_postal(cls, v):
        """Validate postal code format"""
        if len(v) != 5 or not v.isdigit():
            raise ValueError('El código postal debe tener 5 dígitos')
        return v

    def __str__(self) -> str:
        """String representation of the address"""
        partes = [self.calle, self.ciudad]
        if self.provincia:
            partes.append(self.provincia)
        partes.append(self.pais)
        return ", ".join(partes)

    def obtener_coordenadas(self) -> Optional[tuple[float, float]]:
        """Extract latitude and longitude from coordinates string"""
        if self.coordenadas:
            try:
                lat, lng = self.coordenadas.split(',')
                return float(lat.strip()), float(lng.strip())
            except (ValueError, AttributeError):
                return None
        return None

class Coordenadas(BaseModel):
    """Value object representing GPS coordinates"""
    latitud: float = Field(..., ge=-90, le=90, description="Latitude")
    longitud: float = Field(..., ge=-180, le=180, description="Longitude")

    def __str__(self) -> str:
        """String representation of coordinates"""
        return f"{self.latitud},{self.longitud}"

    def calcular_distancia(self, otras: 'Coordenadas') -> float:
        """Calculate approximate distance in kilometers (Haversine formula)"""
        import math

        # Convert to radians
        lat1, lon1 = math.radians(self.latitud), math.radians(self.longitud)
        lat2, lon2 = math.radians(otras.latitud), math.radians(otras.longitud)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        # Radius of Earth in kilometers
        R = 6371
        return R * c

class Ruta(BaseModel):
    """Value object representing a route"""
    origen: Direccion = Field(..., description="Origin address")
    destino: Direccion = Field(..., description="Destination address")
    distancia_km: Optional[float] = Field(None, description="Distance in kilometers")
    tiempo_estimado_horas: Optional[float] = Field(None, description="Estimated time in hours")

    def calcular_distancia_total(self) -> Optional[float]:
        """Calculate total distance if coordinates are available"""
        if self.origen.coordenadas and self.destino.coordenadas:
            coord_origen = self.origen.obtener_coordenadas()
            coord_destino = self.destino.obtener_coordenadas()

            if coord_origen and coord_destino:
                origen_coords = Coordenadas(latitud=coord_origen[0], longitud=coord_origen[1])
                destino_coords = Coordenadas(latitud=coord_destino[0], longitud=coord_destino[1])
                return origen_coords.calcular_distancia(destino_coords)

        return None

    def __str__(self) -> str:
        """String representation of the route"""
        return f"{self.origen} → {self.destino}"