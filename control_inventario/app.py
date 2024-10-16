
from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL
from forms import ProductosForm 
from flask import flash
from functools import wraps
import os
from werkzeug.utils import secure_filename

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
            session['nombre'] = acceder['nombre']
            
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
    return render_template('login.html')


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
    
    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('productos.html', productos=productos, proveedores= proveedores, categorias=categorias)


@app.route('/registro_productos', methods=['POST'])
def registro_productos():
    if request.method == 'POST':
        medida = request.form['medida']
        proveedor_id = request.form['proveedores']
        producto = request.form['producto']
        calidad = request.form['calidad']
        existencia = request.form['existencia']
        rotas = request.form['rotas']
        precio = request.form['precio']
        embalaje = request.form['embalaje']
        ubicacion = request.form['ubicacion']
        categoria_id = request.form['categorias']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (medidas, proveedor, producto, calidad, existencias, rotas, precio, embalaje, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (medida, proveedor_id, producto, calidad, existencia, rotas, precio, embalaje, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()

        
        flash('Difusión registrada exitosamente!', 'success')
        return redirect(url_for('consulta_productos'))

@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        medida = request.form['medidaeditar']
        proveedor_id = request.form['proveedoreseditar']
        producto = request.form['productoeditar']
        calidad = request.form['calidadeditar']
        existencia = request.form['existenciaeditar']
        rotas = request.form['rotaseditar']
        precio = request.form['precioeditar']
        embalaje = request.form['embalajeeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaseditar']

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE productos
            SET medidas = %s, proveedor = %s, producto = %s, calidad = %s, existencias = %s, rotas = %s, precio = %s, embalaje =%s, ubicacion = %s, categoria = %s
            WHERE id_producto = %s
            """,
            (medida, proveedor_id, producto, calidad, existencia, rotas, precio, embalaje, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_productos'))


@app.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM productos WHERE id_producto = %s", (producto_id,))
        mysql.connection.commit()
        cur.close()
        flash('Producto eliminado correctamente!', 'error')
    return redirect(url_for('consulta_productos'))




@app.route('/consulta_proveedores')

def consulta_proveedores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedores')
    proveedores = cur.fetchall()
    cur.close()
    return render_template('proveedores.html', proveedores=proveedores)



UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/registro_proveedor', methods=['POST'])
def registro_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']
        
        # Manejo del archivo de imagen
        foto_db = None
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                # Asegúrate de usar un nombre de archivo seguro
                filename = secure_filename(foto.filename)
                # Guardar la imagen en la carpeta especificada
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(foto_path)

                # Almacena el nombre de la imagen en la base de datos
                foto_db = filename

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO proveedores (nombre, telefono, correo, direccion, foto) VALUES (%s, %s, %s, %s, %s)",
            (nombre, telefono, correo, direccion, foto_db)
        )
        mysql.connection.commit()
        cur.close()

        flash('Proveedor registrado exitosamente!', 'success')
        return redirect(url_for('consulta_proveedores'))

# Asegúrate de que tu carpeta 'uploads' existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.secret_key = "GLACER2024"
    app.run(debug=True)
