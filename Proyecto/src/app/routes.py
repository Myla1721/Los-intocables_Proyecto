from flask import Blueprint, redirect, url_for, session, render_template
from src.app.views.login_view import LoginView
from src.app.controllers.auth_controller import AuthController
from src.app.views.profesor_view import ProfesorView
from src.app.views.alumno_view import AlumnoView

main = Blueprint('main', __name__)


# ============ RUTAS GENERALES ============

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

@main.route('/profesor/crear-curso', methods=['POST'])
def profesor_crear_curso():
    return ProfesorView.crear_curso()

@main.route('/profesor/editar-curso/<int:curso_id>', methods=['POST'])
def profesor_editar_curso(curso_id):
    return ProfesorView.editar_curso(curso_id)

@main.route('/profesor/eliminar-curso/<int:curso_id>')
def profesor_eliminar_curso(curso_id):
    return ProfesorView.eliminar_curso(curso_id)

@main.route('/profesor/subir-material/<int:curso_id>', methods=['POST'])
def profesor_subir_material(curso_id):
    """Subir material a un curso específico"""
    return ProfesorView.subir_material(curso_id)

@main.route('/profesor/eliminar-material/<int:material_id>')
def profesor_eliminar_material(material_id):
    """Eliminar material de un curso"""
    return ProfesorView.eliminar_material(material_id)


# ============ RUTAS DEL ALUMNO ============

@main.route('/alumno/registro', methods=['GET'])
def alumno_registro_form():
    """Formulario de registro de alumno"""
    return AlumnoView.mostrar_registro()

@main.route('/alumno/registro', methods=['POST'])
def alumno_registro():
    """Procesa el registro de un nuevo alumno"""
    return AlumnoView.procesar_registro()

@main.route('/alumno/cursos')
def alumno_cursos():
    """Ver todos los cursos disponibles en la plataforma"""
    return AlumnoView.ver_cursos_disponibles()

@main.route('/alumno/inscribirse/<int:curso_id>', methods=['POST'])
def alumno_inscribirse(curso_id):
    """Inscribir al alumno en un curso"""
    return AlumnoView.inscribirse(curso_id)

@main.route('/alumno/mis-cursos')
def alumno_mis_cursos():
    """Ver los cursos en los que el alumno está inscrito"""
    return AlumnoView.ver_mis_cursos()

@main.route('/alumno/mis-cursos/<int:curso_id>/material')
def alumno_material_curso(curso_id):
    """Ver el material de un curso inscrito"""
    return AlumnoView.ver_material_curso(curso_id)
