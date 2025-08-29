# 🚛 Elfosoftware Demo Flota Transportistes

Demo de flota per a transportistes creada des de zero amb arquitectura alineada amb DELFOS i allotjada a l'organització per usar eines d'Isus, Copilotagen i CI/CD corporatiu.

*Fleet demo for carriers, built from scratch with architecture aligned with DELFOS and hosted within the organization to use Isus tools, Copilotagen tools, and corporate CI/CD.*

## 🏗️ Arquitectura DELFOS

Este proyecto implementa la arquitectura **DELFOS** (Domain-driven Enterprise Layered Framework for Optimal Solutions):

- **Domain Layer**: Entidades de negocio, Value Objects, Domain Services
- **Application Layer**: Use Cases y Application Services  
- **Infrastructure Layer**: Repositories, servicios externos, persistencia
- **Presentation Layer**: APIs, Controllers, DTOs

## 🤖 Modo Organización Habilitado

### ✅ GitHub Copilot Configurado
- 📋 **Custom Instructions**: Ver [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
- 🎯 Configurado para DDD, testing, estilo y arquitectura DELFOS
- 🔧 Optimizado para desarrollo de sistemas de transporte

### ✅ Gestión de Proyectos
- 📊 **Issues Templates**: Bug reports y feature requests con contexto DDD
- 🔄 **PR Templates**: Incluye checklist de arquitectura DELFOS  
- 👥 **CODEOWNERS**: Reviews obligatorias por equipo especializado

### ✅ Seguridad por Defecto
- 🔒 **CodeQL**: Análisis estático de seguridad automatizado
- 📦 **Dependabot**: Actualizaciones automáticas de dependencias
- 🛡️ **Private Vulnerability Reporting**: Via [`SECURITY.md`](SECURITY.md)
- 🔍 **Trivy**: Escaneo de vulnerabilidades en dependencies

### ✅ Entornos de Desarrollo
- 🐳 **Dev Containers**: Configuración completa en [`.devcontainer/`](.devcontainer/)
- ☁️ **Codespaces**: Ready para desarrollo en la nube
- 🛠️ **Herramientas Preconfiguradas**: Python, FastAPI, pytest, ruff, mypy

### ✅ CI/CD Sin Secretos
- 🔐 **OIDC**: Configurado para AWS, Azure y GCP
- 🚀 **GitHub Actions**: Pipeline completo de CI/CD
- 🧪 **Testing**: Unit, integration y e2e tests
- 📈 **Coverage**: Reportes automáticos de cobertura

## 🚀 Desarrollo Rápido

### Comenzar con Codespaces
1. Haz clic en "Code" → "Create codespace on main"
2. El entorno se configurará automáticamente con todas las herramientas
3. Ejecuta `dev` para iniciar el servidor FastAPI

### Desarrollo Local con Dev Containers
1. Abre el proyecto en VS Code
2. Instala la extensión "Dev Containers"
3. Comando: "Dev Containers: Reopen in Container"

### Comandos Útiles
```bash
# Servidor de desarrollo
dev

# Ejecutar tests
test-all           # Todos los tests con coverage
test-unit          # Solo tests unitarios
test-integration   # Solo tests de integración

# Linting y formato
lint               # ruff + mypy
format             # black + isort
```

## 🏭 Dominio: Flota de Transportistes

### Bounded Contexts
- **Flota**: Gestión de vehículos y recursos
- **Transportista**: Conductores y operadores
- **Tracking**: Seguimiento en tiempo real  
- **Rutas**: Planificación y optimización

### Entidades Principales
- `Flota` (Aggregate Root)
- `Transportista` (Entity)
- `Vehiculo` (Entity)
- `Ruta` (Value Object)
- `Carga` (Entity)

## 📚 Recursos

- [Copilot Instructions](.github/copilot-instructions.md) - Guías para IA
- [Security Policy](SECURITY.md) - Política de seguridad
- [Contributing Guidelines](.github/PULL_REQUEST_TEMPLATE.md) - Cómo contribuir
- [Architecture Decision Records](docs/adr/) - Decisiones de arquitectura

## 🎯 Estado del Proyecto

- [x] Configuración organizacional completa
- [x] Arquitectura DELFOS definida
- [ ] Implementación del dominio Flota
- [ ] APIs REST con FastAPI
- [ ] Integración con servicios externos
- [ ] Dashboard de gestión
