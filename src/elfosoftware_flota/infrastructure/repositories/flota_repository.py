"""FlotaRepository Implementation

Implementación del repositorio de Flota usando SQLAlchemy.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from elfosoftware_flota.domain.entities.flota import Flota
from elfosoftware_flota.domain.repositories.i_flota_repository import IFlotaRepository
from elfosoftware_flota.infrastructure.persistence.models import FlotaModel


class FlotaRepository(IFlotaRepository):
    """Implementación SQLAlchemy del repositorio de Flota."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, flota: Flota) -> None:
        """Guarda una flota en el repositorio."""
        # Convertir entidad de dominio a modelo de base de datos
        flota_model = FlotaModel(
            id=flota.id,
            nombre=flota.nombre,
            descripcion=flota.descripcion,
            activo=flota.activo,
            fecha_creacion=flota.fecha_creacion,
            fecha_actualizacion=flota.fecha_actualizacion
        )

        self.session.add(flota_model)
        await self.session.flush()  # Para obtener el ID si es auto-generado

    async def find_by_id(self, flota_id: UUID) -> Optional[Flota]:
        """Busca una flota por su ID."""
        stmt = select(FlotaModel).where(FlotaModel.id == flota_id)
        result = await self.session.execute(stmt)
        flota_model = result.scalar_one_or_none()

        if flota_model is None:
            return None

        # Convertir modelo a entidad de dominio
        return Flota(
            id=flota_model.id,
            nombre=flota_model.nombre,
            descripcion=flota_model.descripcion,
            activo=flota_model.activo,
            fecha_creacion=flota_model.fecha_creacion,
            fecha_actualizacion=flota_model.fecha_actualizacion
        )

    async def find_by_nombre(self, nombre: str) -> Optional[Flota]:
        """Busca una flota por su nombre."""
        stmt = select(FlotaModel).where(FlotaModel.nombre == nombre)
        result = await self.session.execute(stmt)
        flota_model = result.scalar_one_or_none()

        if flota_model is None:
            return None

        return Flota(
            id=flota_model.id,
            nombre=flota_model.nombre,
            descripcion=flota_model.descripcion,
            activo=flota_model.activo,
            fecha_creacion=flota_model.fecha_creacion,
            fecha_actualizacion=flota_model.fecha_actualizacion
        )

    async def find_all_activas(self) -> List[Flota]:
        """Retorna todas las flotas activas."""
        stmt = select(FlotaModel).where(FlotaModel.activo == True)
        result = await self.session.execute(stmt)
        flota_models = result.scalars().all()

        return [
            Flota(
                id=model.id,
                nombre=model.nombre,
                descripcion=model.descripcion,
                activo=model.activo,
                fecha_creacion=model.fecha_creacion,
                fecha_actualizacion=model.fecha_actualizacion
            )
            for model in flota_models
        ]

    async def find_by_transportista_id(self, transportista_id: UUID) -> List[Flota]:
        """Busca flotas que contengan un transportista específico."""
        # Esta implementación requiere una query más compleja con joins
        # Por simplicidad, retornamos lista vacía por ahora
        return []

    async def find_by_vehiculo_id(self, vehiculo_id: UUID) -> List[Flota]:
        """Busca flotas que contengan un vehículo específico."""
        # Esta implementación requiere una query más compleja con joins
        # Por simplicidad, retornamos lista vacía por ahora
        return []

    async def delete(self, flota_id: UUID) -> None:
        """Elimina una flota del repositorio."""
        flota_model = await self.session.get(FlotaModel, flota_id)
        if flota_model:
            await self.session.delete(flota_model)

    async def exists(self, flota_id: UUID) -> bool:
        """Verifica si existe una flota con el ID dado."""
        stmt = select(FlotaModel.id).where(FlotaModel.id == flota_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_activas(self) -> int:
        """Cuenta el número de flotas activas."""
        from sqlalchemy import func
        stmt = select(func.count()).where(FlotaModel.activo == True)
        result = await self.session.execute(stmt)
        return result.scalar_one()
