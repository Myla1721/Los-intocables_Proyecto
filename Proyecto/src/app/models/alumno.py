from src.app import db
from datetime import date


class Alumno(db.Model):
    """
    Modelo que representa la tabla 'Alumno' en la base de datos.
    Cada alumno está asociado a un usuario con rol ALUMNO.
    """
    __tablename__ = 'Alumno'

    id_alumno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )
    matricula = db.Column(db.String(50), unique=True)
    nivel_idioma = db.Column(db.Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2'))
    fecha_inscripcion_plataforma = db.Column(db.Date, default=date.today)

    # Relaciones
    usuario = db.relationship('User', backref='alumno', lazy=True)
    inscripciones = db.relationship('Inscripcion', backref='alumno', lazy=True, cascade='all, delete-orphan')
