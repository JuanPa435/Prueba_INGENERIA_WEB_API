import os
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb()


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Usar la URL de la base de datos desde el archivo .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Usa SECRET_KEY desde el .env
