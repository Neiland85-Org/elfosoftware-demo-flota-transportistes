"""In-Memory Transportista Repository Implementation.

Implementación en memoria del repositorio de Transportista para desarrollo y testing.
Arquitectura DELFOS - Infrastructure Layer.
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from elfosoftware_flota.domain.entities.transportista import Transportista
from elfosoftware_flota.domain.repositories.i_transportista_repository import ITransportistaRepository


class InMemoryTransportistaRepository(ITransportistaRepository):
    """Implementación en memoria del repositorio de Transportista."""
    
    def __init__(self):
        """Inicializar el repositorio con almacenamiento en memoria."""
        self._transportistas: dict[UUID, Transportista] = {}
    
    async def save(self, transportista: Transportista) -> None:
        """Guarda un transportista en el repositorio."""
        self._transportistas[transportista.id] = transportista
    
    async def find_by_id(self, transportista_id: UUID) -> Optional[Transportista]:
        """Busca un transportista por su ID."""
        return self._transportistas.get(transportista_id)
    
    async def find_by_email(self, email: str) -> Optional[Transportista]:
        """Busca un transportista por su email."""
        for transportista in self._transportistas.values():
            if transportista.email == email:
                return transportista
        return None
    
    async def find_by_numero_licencia(self, numero_licencia: str) -> Optional[Transportista]:
        """Busca un transportista por su número de licencia."""
        for transportista in self._transportistas.values():
            if transportista.numero_licencia == numero_licencia:
                return transportista
        return None
    
    async def find_all_activos(self) -> List[Transportista]:
        """Retorna todos los transportistas activos."""
        return [transportista for transportista in self._transportistas.values() 
                if transportista.activo]
    
    async def find_by_licencia_vigente(self, vigente: bool = True) -> List[Transportista]:
        """Busca transportistas con licencia vigente o expirada."""
        resultado = []
        for transportista in self._transportistas.values():
            if transportista.licencia_vigente == vigente:
                resultado.append(transportista)
        return resultado
    
    async def find_by_edad_rango(self, edad_min: int, edad_max: int) -> List[Transportista]:
        """Busca transportistas dentro de un rango de edad."""
        resultado = []
        for transportista in self._transportistas.values():
            edad = transportista.edad
            if edad_min <= edad <= edad_max:
                resultado.append(transportista)
        return resultado
    
    async def delete(self, transportista_id: UUID) -> None:
        """Elimina un transportista del repositorio."""
        if transportista_id in self._transportistas:
            del self._transportistas[transportista_id]
    
    async def exists(self, transportista_id: UUID) -> bool:
        """Verifica si existe un transportista con el ID dado."""
        return transportista_id in self._transportistas
    
    async def count_activos(self) -> int:
        """Cuenta el número de transportistas activos."""
        return len([t for t in self._transportistas.values() if t.activo])
    
    async def _initialize_test_data(self) -> None:
        """Inicializa el repositorio con datos de prueba."""
        test_transportistas = [
            Transportista(
                nombre="Juan",
                apellido="Pérez",
                email="juan.perez@email.com",
                telefono="+34612345678",
                fecha_nacimiento=date(1985, 6, 15),
                numero_licencia="LIC123456789",
                fecha_expiracion_licencia=date(2030, 6, 15)
            ),
            Transportista(
                nombre="María",
                apellido="García",
                email="maria.garcia@email.com",
                telefono="+34687654321",
                fecha_nacimiento=date(1990, 3, 22),
                numero_licencia="LIC987654321",
                fecha_expiracion_licencia=date(2028, 3, 22)
            ),
            Transportista(
                nombre="Pedro",
                apellido="López",
                email="pedro.lopez@email.com",
                telefono="+34611223344",
                fecha_nacimiento=date(1988, 11, 8),
                numero_licencia="LIC555666777",
                fecha_expiracion_licencia=date(2029, 11, 8)
            )
        ]
        
        for transportista in test_transportistas:
            await self.save(transportista)