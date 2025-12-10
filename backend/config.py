import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar .env PRIMERO
load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TiDB Cloud Configuration - Lee EXACTAMENTE del .env
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '4000')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    
    # Construir URI - Para TiDB Cloud ignora SSL
    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DB:
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4&ssl_verify_cert=false'
    else:
        raise ValueError("Faltan credenciales de BD en .env (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)")
    
    # GitHub API
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    
    # Rutas
    REPOS_DIR = os.environ.get('REPOS_DIR') or os.path.join(os.path.dirname(__file__), '..', 'repos')
    
class DevelopmentConfig(Config):
    """Configuración desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración producción"""
    DEBUG = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
