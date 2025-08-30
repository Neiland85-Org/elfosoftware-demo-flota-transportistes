#!/usr/bin/env python3
"""
Example usage of CMR OCR API endpoint
"""
import requests
from pathlib import Path

def example_cmr_api_usage():
    """
    Example of how to use the CMR OCR API endpoint
    """

    # API endpoint URL (when running locally)
    api_url = "http://localhost:8000"

    print("📋 CMR OCR API Usage Example")
    print("=" * 40)

    print("\n1. Health Check:")
    print(f"   GET {api_url}/documents/cmr/health")
    print("   Response: Check if CMR service is healthy")

    print("\n2. Extract CMR Data:")
    print(f"   POST {api_url}/documents/cmr/extract")
    print("   Content-Type: multipart/form-data")
    print("   Body: file (PDF document)")
    print("   Response: Normalized CMR data in JSON format")

    print("\n3. Example cURL command:")
    print("# curl -X POST \"http://localhost:8000/documents/cmr/extract\" \\")
    print("#      -H \"accept: application/json\" \\")
    print("#      -H \"Content-Type: multipart/form-data\" \\")
    print("#      -F \"file=@/path/to/your/cmr_document.pdf\"")

    print("\n4. Example Python requests:")
    print("""
import requests

# Health check
response = requests.get("http://localhost:8000/documents/cmr/health")
print(response.json())

# Extract CMR data
with open("cmr_document.pdf", "rb") as f:
    files = {"file": ("cmr_document.pdf", f, "application/pdf")}
    response = requests.post(
        "http://localhost:8000/documents/cmr/extract",
        files=files
    )

if response.status_code == 200:
    cmr_data = response.json()
    print(f"CMR Number: {cmr_data['numero_cmr']}")
    print(f"Sender: {cmr_data['remitente']['nombre']}")
    print(f"Recipient: {cmr_data['destinatario']['nombre']}")
    print(f"Vehicle: {cmr_data['matricula_vehiculo']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
    """)

    print("\n5. Expected JSON Response Structure:")
    print("""
{
  "numero_cmr": "CMR-2024-001234",
  "fecha_emision": "2024-01-15T00:00:00",
  "fecha_carga": "2024-01-16T00:00:00",
  "fecha_entrega": "2024-01-18T00:00:00",
  "remitente": {
    "nombre": "Empresa Transportes S.A.",
    "direccion": "Calle Mayor 123",
    "ciudad": "Madrid",
    "pais": "España",
    "codigo_postal": null,
    "contacto": "Juan Pérez"
  },
  "destinatario": {
    "nombre": "Logística Industrial Ltd.",
    "direccion": "Avenida Industrial 456",
    "ciudad": "Barcelona",
    "pais": "España",
    "codigo_postal": null,
    "contacto": "María García"
  },
  "matricula_vehiculo": "1234-ABC",
  "conductor": "Carlos Rodríguez",
  "carga": {
    "descripcion": "Mercancía general - electrodomésticos",
    "tipo": "general",
    "peso_bruto": 2500.0,
    "volumen": 15.0,
    "unidades": 50,
    "valor_mercancia": 15000.0
  },
  "instrucciones_especiales": "Manejar con cuidado. Temperatura controlada 15-25°C.",
  "condiciones_transporte": null,
  "estado_procesamiento": "procesado",
  "fecha_procesamiento": "2024-01-15T10:30:00",
  "errores_procesamiento": null
}
    """)

    print("\n6. Error Responses:")
    print("   400 - Bad Request: Invalid file type or empty file")
    print("   400 - Bad Request: File too large (>10MB)")
    print("   422 - Unprocessable Entity: Invalid CMR data extracted")
    print("   500 - Internal Server Error: Processing failed")

    print("\n7. Supported File Types:")
    print("   - PDF documents (.pdf extension required)")
    print("   - Maximum file size: 10MB")
    print("   - Content: CMR (Carta de Porte) documents")

    print("\n8. Data Validation:")
    print("   - CMR number must be present and valid")
    print("   - Sender and recipient information required")
    print("   - Vehicle license plate required")
    print("   - Gross weight must be > 0")
    print("   - Load dates must be logical (loading before delivery)")

if __name__ == "__main__":
    example_cmr_api_usage()
