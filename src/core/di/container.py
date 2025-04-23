"""
Contenedor principal de dependencias para VisionArtificial_py.
Define providers para servicios principales y configuración.
"""
from dependency_injector import containers, providers
from src.utils.logging.simple_logger import LoggerService
from src.services.video_capture_service import VideoCaptureService
from src.services.video_processing import VideoProcessingService
from src.config.config_loader import load_config

class AppContainer(containers.DeclarativeContainer):
    config = providers.Singleton(load_config)
    logger = providers.Singleton(LoggerService, use_context=True)
    video_capture_service = providers.Factory(
        VideoCaptureService,
        camera_index=0,  # Puede ser parametrizado dinámicamente
        timeout=None
    )
    video_processing_service = providers.Factory(
        VideoProcessingService
    )
    # Agregar más providers según sea necesario
