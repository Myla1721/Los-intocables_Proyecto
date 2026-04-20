from flask import render_template, redirect, url_for, request, flash, session
from src.app.controllers.profesor_controller import (
    obtener_cursos_disponibles,
    subir_material_curso,
    eliminar_material_curso
)

class ProfesorView:
    
    @staticmethod
    def verificar_autenticacion():
        """Verifica si hay sesión activa"""
        return 'user_id' in session
    
    @staticmethod
    def verificar_rol_profesor():
        """Verifica si el usuario es profesor"""
        return session.get('rol') == 'PROFESOR'
    
    @classmethod
    def ver_cursos(cls):
        """Muestra la página de cursos del profesor"""
        if not cls.verificar_autenticacion():
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('main.index'))
        
        if not cls.verificar_rol_profesor():
            flash('Acceso denegado. Solo para profesores', 'danger')
            return redirect(url_for('main.home'))
        
        profesor_id = session['user_id']
        cursos = obtener_cursos_disponibles(profesor_id)
        
        # Mensaje informativo si es un curso demo
        if cursos and "Demo" in cursos[0].nombre:
            flash('ℹ️ Este es un curso de demostración. Puedes subir y eliminar material para probar.', 'info')
        
        return render_template('profesor/cursos.html', 
                            cursos=cursos, 
                            nombre=session.get('nombre'))
    
    @classmethod
    def subir_material(cls, curso_id):
        """Procesa la subida de material"""
        if not cls.verificar_autenticacion():
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('main.index'))
        
        if not cls.verificar_rol_profesor():
            flash('Acceso denegado. Solo para profesores', 'danger')
            return redirect(url_for('main.home'))
        
        archivo = request.files.get('archivo')
        profesor_id = session['user_id']
        
        resultado = subir_material_curso(curso_id, profesor_id, archivo)
        
        if resultado['exito']:
            flash(resultado['mensaje'], 'success')
        else:
            flash(resultado['mensaje'], 'danger')
        
        return redirect(url_for('main.profesor_cursos'))
    
    @classmethod
    def eliminar_material(cls, material_id):
        """Procesa la eliminación de material"""
        if not cls.verificar_autenticacion():
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('main.index'))
        
        if not cls.verificar_rol_profesor():
            flash('Acceso denegado. Solo para profesores', 'danger')
            return redirect(url_for('main.home'))
        
        profesor_id = session['user_id']
        resultado = eliminar_material_curso(material_id, profesor_id)
        
        if resultado['exito']:
            flash(resultado['mensaje'], 'success')
        else:
            flash(resultado['mensaje'], 'danger')
        
        return redirect(url_for('main.profesor_cursos'))