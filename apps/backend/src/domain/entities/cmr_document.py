"""
CMR (Carta de Porte) domain entities and services
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class TipoCarga(Enum):
    """Load type enumeration"""
    GENERAL = "general"
    PELIGROSA = "peligrosa"
    FRAGIL = "fragil"
    REFRIGERADA = "refrigerada"
    LIQUIDA = "liquida"

class EstadoCMR(Enum):
    """CMR document status"""
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"
    ERROR = "error"

class Remitente(BaseModel):
    """Sender information"""
    nombre: str = Field(..., description="Sender company name")
    direccion: str = Field(..., description="Sender address")
    ciudad: str = Field(..., description="Sender city")
    pais: str = Field(..., description="Sender country")
    codigo_postal: Optional[str] = Field(None, description="Sender postal code")
    contacto: Optional[str] = Field(None, description="Sender contact person")

class Destinatario(BaseModel):
    """Recipient information"""
    nombre: str = Field(..., description="Recipient company name")
    direccion: str = Field(..., description="Recipient address")
    ciudad: str = Field(..., description="Recipient city")
    pais: str = Field(..., description="Recipient country")
    codigo_postal: Optional[str] = Field(None, description="Recipient postal code")
    contacto: Optional[str] = Field(None, description="Recipient contact person")

class Carga(BaseModel):
    """Load information"""
    descripcion: str = Field(..., description="Load description")
    tipo: TipoCarga = Field(..., description="Load type")
    peso_bruto: float = Field(..., description="Gross weight in kg")
    volumen: Optional[float] = Field(None, description="Volume in m³")
    unidades: Optional[int] = Field(None, description="Number of units/packages")
    valor_mercancia: Optional[float] = Field(None, description="Goods value")

class CMRDocument(BaseModel):
    """Normalized CMR document model"""
    numero_cmr: str = Field(..., description="CMR document number")
    fecha_emision: datetime = Field(..., description="Document issue date")
    fecha_carga: Optional[datetime] = Field(None, description="Loading date")
    fecha_entrega: Optional[datetime] = Field(None, description="Delivery date")

    remitente: Remitente = Field(..., description="Sender information")
    destinatario: Destinatario = Field(..., description="Recipient information")

    matricula_vehiculo: str = Field(..., description="Vehicle license plate")
    conductor: Optional[str] = Field(None, description="Driver name")

    carga: Carga = Field(..., description="Load information")

    instrucciones_especiales: Optional[str] = Field(None, description="Special instructions")
    condiciones_transporte: Optional[str] = Field(None, description="Transport conditions")

    # Metadata
    estado_procesamiento: EstadoCMR = Field(default=EstadoCMR.PENDIENTE, description="Processing status")
    fecha_procesamiento: Optional[datetime] = Field(None, description="Processing timestamp")
    errores_procesamiento: Optional[str] = Field(None, description="Processing errors")

class RawCMRData(BaseModel):
    """Raw extracted data from CMR document"""
    raw_text: str = Field(..., description="Raw extracted text")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores for extracted fields")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
