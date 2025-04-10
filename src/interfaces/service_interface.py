from abc import ABC, abstractmethod

class IService(ABC):
    """
    Interfaz para servicios compartidos.
    """

    @abstractmethod
    def initialize(self):
        """
        Inicializa el servicio.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Finaliza el servicio.
        """
        pass
