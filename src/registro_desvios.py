
from logs.config_logger import configurar_logging
import mysql.connector
from datetime import datetime
from pytz import timezone
import requests
from pid_controller import PIDController, enviar_datos, enviar_datos_sql

# Configuración del logger
logger = configurar_logging()

def registrar_desvio(desvio_mm, TOLERANCIA):
    # Mostrar el desvío en la consola
    if desvio_mm > TOLERANCIA:
        logger.info(f"Desvío registrado: {desvio_mm} mm ENG")
        texto1 = f" Desvio: {desvio_mm} mm ENG"
        enviar_datos("ena_f",desvio_mm)


    elif desvio_mm < -TOLERANCIA:
        logger.info(f"Desvío registrado: {desvio_mm} mm OP")
        texto1 = f"Desvio: {desvio_mm} mm OP"
        enviar_datos("ena_r",desvio_mm)

    else:  # Esto cubre el caso donde el desvío está dentro de la tolerancia de +/- 2mm
        logger.info(f"Desvío registrado: {desvio_mm} mm - Centrado")
        if desvio_mm > 0:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado ENG"
        elif desvio_mm < 0:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado OP"
        else:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado"

    return texto1
    # Enviar el desvío a la base de datos