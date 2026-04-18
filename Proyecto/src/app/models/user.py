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

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.String(20))