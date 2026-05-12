"""
Vista del módulo Alumno.
Maneja la presentación y redireccionamiento para los casos de uso del alumno.
"""

from flask import render_template, redirect, url_for, request, flash, session
from src.app.controllers.alumno_controller import (
    registrar_alumno,
    obtener_cursos_disponibles,
    inscribirse_curso,
    obtener_mis_cursos,
    obtener_material_curso,
)


class AlumnoView:

    # ------------------------------------------------------------------
    # Helpers de autenticación
    # ------------------------------------------------------------------

    @staticmethod
    def _verificar_autenticacion():
        return 'user_id' in session

    @staticmethod
    def _verificar_rol_alumno():
        return session.get('rol') == 'ALUMNO'

    # ------------------------------------------------------------------
    # Caso de uso 1: Crear cuenta de usuario
    # ------------------------------------------------------------------

    @staticmethod
    def mostrar_registro():
        """GET /alumno/registro — Muestra el formulario de registro."""
        # Si ya hay sesión activa, redirigir al home
        if 'user_id' in session:
            return redirect(url_for('main.home'))
        return render_template('alumno/registro.html')

    @staticmethod
    def procesar_registro():
        """POST /alumno/registro — Procesa el formulario de registro."""
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        resultado = registrar_alumno(nombre, apellido, correo, contrasena)

        if resultado['exito']:
            flash(resultado['mensaje'], 'success')
            return redirect(url_for('main.index'))
        else:
            flash(resultado['mensaje'], 'danger')
            return render_template('alumno/registro.html',
                                   nombre=nombre, apellido=apellido, correo=correo)

    # ------------------------------------------------------------------
    # Caso de uso 2: Ver cursos disponibles
    # ------------------------------------------------------------------

    @classmethod
    def ver_cursos_disponibles(cls):
        """GET /alumno/cursos — Lista todos los cursos de la plataforma."""
        if not cls._verificar_autenticacion():
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('main.index'))

        if not cls._verificar_rol_alumno():
            flash('Acceso denegado. Solo para alumnos.', 'danger')
            return redirect(url_for('main.home'))

        cursos = obtener_cursos_disponibles()
        return render_template('alumno/cursos_disponibles.html',
                               cursos=cursos,
                               nombre=session.get('nombre'))

    # ------------------------------------------------------------------
    # Caso de uso 3: Inscribirse a un curso
    # ------------------------------------------------------------------

    @classmethod
    def inscribirse(cls, curso_id):
        """POST /alumno/inscribirse/<curso_id> — Inscribe al alumno."""
        if not cls._verificar_autenticacion():
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('main.index'))

        if not cls._verificar_rol_alumno():
            flash('Acceso denegado. Solo para alumnos.', 'danger')
            return redirect(url_for('main.home'))

        resultado = inscribirse_curso(session['user_id'], curso_id)
        flash(resultado['mensaje'], 'success' if resultado['exito'] else 'danger')
        return redirect(url_for('main.alumno_cursos'))

    # ------------------------------------------------------------------
    # Caso de uso 4: Consultar material
    # ------------------------------------------------------------------

    @classmethod
    def ver_mis_cursos(cls):
        """GET /alumno/mis-cursos — Cursos en los que está inscrito el alumno."""
        if not cls._verificar_autenticacion():
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('main.index'))

        if not cls._verificar_rol_alumno():
            flash('Acceso denegado. Solo para alumnos.', 'danger')
            return redirect(url_for('main.home'))

        cursos = obtener_mis_cursos(session['user_id'])
        return render_template('alumno/mis_cursos.html',
                               cursos=cursos,
                               nombre=session.get('nombre'))

    @classmethod
    def ver_material_curso(cls, curso_id):
        """GET /alumno/mis-cursos/<curso_id>/material — Material de un curso inscrito."""
        if not cls._verificar_autenticacion():
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('main.index'))

        if not cls._verificar_rol_alumno():
            flash('Acceso denegado. Solo para alumnos.', 'danger')
            return redirect(url_for('main.home'))

        datos = obtener_material_curso(curso_id, session['user_id'])

        if not datos['exito']:
            flash(datos['mensaje'], 'danger')
            return redirect(url_for('main.alumno_mis_cursos'))

        return render_template('alumno/material_curso.html',
                               curso=datos['curso'],
                               materiales=datos['materiales'],
                               nombre=session.get('nombre'))
