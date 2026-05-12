"""
Controlador del módulo Alumno.
Contiene toda la lógica de negocio para los casos de uso del alumno.
"""

from datetime import date
from src.app import db
from src.app.models.user import User
from src.app.models.alumno import Alumno
from src.app.models.curso import Curso
from src.app.models.inscripcion import Inscripcion
from src.app.models.material import Material


# ---------------------------------------------------------------------------
# Caso de uso 1: Crear cuenta de usuario
# ---------------------------------------------------------------------------

def registrar_alumno(nombre, apellido, correo, contrasena):
    """
    Registra un nuevo alumno en la plataforma.

    Crea un registro en la tabla Usuario (rol=ALUMNO) y otro en la tabla Alumno.
    Genera una matrícula automática basada en el año actual y el id del usuario.

    Args:
        nombre     (str): Nombre del alumno.
        apellido   (str): Apellido del alumno.
        correo     (str): Correo electrónico (debe ser único).
        contrasena (str): Contraseña en texto plano.

    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    # Validar campos obligatorios
    if not all([nombre, apellido, correo, contrasena]):
        return {'exito': False, 'mensaje': 'Todos los campos son obligatorios.'}

    # Flujo excepcional: correo ya registrado
    if User.query.filter_by(correo=correo).first():
        return {'exito': False, 'mensaje': 'El correo ya está registrado. Utiliza otro correo.'}

    try:
        # Crear usuario
        nuevo_usuario = User(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contrasena,
            rol='ALUMNO'
        )
        db.session.add(nuevo_usuario)
        db.session.flush()  # Obtener el id_usuario antes del commit

        # Generar matrícula: A<año><id_usuario con 4 dígitos>
        matricula = f"A{date.today().year}{str(nuevo_usuario.id_usuario).zfill(4)}"

        # Crear perfil de alumno
        nuevo_alumno = Alumno(
            id_usuario=nuevo_usuario.id_usuario,
            matricula=matricula,
            fecha_inscripcion_plataforma=date.today()
        )
        db.session.add(nuevo_alumno)
        db.session.commit()

        return {'exito': True, 'mensaje': 'Cuenta creada exitosamente. ¡Ya puedes iniciar sesión!'}

    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'mensaje': f'Error al crear la cuenta: {str(e)}'}


# ---------------------------------------------------------------------------
# Caso de uso 2: Ver cursos disponibles
# ---------------------------------------------------------------------------

def obtener_cursos_disponibles():
    """
    Obtiene todos los cursos registrados en la plataforma.

    Returns:
        list[Curso]: Lista de objetos Curso. Lista vacía si no hay cursos.
    """
    try:
        return Curso.query.order_by(Curso.fecha_creacion.desc()).all()
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Caso de uso 3: Inscribirse a un curso
# ---------------------------------------------------------------------------

def obtener_id_alumno_desde_usuario(user_id):
    """
    Obtiene el id_alumno a partir del id_usuario de sesión.

    Args:
        user_id (int): ID del usuario en sesión.

    Returns:
        int | None: ID del alumno o None si no existe.
    """
    alumno = Alumno.query.filter_by(id_usuario=user_id).first()
    return alumno.id_alumno if alumno else None


def inscribirse_curso(user_id, curso_id):
    """
    Inscribe a un alumno en un curso disponible.

    Flujo alternativo: si el alumno ya está inscrito, retorna mensaje informativo.
    Flujo excepcional: error de base de datos.

    Args:
        user_id  (int): ID del usuario (alumno) en sesión.
        curso_id (int): ID del curso al que desea inscribirse.

    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    id_alumno = obtener_id_alumno_desde_usuario(user_id)
    if not id_alumno:
        return {'exito': False, 'mensaje': 'No se encontró el perfil de alumno.'}

    # Verificar que el curso existe
    curso = Curso.query.get(curso_id)
    if not curso:
        return {'exito': False, 'mensaje': 'El curso no existe.'}

    # Flujo alternativo: alumno ya inscrito
    ya_inscrito = Inscripcion.query.filter_by(
        id_alumno=id_alumno, id_curso=curso_id
    ).first()
    if ya_inscrito:
        return {'exito': False, 'mensaje': f'Ya estás inscrito en el curso "{curso.nombre}".'}

    try:
        inscripcion = Inscripcion(id_alumno=id_alumno, id_curso=curso_id)
        db.session.add(inscripcion)
        db.session.commit()
        return {'exito': True, 'mensaje': f'¡Inscripción exitosa en "{curso.nombre}"!'}
    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'mensaje': 'Hubo un error al realizar la inscripción. Intente nuevamente.'}


# ---------------------------------------------------------------------------
# Caso de uso 4: Consultar material
# ---------------------------------------------------------------------------

def obtener_mis_cursos(user_id):
    """
    Obtiene los cursos en los que el alumno está inscrito.

    Args:
        user_id (int): ID del usuario en sesión.

    Returns:
        list[Curso]: Lista de cursos inscritos. Lista vacía si no hay ninguno.
    """
    id_alumno = obtener_id_alumno_desde_usuario(user_id)
    if not id_alumno:
        return []

    try:
        inscripciones = Inscripcion.query.filter_by(id_alumno=id_alumno).all()
        return [i.curso for i in inscripciones]
    except Exception:
        return []


def obtener_material_curso(curso_id, user_id):
    """
    Obtiene el material de un curso, verificando que el alumno esté inscrito.

    Args:
        curso_id (int): ID del curso.
        user_id  (int): ID del usuario en sesión.

    Returns:
        dict: {
            'exito'    : bool,
            'mensaje'  : str,
            'curso'    : Curso | None,
            'materiales': list[Material]
        }
    """
    id_alumno = obtener_id_alumno_desde_usuario(user_id)
    if not id_alumno:
        return {'exito': False, 'mensaje': 'No se encontró el perfil de alumno.', 'curso': None, 'materiales': []}

    # Verificar inscripción
    inscripcion = Inscripcion.query.filter_by(
        id_alumno=id_alumno, id_curso=curso_id
    ).first()
    if not inscripcion:
        return {
            'exito': False,
            'mensaje': 'No tienes acceso a este curso. Debes inscribirte primero.',
            'curso': None,
            'materiales': []
        }

    curso = Curso.query.get(curso_id)
    if not curso:
        return {'exito': False, 'mensaje': 'El curso no existe.', 'curso': None, 'materiales': []}

    try:
        materiales = Material.query.filter_by(id_curso=curso_id).order_by(Material.fecha_subida.desc()).all()
        return {'exito': True, 'mensaje': '', 'curso': curso, 'materiales': materiales}
    except Exception:
        return {
            'exito': False,
            'mensaje': 'No fue posible cargar el material. Intente nuevamente más tarde.',
            'curso': curso,
            'materiales': []
        }
