from flask import Flask, render_template, request, redirect, url_for, session

import controlador
from usuario import *

app = Flask(__name__)

app.secret_key = 'Rec3T@'

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
        usuario = controlador.recuperar_usuario(correo.strip(), clave.strip())
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
        usuario = Usuario(session['codigo'], session['nombre_completo'], session['correo'], session['rol'])
    except:
        usuario = None
    return usuario

if __name__ == '__main__':
    app.run(debug=True, port=3000)