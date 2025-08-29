# Pull Request Template

## 📋 Descripción
<!-- Describe brevemente los cambios realizados -->

### Tipo de Cambio
- [ ] 🐛 Bug fix (cambio que corrige un problema)
- [ ] ✨ Nueva funcionalidad (cambio que añade funcionalidad)
- [ ] 💥 Breaking change (cambio que podría romper funcionalidad existente)
- [ ] 📚 Documentación (cambios solo en documentación)
- [ ] 🧹 Refactor (cambio de código que no corrige bugs ni añade funcionalidad)
- [ ] 🧪 Tests (añadir o corregir tests)
- [ ] 🔧 Configuración (cambios en herramientas, CI/CD, etc.)

## 🏗️ Arquitectura DELFOS

### Capas Afectadas
- [ ] **Domain Layer** (Entidades, Value Objects, Domain Services)
- [ ] **Application Layer** (Use Cases, Application Services)
- [ ] **Infrastructure Layer** (Repositories, External Services)
- [ ] **Presentation Layer** (API, Controllers, DTOs)

### Bounded Context
<!-- ¿A qué bounded context pertenecen estos cambios? -->
- [ ] Flota
- [ ] Transportista  
- [ ] Tracking
- [ ] Rutas
- [ ] Otro: _____________

## 🧪 Testing

### Tipos de Tests Incluidos
- [ ] Unit Tests (Domain Layer)
- [ ] Integration Tests (Infrastructure Layer)
- [ ] API Tests (Presentation Layer)
- [ ] E2E Tests (Workflows completos)

### Coverage
<!-- Incluye información sobre el coverage de tests si aplica -->
- Coverage actual: _%
- Tests añadidos: __
- Tests modificados: __

## 🔍 Checklist de Calidad

### Código
- [ ] El código sigue las convenciones de estilo (PEP 8)
- [ ] Se han añadido type hints donde corresponde
- [ ] Se han añadido docstrings para métodos públicos
- [ ] El código pasa todas las comprobaciones de linting (ruff, mypy)
- [ ] Se han ejecutado los tests y todos pasan

### DDD & DELFOS
- [ ] Las entidades de dominio están correctamente encapsuladas
- [ ] Los Value Objects son inmutables
- [ ] Los Aggregates mantienen consistencia interna
- [ ] Los Domain Events se usan apropiadamente (si aplica)
- [ ] La separación de capas se mantiene correctamente

### Documentación
- [ ] Se ha actualizado la documentación relevante
- [ ] Se han añadido comentarios donde el código es complejo
- [ ] Los cambios en API están documentados

## 🔗 Issues Relacionadas
<!-- Enlaza las issues que este PR resuelve -->
Fixes #(issue)
Relates to #(issue)

## 📸 Capturas de Pantalla
<!-- Si aplica, incluye capturas de pantalla de cambios en UI -->

## 🚀 Instrucciones de Deployment
<!-- Si requiere pasos especiales para deployment -->
- [ ] Requiere migración de base de datos
- [ ] Requiere variables de entorno nuevas
- [ ] Requiere actualización de dependencias
- [ ] Cambios en configuración de infraestructura

## 👀 Notas para Reviewers
<!-- Información adicional que puede ser útil para los reviewers -->

### Áreas de Enfoque
<!-- Indica en qué deberían enfocarse especialmente los reviewers -->

### Preocupaciones
<!-- Menciona cualquier preocupación específica sobre estos cambios -->