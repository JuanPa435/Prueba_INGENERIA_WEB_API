# Config/Config.py
import os
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb() 

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'mysecretkey'))
    JWT_ALGORITHM = 'HS256'
