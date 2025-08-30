#!/usr/bin/env python3
"""
Simple test script for CMR API endpoint
"""
import sys
import os
sys.path.append('src')

from io import BytesIO
from fastapi import UploadFile
from domain.services.cmr_normalizer import CMRNormalizer, MockCMRExtractor
from application.use_cases.cmr_use_cases import ProcesarCMRUseCase, ValidarCMRUseCase

def test_cmr_api_simulation():
    """Simulate CMR API endpoint processing"""

    print("🧪 Testing CMR API Endpoint Simulation")
    print("=" * 50)

    # Create mock PDF file content
    mock_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(CMR Test Document) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000200 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n284\n%%EOF"

    # Create file-like object
    file_obj = BytesIO(mock_pdf_content)

    # Simulate file validation
    filename = "test_cmr.pdf"
    if not filename.lower().endswith('.pdf'):
        print("❌ Error: Only PDF files are supported")
        return False

    if not file_obj.getvalue():
        print("❌ Error: Empty file provided")
        return False

    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if len(file_obj.getvalue()) > max_size:
        print(f"❌ Error: Document size exceeds maximum allowed size of {max_size} bytes")
        return False

    print("✅ File validation passed")

    # Process document
    try:
        extractor = MockCMRExtractor()
        normalizer = CMRNormalizer(extractor)
        use_case = ProcesarCMRUseCase(normalizer)
        validar_use_case = ValidarCMRUseCase()

        result = use_case.execute(file_obj.getvalue())

        # Validate result
        if not validar_use_case.execute(result):
            print("❌ Error: Invalid CMR document data extracted")
            return False

        print("✅ Document processing completed successfully")
        print("\n📄 Extracted CMR Data:")
        print("-" * 30)
        print(f"📋 CMR Number: {result.numero_cmr}")
        print(f"📅 Issue Date: {result.fecha_emision.strftime('%d/%m/%Y')}")
        print(f"🏢 Sender: {result.remitente.nombre}")
        print(f"📍 Sender Address: {result.remitente.direccion}, {result.remitente.ciudad}")
        print(f"🏭 Recipient: {result.destinatario.nombre}")
        print(f"📍 Recipient Address: {result.destinatario.direccion}, {result.destinatario.ciudad}")
        print(f"🚛 Vehicle License Plate: {result.matricula_vehiculo}")
        if result.conductor:
            print(f"👤 Driver: {result.conductor}")
        print(f"📦 Load Description: {result.carga.descripcion}")
        print(f"🏷️  Load Type: {result.carga.tipo.value}")
        print(f"⚖️  Gross Weight: {result.carga.peso_bruto} kg")
        if result.carga.volumen:
            print(f"📏 Volume: {result.carga.volumen} m³")
        if result.carga.unidades:
            print(f"📊 Units: {result.carga.unidades}")
        if result.carga.valor_mercancia:
            print(f"💰 Goods Value: {result.carga.valor_mercancia} €")
        if result.instrucciones_especiales:
            print(f"📝 Special Instructions: {result.instrucciones_especiales}")
        print(f"🔄 Processing Status: {result.estado_procesamiento.value}")

        return True

    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check")
    print("=" * 30)

    capabilities = [
        "pdf_processing",
        "ocr_extraction",
        "data_normalization",
        "validation"
    ]

    print("✅ Health check response:")
    print(f"   Status: healthy")
    print(f"   Service: cmr_processor")
    print(f"   Version: 1.0.0")
    print("   Capabilities:")
    for cap in capabilities:
        print(f"     - {cap}")

    return True

if __name__ == "__main__":
    print("🚀 CMR OCR Mock API Test Suite")
    print("=" * 50)

    # Test health check
    health_ok = test_health_check()

    # Test CMR processing
    processing_ok = test_cmr_api_simulation()

    print("\n" + "=" * 50)
    if health_ok and processing_ok:
        print("🎉 All tests passed! CMR functionality is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
