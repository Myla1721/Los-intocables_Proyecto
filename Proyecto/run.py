from src.app import create_app

#Creamos la aplicación Flask
app = create_app()

if __name__ == '__main__':
    """
    Ejecuta el servidor
    """
    app.run(debug=True)