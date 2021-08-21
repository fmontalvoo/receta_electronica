from .conexion_db import obtener_conexion

from modelos.receta_cabecera import *
from modelos.receta_detalle import *


def registrar_receta(cabecera, medicamentos):
    codigo_cabecera = registrar_cabecera(cabecera)

    for medicamento in medicamentos:
        detalle = RecetaDetalle(0, codigo_cabecera, medicamento)
        registrar_detalle(detalle)


def registrar_cabecera(cabecera):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO receta_cabecera (codigo_medico, codigo_paciente, fecha) values(%s, %s, %s)"
        cursor.execute(sql, (cabecera.codigo_medico,
                       cabecera.codigo_paciente, cabecera.fecha))
        codigo = cursor.lastrowid
        conexion.commit()
        return codigo


def registrar_detalle(detalle):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO receta_detalle (codigo_cabecera, codigo_medicamento) values(%s, %s)"
        cursor.execute(sql, (detalle.codigo_cabecera,
                       detalle.codigo_medicamento))
        conexion.commit()


def recuperar_recetas_paciente(codigo):
    recetas = recuperar_cabeceras(codigo)
    return recetas


def recuperar_recetas_medico(codigo):
    recetas = recuperar_cabeceras(codigo, True)
    return recetas


def recuperar_cabeceras(codigo, es_medico=False):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = ""
        if es_medico:
            sql = "SELECT * FROM receta_cabecera WHERE codigo_medico=%s"
        else:
            sql = "SELECT * FROM receta_cabecera WHERE codigo_paciente=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchall()
        cabeceras = []
        if result != None:
            for fila in result:
                cabecera = RecetaCabecera(
                    fila['codigo'], fila['codigo_medico'], fila['codigo_paciente'], fila['fecha'])
                cabeceras.append(cabecera)

            return cabeceras
    return None


def recuperar_detalles(codigo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "SELECT * FROM receta_detalle WHERE codigo_cabecera=%s"
        cursor.execute(sql, (codigo))
        result = cursor.fetchall()
        if result != None:
            detalles = []
            for fila in result:
                detalle = RecetaDetalle(
                    fila['codigo'], fila['codigo_cabecera'], fila['codigo_medicamento'])
                detalles.append(detalle)
            return detalles

    return None


def recuperar_receta(codigo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT c.codigo, c.codigo_medico, c.codigo_paciente, d.codigo as codigo_detalle, d.codigo_medicamento 
            FROM receta_cabecera c, receta_detalle d 
            WHERE c.codigo = d.codigo_cabecera AND c.codigo=%s
        '''
        cursor.execute(sql, (codigo))
        result = cursor.fetchall()
        if result != None:
            c = result[0]
            cabecera = RecetaCabecera(
                c['codigo'], c['codigo_medico'], c['codigo_paciente'])
            detalles = []
            for fila in result:
                detalle = RecetaDetalle(
                    fila['codigo_detalle'], fila['codigo'], fila['codigo_medicamento'])
                detalles.append(detalle)

            return cabecera, detalles
        return None
