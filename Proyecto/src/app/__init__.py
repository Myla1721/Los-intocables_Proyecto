import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import Config

db = SQLAlchemy() #Instancia global de SQLAlchemy

def create_app():
    """
    Función fábrica de la aplicación Flask.

    Configura rutas, la base de datos y templates

    Devuelve:
         app (Flask): instancia configurada de la aplicación
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')  #Ruta a la carpeta de templates

    app = Flask(__name__, template_folder=template_dir)  #Se crea aplicación Flask
    app.config.from_object(Config) #Cargamos configuración

    db.init_app(app) #Inicializamos la base de datos con la app

    #Registramos rutas
    from src.app.routes import main
    app.register_blueprint(main)

    return app