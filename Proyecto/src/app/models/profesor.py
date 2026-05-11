from src.app import db

class Profesor(db.Model):
    __tablename__ = 'Profesor'
    
    id_profesor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'), nullable=False, unique=True)
    especialidad = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    fecha_contratacion = db.Column(db.Date)
    
    # Relación
    usuario = db.relationship('User', backref='profesor', lazy=True)