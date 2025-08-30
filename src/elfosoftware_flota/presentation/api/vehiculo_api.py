"""Vehiculo API Routes

Endpoints REST para la gestión de Vehículos.
Utiliza FastAPI con arquitectura limpia.
"""

from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from elfosoftware_flota.domain.entities.vehiculo import Vehiculo
from elfosoftware_flota.domain.repositories.i_vehiculo_repository import IVehiculoRepository
from elfosoftware_flota.domain.value_objects.matricula import Matricula
from elfosoftware_flota.infrastructure.dependencies import get_vehiculo_repository
from elfosoftware_flota.presentation.dto.vehiculo_dto import (
    ActualizarKilometrajeDTO,
    ActualizarVehiculoDTO,
    CrearVehiculoDTO,
    RegistrarRevisionDTO,
    VehiculoDTO,
    VehiculoResumenDTO,
)

# Crear router
vehiculo_router = APIRouter(tags=["vehículos"])


def vehiculo_to_dto(vehiculo: Vehiculo) -> VehiculoDTO:
    """Convierte una entidad Vehiculo a VehiculoDTO."""
    try:
        necesita_rev = vehiculo.necesita_revision
    except Exception as e:
        print(f"Error calculando necesita_revision: {e}")
        necesita_rev = True

    try:
        antiguedad = vehiculo.antiguedad_anios
    except Exception as e:
        print(f"Error calculando antiguedad_anios: {e}")
        antiguedad = 0

    return VehiculoDTO(
        id=vehiculo.id,
        matricula=str(vehiculo.matricula),
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        anio=vehiculo.anio,
        capacidad_carga_kg=vehiculo.capacidad_carga_kg,
        tipo_vehiculo=vehiculo.tipo_vehiculo,
        fecha_matriculacion=vehiculo.fecha_matriculacion,
        fecha_ultima_revision=vehiculo.fecha_ultima_revision,
        kilometraje_actual=vehiculo.kilometraje_actual,
        activo=vehiculo.activo,
        fecha_creacion=vehiculo.fecha_creacion,
        fecha_actualizacion=vehiculo.fecha_actualizacion,
        necesita_revision=necesita_rev,
        antiguedad_anios=antiguedad,
    )


def vehiculo_to_resumen_dto(vehiculo: Vehiculo) -> VehiculoResumenDTO:
    """Convierte una entidad Vehiculo a VehiculoResumenDTO."""
    try:
        necesita_rev = vehiculo.necesita_revision
    except Exception as e:
        print(f"Error en vehiculo_to_resumen_dto calculando necesita_revision: {e}")
        necesita_rev = True

    return VehiculoResumenDTO(
        id=vehiculo.id,
        matricula=str(vehiculo.matricula),
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        tipo_vehiculo=vehiculo.tipo_vehiculo,
        activo=vehiculo.activo,
        necesita_revision=necesita_rev,
    )


@vehiculo_router.get(
    "/",
    response_model=List[VehiculoResumenDTO],
    summary="Listar vehículos",
    description="Retorna una lista de todos los vehículos activos."
)
async def listar_vehiculos(
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Listar todos los vehículos activos."""
    vehiculos = await repository.find_all_activos()
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/{vehiculo_id}",
    response_model=VehiculoDTO,
    summary="Obtener vehículo por ID",
    description="Retorna los detalles completos de un vehículo específico."
)
async def obtener_vehiculo(
    vehiculo_id: UUID,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Obtener un vehículo por su ID."""
    vehiculo = await repository.find_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )
    return vehiculo_to_dto(vehiculo)


