from flask import Blueprint, render_template, request
from src.app.models import User


main = Blueprint('main', __name__) #Blueprint para manejar las rutas

@main.route('/')
def index():
    """
    Muestra la página de login.
    """
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login():
    """
    Procesa el formulario de inicio de sesión.

    Obtiene los datos del formulario (usuario y contraseña) y verifica si existen en la base de datos y redirige:

    - Si el usuario existe: muestra la página principal (home)
    - Si no existe: regresa al login con mensaje de error
    """
    #Obtenemos los datos del formulario
    username = request.form['username']
    password = request.form['password']

    #Buscamos al usuario en la base de datos
    user = User.query.filter_by(
        nombre_usuario=username,
        contrasena=password
    ).first()

    #Verificamos si el usuario existe
    if user:
        return render_template('home.html', user=user)
    else:
        return render_template('login.html', error="Usuario o contraseña incorrectos")