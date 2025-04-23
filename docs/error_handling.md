# Sistema de Manejo de Errores en VisionArtificial_py

## 1. Jerarquía de Excepciones Personalizadas
- Todas las excepciones del dominio heredan de `VisionArtificialError` (en `src/exceptions/base.py`).
- Existen subclases para errores de servicio (`ServiceError`, `ServiceUnavailableError`, etc.) y de configuración (`ConfigError`, `ConfigNotFoundError`, etc.).
- Permite distinguir y manejar de forma granular los distintos tipos de errores.

## 2. Middleware de Manejo Centralizado de Excepciones
- Implementado en `src/middleware/error_handler.py` y registrado en `main.py`.
- Captura todas las excepciones no manejadas y las transforma en respuestas HTTP estructuradas.
- Registra los errores usando el sistema de logging contextual.
- Proporciona respuestas diferenciadas según el tipo de excepción (400, 500, 503, etc.).

## 3. Logging Contextual
- El logger (`LoggerService` en `src/utils/logging/simple_logger.py`) puede usar un `ContextLogger` que añade información contextual (ID de solicitud, IP, ruta, método HTTP).
- Todos los logs de errores y excepciones incluyen este contexto para facilitar el diagnóstico.
- El logger contextual se activa pasando `use_context=True` al inicializar `LoggerService`.

## 4. Estrategias de Recuperación y Fallback
- Definidas en `src/services/recovery/strategies.py`.
- Ejemplo: `SimpleRetryStrategy` permite reintentar operaciones críticas (abrir cámara, leer frame) ante fallos temporales.
- Integrado en `video_capture_service.py` y `camera_service.py` para mejorar la resiliencia.

## 5. Mejores Prácticas
- Utiliza siempre excepciones específicas del dominio para errores esperados.
- No capturar excepciones genéricas en rutas: deja que el middleware las gestione.
- Usa el logger contextual para todos los mensajes de error.
- Aplica estrategias de recuperación en servicios críticos para evitar caídas por fallos transitorios.

---

**Referencia rápida de archivos:**
- Excepciones: `src/exceptions/`
- Middleware: `src/middleware/error_handler.py`
- Logging: `src/utils/logging/`
- Estrategias de recuperación: `src/services/recovery/strategies.py`