@vehiculo_router.get(
    "/matricula/{matricula}",
    response_model=VehiculoDTO,
    summary="Obtener vehículo por matrícula",
    description="Retorna los detalles de un vehículo por su matrícula."
)
async def obtener_vehiculo_por_matricula(
    matricula: str,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Obtener un vehículo por su matrícula."""
    matricula_obj = Matricula(matricula)
    vehiculo = await repository.find_by_matricula(matricula_obj)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con matrícula {matricula} no encontrado"
        )
    return vehiculo_to_dto(vehiculo)


@vehiculo_router.post(
    "/",
    response_model=VehiculoDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear vehículo",
    description="Crea un nuevo vehículo en el sistema."
)
async def crear_vehiculo(
    vehiculo_data: CrearVehiculoDTO,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Crear un nuevo vehículo."""
    print(f"📥 Recibidos datos: {vehiculo_data}")
    print(f"📝 Matrícula: {vehiculo_data.matricula}")
    print(f"🏢 Marca: {vehiculo_data.marca}")

    try:
        # Verificar si ya existe un vehículo con esa matrícula
        matricula_obj = Matricula(vehiculo_data.matricula)
        print(f"✅ Matrícula creada: {matricula_obj}")
    except Exception as e:
        print(f"❌ Error creando matrícula: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en matrícula: {str(e)}"
        )

    if await repository.exists_by_matricula(matricula_obj):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un vehículo con la matrícula {vehiculo_data.matricula}"
        )

    try:
        # Crear la entidad Vehiculo
        vehiculo = Vehiculo(
            matricula=matricula_obj,
            marca=vehiculo_data.marca,
            modelo=vehiculo_data.modelo,
            anio=vehiculo_data.anio,
            capacidad_carga_kg=vehiculo_data.capacidad_carga_kg,
            tipo_vehiculo=vehiculo_data.tipo_vehiculo,
            fecha_matriculacion=vehiculo_data.fecha_matriculacion,
            fecha_ultima_revision=vehiculo_data.fecha_ultima_revision,
            kilometraje_actual=vehiculo_data.kilometraje_actual or 0,
        )
        print(f"✅ Vehículo creado: {vehiculo.id}")
    except Exception as e:
        print(f"❌ Error creando vehículo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando entidad vehículo: {str(e)}"
        )

    try:
        # Guardar en el repositorio
        await repository.save(vehiculo)
        print(f"✅ Vehículo guardado en repositorio")
    except Exception as e:
        print(f"❌ Error guardando en repositorio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error guardando vehículo: {str(e)}"
        )

    try:
        result = vehiculo_to_dto(vehiculo)
        print(f"✅ DTO creado exitosamente")
        return result
    except Exception as e:
        print(f"❌ Error convirtiendo a DTO: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error convirtiendo respuesta: {str(e)}"
        )


@vehiculo_router.put(
    "/{vehiculo_id}",
    response_model=VehiculoDTO,
    summary="Actualizar vehículo",
    description="Actualiza los datos de un vehículo existente."
)
async def actualizar_vehiculo(
    vehiculo_id: UUID,
    vehiculo_data: ActualizarVehiculoDTO,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Actualizar un vehículo existente."""
    vehiculo = await repository.find_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )

    # Actualizar los datos del vehículo
    vehiculo.actualizar_datos(
        marca=vehiculo_data.marca,
        modelo=vehiculo_data.modelo,
        capacidad_carga_kg=vehiculo_data.capacidad_carga_kg,
        tipo_vehiculo=vehiculo_data.tipo_vehiculo,
    )

    # Actualizar fecha de última revisión si se proporciona
    if vehiculo_data.fecha_ultima_revision is not None:
        vehiculo.registrar_revision(vehiculo_data.fecha_ultima_revision)

    # Actualizar kilometraje si se proporciona
    if vehiculo_data.kilometraje_actual is not None:
        vehiculo.actualizar_kilometraje(vehiculo_data.kilometraje_actual)

    # Actualizar estado activo si se proporciona
    if vehiculo_data.activo is not None:
        if vehiculo_data.activo:
            vehiculo.activar()
        else:
            vehiculo.desactivar()

    # Guardar cambios
    await repository.save(vehiculo)

    return vehiculo_to_dto(vehiculo)


@vehiculo_router.delete(
    "/{vehiculo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar vehículo",
    description="Elimina un vehículo del sistema."
)
async def eliminar_vehiculo(
    vehiculo_id: UUID,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> None:
    """Eliminar un vehículo."""
    vehiculo = await repository.find_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )

    await repository.delete(vehiculo_id)


@vehiculo_router.put(
    "/{vehiculo_id}/kilometraje",
    response_model=VehiculoDTO,
    summary="Actualizar kilometraje",
    description="Actualiza el kilometraje de un vehículo."
)
async def actualizar_kilometraje(
    vehiculo_id: UUID,
    kilometraje_data: ActualizarKilometrajeDTO,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Actualizar el kilometraje de un vehículo."""
    vehiculo = await repository.find_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )

    vehiculo.actualizar_kilometraje(kilometraje_data.kilometraje_actual)
    await repository.save(vehiculo)

    return vehiculo_to_dto(vehiculo)


