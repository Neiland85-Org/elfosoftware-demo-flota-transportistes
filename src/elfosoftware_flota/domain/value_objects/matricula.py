"""Matricula Value Object

Value Object que representa la matrícula de un vehículo.
Inmutable y con validación de formato.
"""

import re
from typing import Pattern

from pydantic import BaseModel, Field, field_validator


class Matricula(BaseModel):
    """Value Object para matrícula de vehículo."""

    valor: str = Field(..., min_length=1, max_length=10)

    model_config = {"frozen": True}

    @field_validator('valor')
    @classmethod
    def validar_formato_matricula(cls, v: str) -> str:
        """Valida el formato de la matrícula."""
        v_upper = v.upper().strip()

        # Validación simple por ahora
        if len(v_upper) < 1:
            raise ValueError("Matrícula no puede estar vacía")

        return v_upper

    def __str__(self) -> str:
        """Representación en string de la matrícula."""
        return self.valor

    def __eq__(self, other: object) -> bool:
        """Compara dos matrículas por su valor."""
        if not isinstance(other, Matricula):
            return NotImplemented
        return self.valor == other.valor

    def __hash__(self) -> int:
        """Hash basado en el valor de la matrícula."""
        return hash(self.valor)

    @property
    def numero(self) -> str:
        """Retorna la parte numérica de la matrícula."""
        return self.valor[:4]

    @property
    def letras(self) -> str:
        """Retorna la parte alfabética de la matrícula."""
        return self.valor[4:]
