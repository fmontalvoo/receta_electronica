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
            cursor.execute(sql, (codigo, paciente.nombres,
                           paciente.apellidos, paciente.historial_clinico))
            conexion.commit()


def recuperar_paciente(codigo):
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "SELECT p.codigo, nombres, apellidos, correo, clave, historial_clinico FROM usuario u, paciente p WHERE p.codigo_usuario=u.codigo AND p.codigo=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        if result != None:
            return Paciente(result['codigo'], result['nombres'], result['apellidos'],
                            result['correo'], result['historial_clinico'], result['clave'])

        return None


def editar_paciente(paciente):
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "UPDATE usuario u, paciente p SET u.correo=%s, u.clave=%s, p.nombres=%s, p.apellidos=%s, p.historial_clinico=%s WHERE p.codigo_usuario=u.codigo AND p.codigo=%s"
        cursor.execute(sql, (paciente.correo, paciente.clave, paciente.nombres,
                             paciente.apellidos, paciente.historial_clinico, paciente.codigo))
        conexion.commit()


def eliminar_paciente(codigo):
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "DELETE u, p FROM usuario u, paciente p WHERE p.codigo_usuario=u.codigo AND p.codigo=%s"
        cursor.execute(sql, (codigo))
        conexion.commit()


def recuperar_pacientes():
    conexion = obtener_conexion()
    with conexion .cursor() as cursor:
        sql = "SELECT p.codigo, nombres, apellidos, correo, clave, historial_clinico FROM usuario u, paciente p WHERE p.codigo_usuario=u.codigo"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result != None:
            pacientes = []
            for fila in result:
                paciente = Paciente(fila['codigo'], fila['nombres'], fila['apellidos'],
                                    fila['correo'], fila['historial_clinico'], fila['clave'])
                pacientes.append(paciente)
            return pacientes
        return None
