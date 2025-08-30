#!/bin/bash
# Script de desarrollo para el proyecto Elfosoftware Flota Transportistes
# Configura el PYTHONPATH correctamente para el desarrollo local

export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

echo "🐳 PYTHONPATH configurado: $PYTHONPATH"
echo "🚀 Ejecutando comando: $@"

# Ejecutar el comando pasado como argumento
exec "$@"
