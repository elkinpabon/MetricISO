#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migración 006: Actualizar fechas NULL a la fecha actual
"""

import pymysql
from pymysql import Error
import os
from datetime import datetime
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
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Actualizar fechas NULL en proyectos
        update_query_1 = f"""
        UPDATE proyectos 
        SET fecha_creacion = '{now}'
        WHERE fecha_creacion IS NULL
        """
        
        cursor.execute(update_query_1)
        affected_1 = cursor.rowcount
        conn.commit()
        print(f"✓ Actualizadas {affected_1} fechas_creacion NULL en proyectos")
        
        # Actualizar fechas_actualizacion NULL
        update_query_2 = f"""
        UPDATE proyectos 
        SET fecha_actualizacion = '{now}'
        WHERE fecha_actualizacion IS NULL
        """
        
        cursor.execute(update_query_2)
        affected_2 = cursor.rowcount
        conn.commit()
        print(f"✓ Actualizadas {affected_2} fechas_actualizacion NULL en proyectos")
        
        # Actualizar fechas NULL en metricas_base
        update_query_3 = f"""
        UPDATE metricas_base 
        SET fecha_calculo = '{now}'
        WHERE fecha_calculo IS NULL
        """
        
        cursor.execute(update_query_3)
        affected_3 = cursor.rowcount
        conn.commit()
        print(f"✓ Actualizadas {affected_3} fechas_calculo NULL en metricas_base")
        
        # Actualizar fechas NULL en historico_calculos
        update_query_4 = f"""
        UPDATE historico_calculos 
        SET fecha_calculo = '{now}'
        WHERE fecha_calculo IS NULL
        """
        
        cursor.execute(update_query_4)
        affected_4 = cursor.rowcount
        conn.commit()
        print(f"✓ Actualizadas {affected_4} fechas_calculo NULL en historico_calculos")
        
        cursor.close()
        conn.close()
        
        total = affected_1 + affected_2 + affected_3 + affected_4
        if total > 0:
            print(f"\n✓ Total: {total} registros actualizados")
        else:
            print("\n✓ No había fechas NULL para actualizar")
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
