================================================================================
                    GESTIÓN DE CURSOS DE IDIOMAS
                    Los Intocables - Proyecto Final
                    Ingeniería en Software
================================================================================

AUTORA DE UNA PARTE DEL MÓDULO DE PROFESOR 
------------------------------------------
Camila Sánchez Flores

================================================================================
DESCRIPCIÓN DEL PROYECTO
================================================================================

Sistema web para la gestión de cursos de idiomas con tres tipos de usuarios:
- Administrador: Gestiona cuentas de profesores y usuarios
- Profesor: Gestiona cursos y materiales
- Alumno: Se inscribe a cursos y consulta material

================================================================================
MÓDULO DESARROLLADO: PROFESOR
================================================================================

CASOS DE USO IMPLEMENTADOS:

[✅] Ver cursos disponibles
     El profesor puede visualizar todos los cursos que tiene asignados

[✅] Subir material
     El profesor puede subir archivos (PDF, Word, imágenes, videos) a sus cursos

[✅] Eliminar material
     El profesor puede eliminar materiales previamente subidos

FUNCIONALIDADES ADICIONALES:

- Creación automática de curso de demostración si no hay cursos asignados
- Validación de permisos por rol (solo accesible para PROFESOR)
- Interfaz responsive con Bootstrap 5
- Mensajes de confirmación para acciones críticas
- Manejo seguro de archivos con nombres únicos

================================================================================
TECNOLOGÍAS UTILIZADAS
================================================================================

Python 3         - Lenguaje de programación principal
Flask            - Framework web
SQLAlchemy       - ORM para base de datos
SQLite           - Base de datos (desarrollo/pruebas)
MySQL            - Base de datos (producción)
Bootstrap 5      - Framework CSS para interfaz
Jinja2           - Motor de plantillas
Werkzeug         - Manejo seguro de archivos

================================================================================
ESTRUCTURA DE ARCHIVOS DEL MÓDULO
================================================================================

src/app/
├── models/
│   ├── curso.py              # Modelo de Curso
│   ├── material.py           # Modelo de Material
│   └── profesor.py           # Modelo de Profesor
├── controllers/
│   └── profesor_controller.py # Lógica de negocio del profesor
├── views/
│   └── profesor_view.py      # Vistas y validaciones del profesor
├── templates/
│   └── profesor/
│       └── cursos.html       # Interfaz de gestión de cursos
├── static/
│   └── uploads/              # Archivos subidos por profesores
└── routes.py                 # Rutas del módulo (/profesor/*)

================================================================================
INSTALACIÓN Y EJECUCIÓN
================================================================================

1. Clonar el repositorio
   git clone https://github.com/Myla1721/Los-intocables_Proyecto.git
   cd Los-intocables_Proyecto/Proyecto

2. Crear y activar entorno virtual
   python -m venv .venv
   .venv\Scripts\activate

3. Instalar dependencias
   pip install -r requirements.txt

4. Ejecutar la aplicación
   python run.py

5. Acceder al sistema
   URL: http://127.0.0.1:5000
   Usuario Profesor: charlier45@correo.com
   Contraseña: MPyAlqm1990

================================================================================
EVIDENCIA DEL FUNCIONAMIENTO
================================================================================

[ ] Página de Inicio del Profesor
[ ] Gestión de Cursos y Materiales
[ ] Subida de Material
[ ] Eliminación de Material

================================================================================
FLUJO DE TRABAJO CON GIT
================================================================================

# Rama de desarrollo
git checkout rama-lider

# Agregar cambios
git add .

# Commit
git commit -m "Módulo de Profesor completo"

# Subir a GitHub
git push origin rama-lider

================================================================================
EQUIPO DE DESARROLLO
================================================================================

Nombre                    Rol              Módulo
----------------------------------------------------------------------------
Camila Sánchez Flores     Desarrolladora   Profesor (Ver cursos, Subir/Eliminar)
[Compañero]               Desarrollador    Profesor (Crear/Modificar/Eliminar)
[Compañero]               Desarrollador    Administrador
[Compañero]               Desarrollador    Alumno

================================================================================
FECHA DE ENTREGA
================================================================================

20 de abril de 2026

================================================================================
NOTAS
================================================================================

- El proyecto utiliza SQLite para desarrollo y pruebas locales
- La configuración de MySQL está preparada para producción
- Los archivos subidos se almacenan en src/app/static/uploads/

================================================================================
© 2026 Los Intocables - Todos los derechos reservados.
================================================================================
