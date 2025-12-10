#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migración 007: Convertir fechas de UTC a hora local (UTC-5)
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
        
        # Convertir fechas_creacion en proyectos de UTC a UTC-5 (restar 5 horas)
        update_query_1 = """
        UPDATE proyectos 
        SET fecha_creacion = DATE_SUB(fecha_creacion, INTERVAL 5 HOUR)
        WHERE fecha_creacion IS NOT NULL
        """
        
        cursor.execute(update_query_1)
        affected_1 = cursor.rowcount
        conn.commit()
        print(f"✓ Convertidas {affected_1} fechas_creacion de UTC a hora local")
        
        # Convertir fechas_actualizacion en proyectos
        update_query_2 = """
        UPDATE proyectos 
        SET fecha_actualizacion = DATE_SUB(fecha_actualizacion, INTERVAL 5 HOUR)
        WHERE fecha_actualizacion IS NOT NULL
        """
        
        cursor.execute(update_query_2)
        affected_2 = cursor.rowcount
        conn.commit()
        print(f"✓ Convertidas {affected_2} fechas_actualizacion de UTC a hora local")
        
        # Convertir fechas_calculo en metricas_base
        update_query_3 = """
        UPDATE metricas_base 
        SET fecha_calculo = DATE_SUB(fecha_calculo, INTERVAL 5 HOUR)
        WHERE fecha_calculo IS NOT NULL
        """
        
        cursor.execute(update_query_3)
        affected_3 = cursor.rowcount
        conn.commit()
        print(f"✓ Convertidas {affected_3} fechas_calculo en metricas_base de UTC a hora local")
        
        # Convertir fechas_calculo en historico_calculos
        update_query_4 = """
        UPDATE historico_calculos 
        SET fecha_calculo = DATE_SUB(fecha_calculo, INTERVAL 5 HOUR)
        WHERE fecha_calculo IS NOT NULL
        """
        
        cursor.execute(update_query_4)
        affected_4 = cursor.rowcount
        conn.commit()
        print(f"✓ Convertidas {affected_4} fechas_calculo en historico_calculos de UTC a hora local")
        
        cursor.close()
        conn.close()
        
        total = affected_1 + affected_2 + affected_3 + affected_4
        print(f"\n✓ Total: {total} fechas convertidas de UTC a hora local (UTC-5)")
        return True
        
    except pymysql.Error as e:
        print(f"✗ Error en migración: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = run_migration()
    exit(0 if success else 1)
