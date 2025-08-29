"""SQLAlchemy Models

Modelos de base de datos para las entidades del dominio.
Utiliza SQLAlchemy con configuración asíncrona.
"""

from datetime import date, datetime
from typing import List
from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from elfosoftware_flota.domain.value_objects.matricula import Matricula


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# Tabla de asociación muchos a muchos entre Flota y Transportista
flota_transportista_association = Table(
    'flota_transportista',
    Base.metadata,
    Column('flota_id', UUID(as_uuid=True), ForeignKey('flota.id'), primary_key=True),
    Column('transportista_id', UUID(as_uuid=True), ForeignKey('transportista.id'), primary_key=True)
)

# Tabla de asociación muchos a muchos entre Flota y Vehiculo
flota_vehiculo_association = Table(
    'flota_vehiculo',
    Base.metadata,
    Column('flota_id', UUID(as_uuid=True), ForeignKey('flota.id'), primary_key=True),
    Column('vehiculo_id', UUID(as_uuid=True), ForeignKey('vehiculo.id'), primary_key=True)
)


class FlotaModel(Base):
    """Modelo SQLAlchemy para Flota."""

    __tablename__ = "flota"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    transportistas: Mapped[List["TransportistaModel"]] = relationship(
        "TransportistaModel",
        secondary=flota_transportista_association,
        back_populates="flotas"
    )
    vehiculos: Mapped[List["VehiculoModel"]] = relationship(
        "VehiculoModel",
        secondary=flota_vehiculo_association,
        back_populates="flotas"
    )


class TransportistaModel(Base):
    """Modelo SQLAlchemy para Transportista."""

    __tablename__ = "transportista"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    numero_licencia: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    fecha_expiracion_licencia: Mapped[date] = mapped_column(Date, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    flotas: Mapped[List[FlotaModel]] = relationship(
        "FlotaModel",
        secondary=flota_transportista_association,
        back_populates="transportistas"
    )


class VehiculoModel(Base):
    """Modelo SQLAlchemy para Vehiculo."""

    __tablename__ = "vehiculo"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    matricula_valor: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    capacidad_carga_kg: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_vehiculo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_matriculacion: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_ultima_revision: Mapped[date] = mapped_column(Date, nullable=True)
    kilometraje_actual: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    flotas: Mapped[List[FlotaModel]] = relationship(
        "FlotaModel",
        secondary=flota_vehiculo_association,
        back_populates="vehiculos"
    )

    @property
    def matricula(self) -> Matricula:
        """Convierte el valor de matrícula a Value Object."""
        return Matricula(valor=self.matricula_valor)
