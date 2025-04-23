import logging
import time
import threading
from flask import has_request_context, request, g

class ContextLogger(logging.LoggerAdapter):
    """
    Logger que añade contexto de la petición Flask (ID, IP, tiempo, etc.) a cada mensaje.
    """
    def process(self, msg, kwargs):
        context = self._get_context()
        msg = f"{context} | {msg}"
        return msg, kwargs

    def _get_context(self):
        if has_request_context():
            req_id = getattr(g, 'request_id', threading.get_ident())
            ip = request.remote_addr
            path = request.path
            method = request.method
            return f"RID={req_id} IP={ip} {method} {path}"
        else:
            return f"RID={threading.get_ident()}"

# Utilidad para inicializar el logger contextual

def get_context_logger(name="app_logger"):
    base_logger = logging.getLogger(name)
    return ContextLogger(base_logger, {})
