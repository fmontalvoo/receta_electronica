from flask import Flask, render_template, request, redirect, url_for, session

from decouple import config

import controlador
from modelos.usuario import *

app = Flask(__name__)

app.secret_key = config('SECRET_KEY')


@app.before_request
def session_management():
    session.permanent = True


@app.route('/')
def index():
    usuario = recuperar_usuario()
    if usuario == None:
        return redirect(url_for('login'))
    return render_template('index.html', data=usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario = recuperar_usuario()
    if usuario != None:
        return redirect(url_for('index'))

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
            return redirect(url_for('index'))
    return render_template('usuario/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def recuperar_usuario():
    try:
        usuario = Usuario(
            session['codigo'], session['nombre_completo'], session['correo'], session['rol'])
    except:
        usuario = None
    return usuario

# C.R.U.D de Medicos


@app.route('/registrar_medico', methods=['GET', 'POST'])
def registrar_medico():
    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        especialidad = data['especialidad']
        clave = data['clave']
        controlador.registrar_medico(nombres, apellidos, correo, especialidad, clave)
    return render_template('usuario/medico/crear.html')

# C.R.U.D de Pacientes


@app.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        data = request.form
        nombres = data['nombres']
        apellidos = data['apellidos']
        correo = data['correo']
        especialidad = data['historia_clinica']
        clave = data['clave']
        controlador.registrar_paciente(nombres, apellidos, correo, especialidad, clave)
    return render_template('usuario/paciente/crear.html')

# C.R.U.D de Medicamentos


if __name__ == '__main__':
    app.run(debug=True, port=3000)
