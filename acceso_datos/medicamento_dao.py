from .conexion_db import obtener_conexion

from modelos.medicamento import *

conexion = obtener_conexion()

def registrar_medicamento(medicamento):
    with conexion.cursor() as cursor:
        sql = "INSERT INTO medicamento(nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento) values(%s, %s, %s, %s)"
        cursor.execute(sql, (medicamento.nombre, medicamento.registro_sanitario, medicamento.fecha_elaboracion, medicamento.fecha_vencimiento))
        conexion.commit()