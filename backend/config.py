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
    
    # Construir URI - Para TiDB Cloud con SSL habilitado
    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DB:
        SQLALCHEMY_DATABASE_URI = (
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
            '?charset=utf8mb4'
            '&ssl_ca=false'
            '&autocommit=true'
            '&connect_timeout=10'
            '&read_timeout=30'
            '&write_timeout=30'
            '&init_command=SET time_zone="-05:00"'  # UTC-5 para Colombia
        )
    else:
        raise ValueError("Faltan credenciales de BD en .env (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)")
    
    # SQLAlchemy Engine Pool Configuration
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 10,
        'connect_args': {
            'connect_timeout': 10,
            'read_timeout': 30,
            'write_timeout': 30,
            'charset': 'utf8mb4',
            'ssl': {'ssl': True},
        }
    }
    
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
