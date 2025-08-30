"""
CMR document processing domain services
"""
import re
from typing import Optional, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod

from src.domain.entities.cmr_document import (
    CMRDocument,
    Remitente,
    Destinatario,
    Carga,
    TipoCarga,
    EstadoCMR,
    RawCMRData
)

class CMRExtractor(ABC):
    """Abstract base class for CMR document extractors"""

    @abstractmethod
    def extract_data(self, document_bytes: bytes) -> RawCMRData:
        """Extract raw data from CMR document"""
        pass

class MockCMRExtractor(CMRExtractor):
    """Mock CMR extractor for demonstration purposes"""

    def extract_data(self, document_bytes: bytes) -> RawCMRData:
        """Extract data from mock CMR document"""
        # Simulate OCR extraction with mock data
        mock_text = """
        CMR - Carta de Porte Internacional
        N° CMR: CMR-2024-001234

        REMITENTE / EXPEDITEUR / SENDER
        Empresa Transportes S.A.
        Calle Mayor 123
        Madrid, España
        Contacto: Juan Pérez

        DESTINATARIO / DESTINATAIRE / RECIPIENT
        Logística Industrial Ltd.
        Avenida Industrial 456
        Barcelona, España
        Contacto: María García

        FECHAS / DATES
        Fecha de emisión: 15/01/2024
        Fecha de carga: 16/01/2024
        Fecha de entrega: 18/01/2024

        VEHÍCULO / VEHICLE
        Matrícula: 1234-ABC
        Conductor: Carlos Rodríguez

        CARGA / CHARGE / LOAD
        Descripción: Mercancía general - electrodomésticos
        Tipo: General
        Peso bruto: 2500 kg
        Volumen: 15 m³
        Unidades: 50 paquetes
        Valor mercancía: 15000 €

        INSTRUCCIONES ESPECIALES
        Manejar con cuidado. Temperatura controlada 15-25°C.
        """

        return RawCMRData(
            raw_text=mock_text,
            confidence_scores={
                "numero_cmr": 0.95,
                "remitente": 0.90,
                "destinatario": 0.88,
                "fechas": 0.92,
                "matricula": 0.98,
                "carga": 0.85
            },
            metadata={
                "document_type": "CMR",
                "extraction_method": "mock_ocr",
                "processing_timestamp": datetime.now().isoformat()
            }
        )

