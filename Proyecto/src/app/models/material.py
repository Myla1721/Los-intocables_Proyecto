from src.app import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = 'materiales'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)