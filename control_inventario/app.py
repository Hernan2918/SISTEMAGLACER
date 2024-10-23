

from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL
from forms import ProductosForm 
from flask import flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'glacer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logeado' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache_view

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
        cur.execute('SELECT * FROM usuarios WHERE usuario=%s', (usuario,))
        acceder = cur.fetchone()

        print(f"Usuario encontrado: {acceder}")  # Para depuración
        

        if acceder:

            print(f"Contraseña ingresada: {contrasena}")  # Para depuración
            print(f"Hash de la contraseña: {acceder['contrasena']}")  
            # Verificar la contraseña usando check_password_hash
            if check_password_hash(acceder['contrasena'], contrasena):
                session['logeado'] = True
                session['id_usuario'] = acceder['id_usuario']
                session['usuario'] = acceder['usuario']
                session['nombre'] = acceder['nombre']

                return redirect(url_for('consulta_productos'))
            else:
                return render_template('login.html', mensaje='Usuario o contraseña incorrectos.')
        else:
            return render_template('login.html', mensaje='Usuario o contraseña incorrectos.')
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

        hashed_contrasena = generate_password_hash(contrasena)
        print(f"Hash almacenado: {hashed_contrasena}") 

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, apellidos, genero, usuario, contrasena) VALUES (%s, %s, %s, %s, %s)",
                         (nombre, apellidos, genero, usuario, hashed_contrasena))
            mysql.connection.commit()
            cur.close()

            flash('Usuario registrado exitosamente!', 'success')
            return redirect(url_for('acceso'))
    
        except Exception as e:
            flash(f"Error al registrar el usuario: {e}")
            return redirect('/registro')
    return render_template('login.html')


