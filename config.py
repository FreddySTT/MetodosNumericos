import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or os.environ.get('SECRET_KEY')
    DATA_BACKEND = os.environ.get('DATA_BACKEND', 'mysql').strip().lower()
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'sistema_fatiga')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    SQLSERVER_DRIVER = os.environ.get('SQLSERVER_DRIVER', 'ODBC Driver 18 for SQL Server')
    SQLSERVER_HOST = os.environ.get('SQLSERVER_HOST', 'localhost')
    SQLSERVER_PORT = os.environ.get('SQLSERVER_PORT', '1433')
    SQLSERVER_DATABASE = os.environ.get('SQLSERVER_DATABASE', 'sistema_fatiga')
    SQLSERVER_TRUSTED = os.environ.get('SQLSERVER_TRUSTED', '1') == '1'
    SQLSERVER_USER = os.environ.get('SQLSERVER_USER', '')
    SQLSERVER_PASSWORD = os.environ.get('SQLSERVER_PASSWORD', '')
    SQLSERVER_ENCRYPT = os.environ.get('SQLSERVER_ENCRYPT', 'yes')
    SQLSERVER_TRUST_CERT = os.environ.get('SQLSERVER_TRUST_CERT', 'yes')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('COOKIE_SECURE', '0') == '1'
    JSON_AS_ASCII = False
