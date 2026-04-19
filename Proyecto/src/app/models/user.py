from src.app import db

class User(db.Model):
    """
     Modelo que representa la tabla 'Usuario' en la base de datos.

    Atributos:
        id: Identificador único del usuario
        nombre_usuario: Nombre de usuario
        contrasena: Contraseña del usuario
        rol: Rol del usuario (administrador o usuario)
    """
    __tablename__ = "Usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('ADMIN', 'PROFESOR', 'ALUMNO'), nullable=False)

    fecha_registro = db.Column(db.DateTime)
    sesion_activa = db.Column(db.Boolean, default=False)
    ultimo_acceso = db.Column(db.DateTime)