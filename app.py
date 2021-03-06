from datetime import date

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from decouple import config

import controlador
from modelos.usuario import *

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')


@app.before_request
def session_management():
    session.permanent = True


@app.route('/')
def inicio():
    usuario = recuperar_usuario()
    if usuario == None:
        return redirect(url_for('login'))
    return render_template('inicio.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario = recuperar_usuario()
    if usuario != None:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        data = request.form
        correo = data['correo']
        clave = data['clave']
        print(data)
        usuario = controlador.login(correo.strip(), clave.strip())
        if usuario != None:
            session.clear()
            session['codigo'] = usuario.codigo
            session['nombre_completo'] = usuario.nombre_completo
            session['correo'] = usuario.correo
            session['rol'] = usuario.rol
            return redirect(url_for('inicio'))
    return render_template('usuario/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

    """C.R.U.D de Medicos"""


@app.route('/registrar_medico', methods=['GET', 'POST'])
def registrar_medico():
    tiene_permiso, ruta = verificar_sesion(['Administrador'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        especialidad = data['especialidad']
        clave = data['clave']
        controlador.registrar_medico(
            nombres, apellidos, correo, especialidad, clave)
        return redirect(url_for('lista_medicos'))

    return render_template('usuario/medico/crear.html')


@app.route('/lista_medicos')
def lista_medicos():
    tiene_permiso, ruta = verificar_sesion(['Administrador'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    medicos = controlador.recuperar_medicos()
    return render_template('usuario/medico/lista.html', data={'medicos': medicos})


@app.route('/editar_medico/<int:codigo>', methods=['GET', 'POST'])
def editar_medico(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        especialidad = data['especialidad']
        clave = data['clave']
        controlador.editar_medico(codigo,
                                  nombres, apellidos, correo, especialidad, clave)
        return redirect(url_for('lista_medicos'))

    medico = controlador.recuperar_medico(codigo)

    return render_template('usuario/medico/editar.html', medico=medico)


@app.route('/eliminar_medico/<int:codigo>')
def eliminar_medico(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    controlador.eliminar_medico(codigo)

    return redirect(url_for('lista_medicos'))

    """C.R.U.D de Pacientes"""


@app.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        especialidad = data['historia_clinica']
        clave = data['clave']
        controlador.registrar_paciente(
            nombres, apellidos, correo, especialidad, clave)
        return redirect(url_for('lista_pacientes'))
    return render_template('usuario/paciente/crear.html')


@app.route('/lista_pacientes')
def lista_pacientes():
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    pacientes = controlador.recuperar_pacientes()
    return render_template('usuario/paciente/lista.html', data={'pacientes': pacientes})


@app.route('/editar_paciente/<int:codigo>', methods=['GET', 'POST'])
def editar_paciente(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        historia_clinica = data['historia_clinica']
        clave = data['clave']
        controlador.editar_paciente(
            codigo, nombres, apellidos, correo, historia_clinica, clave)
        return redirect(url_for('lista_pacientes'))

    paciente = controlador.recuperar_paciente(codigo)

    return render_template('usuario/paciente/editar.html', paciente=paciente)


@app.route('/eliminar_paciente/<int:codigo>')
def eliminar_paciente(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    controlador.eliminar_paciente(codigo)

    return redirect(url_for('lista_pacientes'))

    """C.R.U.D de Medicamentos"""


@app.route('/registrar_medicamento', methods=['GET', 'POST'])
def registrar_medicamento():
    usuario = recuperar_usuario()
    if usuario == None:
        return redirect(url_for('login'))
    if usuario.rol != 'Administrador' and usuario.rol != 'Medico':
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        data = request.form
        nombre = data['nombre']
        registro = data['registro']
        fecha_elaboracion = data['fecha_elaboracion']
        fecha_vencimiento = data['fecha_vencimiento']
        controlador.registrar_medicamento(
            nombre, registro, fecha_elaboracion, fecha_vencimiento
        )

        return redirect(url_for('lista_medicamentos'))

    return render_template('medicamentos/crear.html')


@app.route('/lista_medicamentos')
def lista_medicamentos():
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))
    medicamentos = controlador.recuperar_medicamentos()
    return render_template('medicamentos/lista.html', data={'medicamentos': medicamentos})


@app.route('/editar_medicamento/<int:codigo>', methods=['GET', 'POST'])
def editar_medicamento(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    if request.method == 'POST':
        data = request.form
        nombre = data['nombre']
        registro = data['registro']
        fecha_elaboracion = data['fecha_elaboracion']
        fecha_vencimiento = data['fecha_vencimiento']
        controlador.editar_medicamento(codigo,
                                       nombre, registro,
                                       fecha_elaboracion,
                                       fecha_vencimiento)
        return redirect(url_for('lista_medicamentos'))

    medicamento = controlador.recuperar_medicamento(codigo)

    return render_template('medicamentos/editar.html', medicamento=medicamento)


@app.route('/eliminar_medicamento/<int:codigo>')
def eliminar_medicamento(codigo):
    tiene_permiso, ruta = verificar_sesion(['Administrador', 'Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    controlador.eliminar_medicamento(codigo)

    return redirect(url_for('lista_medicamentos'))

    """C.R.U.D de Receta medica"""


@app.route('/crear_receta/<int:codigo>', methods=['GET', 'POST'])
def crear_receta(codigo):
    tiene_permiso, ruta = verificar_sesion(['Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    hoy = date.today()
    usuario = recuperar_usuario()
    fecha = hoy.strftime("%d/%m/%Y")
    paciente = controlador.recuperar_paciente(codigo)
    medicamentos = controlador.recuperar_medicamentos()

    if request.method == 'POST':
        medicinas = request.json['medicamentos']
        controlador.registrar_receta(
            usuario.codigo, paciente.codigo, medicinas, fecha)
        return jsonify({'status': 201})

    return render_template('receta/crear.html',
                           data={'fecha': fecha,
                                 'paciente': paciente,
                                 'medicamentos': medicamentos
                                 })


@app.route('/lista_recetas')
def lista_recetas():
    usuario = recuperar_usuario()
    if usuario == None:
        return redirect(url_for('login'))

    es_administrador, _ = verificar_sesion(['Administrador'])
    if es_administrador:
        return redirect(url_for('inicio'))

    tiene_permiso, _ = verificar_sesion(['Medico'])

    if tiene_permiso:
        recetas = controlador.recuperar_recetas_medico(
            usuario.codigo)
        return render_template('receta/lista.html', data={'recetas': recetas})

    recetas = controlador.recuperar_recetas_paciente(usuario.codigo)
    return render_template('receta/lista.html', data={'recetas': recetas})


@app.route('/consultar_receta/<int:codigo>')
def recuperar_receta(codigo):
    usuario = recuperar_usuario()
    if usuario == None:
        return redirect(url_for('login'))

    es_administrador, _ = verificar_sesion(['Administrador'])
    if es_administrador:
        return redirect(url_for('inicio'))

    cabecera, detalles = controlador.recuperar_receta(codigo)
    return render_template('receta/detalle.html', data={'cabecera': cabecera, 'detalles': detalles})

@app.route('/eliminar_receta/<int:codigo>')
def eliminar_receta(codigo):
    tiene_permiso, ruta = verificar_sesion(['Medico'])
    if not tiene_permiso:
        return redirect(url_for(ruta))

    controlador.eliminar_receta(codigo)

    return redirect(url_for('lista_recetas'))

def recuperar_usuario():
    try:
        usuario = Usuario(
            session['codigo'], session['nombre_completo'], session['correo'], session['rol'])
    except:
        usuario = None
    return usuario


def verificar_sesion(roles=[]):

    usuario = recuperar_usuario()

    if usuario == None:
        return (False, 'login')

    tiene_permiso = False
    for rol in roles:
        tiene_permiso += (rol == usuario.rol)

    if not tiene_permiso:
        return (False, 'inicio')

    return (True, '')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
