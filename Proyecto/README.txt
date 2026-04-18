PRACTICA 4 - LOGIN FLASK

Luis Juárez Erick

Descripción:
Este proyecto consiste en una aplicación web desarrollada con Flask que implementa un sistema de login conectado a una base de datos MySQL


REQUISITOS

- Python 3.12
- MySQL Server
- pip


INSTALACIÓN


1. Clonar o descargar el proyecto.

2. Crear un entorno virtual:

   python3 -m venv .venv

3. Activar el entorno virtual:

   En Linux:
   source .venv/bin/activate

4. Instalar dependencias:

   pip install -r requirements.txt




CONFIGURACIÓN DE BASE DE DATOS


1. Abrir MySQL.

2. Ejecutar el archivo SQL proporcionado:

   Practica4.sql

   Esto creará:
   - Base de datos: practica4
   - Tabla: Usuario
   - Usuarios de prueba

3. Verificar credenciales en config.py:

   username = ericko
   password = MPyAlqm2005_
   database = practica4


EJECUCIÓN

1. Posicionar en la carpeta Practica4 con cd Practica4

2. Ejecutar la aplicación:

   python run.py

3. Abrir navegador en:

   http://127.0.0.1:5000


USO


- Ingresar un usuario y contraseña de la base de datos.
- Si las credenciales son correctas:
  → Se muestra una pantalla de bienvenida con el rol.
- Si son incorrectas:
  → Se muestra un mensaje de error.




