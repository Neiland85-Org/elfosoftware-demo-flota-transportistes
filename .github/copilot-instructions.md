# Copilot Instructions - Elfosoftware Demo Flota Transportistes

## Arquitectura DELFOS
Este proyecto sigue la arquitectura DELFOS (Domain-driven Enterprise Layered Framework for Optimal Solutions):

- **Domain Layer**: Implementar entidades de dominio, value objects, y domain services
- **Application Layer**: Use cases y application services 
- **Infrastructure Layer**: Repositories, external services, y persistence
- **Presentation Layer**: Controllers, DTOs, y presentation logic

## Principios de Desarrollo

### Domain-Driven Design (DDD)
- Usar ubiquitous language en toda la codebase
- Implementar bounded contexts claros
- Crear aggregates para encapsular business logic
- Usar domain events para comunicación entre bounded contexts

### Testing Guidelines
- **Unit Tests**: Cada clase de dominio debe tener tests unitarios
- **Integration Tests**: Testear la integración entre capas
- **End-to-End Tests**: Validar workflows completos del negocio
- Usar TDD cuando sea posible
- Aim for >80% code coverage
- Mock external dependencies en unit tests

### Estilo de Código
- Seguir PEP 8 para Python
- Usar type hints en todas las funciones públicas
- Documentar métodos públicos con docstrings
- Variables y funciones en snake_case
- Clases en PascalCase
- Constantes en UPPER_CASE

### Arquitectura del Proyecto
```
src/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── repositories/
│   └── services/
├── application/
│   ├── use_cases/
│   └── services/
├── infrastructure/
│   ├── persistence/
│   ├── external_services/
│   └── repositories/
└── presentation/
    ├── api/
    ├── dto/
    └── controllers/
```

### Transportistas Domain Specifics
- **Flota**: Aggregate root para gestión de vehículos
- **Transportista**: Entity que representa el conductor/operador
- **Ruta**: Value object para rutas y destinos
- **Carga**: Entity para mercancías transportadas
- **Tracking**: Domain service para seguimiento en tiempo real

## Patterns a Usar
- Repository Pattern para acceso a datos
- Factory Pattern para creación de entidades complejas
- Strategy Pattern para diferentes tipos de cálculos (rutas, costos)
- Observer Pattern para eventos de dominio
- Command Pattern para operaciones de aplicación

## Evitar
- Anemic Domain Model
- Tight coupling entre capas
- Business logic en controllers
- Direct database access desde domain layer
- Hardcoded values (usar configuration)

## Herramientas y Frameworks
- **FastAPI** para REST APIs
- **SQLAlchemy** con Repository Pattern
- **Pydantic** para validation y DTOs
- **pytest** para testing
- **Ruff** para linting
- **mypy** para type checking