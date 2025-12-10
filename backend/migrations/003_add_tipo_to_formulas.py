"""
Migración 003: Agregar columna tipo a formulas_iso
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from dotenv import load_dotenv
import ssl

load_dotenv()

def migrate():
    """Ejecutar migración"""
    try:
        db_config = {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'user': os.environ.get('MYSQL_USER', 'root'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'database': os.environ.get('MYSQL_DB', 'metriciso'),
            'port': int(os.environ.get('MYSQL_PORT', 3306)),
            'ssl': {'ssl': True},
            'charset': 'utf8mb4',
            'autocommit': True,
            'connect_timeout': 10
        }
        
        conn = pymysql.connect(**db_config)
        
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'formulas_iso' AND COLUMN_NAME = 'tipo'
        """)
        
        if not cursor.fetchone():
            print("Agregando columna 'tipo' a tabla 'formulas_iso'...")
            cursor.execute("""
                ALTER TABLE formulas_iso 
                ADD COLUMN tipo VARCHAR(100) DEFAULT 'General' AFTER unidad
            """)
            conn.commit()
            print("✓ Columna 'tipo' agregada exitosamente")
        else:
            print("✓ Columna 'tipo' ya existe")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    migrate()
