"""
SQLAlchemy models for the application
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.domain.entities.vehiculo import TipoVehiculo, EstadoVehiculo
from src.infrastructure.persistence.session import Base

class VehiculoModel(Base):
    """SQLAlchemy model for Vehiculo entity"""
    __tablename__ = "vehiculos"

    id = Column(String, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True, nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    tipo = Column(Enum(TipoVehiculo), nullable=False)
    capacidad_carga = Column(Float, nullable=False)
    estado = Column(Enum(EstadoVehiculo), nullable=False, default=EstadoVehiculo.DISPONIBLE)
    fecha_matriculacion = Column(DateTime, nullable=False)
    fecha_ultimo_mantenimiento = Column(DateTime, nullable=True)
    kilometraje = Column(Integer, nullable=False, default=0)
    flota_id = Column(String, nullable=True)  # Removed FK constraint
    transportista_id = Column(String, nullable=True)  # Removed FK constraint

    def __repr__(self):
        return f"<VehiculoModel(id={self.id}, matricula={self.matricula}, tipo={self.tipo.value})>"


class TransportModel(Base):
    """SQLAlchemy model for Transport entity"""
    __tablename__ = "transports"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Float, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<TransportModel(id={self.id}, code={self.code}, capacity={self.capacity})>"
