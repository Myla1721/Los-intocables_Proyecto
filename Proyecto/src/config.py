from sqlalchemy.engine import URL

class Config:
    """
    Clase de configuración de la aplicación Flask

    Define la conexión a la base de datos MySQL usando SQLAlchemy
    """
    SQLALCHEMY_DATABASE_URI = URL.create( #URI de conexión a la base de datos
        drivername="mysql+pymysql",
        username="intocable",
        password="Ing2026!",
        host="localhost",
        port=3306,
        database="GestionCursosBD"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False #Desactiva notificaciones innecesarias de SQLAlchemy
    SECRET_KEY = "dev" #Clave secreta para sesiones y seguridad