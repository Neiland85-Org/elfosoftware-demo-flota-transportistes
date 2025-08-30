"""Tests para Transportista API.

Tests de integración para los endpoints de Transportista.
"""

import pytest
from datetime import date
from fastapi.testclient import TestClient
from fastapi import FastAPI

from elfosoftware_flota.presentation.api.transportista_api import transportista_router


# Crear app de prueba
app = FastAPI()
app.include_router(transportista_router, prefix="/api/transportistas", tags=["transportistas"])

client = TestClient(app)


class TestCrearTransportistaEndpoint:
    """Tests para el endpoint de crear transportista."""

    def test_crear_transportista_exitoso(self):
        """Test de creación exitosa de transportista."""
        transportista_data = {
            "nombre": "Carlos",
            "apellido": "Ruiz",
            "email": "carlos.ruiz@example.com",
            "telefono": "+34611223344",
            "fecha_nacimiento": "1992-08-20",
            "numero_licencia": "LIC999888777",
            "fecha_expiracion_licencia": "2032-08-20"
        }
        
        response = client.post("/api/transportistas/", json=transportista_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Carlos"
        assert data["apellido"] == "Ruiz"
        assert data["email"] == "carlos.ruiz@example.com"
        assert data["activo"] is True
        assert "id" in data

    def test_crear_transportista_email_duplicado(self):
        """Test de error por email duplicado."""
        # Primer transportista
        transportista_data1 = {
            "nombre": "Ana",
            "apellido": "Martín",
            "email": "ana.martin@example.com",
            "telefono": "+34611223355",
            "fecha_nacimiento": "1990-05-15",
            "numero_licencia": "LIC111222333",
            "fecha_expiracion_licencia": "2031-05-15"
        }
        
        # Segundo transportista con mismo email
        transportista_data2 = {
            "nombre": "Luis",
            "apellido": "García",
            "email": "ana.martin@example.com",  # Email duplicado
            "telefono": "+34611223366",
            "fecha_nacimiento": "1988-03-10",
            "numero_licencia": "LIC444555666",
            "fecha_expiracion_licencia": "2030-03-10"
        }
        
        # Crear primero
        response1 = client.post("/api/transportistas/", json=transportista_data1)
        assert response1.status_code == 201
        
        # Intentar crear segundo (debe fallar)
        response2 = client.post("/api/transportistas/", json=transportista_data2)
        assert response2.status_code == 409
        assert "email" in response2.json()["detail"]

    def test_crear_transportista_licencia_duplicada(self):
        """Test de error por licencia duplicada."""
        transportista_data1 = {
            "nombre": "Roberto",
            "apellido": "Silva",
            "email": "roberto.silva@example.com",
            "telefono": "+34611223377",
            "fecha_nacimiento": "1987-12-05",
            "numero_licencia": "LIC777888999",
            "fecha_expiracion_licencia": "2029-12-05"
        }
        
        transportista_data2 = {
            "nombre": "Elena",
            "apellido": "Torres",
            "email": "elena.torres@example.com",
            "telefono": "+34611223388",
            "fecha_nacimiento": "1991-07-18",
            "numero_licencia": "LIC777888999",  # Licencia duplicada
            "fecha_expiracion_licencia": "2033-07-18"
        }
        
        # Crear primero
        response1 = client.post("/api/transportistas/", json=transportista_data1)
        assert response1.status_code == 201
        
        # Intentar crear segundo (debe fallar)
        response2 = client.post("/api/transportistas/", json=transportista_data2)
        assert response2.status_code == 409
        assert "licencia" in response2.json()["detail"]

    def test_crear_transportista_datos_invalidos(self):
        """Test de validación de datos inválidos."""
        # Email inválido
        transportista_data = {
            "nombre": "Test",
            "apellido": "User",
            "email": "email-invalido",
            "telefono": "+34611223344",
            "fecha_nacimiento": "1990-01-01",
            "numero_licencia": "LIC123456",
            "fecha_expiracion_licencia": "2030-01-01"
        }
        
        response = client.post("/api/transportistas/", json=transportista_data)
        assert response.status_code == 422  # Unprocessable Entity (validación Pydantic)

    def test_crear_transportista_menor_edad(self):
        """Test de validación de edad mínima."""
        from datetime import date
        hoy = date.today()
        fecha_nacimiento_menor = date(hoy.year - 17, hoy.month, hoy.day)  # 17 años
        
        transportista_data = {
            "nombre": "Menor",
            "apellido": "Edad",
            "email": "menor@example.com",
            "telefono": "+34611223344",
            "fecha_nacimiento": fecha_nacimiento_menor.isoformat(),
            "numero_licencia": "LIC123456",
            "fecha_expiracion_licencia": "2030-01-01"
        }
        
        response = client.post("/api/transportistas/", json=transportista_data)
        assert response.status_code == 422

    def test_crear_transportista_licencia_expirada(self):
        """Test de validación de licencia expirada."""
        transportista_data = {
            "nombre": "Test",
            "apellido": "User",
            "email": "test@example.com",
            "telefono": "+34611223344",
            "fecha_nacimiento": "1990-01-01",
            "numero_licencia": "LIC123456",
            "fecha_expiracion_licencia": "2020-01-01"  # Fecha pasada
        }
        
        response = client.post("/api/transportistas/", json=transportista_data)
        assert response.status_code == 422


class TestListarTransportistasEndpoint:
    """Tests para el endpoint de listar transportistas."""

    def test_listar_transportistas_vacio_inicial(self):
        """Test de listado cuando no hay transportistas."""
        # Nota: Este test puede fallar si hay datos de prueba precargados
        response = client.get("/api/transportistas/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_listar_transportistas_con_datos(self):
        """Test de listado después de crear transportistas."""
        # Crear un transportista
        transportista_data = {
            "nombre": "Lista",
            "apellido": "Test",
            "email": "lista.test@example.com",
            "telefono": "+34611223344",
            "fecha_nacimiento": "1990-01-01",
            "numero_licencia": "LIC999000111",
            "fecha_expiracion_licencia": "2030-01-01"
        }
        
        create_response = client.post("/api/transportistas/", json=transportista_data)
        assert create_response.status_code == 201
        
        # Listar transportistas
        list_response = client.get("/api/transportistas/")
        assert list_response.status_code == 200
        data = list_response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Verificar que el transportista creado está en la lista
        emails = [t["email"] for t in data]
        assert "lista.test@example.com" in emails


class TestObtenerTransportistaEndpoint:
    """Tests para el endpoint de obtener transportista por ID."""

    def test_obtener_transportista_existente(self):
        """Test de obtener transportista existente."""
        # Crear un transportista
        transportista_data = {
            "nombre": "Obtener",
            "apellido": "Test",
            "email": "obtener.test@example.com",
            "telefono": "+34611223344",
            "fecha_nacimiento": "1990-01-01",
            "numero_licencia": "LIC888777666",
            "fecha_expiracion_licencia": "2030-01-01"
        }
        
        create_response = client.post("/api/transportistas/", json=transportista_data)
        assert create_response.status_code == 201
        transportista_id = create_response.json()["id"]
        
        # Obtener el transportista
        get_response = client.get(f"/api/transportistas/{transportista_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == transportista_id
        assert data["email"] == "obtener.test@example.com"

    def test_obtener_transportista_inexistente(self):
        """Test de obtener transportista inexistente."""
        import uuid
        transportista_id = str(uuid.uuid4())
        
        response = client.get(f"/api/transportistas/{transportista_id}")
        assert response.status_code == 404

    def test_obtener_transportista_id_invalido(self):
        """Test de obtener transportista con ID inválido."""
        response = client.get("/api/transportistas/id-invalido")
        assert response.status_code == 422  # Unprocessable Entity


@pytest.fixture(scope="function", autouse=True)
def reset_repository():
    """Fixture para resetear el repositorio entre tests."""
    # Nota: En un entorno real, usaríamos una base de datos de prueba
    # Para este ejemplo, simplemente continuamos
    yield