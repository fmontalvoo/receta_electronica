import acceso_datos.autenticacion as auth
import acceso_datos.medico_dao as mdao
import acceso_datos.paciente_dao as pdao

from modelos.medico import *
from modelos.paciente import *

def login(correo, clave):
    return auth.recuperar_usuario(correo, clave)

def registrar_medico(nombres, apellidos, correo, especialidad, clave):
    medico = Medico(nombres, apellidos, correo, especialidad, clave)
    mdao.registrar_medico(medico)

def registrar_paciente(nombres, apellidos, correo, historial_clinico, clave):
    paciente = Paciente(nombres, apellidos, correo, historial_clinico, clave)
    pdao.registrar_paciente(paciente)
