class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://USER:PASSWORD@localhost/GestionCursosBD"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev"
