
from logs.config_logger import configurar_logging
import mysql.connector
from datetime import datetime

# Configuración del logger
logger = configurar_logging()

def registrar_desvio(desvio_mm, TOLERANCIA):
    # Mostrar el desvío en la consola
    if desvio_mm > TOLERANCIA:
        logger.info(f"Desvío registrado: {desvio_mm} mm ENG")
        texto1 = f" Desvio: {desvio_mm} mm ENG"

    elif desvio_mm < -TOLERANCIA:
        logger.info(f"Desvío registrado: {desvio_mm} mm OP")
        texto1 = f"Desvio: {desvio_mm} mm OP"
    else:  # Esto cubre el caso donde el desvío está dentro de la tolerancia de +/- 2mm
        logger.info(f"Desvío registrado: {desvio_mm} mm - Centrado")
        if desvio_mm > 0:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado ENG"
        elif desvio_mm < 0:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado OP"
        else:
            texto1 = f"Desvio: {desvio_mm} mm - Centrado"

        # Ejemplo de datos a insertar
        datos = [
            (1234567890, 30, 0),  # unixtime, desvio, enable
            (1234567891, -5, 1),
            (1234567892, 3, 1)
        ]
        enviar_datos(datos)
    return texto1





def enviar_datos(datos):
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="registro_va"
        )
        cursor = conn.cursor()


        for unixtime, desvio, enable in datos:
            # Calcular datetime desde unixtime
            dt = datetime.utcfromtimestamp(unixtime)
            
            # Calcular direccion
            direccion = 1 if desvio > 0 else 0
            
            # Calcular enable
            enable_val = 1 if abs(desvio) > 2 else 0
            
            # Insertar datos en la tabla
            cursor.execute('''
                INSERT INTO desvio_papel (unixtime, datetime, desvio, direccion, enable)
                VALUES (%s, %s, %s, %s, %s)
            ''', (unixtime, dt, desvio, direccion, enable_val))

        # Confirmar la transacción
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")

    finally:
        # Cerrar la conexión
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión cerrada")


