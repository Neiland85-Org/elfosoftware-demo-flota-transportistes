"""
Integration tests for CMR API endpoints
"""
import pytest
from io import BytesIO
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.application.use_cases.cmr_use_cases import ProcesarCMRUseCase, ValidarCMRUseCase
from src.domain.services.cmr_normalizer import CMRNormalizer, MockCMRExtractor

class TestCMRApi:
    """Test CMR API endpoints"""

    def test_extract_cmr_data_success(self, client: TestClient):
        """Test successful CMR data extraction"""
        # Create mock PDF file
        mock_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(CMR Test Document) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000200 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n284\n%%EOF"

        # Create file-like object
        file_obj = BytesIO(mock_pdf_content)
        files = {"file": ("test_cmr.pdf", file_obj, "application/pdf")}

        # Make request
        response = client.post("/documents/cmr/extract", files=files)

        # Assert response
        assert response.status_code == 200
        data = response.json()

        # Verify structure
        assert "numero_cmr" in data
        assert "fecha_emision" in data
        assert "remitente" in data
        assert "destinatario" in data
        assert "matricula_vehiculo" in data
        assert "carga" in data
        assert "estado_procesamiento" in data

        # Verify content
        assert data["numero_cmr"] == "CMR-2024-001234"
        assert data["remitente"]["nombre"] == "Empresa Transportes S.A."
        assert data["destinatario"]["nombre"] == "Logística Industrial Ltd."
        assert data["matricula_vehiculo"] == "1234-ABC"
        assert data["carga"]["peso_bruto"] == 2500.0
        assert data["estado_procesamiento"] == "procesado"

    def test_extract_cmr_data_invalid_file_type(self, client: TestClient):
        """Test CMR extraction with invalid file type"""
        # Create text file
        file_obj = BytesIO(b"not a pdf")
        files = {"file": ("test.txt", file_obj, "text/plain")}

        response = client.post("/documents/cmr/extract", files=files)

        assert response.status_code == 400
        assert "Only PDF files are supported" in response.json()["detail"]

    def test_extract_cmr_data_empty_file(self, client: TestClient):
        """Test CMR extraction with empty file"""
        # Create empty file
        file_obj = BytesIO(b"")
        files = {"file": ("empty.pdf", file_obj, "application/pdf")}

        response = client.post("/documents/cmr/extract", files=files)

        assert response.status_code == 400
        assert "Empty file provided" in response.json()["detail"]

    def test_extract_cmr_data_file_too_large(self, client: TestClient):
        """Test CMR extraction with file too large"""
        # Create file larger than 10MB
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        file_obj = BytesIO(large_content)
        files = {"file": ("large.pdf", file_obj, "application/pdf")}

        response = client.post("/documents/cmr/extract", files=files)

        assert response.status_code == 400
        assert "exceeds maximum allowed size" in response.json()["detail"]

    def test_cmr_health_check(self, client: TestClient):
        """Test CMR health check endpoint"""
        response = client.get("/documents/cmr/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["service"] == "cmr_processor"
        assert "pdf_processing" in data["capabilities"]
        assert "ocr_extraction" in data["capabilities"]
        assert "data_normalization" in data["capabilities"]
        assert "validation" in data["capabilities"]

class TestCMRUseCases:
    """Test CMR use cases"""

    def test_procesar_cmr_use_case_success(self):
        """Test successful CMR processing use case"""
        extractor = MockCMRExtractor()
        normalizer = CMRNormalizer(extractor)
        use_case = ProcesarCMRUseCase(normalizer)

        mock_bytes = b"mock pdf content"
        result = use_case.execute(mock_bytes)

        assert result.numero_cmr == "CMR-2024-001234"
        assert result.estado_procesamiento.name == "PROCESADO"

    def test_procesar_cmr_use_case_empty_bytes(self):
        """Test CMR processing with empty bytes"""
        extractor = MockCMRExtractor()
        normalizer = CMRNormalizer(extractor)
        use_case = ProcesarCMRUseCase(normalizer)

        with pytest.raises(ValueError, match="Document bytes cannot be empty"):
            use_case.execute(b"")

    def test_procesar_cmr_use_case_file_too_large(self):
        """Test CMR processing with file too large"""
        extractor = MockCMRExtractor()
        normalizer = CMRNormalizer(extractor)
        use_case = ProcesarCMRUseCase(normalizer)

        large_bytes = b"x" * (11 * 1024 * 1024)  # 11MB
        with pytest.raises(ValueError, match="exceeds maximum allowed size"):
            use_case.execute(large_bytes)

    def test_validar_cmr_use_case_valid(self):
        """Test CMR validation with valid document"""
        use_case = ValidarCMRUseCase()

        # Create valid CMR document
        from domain.entities.cmr_document import CMRDocument, Remitente, Destinatario, Carga, TipoCarga

        valid_doc = CMRDocument(
            numero_cmr="CMR-2024-001",
            fecha_emision=datetime.now(),
            remitente=Remitente(
                nombre="Test Sender",
                direccion="Test Address",
                ciudad="Test City",
                pais="Test Country"
            ),
            destinatario=Destinatario(
                nombre="Test Recipient",
                direccion="Test Address",
                ciudad="Test City",
                pais="Test Country"
            ),
            matricula_vehiculo="1234-ABC",
            carga=Carga(
                descripcion="Test load",
                tipo=TipoCarga.GENERAL,
                peso_bruto=1000.0
            )
        )

        assert use_case.execute(valid_doc) is True

    def test_validar_cmr_use_case_invalid(self):
        """Test CMR validation with invalid document"""
        use_case = ValidarCMRUseCase()

        # Create invalid CMR document
        from domain.entities.cmr_document import CMRDocument, Remitente, Destinatario, Carga, TipoCarga

        invalid_doc = CMRDocument(
            numero_cmr="",  # Invalid: empty CMR number
            fecha_emision=datetime.now(),
            remitente=Remitente(
                nombre="",  # Invalid: empty name
                direccion="Test Address",
                ciudad="Test City",
                pais="Test Country"
            ),
            destinatario=Destinatario(
                nombre="Test Recipient",
                direccion="Test Address",
                ciudad="Test City",
                pais="Test Country"
            ),
            matricula_vehiculo="1234-ABC",
            carga=Carga(
                descripcion="Test load",
                tipo=TipoCarga.GENERAL,
                peso_bruto=0.0  # Invalid: zero weight
            )
        )

        assert use_case.execute(invalid_doc) is False
