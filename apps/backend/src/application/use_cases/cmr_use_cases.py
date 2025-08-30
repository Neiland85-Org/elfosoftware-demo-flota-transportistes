"""
CMR document processing use cases
"""
from typing import Optional
from domain.entities.cmr_document import CMRDocument
from domain.services.cmr_normalizer import CMRNormalizer

class ProcesarCMRUseCase:
    """Use case for processing CMR documents"""

    def __init__(self, cmr_normalizer: CMRNormalizer):
        self.cmr_normalizer = cmr_normalizer

    def execute(self, document_bytes: bytes) -> CMRDocument:
        """
        Process CMR document and return normalized data

        Args:
            document_bytes: Raw PDF document bytes

        Returns:
            Normalized CMR document
        """
        if not document_bytes:
            raise ValueError("Document bytes cannot be empty")

        # Validate document size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(document_bytes) > max_size:
            raise ValueError(f"Document size exceeds maximum allowed size of {max_size} bytes")

        # Process document using domain service
        normalized_document = self.cmr_normalizer.normalize_document(document_bytes)

        return normalized_document

class ValidarCMRUseCase:
    """Use case for validating CMR document data"""

    def execute(self, cmr_document: CMRDocument) -> bool:
        """
        Validate CMR document data

        Args:
            cmr_document: CMR document to validate

        Returns:
            True if valid, False otherwise
        """
        # Basic validation rules
        if not cmr_document.numero_cmr or cmr_document.numero_cmr == "ERROR":
            return False

        if not cmr_document.remitente.nombre or cmr_document.remitente.nombre == "Error":
            return False

        if not cmr_document.destinatario.nombre or cmr_document.destinatario.nombre == "Error":
            return False

        if not cmr_document.matricula_vehiculo or cmr_document.matricula_vehiculo == "ERROR":
            return False

        if cmr_document.carga.peso_bruto <= 0:
            return False

        # Date validation
        if cmr_document.fecha_carga and cmr_document.fecha_entrega:
            if cmr_document.fecha_carga > cmr_document.fecha_entrega:
                return False

        return True