class CMRNormalizer:
    """Domain service for normalizing CMR document data"""

    def __init__(self, extractor: CMRExtractor):
        self.extractor = extractor

    def normalize_document(self, document_bytes: bytes) -> CMRDocument:
        """Normalize CMR document from raw bytes"""
        try:
            # Extract raw data
            raw_data = self.extractor.extract_data(document_bytes)

            # Parse and normalize fields
            normalized_data = self._parse_raw_data(raw_data.raw_text)

            # Create CMR document
            cmr_doc = CMRDocument(
                **normalized_data,
                estado_procesamiento=EstadoCMR.PROCESADO,
                fecha_procesamiento=datetime.now()
            )

            return cmr_doc

        except Exception as e:
            # Return document with error status
            return CMRDocument(
                numero_cmr="ERROR",
                fecha_emision=datetime.now(),
                remitente=Remitente(
                    nombre="Error",
                    direccion="Error",
                    ciudad="Error",
                    pais="Error"
                ),
                destinatario=Destinatario(
                    nombre="Error",
                    direccion="Error",
                    ciudad="Error",
                    pais="Error"
                ),
                matricula_vehiculo="ERROR",
                carga=Carga(
                    descripcion="Error processing document",
                    tipo=TipoCarga.GENERAL,
                    peso_bruto=0.0
                ),
                estado_procesamiento=EstadoCMR.ERROR,
                fecha_procesamiento=datetime.now(),
                errores_procesamiento=str(e)
            )

    def _parse_raw_data(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw text and extract normalized fields"""
        # Extract CMR number
        numero_cmr = self._extract_cmr_number(raw_text)

        # Extract dates
        fechas = self._extract_dates(raw_text)

        # Extract sender info
        remitente = self._extract_remitente(raw_text)

        # Extract recipient info
        destinatario = self._extract_destinatario(raw_text)

        # Extract vehicle info
        matricula, conductor = self._extract_vehicle_info(raw_text)

        # Extract load info
        carga = self._extract_carga(raw_text)

        return {
            "numero_cmr": numero_cmr,
            "fecha_emision": fechas.get("emision", datetime.now()),
            "fecha_carga": fechas.get("carga"),
            "fecha_entrega": fechas.get("entrega"),
            "remitente": remitente,
            "destinatario": destinatario,
            "matricula_vehiculo": matricula,
            "conductor": conductor,
            "carga": carga,
            "instrucciones_especiales": self._extract_instructions(raw_text)
        }

    def _extract_cmr_number(self, text: str) -> str:
        """Extract CMR document number"""
        patterns = [
            r'N°\s*CMR[:\s]*([A-Z0-9\-]+)',
            r'CMR[:\s]*([A-Z0-9\-]+)(?:\s|$)',  # Added word boundary
            r'Número[:\s]*([A-Z0-9\-]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                cmr_number = match.group(1).strip()
                # Validate that the CMR number contains at least one uppercase letter or digit
                if re.search(r'[A-Z0-9]', cmr_number):
                    return cmr_number

        return "CMR-UNKNOWN"

    def _extract_dates(self, text: str) -> Dict[str, datetime]:
        """Extract dates from text"""
        dates = {}

        # Date patterns (DD/MM/YYYY or DD-MM-YYYY)
        date_patterns = [
            r'Fecha de emisión[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
            r'Fecha de carga[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
            r'Fecha de entrega[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})'
        ]

        field_names = ["emision", "carga", "entrega"]

        for pattern, field in zip(date_patterns, field_names):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                try:
                    # Parse date (assuming DD/MM/YYYY format)
                    day, month, year = map(int, date_str.replace('-', '/').split('/'))
                    dates[field] = datetime(year, month, day)
                except ValueError:
                    continue

        return dates

    def _extract_remitente(self, text: str) -> Remitente:
        """Extract sender information"""
        # Find sender section
        sender_pattern = r'REMITENTE.*?/.*?SENDER(.*?)(?=DESTINATARIO|$)'
        match = re.search(sender_pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            sender_text = match.group(1)
            lines = [line.strip() for line in sender_text.split('\n') if line.strip()]

            return Remitente(
                nombre=lines[0] if lines else "Unknown",
                direccion=lines[1] if len(lines) > 1 else "",
                ciudad=lines[2] if len(lines) > 2 else "",
                pais=lines[3] if len(lines) > 3 else "",
                contacto=self._extract_contact(sender_text)
            )

        return Remitente(
            nombre="Unknown",
            direccion="",
            ciudad="",
            pais=""
        )

    def _extract_destinatario(self, text: str) -> Destinatario:
        """Extract recipient information"""
        # Find recipient section
        recipient_pattern = r'DESTINATARIO.*?/.*?RECIPIENT(.*?)(?=FECHAS|VEHÍCULO|$)'
        match = re.search(recipient_pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            recipient_text = match.group(1)
            lines = [line.strip() for line in recipient_text.split('\n') if line.strip()]

            return Destinatario(
                nombre=lines[0] if lines else "Unknown",
                direccion=lines[1] if len(lines) > 1 else "",
                ciudad=lines[2] if len(lines) > 2 else "",
                pais=lines[3] if len(lines) > 3 else "",
                contacto=self._extract_contact(recipient_text)
            )

        return Destinatario(
            nombre="Unknown",
            direccion="",
            ciudad="",
            pais=""
        )

    def _extract_vehicle_info(self, text: str) -> tuple[str, Optional[str]]:
        """Extract vehicle license plate and driver"""
        matricula = "UNKNOWN"
        conductor = None

        # Extract license plate
        plate_match = re.search(r'Matrícula[:\s]*([A-Z0-9\-]+)', text, re.IGNORECASE)
        if plate_match:
            matricula = plate_match.group(1)

        # Extract driver
        driver_match = re.search(r'Conductor[:\s]*([^\n]+)', text, re.IGNORECASE)
        if driver_match:
            conductor = driver_match.group(1).strip()

        return matricula, conductor

    def _extract_carga(self, text: str) -> Carga:
        """Extract load information"""
        # Find load section
        load_pattern = r'CARGA.*?/.*?LOAD(.*?)(?=INSTRUCCIONES|$)'
        match = re.search(load_pattern, text, re.DOTALL | re.IGNORECASE)

        carga_text = match.group(1) if match else text

        # Extract description
        desc_match = re.search(r'Descripción[:\s]*([^\n]+)', carga_text, re.IGNORECASE)
        descripcion = desc_match.group(1).strip() if desc_match else "Mercancía general"

        # Extract weight
        weight_match = re.search(r'Peso bruto[:\s]*(\d+(?:\.\d+)?)\s*kg', carga_text, re.IGNORECASE)
        peso_bruto = float(weight_match.group(1)) if weight_match else 0.0

        # Extract volume
        volume_match = re.search(r'Volumen[:\s]*(\d+(?:\.\d+)?)\s*m³', carga_text, re.IGNORECASE)
        volumen = float(volume_match.group(1)) if volume_match else None

        # Extract units
        units_match = re.search(r'Unidades[:\s]*(\d+)', carga_text, re.IGNORECASE)
        unidades = int(units_match.group(1)) if units_match else None

        # Extract value
        value_match = re.search(r'Valor.*?(\d+(?:\.\d+)?)\s*€', carga_text, re.IGNORECASE)
        valor = float(value_match.group(1)) if value_match else None

        # Determine load type
        tipo = TipoCarga.GENERAL
        if "peligrosa" in descripcion.lower():
            tipo = TipoCarga.PELIGROSA
        elif "frágil" in descripcion.lower():
            tipo = TipoCarga.FRAGIL
        elif "refrigerada" in descripcion.lower():
            tipo = TipoCarga.REFRIGERADA

        return Carga(
            descripcion=descripcion,
            tipo=tipo,
            peso_bruto=peso_bruto,
            volumen=volumen,
            unidades=unidades,
            valor_mercancia=valor
        )

    def _extract_instructions(self, text: str) -> Optional[str]:
        """Extract special instructions"""
        instructions_pattern = r'INSTRUCCIONES ESPECIALES(.*?)(?=$)'
        match = re.search(instructions_pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            instructions = match.group(1).strip()
            return instructions if instructions else None

        return None

    def _extract_contact(self, text: str) -> Optional[str]:
        """Extract contact person from text"""
        contact_match = re.search(r'Contacto[:\s]*([^\n]+)', text, re.IGNORECASE)
        return contact_match.group(1).strip() if contact_match else None
