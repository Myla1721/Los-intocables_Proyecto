from src.app import db
from datetime import datetime


class Inscripcion(db.Model):
    """
    Modelo que representa la tabla 'Inscripcion'.
    Registra qué alumnos están inscritos en qué cursos.
    """
    __tablename__ = 'Inscripcion'

    id_inscripcion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_alumno = db.Column(
        db.Integer,
        db.ForeignKey('Alumno.id_alumno', ondelete='CASCADE'),
        nullable=False
    )
    id_curso = db.Column(
        db.Integer,
        db.ForeignKey('Curso.id_curso', ondelete='CASCADE'),
        nullable=False
    )
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)

    # Restricción única para evitar inscripciones duplicadas
    __table_args__ = (
        db.UniqueConstraint('id_alumno', 'id_curso', name='unique_inscripcion'),
    )

    # Relaciones
    curso = db.relationship('Curso', backref='inscripciones', lazy=True)
