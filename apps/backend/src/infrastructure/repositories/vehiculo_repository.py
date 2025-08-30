"""
SQLAlchemy implementation of VehiculoRepository
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.domain.entities.vehiculo import Vehiculo, EstadoVehiculo
from src.domain.repositories.interfaces import VehiculoRepository
from src.infrastructure.persistence.models import VehiculoModel

class SQLAlchemyVehiculoRepository(VehiculoRepository):
    """SQLAlchemy implementation of VehiculoRepository"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, vehiculo: Vehiculo) -> None:
        """Save a vehicle"""
        # Check if vehicle already exists
        existing = self.session.query(VehiculoModel).filter_by(id=vehiculo.id).first()

        if existing:
            # Update existing vehicle
            existing.matricula = vehiculo.matricula
            existing.marca = vehiculo.marca
            existing.modelo = vehiculo.modelo
            existing.tipo = vehiculo.tipo
            existing.capacidad_carga = vehiculo.capacidad_carga
            existing.estado = vehiculo.estado
            existing.fecha_matriculacion = vehiculo.fecha_matriculacion
            existing.fecha_ultimo_mantenimiento = vehiculo.fecha_ultimo_mantenimiento
            existing.kilometraje = vehiculo.kilometraje
            existing.flota_id = vehiculo.flota_id
            existing.transportista_id = vehiculo.transportista_id
        else:
            # Create new vehicle
            vehiculo_model = VehiculoModel(
                id=vehiculo.id,
                matricula=vehiculo.matricula,
                marca=vehiculo.marca,
                modelo=vehiculo.modelo,
                tipo=vehiculo.tipo,
                capacidad_carga=vehiculo.capacidad_carga,
                estado=vehiculo.estado,
                fecha_matriculacion=vehiculo.fecha_matriculacion,
                fecha_ultimo_mantenimiento=vehiculo.fecha_ultimo_mantenimiento,
                kilometraje=vehiculo.kilometraje,
                flota_id=vehiculo.flota_id,
                transportista_id=vehiculo.transportista_id
            )
            self.session.add(vehiculo_model)

        self.session.commit()

    def find_by_id(self, vehiculo_id: str) -> Optional[Vehiculo]:
        """Find a vehicle by ID"""
        vehiculo_model = self.session.query(VehiculoModel).filter_by(id=vehiculo_id).first()
        if vehiculo_model:
            return self._model_to_entity(vehiculo_model)
        return None

    def find_all(self) -> List[Vehiculo]:
        """Find all vehicles"""
        vehiculo_models = self.session.query(VehiculoModel).all()
        return [self._model_to_entity(model) for model in vehiculo_models]

    def find_by_flota(self, flota_id: str) -> List[Vehiculo]:
        """Find vehicles by fleet ID"""
        vehiculo_models = self.session.query(VehiculoModel).filter_by(flota_id=flota_id).all()
        return [self._model_to_entity(model) for model in vehiculo_models]

    def find_by_estado(self, estado: str) -> List[Vehiculo]:
        """Find vehicles by status"""
        try:
            estado_enum = EstadoVehiculo(estado)
            vehiculo_models = self.session.query(VehiculoModel).filter_by(estado=estado_enum).all()
            return [self._model_to_entity(model) for model in vehiculo_models]
        except ValueError:
            return []

    def find_disponibles(self) -> List[Vehiculo]:
        """Find available vehicles"""
        vehiculo_models = self.session.query(VehiculoModel).filter_by(estado=EstadoVehiculo.DISPONIBLE).all()
        return [self._model_to_entity(model) for model in vehiculo_models]

    def delete(self, vehiculo_id: str) -> None:
        """Delete a vehicle by ID"""
        vehiculo_model = self.session.query(VehiculoModel).filter_by(id=vehiculo_id).first()
        if vehiculo_model:
            self.session.delete(vehiculo_model)
            self.session.commit()

    def _model_to_entity(self, model: VehiculoModel) -> Vehiculo:
        """Convert SQLAlchemy model to domain entity"""
        return Vehiculo(
            id=model.id,
            matricula=model.matricula,
            marca=model.marca,
            modelo=model.modelo,
            tipo=model.tipo,
            capacidad_carga=model.capacidad_carga,
            estado=model.estado,
            fecha_matriculacion=model.fecha_matriculacion,
            fecha_ultimo_mantenimiento=model.fecha_ultimo_mantenimiento,
            kilometraje=model.kilometraje,
            flota_id=model.flota_id,
            transportista_id=model.transportista_id
        )
