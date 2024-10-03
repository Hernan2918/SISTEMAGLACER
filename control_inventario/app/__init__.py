from flask import Flask

# Crear la aplicación Flask
app = Flask(__name__)

from app import app as application