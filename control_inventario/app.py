
from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL

from flask import flash
from functools import wraps


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'glacer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro_usuario.html')

@app.route('/acceso', methods=["GET", "POST"])
def acceso():
    if request.method == 'POST' and 'txtusuario' in request.form and 'txtcontrasena' in request.form:
        usuario = request.form['txtusuario']
        contrasena = request.form['txtcontrasena']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE usuario=%s and contrasena=%s', (usuario, contrasena))
        acceder = cur.fetchone()

        if acceder:
            session['logeado'] = True
            session['id_usuario'] = acceder['id_usuario']
            session['usuario'] = acceder['usuario']
            
            return redirect(url_for('consulta_productos'))
        else:
            return render_template('login.html', mensaje='Usuario o contraseña incorrectos..')
    return redirect('/')


@app.route('/consulta_productos')

def consulta_productos():

    return render_template('productos.html')



if __name__ == '__main__':
    app.secret_key = "GLACER2024"
    app.run(debug=True)
