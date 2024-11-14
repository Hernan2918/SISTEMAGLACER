from app.db import db
from sqlalchemy import ForeignKey


class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    medidas = db.Column(db.String(100))
    proveedor = db.Column(db.Integer, ForeignKey('proveedores.id_proveedor'))
    producto = db.Column(db.String(250))
    calidad = db.Column(db.String(250))
    existencia = db.Column(db.Integer, nullable=False)
    rotas = db.Column(db.String(250))
    precio = db.Column(db.String(250))
    embalaje = db.Column(db.String(250))
    ubicacion = db.Column(db.String(250))
    categoria = db.Column(db.Integer, ForeignKey('categorias.id_categoria'))
    

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    direccion = db.Column(db.String(250))
    foto = db.Column(db.String(250))

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_escuela = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    
