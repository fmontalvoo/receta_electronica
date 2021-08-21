import acceso_datos.autenticacion as auth
import acceso_datos.medico_dao as mdao
import acceso_datos.paciente_dao as pdao
import acceso_datos.medicamento_dao as medao
import acceso_datos.receta_dao as rdao

from modelos.medico import *
from modelos.paciente import *
from modelos.medicamento import *
from modelos.receta_cabecera import *
from modelos.receta_detalle import *


def login(correo, clave):
    return auth.recuperar_usuario(correo, clave)


def registrar_medico(nombres, apellidos, correo, especialidad, clave):
    medico = Medico(0, nombres, apellidos, correo, especialidad, clave)
    mdao.registrar_medico(medico)


def recuperar_medico(codigo):
    return mdao.recuperar_medico(codigo)


def editar_medico(codigo, nombres, apellidos, correo, especialidad, clave):
    medico = Medico(codigo, nombres, apellidos, correo, especialidad, clave)
    mdao.editar_medico(medico)


def eliminar_medico(codigo):
    mdao.eliminar_medico(codigo)


def recuperar_medicos():
    return mdao.recuperar_medicos()


def registrar_paciente(nombres, apellidos, correo, historial_clinico, clave):
    paciente = Paciente(0, nombres, apellidos, correo,
                        historial_clinico, clave)
    pdao.registrar_paciente(paciente)


def recuperar_paciente(codigo):
    return pdao.recuperar_paciente(codigo)


def editar_paciente(codigo, nombres, apellidos, correo, historial_clinico, clave):
    paciente = Paciente(codigo, nombres, apellidos,
                        correo, historial_clinico, clave)
    pdao.editar_paciente(paciente)


def eliminar_paciente(codigo):
    pdao.eliminar_paciente(codigo)


def recuperar_pacientes():
    return pdao.recuperar_pacientes()


def registrar_medicamento(nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento):
    medicamento = Medicamento(0,
                              nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento)
    medao.registrar_medicamento(medicamento)


def editar_medicamento(codigo, nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento):
    medicamento = Medicamento(codigo,
                              nombre, registro_sanitario, fecha_elaboracion, fecha_vencimiento)
    medao.editar_medicamento(medicamento)


def recuperar_medicamento(codigo):
    return medao.recuperar_medicamento(codigo)


def eliminar_medicamento(codigo):
    medao.eliminar_medicamento(codigo)


def recuperar_medicamentos():
    return medao.recuperar_medicamentos()


def registrar_receta(codigo_medico, codigo_paciente, medicamentos, fecha):
    cabecera = RecetaCabecera(0, codigo_medico, codigo_paciente, fecha)
    rdao.registrar_receta(cabecera, medicamentos)


def recuperar_recetas_paciente(codigo):
    recetas = []
    for receta in rdao.recuperar_recetas_paciente(codigo):
        cabecera = RecetaCabecera(receta.codigo, recuperar_medico(
            receta.codigo_medico), recuperar_paciente(receta.codigo_paciente), receta.fecha)
        recetas.append(cabecera)
        # print(cab.codigo)
        # detalles = []
        # for d in det:
        #     print(f'\t{d.codigo}, {d.codigo_cabecera}')
        #     detalle = RecetaDetalle(
        #         d.codigo, cab.codigo, recuperar_medicamento(d.codigo_medicamento))
        #     detalles.append(detalle)
        # recetas.append((cabecera, detalles))
    return recetas


def recuperar_recetas_medico(codigo):
    recetas = []
    for receta in rdao.recuperar_recetas_medico(codigo):
        cabecera = RecetaCabecera(receta.codigo, recuperar_medico(
            receta.codigo_medico), recuperar_paciente(receta.codigo_paciente), receta.fecha)
        recetas.append(cabecera)
        # print(cab.codigo)
        # detalles = []
        # for d in det:
        #     print(f'\t{d.codigo}, {d.codigo_cabecera}')
        #     detalle = RecetaDetalle(
        #         d.codigo, cab.codigo, recuperar_medicamento(d.codigo_medicamento))
        #     detalles.append(detalle)
        # recetas.append((cabecera, detalles))
    return recetas
