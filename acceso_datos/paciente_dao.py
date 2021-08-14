from .conexion_db import obtener_conexion

from modelos.paciente import *

conexion = obtener_conexion()

def registrar_paciente(paciente):
    with conexion:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO usuario (correo, clave, rol) values(%s, %s, %s)"
            cursor.execute(sql, (paciente.correo, paciente.clave, 'Paciente'))
            # conexion.commit()

        with conexion.cursor() as cursor:
            sql = "SELECT codigo FROM usuario WHERE correo=%s"
            cursor.execute(sql, (paciente.correo))
            result = cursor.fetchone()
            codigo = result['codigo']

        with conexion.cursor() as cursor:
            sql = "INSERT INTO paciente (codigo_usuario, nombres, apellidos, historial_clinico) values(%s, %s, %s, %s)"
            cursor.execute(sql, (codigo, paciente.nombres, paciente.apellidos, paciente.historial_clinico))
            conexion.commit()
        

        

        