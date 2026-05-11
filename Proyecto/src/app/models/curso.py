from src.app import db

class Curso(db.Model):
    __tablename__ = 'Curso'
    
    id_curso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    id_profesor = db.Column(db.Integer, db.ForeignKey('Profesor.id_profesor', ondelete='CASCADE'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    profesor = db.relationship('Profesor', backref='cursos', lazy=True)
    materiales = db.relationship('Material', backref='curso', lazy=True, cascade="all, delete-orphan")