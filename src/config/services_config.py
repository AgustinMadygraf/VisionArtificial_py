"""
Configuración específica para servicios utilizados en la aplicación.
"""

SERVICES_CONFIG = {
    'video_capture_service': {
        'camera_index': 0,
        'timeout': 10,
    },
    'video_processing_service': {
        'processing_mode': 'fast',
        'use_gpu': False,
        'processor_name': 'grayscale',  # Selección dinámica de algoritmo
    },
    # Puedes agregar más configuraciones de servicios aquí
}
