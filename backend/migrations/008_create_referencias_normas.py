#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migración 008: Crear tabla de referencias de normas
"""

import pymysql
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
        
        # Crear tabla referencias_normas
        create_table_query = """
        CREATE TABLE IF NOT EXISTS referencias_normas (
            id INT PRIMARY KEY AUTO_INCREMENT,
            codigo_formula VARCHAR(50) NOT NULL,
            nombre_formula VARCHAR(255) NOT NULL,
            norma_iso VARCHAR(100) NOT NULL,
            valor_excelente FLOAT,
            valor_bueno FLOAT,
            valor_aceptable FLOAT,
            valor_malo FLOAT,
            valor_critico FLOAT,
            descripcion_excelente VARCHAR(255),
            descripcion_bueno VARCHAR(255),
            descripcion_aceptable VARCHAR(255),
            descripcion_malo VARCHAR(255),
            descripcion_critico VARCHAR(255),
            interpretacion LONGTEXT,
            UNIQUE KEY unique_formula (codigo_formula)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("✓ Tabla 'referencias_normas' creada exitosamente")
        
        # Insertar datos de referencia para ISO/IEC 9126
        insert_references = """
        INSERT INTO referencias_normas 
        (codigo_formula, nombre_formula, norma_iso, valor_excelente, valor_bueno, valor_aceptable, valor_malo, valor_critico,
         descripcion_excelente, descripcion_bueno, descripcion_aceptable, descripcion_malo, descripcion_critico, interpretacion)
        VALUES
        ('ICP', 'Índice de Capacidad del Proceso', 'ISO/IEC 9126', 1.33, 1.25, 1.0, 0.67, 0.5,
         'Excelente capacidad (Cpk ≥ 1.33)', 'Buena capacidad (1.25 ≤ Cpk < 1.33)', 'Capacidad aceptable (1.0 ≤ Cpk < 1.25)',
         'Capacidad baja (0.67 ≤ Cpk < 1.0)', 'Capacidad crítica (Cpk < 0.67)',
         'El Índice de Capacidad del Proceso mide si el proceso cumple con las especificaciones requeridas.'),
        
        ('FR', 'Funcionalidad', 'ISO/IEC 9126', 95, 85, 75, 50, 25,
         'Funcionalidad completa (>95%)', 'Funcionalidad buena (85-95%)', 'Funcionalidad aceptable (75-85%)',
         'Funcionalidad baja (50-75%)', 'Funcionalidad crítica (<50%)',
         'Porcentaje de funciones implementadas correctamente según especificaciones.'),
        
        ('MTBF', 'Tiempo Medio Entre Fallos', 'ISO/IEC 9126', 720, 480, 240, 120, 24,
         'Confiabilidad excelente (>720h)', 'Buena confiabilidad (480-720h)', 'Confiabilidad aceptable (240-480h)',
         'Confiabilidad baja (120-240h)', 'Confiabilidad crítica (<24h)',
         'Horas promedio que el sistema funciona sin fallos. Mayor es mejor.'),
        
        ('NC', 'No Conformidades', 'ISO 9001', 0, 1, 3, 5, 10,
         'Cero no conformidades', '1 no conformidad', '2-3 no conformidades',
         '4-5 no conformidades', '> 5 no conformidades',
         'Número de desviaciones encontradas durante auditorías. Menor es mejor.'),
        
        ('IVC', 'Índice de Vulnerabilidades Críticas', 'ISO/IEC 27001', 0, 0, 1, 3, 5,
         'Sin vulnerabilidades críticas', 'Sin vulnerabilidades críticas', 'Hasta 1 vulnerabilidad crítica',
         '2-3 vulnerabilidades críticas', '> 3 vulnerabilidades críticas',
         'Número de vulnerabilidades de seguridad críticas identificadas. Cero es objetivo.'),
        
        ('CC', 'Cobertura de Código', 'ISO/IEC 20246', 90, 80, 70, 50, 30,
         'Cobertura excelente (>90%)', 'Buena cobertura (80-90%)', 'Cobertura aceptable (70-80%)',
         'Cobertura baja (50-70%)', 'Cobertura crítica (<30%)',
         'Porcentaje de líneas de código ejecutadas durante pruebas. Mayor es mejor.'),
        
        ('E', 'Eficiencia', 'ISO/IEC 25010', 90, 80, 70, 50, 30,
         'Excelente eficiencia (>90%)', 'Buena eficiencia (80-90%)', 'Eficiencia aceptable (70-80%)',
         'Eficiencia baja (50-70%)', 'Eficiencia crítica (<30%)',
         'Medida de cuán bien utiliza el sistema los recursos (CPU, memoria, tiempo).')
        """
        
        try:
            cursor.execute(insert_references)
            conn.commit()
            print(f"✓ Insertadas referencias de normas exitosamente")
        except pymysql.Error as e:
            if "Duplicate" in str(e):
                print("⚠ Las referencias ya existen")
            else:
                raise
        
        cursor.close()
        conn.close()
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
