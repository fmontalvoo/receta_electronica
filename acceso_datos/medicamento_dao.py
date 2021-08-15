from .conexion_db import obtener_conexion

from modelos.medicamento import *

conexion = obtener_conexion()


def registrar_medicamento(medicamento):
    with conexion.cursor() as cursor:
        sql = "INSERT INTO medicamento(nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento) values(%s, %s, %s, %s)"
        cursor.execute(sql, (medicamento.nombre, medicamento.registro_sanitario,
                       medicamento.fecha_elaboracion, medicamento.fecha_vencimiento))
        conexion.commit()


def recuperar_medicamentos():
    with conexion .cursor() as cursor:
        sql = "SELECT * FROM medicamento"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result != None:
            medicamentos = []
            for fila in result:
                medicamento = Medicamento(
                    fila['codigo'], fila['nombre'], fila['registro_sanitario'], fila['fecha_elaboracion'], fila['fecha_elaboracion'])
                medicamentos.append(medicamento)
            return medicamentos
        return None
