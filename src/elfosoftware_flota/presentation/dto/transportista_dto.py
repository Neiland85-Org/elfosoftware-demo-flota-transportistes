"""DTOs para Transportista.

Data Transfer Objects para la gestión de Transportistas.
Arquitectura DELFOS - Presentation Layer.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class CrearTransportistaRequest(BaseModel):
    """DTO para crear un nuevo transportista."""
    
    nombre: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Nombre del transportista",
        example="Juan"
    )
    apellido: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Apellido del transportista",
        example="Pérez García"
    )
    email: EmailStr = Field(
        ...,
        description="Dirección de email del transportista",
        example="juan.perez@email.com"
    )
    telefono: str = Field(
        ...,
        min_length=9,
        max_length=20,
        description="Número de teléfono del transportista",
        example="+34612345678"
    )
    fecha_nacimiento: date = Field(
        ...,
        description="Fecha de nacimiento del transportista",
        example="1985-06-15"
    )
    numero_licencia: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Número de licencia de conducir",
        example="LIC123456789"
    )
    fecha_expiracion_licencia: date = Field(
        ...,
        description="Fecha de expiración de la licencia",
        example="2030-06-15"
    )
    
    @validator('nombre', 'apellido')
    def validar_nombres(cls, v):
        """Validar que los nombres no estén vacíos y tengan formato correcto."""
        if not v or not v.strip():
            raise ValueError('El nombre/apellido no puede estar vacío')
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('El nombre/apellido solo puede contener letras y espacios')
        return v.strip().title()
    
    @validator('telefono')
    def validar_telefono(cls, v):
        """Validar formato básico del teléfono."""
        # Remover espacios y caracteres comunes
        telefono_limpio = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not telefono_limpio.replace('+', '').isdigit():
            raise ValueError('El teléfono debe contener solo números y el símbolo +')
        return v
    
    @validator('numero_licencia')
    def validar_licencia(cls, v):
        """Validar formato básico de la licencia."""
        if not v or not v.strip():
            raise ValueError('La licencia no puede estar vacía')
        licencia_limpia = v.strip().upper()
        if len(licencia_limpia) < 5:
            raise ValueError('La licencia debe tener al menos 5 caracteres')
        return licencia_limpia
    
    @validator('fecha_nacimiento')
    def validar_fecha_nacimiento(cls, v):
        """Validar que la fecha de nacimiento sea coherente."""
        hoy = date.today()
        if v >= hoy:
            raise ValueError('La fecha de nacimiento debe ser anterior a la fecha actual')
        # Verificar que la persona tenga al menos 18 años
        edad = hoy.year - v.year - ((hoy.month, hoy.day) < (v.month, v.day))
        if edad < 18:
            raise ValueError('El transportista debe ser mayor de 18 años')
        if edad > 100:
            raise ValueError('La fecha de nacimiento no parece válida')
        return v
    
    @validator('fecha_expiracion_licencia')
    def validar_fecha_expiracion(cls, v):
        """Validar que la fecha de expiración sea válida."""
        hoy = date.today()
        if v <= hoy:
            raise ValueError('La fecha de expiración de la licencia debe ser futura')
        return v


class TransportistaResponse(BaseModel):
    """DTO para respuesta de transportista."""
    
    id: UUID = Field(..., description="ID único del transportista")
    nombre: str = Field(..., description="Nombre del transportista")
    apellido: str = Field(..., description="Apellido del transportista")
    email: EmailStr = Field(..., description="Email del transportista")
    telefono: str = Field(..., description="Teléfono del transportista")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento")
    numero_licencia: str = Field(..., description="Número de licencia")
    fecha_expiracion_licencia: date = Field(..., description="Fecha de expiración de licencia")
    activo: bool = Field(..., description="Si el transportista está activo")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    fecha_actualizacion: datetime = Field(..., description="Fecha de actualización")
    
    class Config:
        """Configuración de Pydantic."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class TransportistaErrorResponse(BaseModel):
    """DTO para respuestas de error."""
    
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    details: Optional[dict] = Field(None, description="Detalles adicionales del error")
    
    class Config:
        """Configuración de Pydantic."""
        json_schema_extra = {
            "example": {
                "error": "VALIDATION_ERROR",
                "message": "Los datos proporcionados no son válidos",
                "details": {
                    "field": "email",
                    "issue": "Formato de email inválido"
                }
            }
        }