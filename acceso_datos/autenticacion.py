from .conexion_db import obtener_conexion

from modelos.usuario import *

conexion = obtener_conexion()


def recuperar_usuario(correo, clave):
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM usuario WHERE correo=%s AND clave=%s"
        cursor.execute(sql, (correo, clave))
        result = cursor.fetchone()
        print(result)
        if result != None:
            codigo = result['codigo']
            rol = result['rol']
            if rol == 'Administrador':
                return Usuario(codigo, 'Usuario administrador', correo, rol)
            return None


def recuperar_medico(codigo):
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM medico WHERE codigo_usuario=%d"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        print(result)


def recuperar_paciente(codigo):
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM paciente WHERE codigo_usuario=%d"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        print(result)
