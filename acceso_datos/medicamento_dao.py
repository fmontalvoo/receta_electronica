from .conexion_db import obtener_conexion

from modelos.medicamento import *

conexion = obtener_conexion()


def registrar_medicamento(medicamento):
    with conexion.cursor() as cursor:
        sql = "INSERT INTO medicamento(nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento) values(%s, %s, %s, %s)"
        cursor.execute(sql, (medicamento.nombre, medicamento.registro_sanitario,
                       medicamento.fecha_elaboracion, medicamento.fecha_vencimiento))
        conexion.commit()


def recuperar_medicamento(codigo):
    with conexion .cursor() as cursor:
        sql = "SELECT * FROM medicamento WHERE codigo=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        if result != None:
            return Medicamento(
                result['codigo'], result['nombre'], result['registro_sanitario'], result['fecha_elaboracion'], result['fecha_elaboracion'])
        return None


def editar_medicamento(medicamento):
    with conexion.cursor() as cursor:
        sql = "UPDATE medicamento SET nombre=%s, registro_sanitario=%s, fecha_elaboracion=%s, fecha_vencimiento=%s WHERE codigo=%s"
        cursor.execute(sql, (medicamento.nombre, medicamento.registro_sanitario,
                       medicamento.fecha_elaboracion, medicamento.fecha_vencimiento, medicamento.codigo))
        conexion.commit()


def eliminar_medicamento(codigo):
    with conexion.cursor() as cursor:
        sql = "DELETE FROM medicamento WHERE codigo=%s"
        cursor.execute(sql, (codigo))
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