@app.route('/consulta_productos')
@login_required
@no_cache
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

        
        flash('Producto registrada exitosamente!', 'success')
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
@login_required
@no_cache
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
        
        foto_db = None
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                filename = secure_filename(foto.filename)
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(foto_path)
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


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/actualizar_proveedor', methods=['POST'])
def actualizar_proveedor():
    if request.method == 'POST':
        id_proveedor = request.form['id_proveedor']
        nombre = request.form['nombreeditar']
        telefono = request.form['telefonoeditar']
        correo = request.form['correoeditar']
        direccion = request.form['direccioneditar']

        cur = mysql.connection.cursor()

        try:
            cur.execute("SELECT foto FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
            resultado = cur.fetchone()

            if resultado is None:
                flash('Proveedor no encontrado', 'error')
                return redirect(url_for('consulta_proveedores'))

            current_foto = resultado['foto'] 

            if 'fotoeditar' in request.files and request.files['fotoeditar'].filename != '':
                foto = request.files['fotoeditar']
                print(f'Archivo subido: {foto.filename}')  
                filename = secure_filename(foto.filename)
                new_file_path = os.path.join('static/uploads/', filename)


                try:
                    foto.save(new_file_path)
                    print(f'Nueva foto guardada en: {new_file_path}')  
                    foto_actualizada = filename  
                except Exception as e:
                    print(f"Error al guardar la nueva foto: {e}")
                    flash('Error al guardar la nueva foto', 'error')
                    return redirect(url_for('consulta_proveedores'))
            else:
                print("No se subió una nueva foto. Manteniendo la foto actual.")
                foto_actualizada = current_foto  # Mantiene la foto actual si no se subió una nueva

            print(f'Actualizando proveedor con ID: {id_proveedor}, Nueva foto: {foto_actualizada}')  # Verificar los valores
            cur.execute("""
                UPDATE proveedores
                SET nombre = %s, telefono = %s, correo = %s, direccion = %s, foto = %s
                WHERE id_proveedor = %s
            """, (nombre, telefono, correo, direccion, foto_actualizada, id_proveedor))

            mysql.connection.commit()

            # Confirmar actualización
            cur.execute("SELECT foto FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
            nueva_foto = cur.fetchone()
            print(f'Foto actualizada en la base de datos: {nueva_foto["foto"]}')  # Verificar la nueva foto

            flash('Proveedor actualizado exitosamente!', 'info')

        except Exception as e:
            print(f"Error al actualizar el proveedor: {e}")
            flash('Error al actualizar el proveedor', 'error')
        finally:
            cur.close()

        return redirect(url_for('consulta_proveedores'))


@app.route('/eliminar_proveedor/<int:proveedor_id>', methods=['POST'])
def eliminar_proveedor(proveedor_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (proveedor_id,))
        mysql.connection.commit()
        cur.close()
        flash('Proveedor eliminado correctamente!', 'error')
    return redirect(url_for('consulta_proveedores'))


@app.route('/consulta_categorias')
@login_required
@no_cache
def consulta_categorias():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categorias')
    categorias = cur.fetchall()
    cur.close()
    return render_template('categorias.html', categorias=categorias)


@app.route('/registro_categorias', methods=['POST'])
def registro_categorias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        mysql.connection.commit()
        cur.close()

        flash('Categoría registrada exitosamente!', 'success')
        return redirect(url_for('consulta_categorias'))


@app.route('/actualizar_categoria', methods=['POST'])
def actualizar_categoria():
    if request.method == 'POST':
        id_categoria=request.form['id_categoria']
        nombre = request.form['nombreeditar']
        descripcion = request.form['descripcioneditar']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE categorias
            SET nombre = %s, descripcion = %s
            WHERE id_categoria = %s
        """, (nombre, descripcion, id_categoria))
        mysql.connection.commit()
        cur.close()

        flash('Categoría actualizada exitosamente!', 'info')
        return redirect(url_for('consulta_categorias'))



@app.route('/eliminar_categoria/<int:categoria_id>', methods=['POST'])
def eliminar_categoria(categoria_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM categorias WHERE id_categoria = %s", (categoria_id,))
        mysql.connection.commit()
        cur.close()
        flash('Categoría eliminada correctamente!', 'error')
    return redirect(url_for('consulta_categorias'))





@app.route('/consulta_muros')
@login_required
@no_cache
def consulta_muros():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_producto, d.medidas, doc.nombre as proveedor_nombre, producto, calidad, existencias, rotas, precio, embalaje, ubicacion,  esc.nombre as categoria_nombre
    FROM muros d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    """
    cur.execute(query)
    muros = cur.fetchall()

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

    return render_template('muros.html', muros=muros, proveedores= proveedores, categorias=categorias)






@app.route('/registro_muros', methods=['POST'])
def registro_muros():
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
        cur.execute("INSERT INTO muros (medidas, proveedor, producto, calidad, existencias, rotas, precio, embalaje, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (medida, proveedor_id, producto, calidad, existencia, rotas, precio, embalaje, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()

        
        flash('Producto registrada exitosamente!', 'success')
        return redirect(url_for('consulta_muros'))

@app.route('/actualizar_muros', methods=['POST'])
def actualizar_muros():
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
            UPDATE muros
            SET medidas = %s, proveedor = %s, producto = %s, calidad = %s, existencias = %s, rotas = %s, precio = %s, embalaje =%s, ubicacion = %s, categoria = %s
            WHERE id_producto = %s
            """,
            (medida, proveedor_id, producto, calidad, existencia, rotas, precio, embalaje, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_muros'))




@app.route('/eliminar_muros/<int:muro_id>', methods=['POST'])
def eliminar_muros(muro_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM muros WHERE id_producto = %s", (muro_id,))
        mysql.connection.commit()
        cur.close()
        flash('Producto eliminado correctamente!', 'error')
    return redirect(url_for('consulta_muros'))


@app.route('/consulta_adhesivos')
@login_required
@no_cache
def consulta_adhesivos():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_adhesivos, doc.nombre as proveedor_nombre, d.nombre, kilogramos, existencia, precio, ubicacion,  esc.nombre as categoria_nombre
    FROM adhesivos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    """
    cur.execute(query)
    adhesivos = cur.fetchall()

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

    return render_template('adhesivos.html', adhesivos=adhesivos, proveedores= proveedores, categorias=categorias)


@app.route('/registro_adhesivos', methods=['POST'])
def registro_adhesivos():
    if request.method == 'POST':
        proveedor = request.form['proveedores']
        nombre = request.form['producto']
        kilogramos = request.form['kilogramos']
        existencia = request.form['existencia']
        precio = request.form['precio']
        ubicacion = request.form['ubicacion']
        categoria_id = request.form['categorias']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO adhesivos (proveedor, nombre, kilogramos, existencia, precio, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (proveedor, nombre, kilogramos, existencia, precio, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()

        
        flash('Producto registrada exitosamente!', 'success')
        return redirect(url_for('consulta_adhesivos'))




@app.route('/actualizar_adhesivos', methods=['POST'])
def actualizar_adhesivos():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        proveedor_id = request.form['proveedoreseditar']
        producto = request.form['productoeditar']
        kilogramos = request.form['kilogramoseditar']
        existencia = request.form['existenciaeditar']
        precio = request.form['precioeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaseditar']

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE adhesivos
            SET  proveedor = %s, nombre = %s, kilogramos = %s, existencia = %s,  precio = %s,  ubicacion = %s, categoria = %s
            WHERE id_adhesivos = %s
            """,
            (proveedor_id, producto, kilogramos, existencia, precio, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_adhesivos'))




@app.route('/eliminar_adhesivos/<int:adhesivo_id>', methods=['POST'])
def eliminar_adhesivos(adhesivo_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM adhesivos WHERE id_adhesivos = %s", (adhesivo_id,))
        mysql.connection.commit()
        cur.close()
        flash('Producto eliminado correctamente!', 'error')
    return redirect(url_for('consulta_adhesivos'))



@app.route('/logout')
def logout():
    session.pop('logeado', None)  # Eliminar 'logeado' de la sesión
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = "GLACER2024"
    app.run(debug=True)
