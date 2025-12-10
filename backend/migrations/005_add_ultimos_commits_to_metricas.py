#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migración 005: Agregar columna ultimos_commits a la tabla metricas_base
"""

import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv

def run_migration():
    load_dotenv()
    
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT', 4000)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            ssl={'ssl': True}
        )
        cursor = conn.cursor()
        
        # Agregar columna ultimos_commits
        alter_query = """
        ALTER TABLE metricas_base 
        ADD COLUMN ultimos_commits LONGTEXT
        """
        
        cursor.execute(alter_query)
        conn.commit()
        print("✓ Columna 'ultimos_commits' agregada exitosamente a metricas_base")
        
        cursor.close()
        conn.close()
        return True
        
    except pymysql.Error as e:
        if "Duplicate column name" in str(e):
            print("⚠ La columna 'ultimos_commits' ya existe")
            return True
        print(f"✗ Error en migración: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = run_migration()
    exit(0 if success else 1)
