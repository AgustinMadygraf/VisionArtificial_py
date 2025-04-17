# Configuración de la Aplicación Flask por Entorno

La aplicación permite seleccionar la configuración (desarrollo, producción, etc.) de forma flexible al inicializar la clase `MainApp`.

## Estrategia de Configuración

- **Clases de configuración**: Se encuentran en `src/config/`.
  - `DefaultConfig`: Configuración por defecto/desarrollo.
  - `ProductionConfig`: Configuración para producción.
- **Selección de entorno**: Se realiza al crear la instancia de `MainApp` en `run.py`.

### Ejemplo de uso en `run.py`

```python
from src.main import MainApp
from src.utils.logging.simple_logger import LoggerService
from src.config.production import ProductionConfig  # O usa DefaultConfig para desarrollo

if __name__ == "__main__":
    logger = LoggerService()
    main_app = MainApp(logger, config_object=ProductionConfig)  # Cambia aquí la configuración
    main_app.run()
```

- Para cambiar de entorno, importa y pasa la clase de configuración deseada (`ProductionConfig` o `DefaultConfig`).
- Si no se pasa ningún argumento, se usará `DefaultConfig` por defecto.

## Añadir o modificar configuraciones

1. Crea una nueva clase en `src/config/` que herede de `DefaultConfig`.
2. Define los parámetros específicos para ese entorno.
3. Importe y pásala como argumento al crear `MainApp`.

---

**Ejemplo de nueva configuración:**

```python
# src/config/staging.py
from src.config.default import DefaultConfig
class StagingConfig(DefaultConfig):
    DEBUG = True
    SECRET_KEY = 'staging-secret-key'
```

Luego en `run.py`:
```python
from src.config.staging import StagingConfig
main_app = MainApp(logger, config_object=StagingConfig)
```