@vehiculo_router.put(
    "/{vehiculo_id}/revision",
    response_model=VehiculoDTO,
    summary="Registrar revisión",
    description="Registra una nueva revisión para un vehículo."
)
async def registrar_revision(
    vehiculo_id: UUID,
    revision_data: RegistrarRevisionDTO,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> VehiculoDTO:
    """Registrar una revisión para un vehículo."""
    vehiculo = await repository.find_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )

    vehiculo.registrar_revision(revision_data.fecha_revision)
    await repository.save(vehiculo)

    return vehiculo_to_dto(vehiculo)


@vehiculo_router.get(
    "/necesitan-revision/",
    response_model=List[VehiculoResumenDTO],
    summary="Vehículos que necesitan revisión",
    description="Retorna una lista de vehículos que necesitan revisión."
)
async def vehiculos_necesitan_revision(
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Obtener vehículos que necesitan revisión."""
    vehiculos = await repository.find_necesitan_revision()
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/marca/{marca}",
    response_model=List[VehiculoResumenDTO],
    summary="Buscar por marca",
    description="Busca vehículos por marca."
)
async def buscar_por_marca(
    marca: str,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Buscar vehículos por marca."""
    vehiculos = await repository.find_by_marca(marca)
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/tipo/{tipo_vehiculo}",
    response_model=List[VehiculoResumenDTO],
    summary="Buscar por tipo",
    description="Busca vehículos por tipo."
)
async def buscar_por_tipo(
    tipo_vehiculo: str,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Buscar vehículos por tipo."""
    vehiculos = await repository.find_by_tipo(tipo_vehiculo)
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/capacidad/{capacidad_minima}",
    response_model=List[VehiculoResumenDTO],
    summary="Buscar por capacidad mínima",
    description="Busca vehículos con capacidad de carga mínima."
)
async def buscar_por_capacidad(
    capacidad_minima: float,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Buscar vehículos por capacidad mínima."""
    vehiculos = await repository.find_by_capacidad_minima(capacidad_minima)
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/anio/{anio_min}/{anio_max}",
    response_model=List[VehiculoResumenDTO],
    summary="Buscar por rango de años",
    description="Busca vehículos dentro de un rango de años."
)
async def buscar_por_anio_rango(
    anio_min: int,
    anio_max: int,
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> List[VehiculoResumenDTO]:
    """Buscar vehículos por rango de años."""
    vehiculos = await repository.find_by_anio_rango(anio_min, anio_max)
    return [vehiculo_to_resumen_dto(v) for v in vehiculos]


@vehiculo_router.get(
    "/count/activos",
    summary="Contar vehículos activos",
    description="Retorna el número de vehículos activos."
)
async def contar_vehiculos_activos(
    repository: IVehiculoRepository = Depends(get_vehiculo_repository)
) -> dict:
    """Contar vehículos activos."""
    count = await repository.count_activos()
    return {"count": count, "message": f"Hay {count} vehículos activos"}


@vehiculo_router.post(
    "/test",
    summary="Endpoint de prueba",
    description="Endpoint simple para probar la funcionalidad básica."
)
async def test_endpoint():
    """Endpoint de prueba simple."""
    return {"message": "Test endpoint working", "timestamp": "2025-08-30"}
