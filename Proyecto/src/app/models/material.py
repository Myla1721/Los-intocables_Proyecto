from src.app import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = 'Material'
    
    id_material = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    archivo_url = db.Column(db.Text, nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso', ondelete='CASCADE'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)