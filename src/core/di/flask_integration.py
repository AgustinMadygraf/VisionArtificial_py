"""
Integración del contenedor DI con Flask.
Permite adjuntar el contenedor a la app y accederlo desde cualquier parte.
"""
def attach_container(app, container):
    """Adjunta el contenedor DI a la app Flask."""
    app.container = container

def get_container(app):
    """Obtiene el contenedor DI desde la app Flask."""
    return getattr(app, 'container', None)
