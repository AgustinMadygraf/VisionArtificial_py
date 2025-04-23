# Evaluación de Bibliotecas de Inyección de Dependencias (DI) para VisionArtificial_py

## Objetivo
Seleccionar la biblioteca de DI más adecuada para reemplazar el sistema factory actual, facilitando la gestión de dependencias, configuración y modularidad.

## Opciones Evaluadas

### 1. dependency-injector
- **Ventajas:**
  - Muy popular y activo.
  - Soporta providers, configuración, scopes (singleton/transient), wiring automático.
  - Documentación extensa y ejemplos para Flask.
  - Integración sencilla con testing y configuración por entorno.
- **Desventajas:**
  - Sintaxis algo más extensa que otras opciones.

### 2. injector
- **Ventajas:**
  - Sintaxis simple y minimalista.
  - Inspirado en Guice (Google).
- **Desventajas:**
  - Menos características avanzadas (no soporta scopes complejos ni configuración avanzada).
  - Menor actividad y comunidad.

### 3. punq
- **Ventajas:**
  - Muy ligero y fácil de usar.
  - Ideal para proyectos pequeños o prototipos.
- **Desventajas:**
  - No soporta scopes, configuración avanzada ni integración con frameworks.
  - Comunidad pequeña.

## Recomendación
**Se recomienda usar `dependency-injector`** por su madurez, soporte de scopes, integración con Flask y flexibilidad para proyectos medianos y grandes.

## Referencias
- https://python-dependency-injector.ets-labs.org/
- https://injector.readthedocs.io/
- https://github.com/bobthemighty/punq

---

**Próximo paso:** Agregar `dependency-injector` a requirements.txt e iniciar el diseño del contenedor DI.
