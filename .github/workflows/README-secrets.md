# Secretos requeridos para CI/CD

## Secretos Obligatorios

- **DOCKER_HUB_USERNAME**: Usuario de Docker Hub para pushes de imágenes
- **DOCKERHUB_PAT_TOKEN**: Token de acceso personal de Docker Hub
- **PYPI_API_TOKEN**: Token de API de PyPI para publicar paquetes Python

## Secretos Opcionales (dependiendo del setup)

- **CODECOV_TOKEN**: Para subir reportes de cobertura a Codecov
- **NPM_TOKEN**: Si usas paquetes privados de npm (@elfosoftware scope)
- **NODE_AUTH_TOKEN**: Token alternativo para registry npm privado

## GITHUB_TOKEN

Ya está disponible automáticamente, pero asegúrate de que tenga permisos para:

- Leer contenido del repo
- Escribir en security-events (para Trivy)
- Crear releases (para release-please)
