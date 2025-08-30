"""Database Configuration

Configuración de la base de datos para la aplicación.
Utiliza SQLAlchemy con configuración asíncrona.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/flota_transportistes"
)

# Crear engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Mostrar SQL queries en desarrollo
    poolclass=NullPool,  # Deshabilitar connection pooling para desarrollo
)

# Crear session factory
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesiones de base de datos asíncronas."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Crea todas las tablas en la base de datos."""
    from sqlalchemy import MetaData

    # Importar aquí para evitar dependencias circulares
    from elfosoftware_flota.infrastructure.persistence.models import metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def drop_tables() -> None:
    """Elimina todas las tablas de la base de datos."""
    from elfosoftware_flota.infrastructure.persistence.models import metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
