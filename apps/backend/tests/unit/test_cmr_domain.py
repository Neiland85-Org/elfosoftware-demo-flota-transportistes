"""
Unit tests for CMR domain entities and services
"""
import pytest
from datetime import datetime
from src.domain.entities.cmr_document import (
    CMRDocument,
    Remitente,
    Destinatario,
    Carga,
    TipoCarga,
    EstadoCMR,
    RawCMRData
)
from src.domain.services.cmr_normalizer import CMRNormalizer, MockCMRExtractor

class TestCMRDocument:
    """Test CMR document entity"""

    def test_cmr_document_creation(self):
        """Test creating a valid CMR document"""
        remitente = Remitente(
            nombre="Empresa S.A.",
            direccion="Calle Mayor 123",
            ciudad="Madrid",
            pais="España"
        )

        destinatario = Destinatario(
            nombre="Cliente Ltd.",
            direccion="Avenida Central 456",
            ciudad="Barcelona",
            pais="España"
        )

        carga = Carga(
            descripcion="Mercancía general",
            tipo=TipoCarga.GENERAL,
            peso_bruto=1500.0,
            volumen=10.0,
            unidades=25
        )

        cmr_doc = CMRDocument(
            numero_cmr="CMR-2024-001",
            fecha_emision=datetime.now(),
            remitente=remitente,
            destinatario=destinatario,
            matricula_vehiculo="1234-ABC",
            carga=carga
        )

        assert cmr_doc.numero_cmr == "CMR-2024-001"
        assert cmr_doc.estado_procesamiento == EstadoCMR.PENDIENTE
        assert cmr_doc.remitente.nombre == "Empresa S.A."
        assert cmr_doc.carga.peso_bruto == 1500.0

class TestMockCMRExtractor:
    """Test mock CMR extractor"""

    def test_extract_data(self):
        """Test extracting data from mock document"""
        extractor = MockCMRExtractor()
        mock_bytes = b"mock pdf content"

        result = extractor.extract_data(mock_bytes)

        assert isinstance(result, RawCMRData)
        assert "CMR" in result.raw_text
        assert "mock_ocr" in result.metadata["extraction_method"]
        assert len(result.confidence_scores) > 0

class TestCMRNormalizer:
    """Test CMR normalizer service"""

    def test_normalize_document_success(self):
        """Test successful document normalization"""
        extractor = MockCMRExtractor()
        normalizer = CMRNormalizer(extractor)

        mock_bytes = b"mock pdf content"
        result = normalizer.normalize_document(mock_bytes)

        assert isinstance(result, CMRDocument)
        assert result.numero_cmr == "CMR-2024-001234"
        assert result.estado_procesamiento == EstadoCMR.PROCESADO
        assert result.fecha_procesamiento is not None
        assert result.remitente.nombre == "Empresa Transportes S.A."
        assert result.destinatario.nombre == "Logística Industrial Ltd."
        assert result.matricula_vehiculo == "1234-ABC"
        assert result.carga.peso_bruto == 2500.0

    def test_normalize_document_with_error(self):
        """Test document normalization with processing error"""
        class FailingExtractor(MockCMRExtractor):
            def extract_data(self, document_bytes):
                raise Exception("OCR processing failed")

        extractor = FailingExtractor()
        normalizer = CMRNormalizer(extractor)

        mock_bytes = b"mock pdf content"
        result = normalizer.normalize_document(mock_bytes)

        assert result.estado_procesamiento == EstadoCMR.ERROR
        assert result.numero_cmr == "ERROR"
        assert result.errores_procesamiento == "OCR processing failed"

    def test_extract_cmr_number(self):
        """Test CMR number extraction"""
        normalizer = CMRNormalizer(MockCMRExtractor())

        test_cases = [
            ("N° CMR: CMR-2024-001234", "CMR-2024-001234"),
            ("CMR: ABC-123-XYZ", "ABC-123-XYZ"),
            ("Número: TEST-001", "TEST-001"),
            ("No CMR number here", "CMR-UNKNOWN")
        ]

        for text, expected in test_cases:
            result = normalizer._extract_cmr_number(text)
            assert result == expected

    def test_extract_dates(self):
        """Test date extraction"""
        normalizer = CMRNormalizer(MockCMRExtractor())

        text = """
        Fecha de emisión: 15/01/2024
        Fecha de carga: 16/01/2024
        Fecha de entrega: 18/01/2024
        """

        dates = normalizer._extract_dates(text)

        assert len(dates) == 3
        assert dates["emision"].day == 15
        assert dates["emision"].month == 1
        assert dates["emision"].year == 2024

    def test_extract_vehicle_info(self):
        """Test vehicle information extraction"""
        normalizer = CMRNormalizer(MockCMRExtractor())

        text = """
        VEHÍCULO / VEHICLE
        Matrícula: 1234-ABC
        Conductor: Carlos Rodríguez
        """

        matricula, conductor = normalizer._extract_vehicle_info(text)

        assert matricula == "1234-ABC"
        assert conductor == "Carlos Rodríguez"

    def test_extract_carga(self):
        """Test load information extraction"""
        normalizer = CMRNormalizer(MockCMRExtractor())

        text = """
        CARGA / CHARGE / LOAD
        Descripción: Mercancía refrigerada - alimentos
        Tipo: Refrigerada
        Peso bruto: 1200 kg
        Volumen: 8 m³
        Unidades: 30 paquetes
        Valor mercancía: 5000 €
        """

        carga = normalizer._extract_carga(text)

        assert carga.descripcion == "Mercancía refrigerada - alimentos"
        assert carga.tipo == TipoCarga.REFRIGERADA
        assert carga.peso_bruto == 1200.0
        assert carga.volumen == 8.0
        assert carga.unidades == 30
        assert carga.valor_mercancia == 5000.0
