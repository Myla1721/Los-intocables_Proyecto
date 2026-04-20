import os
from werkzeug.utils import secure_filename
from flask import current_app
from src.app import db
from src.app.models.curso import Curso
from src.app.models.material import Material
from src.app.models.profesor import Profesor

# Configuración para subida de archivos
UPLOAD_FOLDER = 'src/app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'jpg', 'jpeg', 'png', 'mp4'}

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def obtener_id_profesor_desde_usuario(user_id):
    """
    Obtiene el id_profesor a partir del id_usuario
    
    Args:
        user_id (int): ID del usuario en sesión
    
    Returns:
        int: ID del profesor o None si no existe
    """
    profesor = Profesor.query.filter_by(id_usuario=user_id).first()
    if profesor:
        return profesor.id_profesor
    return None

def obtener_cursos_disponibles(user_id=None):
    """
    Obtiene los cursos del profesor.
    Si no tiene cursos, crea uno de demostración automáticamente.
    
    Args:
        user_id (int): ID del usuario (profesor)
    
    Returns:
        list: Lista de cursos con sus materiales
    """
    if user_id:
        # Obtener el id_profesor correspondiente al usuario
        id_profesor = obtener_id_profesor_desde_usuario(user_id)
        
        if id_profesor:
            cursos = Curso.query.filter_by(id_profesor=id_profesor).all()
            
            # Si no tiene cursos, crear uno de demostración
            if not cursos:
                curso_demo = Curso(
                    nombre="Inglés Básico A1 (Demo)",
                    descripcion="Curso de demostración para probar funcionalidades",
                    categoria="Idiomas",
                    id_profesor=id_profesor
                )
                try:
                    db.session.add(curso_demo)
                    db.session.commit()
                    cursos = [curso_demo]
                    print("✅ Curso de demostración creado automáticamente")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error al crear curso demo: {e}")
                    cursos = []
        else:
            cursos = []
    else:
        cursos = Curso.query.all()
    
    return cursos

def subir_material_curso(curso_id, user_id, archivo):
    """
    Sube un archivo de material a un curso específico
    
    Args:
        curso_id (int): ID del curso
        user_id (int): ID del usuario (profesor)
        archivo (FileStorage): Archivo subido desde el formulario
    
    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    # 1. Obtener id_profesor del usuario
    id_profesor = obtener_id_profesor_desde_usuario(user_id)
    
    if not id_profesor:
        return {'exito': False, 'mensaje': 'No se encontró el perfil de profesor'}
    
    # 2. Verificar que el curso existe y pertenece al profesor
    curso = Curso.query.filter_by(id_curso=curso_id, id_profesor=id_profesor).first()
    
    if not curso:
        return {'exito': False, 'mensaje': 'Curso no encontrado o no tienes permisos para modificarlo'}
    
    # 3. Verificar que se subió un archivo
    if not archivo or archivo.filename == '':
        return {'exito': False, 'mensaje': 'No se seleccionó ningún archivo'}
    
    # 4. Validar extensión del archivo
    if not allowed_file(archivo.filename):
        return {'exito': False, 'mensaje': f'Tipo de archivo no permitido. Usar: {", ".join(ALLOWED_EXTENSIONS)}'}
    
    # 5. Guardar archivo
    filename = secure_filename(archivo.filename)
    
    # Crear nombre único para evitar sobrescrituras
    import time
    unique_filename = f"{int(time.time())}_{filename}"
    
    # Ruta completa
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    
    filepath = os.path.join(upload_path, unique_filename)
    archivo.save(filepath)
    
    # 6. Guardar registro en BD
    nuevo_material = Material(
        nombre=filename,
        archivo_url=f'/static/uploads/{unique_filename}',
        id_curso=curso_id
    )
    
    try:
        db.session.add(nuevo_material)
        db.session.commit()
        return {'exito': True, 'mensaje': f'Material "{filename}" subido correctamente'}
    except Exception as e:
        db.session.rollback()
        # Si hay error en BD, eliminar el archivo físico
        if os.path.exists(filepath):
            os.remove(filepath)
        return {'exito': False, 'mensaje': f'Error al guardar en la base de datos: {str(e)}'}

def eliminar_material_curso(material_id, user_id):
    """
    Elimina un material verificando que el profesor sea dueño del curso
    
    Args:
        material_id (int): ID del material a eliminar
        user_id (int): ID del usuario (profesor)
    
    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    # 1. Obtener id_profesor del usuario
    id_profesor = obtener_id_profesor_desde_usuario(user_id)
    
    if not id_profesor:
        return {'exito': False, 'mensaje': 'No se encontró el perfil de profesor'}
    
    # 2. Buscar material y verificar que el curso pertenece al profesor
    material = Material.query.join(Curso).filter(
        Material.id_material == material_id,
        Curso.id_profesor == id_profesor
    ).first()
    
    if not material:
        return {'exito': False, 'mensaje': 'Material no encontrado o no tienes permisos para eliminarlo'}
    
    nombre_material = material.nombre
    
    # 3. Eliminar archivo físico
    try:
        filepath = os.path.join(current_app.root_path, material.archivo_url.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error al eliminar archivo físico: {e}")
        # Continuamos aunque falle la eliminación física
    
    # 4. Eliminar registro de BD
    try:
        db.session.delete(material)
        db.session.commit()
        return {'exito': True, 'mensaje': f'Material "{nombre_material}" eliminado correctamente'}
    except Exception as e:
        db.session.rollback()
        return {'exito': False, 'mensaje': f'Error al eliminar de la base de datos: {str(e)}'}

def obtener_materiales_curso(curso_id):
    """
    Obtiene todos los materiales de un curso
    
    Args:
        curso_id (int): ID del curso
    
    Returns:
        list: Lista de materiales
    """
    return Material.query.filter_by(id_curso=curso_id).order_by(Material.fecha_subida.desc()).all()

def verificar_permisos_profesor(user_id, curso_id=None):
    """
    Verifica si un usuario tiene permisos de profesor sobre un curso
    
    Args:
        user_id (int): ID del usuario
        curso_id (int, optional): ID del curso a verificar
    
    Returns:
        bool: True si tiene permisos, False en caso contrario
    """
    id_profesor = obtener_id_profesor_desde_usuario(user_id)
    
    if not id_profesor:
        return False
    
    if curso_id:
        curso = Curso.query.filter_by(id_curso=curso_id, id_profesor=id_profesor).first()
        return curso is not None
    
    return True