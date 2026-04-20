import os
from werkzeug.utils import secure_filename
from flask import current_app
from src.app import db
from src.app.models.curso import Curso
from src.app.models.material import Material

# Configuración para subida de archivos
UPLOAD_FOLDER = 'src/app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'jpg', 'png', 'mp4'}

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def obtener_cursos_disponibles(profesor_id=None):
    """
    Obtiene todos los cursos o solo los del profesor si se especifica ID
    
    Args:
        profesor_id (int, optional): ID del profesor para filtrar sus cursos
    
    Returns:
        list: Lista de cursos con sus materiales
    """
    if profesor_id:
        cursos = Curso.query.filter_by(profesor_id=profesor_id).all()
    else:
        cursos = Curso.query.all()
    
    return cursos

def subir_material_curso(curso_id, profesor_id, archivo):
    """
    Sube un archivo de material a un curso específico
    
    Args:
        curso_id (int): ID del curso
        profesor_id (int): ID del profesor (para verificar propiedad)
        archivo (FileStorage): Archivo subido desde el formulario
    
    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    # 1. Verificar que el curso existe y pertenece al profesor
    curso = Curso.query.filter_by(id=curso_id, profesor_id=profesor_id).first()
    
    if not curso:
        return {'exito': False, 'mensaje': 'Curso no encontrado o no tienes permisos'}
    
    # 2. Verificar que se subió un archivo
    if not archivo or archivo.filename == '':
        return {'exito': False, 'mensaje': 'No se seleccionó ningún archivo'}
    
    # 3. Validar extensión del archivo
    if not allowed_file(archivo.filename):
        return {'exito': False, 'mensaje': f'Tipo de archivo no permitido. Usar: {", ".join(ALLOWED_EXTENSIONS)}'}
    
    # 4. Guardar archivo
    filename = secure_filename(archivo.filename)
    
    # Crear nombre único para evitar sobrescrituras
    import time
    unique_filename = f"{int(time.time())}_{filename}"
    
    # Ruta completa
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    
    filepath = os.path.join(upload_path, unique_filename)
    archivo.save(filepath)
    
    # 5. Guardar registro en BD
    nuevo_material = Material(
        nombre_archivo=filename,
        ruta_archivo=f'/static/uploads/{unique_filename}',
        curso_id=curso_id
    )
    
    db.session.add(nuevo_material)
    db.session.commit()
    
    return {'exito': True, 'mensaje': f'Material "{filename}" subido correctamente'}

def eliminar_material_curso(material_id, profesor_id):
    """
    Elimina un material verificando que el profesor sea dueño del curso
    
    Args:
        material_id (int): ID del material a eliminar
        profesor_id (int): ID del profesor (para verificar propiedad)
    
    Returns:
        dict: {'exito': bool, 'mensaje': str}
    """
    # 1. Buscar material y verificar que el curso pertenece al profesor
    material = Material.query.join(Curso).filter(
        Material.id == material_id,
        Curso.profesor_id == profesor_id
    ).first()
    
    if not material:
        return {'exito': False, 'mensaje': 'Material no encontrado o no tienes permisos'}
    
    # 2. Eliminar archivo físico
    try:
        filepath = os.path.join(current_app.root_path, material.ruta_archivo.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error al eliminar archivo: {e}")
    
    # 3. Eliminar registro de BD
    nombre_archivo = material.nombre_archivo
    db.session.delete(material)
    db.session.commit()
    
    return {'exito': True, 'mensaje': f'Material "{nombre_archivo}" eliminado correctamente'}