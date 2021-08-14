from flask import Flask, render_template, request, redirect, url_for, session

import controlador

app = Flask(__name__)

app.secret_key = 'Rec3T@'

@app.before_request
def session_management():
    session.permanent = True

@app.route('/')
def index():
    usuario , rol = recuperar_usuario()
    controlador.recuperar_sesion('admin@email.com', 'Admin.123')
    if usuario == 'desconocido':
        return redirect(url_for('login'))
    return render_template('index.html', data={'usuario':usuario, 'rol':rol})

@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario , rol = recuperar_usuario()
    if usuario != 'desconocido':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.form
        correo = data['correo']
        clave = data['clave']
        print(correo, clave)
        if correo == 'test@email.com' and clave == '123':
            session.clear()
            session['correo'] = correo
            session['usuario'] = 'Alan Brito'
            session['rol'] = 'admin'
            return redirect(url_for('index'))
    return render_template('usuario/login.html')

@app.route('/logout')
def logout():
    session.clear()
    usuario = 'desconocido'
    correo = 'ninguno'
    rol = 'ninguno'
    return redirect(url_for('login'))

def recuperar_usuario():
    try:
        usuario = session['usuario']
        correo = session['correo']
        rol = session['rol']
    except:
        usuario = 'desconocido'
        correo = 'ninguno'
        rol = 'ninguno'
    return (usuario, rol)

if __name__ == '__main__':
    app.run(debug=True, port=3000)