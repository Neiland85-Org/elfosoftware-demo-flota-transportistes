#!/bin/bash
echo "🚀 Iniciando servidor FastAPI - Arquitectura DELFOS..."
echo "📍 API disponible en: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs"
echo ""

# Cambiar al directorio src para ejecutar el servidor
cd src

# Ejecutar el servidor con uvicorn
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
