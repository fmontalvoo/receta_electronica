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
            if rol == 'Medico':
                return recuperar_medico(codigo, correo, rol)
            if rol == 'Paciente':
                return recuperar_paciente(codigo, correo, rol)


def recuperar_medico(codigo, correo, rol):
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM medico WHERE codigo_usuario=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        print(result)
        nombre_completo = f"{result['nombres']} {result['apellidos']}"
        return Usuario(codigo, nombre_completo, correo, rol)


def recuperar_paciente(codigo, correo, rol):
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM paciente WHERE codigo_usuario=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchone()
        nombre_completo = f"{result['nombres']} {result['apellidos']}"
        return Usuario(codigo, nombre_completo, correo, rol)
