"""
SQLAlchemy models for the application
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from src.domain.entities.vehiculo import TipoVehiculo, EstadoVehiculo

Base = declarative_base()

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
    flota_id = Column(String, ForeignKey("flotas.id"), nullable=True)
    transportista_id = Column(String, ForeignKey("transportistas.id"), nullable=True)

    # Relationships
    flota = relationship("FlotaModel", back_populates="vehiculos")
    transportista = relationship("TransportistaModel", back_populates="vehiculos")

    def __repr__(self):
        return f"<VehiculoModel(id={self.id}, matricula={self.matricula}, tipo={self.tipo.value})>"
