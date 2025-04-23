# Arquitectura del Contenedor de Inyección de Dependencias (DI) para VisionArtificial_py

## Objetivo
Definir la estructura y organización del contenedor DI usando `dependency-injector`, asegurando flexibilidad, escalabilidad y fácil integración con Flask.

## Estructura Propuesta
- **Directorio:** `src/core/di/`
- **Archivos principales:**
  - `container.py`: Definición del contenedor principal y providers.
  - `providers.py`: Providers personalizados y utilidades para servicios.
  - `config_providers.py`: Providers para configuración dinámica.
  - `flask_integration.py`: Utilidades para integrar el contenedor con Flask.

## Organización de Providers
- **Singleton:** Servicios de infraestructura, logger, configuración, etc.
- **Factory/Transient:** Servicios de dominio, casos de uso, procesadores de video.
- **Configuración:** Provider especial para cargar parámetros desde el sistema de configuración.

## Ejemplo de Providers
- LoggerService: Singleton
- VideoCaptureService: Factory (puede recibir configuración dinámica)
- VideoProcessingService: Factory
- Config: Singleton (inyectado desde config_loader)

## Estrategia de Resolución
- El contenedor resuelve dependencias automáticamente usando wiring.
- Los servicios pueden solicitar dependencias por constructor o método.
- Integración con Flask mediante extensión o inyección en blueprints/routes.

## Consideraciones
- Permitir sobreescritura de providers para testing.
- Soporte para scopes adicionales si se requiere (por request, thread, etc.).
- Documentar cómo registrar nuevos servicios y cómo consumirlos desde rutas o servicios.

---

**Próximo paso:** Implementar la estructura básica del contenedor DI en `src/core/di/` según este diseño.
