"""
Path: src/utils/logging/simple_logger.py
"""

import sys
import logging
import colorlog
from src.interfaces.ILogger import ILogger

# Configuración global inicial (no es usada por LoggerService)
logger = logging.getLogger("profebot")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Nuevo Protocolo de Logging Consistente:
# - Niveles soportados: DEBUG, INFO, WARNING, ERROR
# - Formato estándar del mensaje: [NIVEL] - [timestamp] - Mensaje
# - Todos los módulos deben utilizar este logger para garantizar la trazabilidad uniforme.
# - Se recomienda utilizar métodos: debug(), info(), warning(), error() según el contexto.

class LoggerService(ILogger):
    """
    LoggerService encapsula la configuración central de logging y
    provee métodos para registrar mensajes en distintos niveles
    (debug, info, warning, error, exception).
    Se configura según la variable '--verbose' de sys.argv para ajustar el nivel de detalle.
    """
    def __init__(self):
        self._logger = logging.getLogger("app_logger")
        if '--verbose' in sys.argv:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            app_console_handler = logging.StreamHandler()
            app_formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(filename)15.15s:%(lineno)03d - %(levelname)-5.5s - %(message)s",
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            app_console_handler.setFormatter(app_formatter)
            self._logger.addHandler(app_console_handler)

    def debug(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de depuración."
        self._logger.debug(msg, *args, stacklevel=2, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje informativo."
        self._logger.info(msg, *args, stacklevel=2, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de advertencia."
        self._logger.warning(msg, *args, stacklevel=2, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de error."
        self._logger.error(msg, *args, stacklevel=2, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de excepción con información de la traza."
        self._logger.exception(msg, *args, stacklevel=2, **kwargs)

class SharedLoggerService:
    "Servicio de logging para monitorear servicios compartidos."

    def __init__(self):
        self.logger = logging.getLogger("SharedServicesLogger")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)
