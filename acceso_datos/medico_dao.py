from .conexion_db import obtener_conexion

from modelos.medico import *


def registrar_medico(medico):
    conexion = obtener_conexion()
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


def recuperar_medico(codigo):
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "SELECT m.codigo, nombres, apellidos, correo, clave, especialidad FROM usuario u, medico m WHERE m.codigo_usuario=u.codigo AND m.codigo=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        if result != None:
            return Medico(result['codigo'], result['nombres'], result['apellidos'],
                          result['correo'], result['especialidad'], result['clave'])

        return None


def editar_medico(medico):
    conexion = obtener_conexion()
    with conexion:
        with conexion.cursor() as cursor:
            sql = "UPDATE usuario u, medico m SET u.correo=%s, u.clave=%s, m.nombres=%s, m.apellidos=%s, m.especialidad=%s WHERE m.codigo_usuario=u.codigo AND m.codigo=%s"
            cursor.execute(sql, (medico.correo, medico.clave, medico.nombres,
                           medico.apellidos, medico.especialidad, medico.codigo))
            conexion.commit()


def eliminar_medico(codigo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE u, m FROM usuario u, medico m WHERE m.codigo_usuario=u.codigo AND m.codigo=%s"
        cursor.execute(sql, (codigo))
        conexion.commit()


def recuperar_medicos():
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "SELECT m.codigo, nombres, apellidos, correo, clave, especialidad FROM usuario u, medico m WHERE m.codigo_usuario=u.codigo"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result != None:
            medicos = []
            for fila in result:
                print(fila)
                medico = Medico(fila['codigo'], fila['nombres'], fila['apellidos'],
                                fila['correo'], fila['especialidad'], fila['clave'])
                medicos.append(medico)

            return medicos

        return None
