# Sistema de Configuración para VisionArtificial_py

Este proyecto utiliza un sistema de configuración robusto y flexible, basado en clases de configuración, variables de entorno y segmentación modular por dominio y servicios.

## Selección de entorno

La configuración activa se selecciona automáticamente según la variable de entorno `APP_ENV`:
- `APP_ENV=default` (por defecto)
- `APP_ENV=production`

Ejemplo (Windows):
```
set APP_ENV=production
python run_flask.py
```

## Sobrescritura por variables de entorno

Cualquier variable de entorno en mayúsculas que coincida con un atributo de configuración sobrescribirá su valor. Ejemplo:
```
set SECRET_KEY=mi-clave-secreta
set DEBUG=True
python run_flask.py
```

## Estructura modular

- **default.py** y **production.py**: Configuración base y de producción.
- **video_config.py**: Parámetros específicos del dominio de video.
- **services_config.py**: Parámetros para la factory de servicios.

## Ejemplo de configuración de servicios

En `src/config/services_config.py`:
```python
SERVICES_CONFIG = {
    'video_capture_service': {
        'camera_index': 0,
        'timeout': 10,
    },
    'video_processing_service': {
        'processing_mode': 'fast',
        'use_gpu': False,
    },
}
```

## Extensión

Para agregar un nuevo dominio o servicio:
1. Crea un archivo de configuración (por ejemplo, `logging_config.py`).
2. Importe y agrega la configuración en `default.py` y/o `production.py`.
3. Usa los parámetros desde tu código accediendo a `app.config` o a la clase de configuración activa.

## Referencias
- `src/config/config_loader.py`: Lógica de carga y sobrescritura.
- `src/config/default.py`, `src/config/production.py`: Ejemplo de integración modular.
- `src/core/service_factory.py`: Uso de SERVICES_CONFIG para inicialización flexible.
