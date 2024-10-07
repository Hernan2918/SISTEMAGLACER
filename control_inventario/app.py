
from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL
from forms import DifusionForm 
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


@app.route('/registro_usuarios', methods=['POST'])
def registro_usuarios():
    if request.method == 'POST':
        nombre = request.form['registarnombre']
        apellidos = request.form['registrarapellido']  # Capturar todos los IDs seleccionados
        genero = request.form['registrargenero']
        usuario = request.form['registrarusuario']
        contrasena= request.form['registrarcontraseña']
        confirmar_c = request.form['registrarcontraseñaC']

        if contrasena != confirmar_c:
            flash("Las contraseñas no coinciden. Inténtalo de nuevo.")
            return redirect('/registro')  # Redirigir de nuevo al formulario de registro


        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, apellidos, genero, usuario, contrasena, c_contraseña) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, apellidos, genero, usuario, contrasena, confirmar_c ))
            mysql.connection.commit()
            cur.close()

            flash('Usuario registrado exitosamente!', 'success')
            return redirect(url_for('acceso'))
    
        except Exception as e:
            flash(f"Error al registrar el usuario: {e}")
            return redirect('/registro')
    return render_template('registro.html')


@app.route('/consulta_productos')
def consulta_productos():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_producto, d.medidas, doc.nombre as proveedor_nombre, producto, calidad, existencias, rotas, precio, embalaje, ubicacion,  esc.nombre as categoria_nombre
    FROM productos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    """
    cur.execute(query)
    productos = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()
    cur.close()
    
    form = DifusionForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('productos.html', productos=productos, proveedores= proveedores, categorias=categorias)

if __name__ == '__main__':
    app.secret_key = "GLACER2024"
    app.run(debug=True)
