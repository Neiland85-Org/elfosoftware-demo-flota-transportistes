"""Transportista API Routes

Endpoints REST para la gestión de Transportistas.
Utiliza FastAPI con arquitectura limpia.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from elfosoftware_flota.infrastructure.persistence.database import get_db_session
from elfosoftware_flota.infrastructure.dependencies import get_transportista_repository
from elfosoftware_flota.domain.repositories.i_transportista_repository import ITransportistaRepository
from elfosoftware_flota.application.use_cases.transportista_use_cases import (
    CrearTransportistaUseCase,
    ObtenerTransportistaUseCase,
    ListarTransportistasActivosUseCase
)
from elfosoftware_flota.presentation.dto.transportista_dto import (
    CrearTransportistaRequest,
    TransportistaResponse,
    TransportistaErrorResponse
)

# Crear router
transportista_router = APIRouter()


@transportista_router.get(
    "/",
    summary="Listar transportistas",
    description="Retorna una lista de todos los transportistas activos.",
    response_model=List[TransportistaResponse]
)
async def listar_transportistas(
    repository: ITransportistaRepository = Depends(get_transportista_repository)
) -> List[TransportistaResponse]:
    """Listar todos los transportistas activos."""
    try:
        use_case = ListarTransportistasActivosUseCase(repository)
        transportistas = await use_case.execute()
        return [TransportistaResponse.from_orm(t) for t in transportistas]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@transportista_router.get(
    "/{transportista_id}",
    summary="Obtener transportista por ID",
    description="Retorna los detalles de un transportista específico.",
    response_model=TransportistaResponse,
    responses={
        404: {"model": TransportistaErrorResponse, "description": "Transportista no encontrado"}
    }
)
async def obtener_transportista(
    transportista_id: UUID,
    repository: ITransportistaRepository = Depends(get_transportista_repository)
) -> TransportistaResponse:
    """Obtener un transportista por su ID."""
    try:
        use_case = ObtenerTransportistaUseCase(repository)
        transportista = await use_case.execute(str(transportista_id))
        
        if not transportista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transportista con ID {transportista_id} no encontrado"
            )
        
        return TransportistaResponse.from_orm(transportista)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@transportista_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Crear transportista",
    description="Crea un nuevo transportista en el sistema.",
    response_model=TransportistaResponse,
    responses={
        400: {"model": TransportistaErrorResponse, "description": "Datos de entrada inválidos"},
        409: {"model": TransportistaErrorResponse, "description": "Conflicto - transportista ya existe"}
    }
)
async def crear_transportista(
    transportista_data: CrearTransportistaRequest,
    repository: ITransportistaRepository = Depends(get_transportista_repository)
) -> TransportistaResponse:
    """Crear un nuevo transportista."""
    try:
        use_case = CrearTransportistaUseCase(repository)
        transportista = await use_case.execute(transportista_data)
        
        return TransportistaResponse.from_orm(transportista)
        
    except ValueError as e:
        # Errores de negocio (email/licencia duplicados)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationError as e:
        # Errores de validación de datos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Datos de entrada inválidos: {str(e)}"
        )
    except Exception as e:
        # Errores internos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@transportista_router.put(
    "/{transportista_id}",
    summary="Actualizar transportista",
    description="Actualiza los datos de un transportista existente.",
    response_model=TransportistaResponse,
    responses={
        404: {"model": TransportistaErrorResponse, "description": "Transportista no encontrado"}
    }
)
async def actualizar_transportista(
    transportista_id: UUID,
    transportista_data: CrearTransportistaRequest,
    repository: ITransportistaRepository = Depends(get_transportista_repository)
) -> TransportistaResponse:
    """Actualizar un transportista existente."""
    # TODO: Implementar lógica de negocio completa
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint no implementado aún"
    )


@transportista_router.delete(
    "/{transportista_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar transportista",
    description="Elimina un transportista del sistema.",
    responses={
        404: {"model": TransportistaErrorResponse, "description": "Transportista no encontrado"}
    }
)
async def eliminar_transportista(
    transportista_id: UUID,
    repository: ITransportistaRepository = Depends(get_transportista_repository)
) -> None:
    """Eliminar un transportista."""
    # TODO: Implementar lógica de negocio completa
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint no implementado aún"
    )
