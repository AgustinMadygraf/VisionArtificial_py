class ConfigController:
    """
    Controlador para manejar la lógica de configuración.
    """

    def __init__(self, config_service):
        self.config_service = config_service

    def get_config(self, key, default=None):
        """
        Obtiene un valor de configuración.
        """
        return self.config_service.get(key, default)

    def set_config(self, key, value):
        """
        Establece un valor de configuración.
        """
        self.config_service.set(key, value)

    def add_observer(self, observer):
        """
        Agrega un observador para cambios en la configuración.
        """
        self.config_service.add_observer(observer)

    def remove_observer(self, observer):
        """
        Elimina un observador de cambios en la configuración.
        """
        self.config_service.remove_observer(observer)
