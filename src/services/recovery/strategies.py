"""
Estrategias de recuperación y fallback para servicios críticos.
Permite definir mecanismos automáticos para recuperación ante fallos y degradación controlada.
"""

class RecoveryStrategy:
    """Interfaz base para estrategias de recuperación."""
    def recover(self, *args, **kwargs):
        raise NotImplementedError("Debe implementar el método recover().")

class SimpleRetryStrategy(RecoveryStrategy):
    """Reintenta una operación un número limitado de veces antes de fallar."""
    def __init__(self, retries=3, delay=1):
        self.retries = retries
        self.delay = delay

    def recover(self, func, *args, **kwargs):
        import time
        last_exception = None
        for _ in range(self.retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                time.sleep(self.delay)
        raise last_exception

# Aquí se pueden agregar más estrategias (fallback, circuit breaker, etc.)
