from flask import Blueprint, redirect, url_for, session, render_template
from src.app.views.login_view import LoginView
from src.app.controllers.auth_controller import AuthController
from src.app.views.profesor_view import ProfesorView

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return LoginView.mostrarFormulario()


@main.route('/login', methods=['POST'])
def login():
    correo, password = LoginView.obtenerCredenciales()

    user = AuthController.login(correo, password)

    if user:
        session['user_id'] = user.id_usuario
        session['nombre'] = user.nombre
        session['rol'] = user.rol

        return redirect(url_for('main.home'))
    else:
        return LoginView.mostrarError()


@main.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))

    return render_template(
        'home.html',
        nombre=session['nombre'],
        rol=session['rol']
    )


@main.route('/logout')
def logout():
    if 'user_id' in session:
        AuthController.logout(session['user_id'])

    session.clear()
    return redirect(url_for('main.index'))

# ============ RUTAS DEL PROFESOR ============
@main.route('/profesor/cursos')
def profesor_cursos():
    """Página principal del profesor - Ver sus cursos"""
    return ProfesorView.ver_cursos()

@main.route('/profesor/subir-material/<int:curso_id>', methods=['POST'])
def profesor_subir_material(curso_id):
    """Subir material a un curso específico"""
    return ProfesorView.subir_material(curso_id)

@main.route('/profesor/eliminar-material/<int:material_id>')
def profesor_eliminar_material(material_id):
    """Eliminar material de un curso"""
    return ProfesorView.eliminar_material(material_id)
