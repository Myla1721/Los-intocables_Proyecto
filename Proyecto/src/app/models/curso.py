from src.app import db

class Curso(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    nivel = db.Column(db.String(50), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    
    # Relación con materiales
    materiales = db.relationship('Material', backref='curso', lazy=True, cascade="all, delete-orphan")
    
    # Relación con profesor
    profesor = db.relationship('User', backref='cursos_impartidos', lazy=True)