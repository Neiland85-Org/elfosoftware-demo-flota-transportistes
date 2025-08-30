"""Use Cases para Transportista.

Casos de uso para la gestión de Transportistas.
Arquitectura DELFOS - Application Layer.
"""

from datetime import date
from typing import Optional

from elfosoftware_flota.domain.entities.transportista import Transportista
from elfosoftware_flota.domain.repositories.i_transportista_repository import ITransportistaRepository
from elfosoftware_flota.presentation.dto.transportista_dto import CrearTransportistaRequest


class CrearTransportistaUseCase:
    """Caso de uso para crear un nuevo transportista."""
    
    def __init__(self, transportista_repository: ITransportistaRepository):
        """Inicializar el caso de uso con las dependencias necesarias.
        
        Args:
            transportista_repository: Repositorio de transportistas
        """
        self._transportista_repository = transportista_repository
    
    async def execute(self, request: CrearTransportistaRequest) -> Transportista:
        """Ejecutar la creación de un nuevo transportista.
        
        Args:
            request: Datos del transportista a crear
            
        Returns:
            Transportista: El transportista creado
            
        Raises:
            ValueError: Si ya existe un transportista con el mismo email o licencia
        """
        # Verificar que no exista un transportista con el mismo email
        transportista_existente = await self._transportista_repository.find_by_email(request.email)
        if transportista_existente:
            raise ValueError(f"Ya existe un transportista con el email {request.email}")
        
        # Verificar que no exista un transportista con el mismo número de licencia
        transportista_existente = await self._transportista_repository.find_by_numero_licencia(request.numero_licencia)
        if transportista_existente:
            raise ValueError(f"Ya existe un transportista con la licencia {request.numero_licencia}")
        
        # Crear la nueva entidad transportista
        transportista = Transportista(
            nombre=request.nombre,
            apellido=request.apellido,
            email=request.email,
            telefono=request.telefono,
            fecha_nacimiento=request.fecha_nacimiento,
            numero_licencia=request.numero_licencia,
            fecha_expiracion_licencia=request.fecha_expiracion_licencia
        )
        
        # Guardar en el repositorio
        await self._transportista_repository.save(transportista)
        
        return transportista


class ObtenerTransportistaUseCase:
    """Caso de uso para obtener un transportista por ID."""
    
    def __init__(self, transportista_repository: ITransportistaRepository):
        """Inicializar el caso de uso con las dependencias necesarias.
        
        Args:
            transportista_repository: Repositorio de transportistas
        """
        self._transportista_repository = transportista_repository
    
    async def execute(self, transportista_id: str) -> Optional[Transportista]:
        """Ejecutar la búsqueda de un transportista por ID.
        
        Args:
            transportista_id: ID del transportista a buscar
            
        Returns:
            Optional[Transportista]: El transportista encontrado o None
        """
        from uuid import UUID
        try:
            uuid_id = UUID(transportista_id)
            return await self._transportista_repository.find_by_id(uuid_id)
        except ValueError:
            return None


class ListarTransportistasActivosUseCase:
    """Caso de uso para listar transportistas activos."""
    
    def __init__(self, transportista_repository: ITransportistaRepository):
        """Inicializar el caso de uso con las dependencias necesarias.
        
        Args:
            transportista_repository: Repositorio de transportistas
        """
        self._transportista_repository = transportista_repository
    
    async def execute(self) -> list[Transportista]:
        """Ejecutar la búsqueda de transportistas activos.
        
        Returns:
            list[Transportista]: Lista de transportistas activos
        """
        return await self._transportista_repository.find_all_activos()