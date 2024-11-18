from flask import Flask, render_template, redirect, request, session, url_for, flash, make_response
from flask_mysqldb import MySQL
from forms import ProductosForm
from flask import flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import send_file
from fpdf import FPDF

from io import BytesIO
from flask import jsonify


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
    SELECT d.id_producto, d.medidas, d.producto, d.calidad, d.existencias, d.rotas, d.precio, d.embalaje, d.ubicacion,
           doc.nombre AS proveedor_nombre, doc.id_proveedor, 
           esc.nombre AS categoria_nombre, esc.id_categoria
    FROM productos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;
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

    return render_template('/productos/productos.html', productos=productos, form=form, proveedores=proveedores, categorias=categorias)



@app.route('/obtener_todos_productos')
@login_required
def obtener_todos_productos():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.medidas, doc.nombre AS proveedor_nombre, d.producto, d.calidad, d.existencias,
           d.rotas, d.precio, d.embalaje, d.ubicacion, esc.nombre AS categoria_nombre
    FROM productos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)





@app.route('/paginacion_productos')
@login_required
@no_cache
def paginacion_productos():
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_producto, d.medidas, d.producto, d.calidad, d.existencias, d.rotas, d.precio, d.embalaje, d.ubicacion,
           doc.nombre AS proveedor_nombre, doc.id_proveedor, 
           esc.nombre AS categoria_nombre, esc.id_categoria
    FROM productos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s
    """
    cur.execute(query, (products_per_page, offset))
    productos = cur.fetchall()

    query_count = "SELECT COUNT(*) FROM productos"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    cur.close()

    return jsonify({
        'productos': productos,
        'total_pages': total_pages,
        'current_page': page
    })


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
        proveedor_id = request.form['proveedoreditar']
        producto = request.form['productoeditar']
        calidad = request.form['calidadeditar']
        existencia = request.form['existenciaeditar']
        rotas = request.form['rotaseditar']
        precio = request.form['precioeditar']
        embalaje = request.form['embalajeeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaeditar']

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
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM proveedores LIMIT %s OFFSET %s', (products_per_page, offset))
    proveedores = cur.fetchall()
    
    query_count = "SELECT COUNT(*) FROM proveedores"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    cur.close()
    
    return render_template('/proveedores/proveedores.html', proveedores=proveedores, page=page,total_pages=total_pages, page_range=page_range)

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
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT * FROM categorias LIMIT %s OFFSET %s', (products_per_page, offset))
    categorias = cur.fetchall()

    query_count = "SELECT COUNT(*) FROM categorias"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    
    cur.close()
    return render_template('/categorias/categorias.html', categorias=categorias, page=page,total_pages=total_pages, page_range=page_range)


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
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    
    cur = mysql.connection.cursor()
    
    query = """
    SELECT d.id_producto, d.medidas, d.producto, d.calidad, d.existencias, d.rotas, d.precio, d.embalaje, d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM muros d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s
    """
    cur.execute(query, (products_per_page, offset))
    muros = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()

    query_count = "SELECT COUNT(*) FROM muros"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    cur.close()

    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('/muros/muros.html', muros=muros, proveedores= proveedores, categorias=categorias, page=page, total_pages=total_pages, page_range=page_range)


@app.route('/obtener_todos_muros')
@login_required
def obtener_todos_muros():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_producto, d.medidas, d.producto, d.calidad, d.existencias, d.rotas, d.precio, d.embalaje, d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM muros d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;
    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)


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
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_adhesivos, d.nombre, d.kilogramos, d.existencia,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM adhesivos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s

    """
    cur.execute(query, (products_per_page, offset))
    adhesivos = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()
    query_count = "SELECT COUNT(*) FROM adhesivos"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    cur.close()
    
    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('/adhesivos/adhesivos.html', adhesivos=adhesivos, proveedores= proveedores, categorias=categorias, page=page, total_pages=total_pages, page_range=page_range)


@app.route('/obtener_todos_adhesivos')
@login_required
def obtener_todos_adhesivos():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_adhesivos, d.nombre, d.kilogramos, d.existencia,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM adhesivos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;

    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)

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

        
        flash('Producto registrado exitosamente!', 'success')
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


