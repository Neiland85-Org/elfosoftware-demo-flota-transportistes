#!/bin/bash

echo "🔍 Verificando instalación de Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "📥 Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    echo "   1. Ve al sitio web"
    echo "   2. Descarga la versión para macOS"
    echo "   3. Instala el .dmg"
    echo "   4. Abre Docker Desktop y espera a que inicie"
    exit 1
fi

echo "✅ Docker está instalado"

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "⚠️  Docker no está corriendo"
    echo "▶️  Abre Docker Desktop desde tu dock o aplicaciones"
    echo "   Espera a que el ícono de Docker deje de estar rojo"
    exit 1
fi

echo "✅ Docker está corriendo"

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose no está disponible"
    echo "   Docker Desktop incluye Docker Compose V2"
    echo "   Usa 'docker compose' en lugar de 'docker-compose'"
fi

echo "✅ Docker Compose está disponible"

# Probar Docker con una imagen simple
echo "🧪 Probando Docker con una imagen de prueba..."
if docker run --rm hello-world &> /dev/null; then
    echo "✅ Docker funciona correctamente"
else
    echo "❌ Error al ejecutar contenedor de prueba"
    exit 1
fi

echo ""
echo "🎉 ¡Docker está listo para usar!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Copia .env.example a .env y configura tus variables"
echo "2. Ejecuta: ./deploy.sh dev"
echo "3. O usa: docker compose -f docker-compose.prod.yml up -d"
