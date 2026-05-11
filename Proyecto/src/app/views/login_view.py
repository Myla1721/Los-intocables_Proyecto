"""
Vista LoginView
"""

from flask import render_template, request


class LoginView:

    @staticmethod
    def mostrarFormulario():
        return render_template('login.html')

    @staticmethod
    def obtenerCredenciales():
        correo = request.form.get('correo')
        password = request.form.get('password')
        return correo, password

    @staticmethod
    def mostrarError():
        return render_template('error.html')