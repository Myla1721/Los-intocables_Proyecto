# Gestión de Cursos de Idiomas

Proyecto Final  Ingeniería en Software
Equipo Los Intocables

## Autores

- *Módulo de Profesor*: Camila Sánchez Flores y Erick Luis Juárez

## Descripción del Proyecto

Sistema web para la gestión de cursos de idiomas con tres tipos de usuarios:

- Administrador: Gestiona cuentas de profesores y usuarios
- Profesor: Gestiona cursos y materiales
- Alumno: Se inscribe a cursos y consulta material

## Módulo de Profesor

### Casos de Uso

- [x] Crear curso
El profesor crear un curso.

- [x] Eliminar curso
El profesor eliminar un curso que haya creado previamente.

- [x] Modificar curso
El profesor modifica la información de un curso existente.

- [X] Ver cursos disponibles
El profesor puede visualizar todos los cursos que tiene asignados.

- [X] Subir material
El profesor puede subir archivos (PDF, Word, imágenes, videos) a sus cursos.

- [X] Eliminar material
El profesor puede eliminar materiales previamente subidos.

### Funcionalidades Adicionales:

- Creación automática de curso de demostración si no hay cursos asignados
- Validación de permisos por rol (solo accesible para PROFESOR)
- Interfaz responsive con Bootstrap 5
- Mensajes de confirmación para acciones críticas
- Manejo seguro de archivos con nombres únicos

## Tecnologías Utilizadas

- Python 3         - Lenguaje de programación principal
- Flask            - Framework web
- SQLAlchemy       - ORM para base de datos
- SQLite           - Base de datos (desarrollo/pruebas)
- MySQL            - Base de datos (producción)
- Bootstrap 5      - Framework CSS para interfaz
- Jinja2           - Motor de plantillas
- Werkzeug         - Manejo seguro de archivos

## Estructura del Módulo

src/app/

```
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
```

## Instalación y Ejecución

1. Clonar el repositorio
```
git clone https://github.com/Myla1721/Los-intocables_Proyecto.git
cd Los-intocables_Proyecto/Proyecto
```

2. Crear y activar entorno virtual
```
python -m venv .venv
source .venv/Scripts/activate
```

3. Instalar dependencias
```
pip install -r requirements.txt
```

4. Crear base de datos
```
sudo mysql < db/schema.sql
```

Además hay que modificar Proyecto/src/config.py reemplazando USER y PASSWORD por los valores correspondientes.

5. Ejecutar la aplicación
```
python run.py
```

6. Acceder al sistema
- URL: http://127.0.0.1:5000
- Usuario Profesor: charlier45@correo.com
- Contraseña: MPyAlqm1990

## Equipo de Desarrollo

| Nombre                | Rol            | Módulo                                |
|-----------------------|----------------|---------------------------------------|
| Camila Sánchez Flores | Desarrolladora | Profesor (Ver cursos, Subir/Eliminar) |
| Erick Luis Juárez     | Desarrollador  | Profesor (Crear/Modificar/Eliminar)   |
| [Compañero]           | Desarrollador  | Administrador                         |
| [Compañero]           | Desarrollador  | Alumno                                |

## Fecha de Entrega

20 de abril de 2026

## Notas

- El proyecto utiliza SQLite para desarrollo y pruebas locales
- La configuración de MySQL está preparada para producción
- Los archivos subidos se almacenan en src/app/static/uploads/

| © 2026 Los Intocables - Todos los derechos reservados. |
|--------------------------------------------------------|
