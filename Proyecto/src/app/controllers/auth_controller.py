"""
Controlador de autenticación
"""

from src.app.models import User
from src.app import db
from datetime import datetime


class AuthController:

    @staticmethod
    def login(correo, password):
        user = User.query.filter_by(
            correo=correo,
            contrasena=password
        ).first()

        if user:
            user.sesion_activa = True
            user.ultimo_acceso = datetime.now()
            db.session.commit()

        return user

    @staticmethod
    def logout(user_id):
        user = User.query.get(user_id)

        if user:
            user.sesion_activa = False
            db.session.commit()