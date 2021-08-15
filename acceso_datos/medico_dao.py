from .conexion_db import obtener_conexion

from modelos.medico import *

conexion = obtener_conexion()


def registrar_medico(medico):
    with conexion:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO usuario (correo, clave, rol) values(%s, %s, %s)"
            cursor.execute(sql, (medico.correo, medico.clave, 'Medico'))
            # conexion.commit()

        with conexion.cursor() as cursor:
            sql = "SELECT codigo FROM usuario WHERE correo=%s"
            cursor.execute(sql, (medico.correo))
            result = cursor.fetchone()
            codigo = result['codigo']

        with conexion.cursor() as cursor:
            sql = "INSERT INTO medico (codigo_usuario, nombres, apellidos, especialidad) values(%s, %s, %s, %s)"
            cursor.execute(sql, (codigo, medico.nombres,
                           medico.apellidos, medico.especialidad))
            conexion.commit()