@app.route('/consulta_sanitarios')
@login_required
@no_cache
def consulta_sanitarios():
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_sanitario, d.nombre, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM sanitarios d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s
    """
    cur.execute(query, (products_per_page, offset))
    sanitarios = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()
    
    query_count = "SELECT COUNT(*) FROM sanitarios"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    cur.close()

    
    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('/sanitarios/sanitarios.html', sanitarios=sanitarios, proveedores= proveedores, categorias=categorias, page=page, 
                           total_pages=total_pages,
                           page_range=page_range)



@app.route('/obtener_todos_sanitarios')
@login_required
def obtener_todos_sanitarios():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_sanitario, d.nombre, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM sanitarios d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;
    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)


@app.route('/registro_sanitarios', methods=['POST'])
def registro_saniatarios():
    if request.method == 'POST':
        proveedor = request.form['proveedores']
        nombre = request.form['producto']
        existencias = request.form['existencia']
        rotas = request.form['rotas']
        precio = request.form['precio']
        ubicacion = request.form['ubicacion']
        categoria_id = request.form['categorias']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sanitarios (proveedor, nombre, existencias, rotas, precio, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (proveedor, nombre, existencias, rotas, precio, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()
        
        flash('Producto registrada exitosamente!', 'success')
        return redirect(url_for('consulta_sanitarios'))



@app.route('/actualizar_sanitarios', methods=['POST'])
def actualizar_sanitarios():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        proveedor_id = request.form['proveedoreseditar']
        producto = request.form['productoeditar']
        existencia = request.form['existenciaeditar']
        rotas = request.form['rotaseditar']
        precio = request.form['precioeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaseditar']

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE sanitarios
            SET  proveedor = %s, nombre = %s, existencias = %s, rotas = %s,  precio = %s,  ubicacion = %s, categoria = %s
            WHERE id_sanitario = %s
            """,
            (proveedor_id, producto, existencia, rotas, precio, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_sanitarios'))




@app.route('/eliminar_sanitarios/<int:sanitario_id>', methods=['POST'])
def eliminar_sanitarios(sanitario_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM sanitarios WHERE id_sanitario = %s", (sanitario_id,))
        mysql.connection.commit()
        cur.close()
        flash('Producto eliminado correctamente!', 'error')
    return redirect(url_for('consulta_sanitarios'))



@app.route('/consulta_tinacos')
@login_required
@no_cache
def consulta_tinacos():
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_tinaco, d.nombre, d.litros, d.color, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM tinacos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s
   
    """
    cur.execute(query, (products_per_page, offset))
    tinacos = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()

    query_count = "SELECT COUNT(*) FROM tinacos"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    
    cur.close()
    
    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('/tinacos/tinacos.html', tinacos=tinacos, proveedores= proveedores, categorias=categorias, page=page, total_pages=total_pages, page_range=page_range)


@app.route('/obtener_todos_tinacos')
@login_required
def obtener_todos_tinacos():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_tinaco, d.nombre, d.litros, d.color, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM tinacos d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;
   
    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)


@app.route('/registro_tinacos', methods=['POST'])
def registro_tinacos():
    if request.method == 'POST':
        proveedor = request.form['proveedores']
        nombre = request.form['producto']
        litros = request.form['litros']
        color = request.form['color']
        existencias = request.form['existencia']
        rotas = request.form['rotas']
        precio = request.form['precio']
        ubicacion = request.form['ubicacion']
        categoria_id = request.form['categorias']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tinacos (proveedor, nombre, litros, color, existencias, rotas, precio, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (proveedor, nombre, litros, color, existencias, rotas, precio, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()
        
        flash('Producto registrada exitosamente!', 'success')
        return redirect(url_for('consulta_tinacos'))


@app.route('/actualizar_tinacos', methods=['POST'])
def actualizar_tinacos():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        proveedor_id = request.form['proveedoreseditar']
        producto = request.form['productoeditar']
        litros = request.form['litroseditar']
        color = request.form['coloreditar']
        existencia = request.form['existenciaeditar']
        rotas = request.form['rotaseditar']
        precio = request.form['precioeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaseditar']

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE tinacos
            SET  proveedor = %s, nombre = %s, litros = %s, color= %s, existencias = %s, rotas = %s,  precio = %s,  ubicacion = %s, categoria = %s
            WHERE id_tinaco = %s
            """,
            (proveedor_id, producto, litros, color, existencia, rotas, precio, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_tinacos'))


@app.route('/eliminar_tinacos/<int:tinaco_id>', methods=['POST'])
def eliminar_tinacos(tinaco_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tinacos WHERE id_tinaco = %s", (tinaco_id,))
        mysql.connection.commit()
        cur.close()
        flash('Producto eliminado correctamente!', 'error')
    return redirect(url_for('consulta_tinacos'))



@app.route('/consulta_vitroblocks')
@login_required
@no_cache
def consulta_vitroblocks():
    page = request.args.get('page', 1, type=int)
    products_per_page = 5
    offset = (page - 1) * products_per_page
    
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_vitroblock, d.tipo, d.medidas, d.nombre, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM vitroblocks d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria
    LIMIT %s OFFSET %s
  
    """
    cur.execute(query, (products_per_page, offset))
    vitroblocks = cur.fetchall()

    query_proveedores = "SELECT id_proveedor, nombre FROM proveedores"
    cur.execute(query_proveedores)
    proveedores = cur.fetchall()

    query_categorias = "SELECT id_categoria, nombre FROM categorias"
    cur.execute(query_categorias)
    categorias = cur.fetchall()
    
    query_count = "SELECT COUNT(*) FROM vitroblocks"
    cur.execute(query_count)
    total_products = cur.fetchone()['COUNT(*)']

    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)

    page_range = list(range(1, total_pages + 1))
    
    start_index = max(1, page - 1)
    end_index = min(total_pages, page + 1)
    
    if page - 1 > 1:
        page_range = [1, '...'] + page_range[start_index-1:end_index]
    elif page + 1 < total_pages:
        page_range = page_range[start_index-1:end_index] + ['...'] + [total_pages]

    
    cur.close()
    
    form = ProductosForm()
    form.proveedores.choices = [(proveedor['id_proveedor'], proveedor['nombre']) for proveedor in proveedores]
    form.categorias.choices = [(categoria['id_categoria'], categoria['nombre']) for categoria in categorias]

    return render_template('/vitroblocks/vitroblock.html', vitroblocks=vitroblocks, proveedores= proveedores, categorias=categorias, page=page, total_pages=total_pages, page_range=page_range)



@app.route('/obtener_todos_vitroblocks')
@login_required
def obtener_todos_vitroblocks():
    cur = mysql.connection.cursor()
    query = """
    SELECT d.id_vitroblock, d.tipo, d.medidas, d.nombre, d.existencias, d.rotas,  d.precio,  d.ubicacion,
            doc.nombre AS proveedor_nombre, doc.id_proveedor, 
            esc.nombre AS categoria_nombre, esc.id_categoria
    FROM vitroblocks d
    JOIN proveedores doc ON d.proveedor = doc.id_proveedor
    JOIN categorias esc ON d.categoria = esc.id_categoria;
  
    """
    cur.execute(query)
    productos = cur.fetchall()
    cur.close()
    return jsonify(productos)




@app.route('/registro_vitroblocks', methods=['POST'])
def registro_vitroblocks():
    if request.method == 'POST':
        proveedor = request.form['proveedores']
        tipo = request.form['tipo']
        medidas = request.form['medidas']
        nombre = request.form['nombre']
        existencias = request.form['existencia']
        rotas = request.form['rotas']
        precio = request.form['precio']
        ubicacion = request.form['ubicacion']
        categoria_id = request.form['categorias']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vitroblocks (proveedor, tipo, medidas, nombre, existencias, rotas, precio, ubicacion, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (proveedor, tipo, medidas, nombre, existencias, rotas, precio, ubicacion, categoria_id  ))
        mysql.connection.commit()
        cur.close()
        
        flash('Producto registrada exitosamente!', 'success')
        return redirect(url_for('consulta_vitroblocks'))


@app.route('/actualizar_vitroblocks', methods=['POST'])
def actualizar_vitroblocks():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        proveedor_id = request.form['proveedoreseditar']
        tipo = request.form['tipoeditar']
        medidas = request.form['medidaseditar']
        nombre = request.form['nombreeditar']
        existencia = request.form['existenciaeditar']
        rotas = request.form['rotaseditar']
        precio = request.form['precioeditar']
        ubicacion = request.form['ubicacioneditar']
        categoria_id = request.form['categoriaseditar']

        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE vitroblocks
            SET  proveedor = %s, tipo = %s, medidas = %s, nombre= %s, existencias = %s, rotas = %s,  precio = %s,  ubicacion = %s, categoria = %s
            WHERE id_vitroblock = %s
            """,
            (proveedor_id, tipo, medidas, nombre, existencia, rotas, precio, ubicacion, categoria_id, id_producto)
        )
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('consulta_vitroblocks'))





@app.route('/descargar_etiqueta_producto/<int:producto_id>')
def descargar_etiqueta_producto(producto_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.medidas, p.producto, p.calidad, p.existencias, p.rotas, p.precio, 
               p.embalaje, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM productos p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_producto = %s
    """, (producto_id,))
    producto = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)
    pdf.rect(10, 10, 90, 50)

    nombre_imagen = producto['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=11, y=11, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(75, 15) 
    pdf.cell(0, 10, txt=f"{producto['medidas']}")
    
    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 30)
    pdf.cell(90, 10, txt=producto['producto'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(78, 48)  
    pdf.cell(0, 10, txt=f"{producto['precio']}")

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(15, 48)  
    pdf.cell(0, 10, txt=f"{producto['embalaje']}")



    # Generar el archivo PDF
    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={producto['producto']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response


@app.route('/descargar_etiqueta_muro/<int:muro_id>')
def descargar_etiqueta_muro(muro_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.medidas, p.producto, p.calidad, p.existencias, p.rotas, p.precio, 
               p.embalaje, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM muros p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_producto = %s
    """, (muro_id,))
    muro = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)  
    pdf.rect(10, 10, 90, 50)  

    nombre_imagen = muro['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=11, y=11, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(75, 15)  
    pdf.cell(0, 10, txt=f"{muro['medidas']}")
    

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 30)  
    pdf.cell(90, 10, txt=muro['producto'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(78, 48)  
    pdf.cell(0, 10, txt=f"{muro['precio']}")

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(15, 48)  
    pdf.cell(0, 10, txt=f"{muro['embalaje']}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={muro['producto']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/descargar_etiqueta_adhesivo/<int:adhesivo_id>')
def descargar_etiqueta_adhesivo(adhesivo_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.nombre, p.kilogramos, p.existencia, p.precio, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM adhesivos p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_adhesivos = %s
    """, (adhesivo_id,))
    adhesivo = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)  
    pdf.rect(10, 10, 90, 50)  

    nombre_imagen = adhesivo['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=11, y=11, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(78, 15)  
    pdf.cell(0, 10, txt=f"{adhesivo['kilogramos']}")
    

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 25)  
    pdf.cell(90, 10, txt=adhesivo['proveedor_nombre'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 35)  
    pdf.cell(90, 10, txt=adhesivo['nombre'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(78, 48)  
    pdf.cell(0, 10, txt=f"{adhesivo['precio']}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={adhesivo['nombre']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/descargar_etiqueta_sanitario/<int:sanitario_id>')
def descargar_etiqueta_sanitario(sanitario_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.nombre, p.existencias, p.rotas, p.precio, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM sanitarios p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_sanitario = %s
    """, (sanitario_id,))
    sanitario = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)  
    pdf.rect(10, 10, 90, 50)  

    nombre_imagen = sanitario['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=40, y=13, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 30)  
    pdf.cell(90, 10, txt=sanitario['nombre'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(50, 48)  
    pdf.cell(90, 10, txt=f"{sanitario['precio']}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={sanitario['nombre']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/descargar_etiqueta_tinaco/<int:tinaco_id>')
def descargar_etiqueta_tinaco(tinaco_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.nombre, p.litros, p.color, p.existencias, p.precio, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM tinacos p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_tinaco = %s
    """, (tinaco_id,))
    tinaco = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)  
    pdf.rect(10, 10, 90, 50)  

    nombre_imagen = tinaco['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=40, y=13, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(0, 30)  
    pdf.cell(78, 10, txt=tinaco['nombre'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(15, 45)  
    pdf.cell(90, 10, txt=f"{tinaco['litros']}")

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(20, 30)  
    pdf.cell(98, 10, txt=tinaco['color'].upper(), align="C")

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(73, 45)  
    pdf.cell(90, 10, txt=f"{tinaco['precio']}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={tinaco['nombre']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response

@app.route('/descargar_etiqueta_vitroblock/<int:vitroblock_id>')
def descargar_etiqueta_vitroblock(vitroblock_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.nombre, p.tipo, p.medidas, p.existencias, p.precio, p.ubicacion, p.categoria,
               prov.nombre AS proveedor_nombre, prov.foto AS proveedor_imagen
        FROM vitroblocks p
        JOIN proveedores prov ON p.proveedor = prov.id_proveedor
        WHERE p.id_vitroblock = %s
    """, (vitroblock_id,))
    vitroblock = cur.fetchone()
    cur.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_line_width(1)  
    pdf.rect(10, 10, 90, 50)  

    nombre_imagen = vitroblock['proveedor_imagen'] 

    ruta_imagen = os.path.join(os.getcwd(), 'static', 'uploads', nombre_imagen)

    if os.path.exists(ruta_imagen):
        pdf.image(ruta_imagen, x=10, y=13, w=30)
    else:
        print("La imagen no se encuentra en la ruta especificada:", ruta_imagen)

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 25)  
    pdf.cell(90, 10, txt=vitroblock['nombre'].upper(), align="C")  

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(15, 45)  
    pdf.cell(90, 10, txt=f"{vitroblock['medidas']}")

    pdf.set_font("Arial", "B", size=18)
    pdf.set_xy(10, 35)  
    pdf.cell(90, 10, txt=vitroblock['tipo'].upper(), align="C")

    pdf.set_font("Arial", "B", size=15)
    pdf.set_xy(73, 45)  
    pdf.cell(90, 10, txt=f"{vitroblock['precio']}")

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Disposition"] = f"attachment; filename={vitroblock['nombre']}_etiqueta.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response


@app.route('/logout')
def logout():

    session.pop('logeado', None)  # Eliminar 'logeado' de la sesión
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = "GLACER2024"
    app.run( host='0.0.0.0', port=5000, debug=True)
