"""
Migración para añadir rangos de referencia a todas las 13 fórmulas ISO
"""

def migrate(db):
    """Añade referencias para todas las fórmulas"""
    from app.models import ReferenciaNorma
    
    referencias_data = [
        {
            'codigo_formula': 'ICP',
            'nombre_formula': 'Índice de Cumplimiento de Planificación',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 95,
            'valor_bueno': 85,
            'valor_aceptable': 75,
            'valor_malo': 60,
            'valor_critico': 0,
            'descripcion_excelente': 'Cumplimiento excelente (95-100%)',
            'descripcion_bueno': 'Buen cumplimiento (85-94%)',
            'descripcion_aceptable': 'Cumplimiento aceptable (75-84%)',
            'descripcion_malo': 'Cumplimiento bajo (60-74%)',
            'descripcion_critico': 'Cumplimiento crítico (<60%)',
            'interpretacion': 'Mayor porcentaje indica mejor cumplimiento de planificación'
        },
        {
            'codigo_formula': 'NC',
            'nombre_formula': 'Índice de No Conformidades',
            'norma_iso': 'ISO 9001',
            'valor_excelente': 0.02,
            'valor_bueno': 0.05,
            'valor_aceptable': 0.10,
            'valor_malo': 0.20,
            'valor_critico': 1.0,
            'descripcion_excelente': 'Muy pocas no conformidades (<2%)',
            'descripcion_bueno': 'Pocas no conformidades (2-5%)',
            'descripcion_aceptable': 'Aceptable (5-10%)',
            'descripcion_malo': 'Muchas no conformidades (10-20%)',
            'descripcion_critico': 'Crítico (>20%)',
            'interpretacion': 'Menor ratio es mejor. Indica calidad de auditoría'
        },
        {
            'codigo_formula': 'FR',
            'nombre_formula': 'Tasa de Fallos',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 0.1,
            'valor_bueno': 0.5,
            'valor_aceptable': 1.0,
            'valor_malo': 2.0,
            'valor_critico': 10.0,
            'descripcion_excelente': 'Muy pocos fallos (<0.1 por unidad)',
            'descripcion_bueno': 'Pocos fallos (0.1-0.5 por unidad)',
            'descripcion_aceptable': 'Aceptable (0.5-1.0 por unidad)',
            'descripcion_malo': 'Muchos fallos (1.0-2.0 por unidad)',
            'descripcion_critico': 'Crítico (>2.0 por unidad)',
            'interpretacion': 'Menor tasa es mejor. Indica confiabilidad'
        },
        {
            'codigo_formula': 'MTBF',
            'nombre_formula': 'Tiempo Medio Entre Fallos',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 1000,
            'valor_bueno': 500,
            'valor_aceptable': 200,
            'valor_malo': 50,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente confiabilidad (>1000 horas)',
            'descripcion_bueno': 'Buena confiabilidad (500-1000 horas)',
            'descripcion_aceptable': 'Aceptable (200-500 horas)',
            'descripcion_malo': 'Baja confiabilidad (50-200 horas)',
            'descripcion_critico': 'Crítico (<50 horas)',
            'interpretacion': 'Mayor MTBF indica mejor confiabilidad del sistema'
        },
        {
            'codigo_formula': 'TPR',
            'nombre_formula': 'Tiempo Promedio de Respuesta',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 100,
            'valor_bueno': 250,
            'valor_aceptable': 500,
            'valor_malo': 1000,
            'valor_critico': 5000,
            'descripcion_excelente': 'Respuesta muy rápida (<100 ms)',
            'descripcion_bueno': 'Respuesta rápida (100-250 ms)',
            'descripcion_aceptable': 'Respuesta aceptable (250-500 ms)',
            'descripcion_malo': 'Respuesta lenta (500-1000 ms)',
            'descripcion_critico': 'Respuesta muy lenta (>1000 ms)',
            'interpretacion': 'Menor tiempo es mejor. Impacta en experiencia de usuario'
        },
        {
            'codigo_formula': 'IVC',
            'nombre_formula': 'Índice de Vulnerabilidades Críticas',
            'norma_iso': 'ISO/IEC 27001',
            'valor_excelente': 0,
            'valor_bueno': 2,
            'valor_aceptable': 5,
            'valor_malo': 10,
            'valor_critico': 100,
            'descripcion_excelente': 'Sin vulnerabilidades críticas',
            'descripcion_bueno': 'Pocas vulnerabilidades críticas (0-2%)',
            'descripcion_aceptable': 'Vulnerabilidades críticas (2-5%)',
            'descripcion_malo': 'Muchas vulnerabilidades críticas (5-10%)',
            'descripcion_critico': 'Crítico (>10%)',
            'interpretacion': 'Menor porcentaje es mejor. Seguridad crítica'
        },
        {
            'codigo_formula': 'CC',
            'nombre_formula': 'Complejidad Ciclomática',
            'norma_iso': 'ISO/IEC 20246',
            'valor_excelente': 5,
            'valor_bueno': 10,
            'valor_aceptable': 15,
            'valor_malo': 25,
            'valor_critico': 50,
            'descripcion_excelente': 'Baja complejidad (<5)',
            'descripcion_bueno': 'Complejidad moderada (5-10)',
            'descripcion_aceptable': 'Complejidad aceptable (10-15)',
            'descripcion_malo': 'Alta complejidad (15-25)',
            'descripcion_critico': 'Muy alta complejidad (>25)',
            'interpretacion': 'Menor complejidad facilita mantenimiento y pruebas'
        },
        {
            'codigo_formula': 'TS',
            'nombre_formula': 'Tasa de Sobrevivencia',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 98,
            'valor_bueno': 90,
            'valor_aceptable': 80,
            'valor_malo': 70,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente tasa de éxito (98-100%)',
            'descripcion_bueno': 'Buena tasa de éxito (90-97%)',
            'descripcion_aceptable': 'Aceptable (80-89%)',
            'descripcion_malo': 'Baja tasa de éxito (70-79%)',
            'descripcion_critico': 'Crítico (<70%)',
            'interpretacion': 'Mayor porcentaje indica más tests pasando'
        },
        {
            'codigo_formula': 'IC',
            'nombre_formula': 'Índice de Compatibilidad',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 95,
            'valor_bueno': 85,
            'valor_aceptable': 75,
            'valor_malo': 60,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente compatibilidad (95-100%)',
            'descripcion_bueno': 'Buena compatibilidad (85-94%)',
            'descripcion_aceptable': 'Aceptable (75-84%)',
            'descripcion_malo': 'Compatibilidad limitada (60-74%)',
            'descripcion_critico': 'Crítico (<60%)',
            'interpretacion': 'Mayor porcentaje indica mejor cobertura de plataformas'
        },
        {
            'codigo_formula': 'Ef',
            'nombre_formula': 'Eficiencia',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 10,
            'valor_bueno': 5,
            'valor_aceptable': 2,
            'valor_malo': 1,
            'valor_critico': 0,
            'descripcion_excelente': 'Muy eficiente (>10 tareas/hora)',
            'descripcion_bueno': 'Eficiente (5-10 tareas/hora)',
            'descripcion_aceptable': 'Aceptable (2-5 tareas/hora)',
            'descripcion_malo': 'Baja eficiencia (1-2 tareas/hora)',
            'descripcion_critico': 'Crítico (<1 tarea/hora)',
            'interpretacion': 'Mayor valor indica mejor productividad'
        },
        {
            'codigo_formula': 'E',
            'nombre_formula': 'Exactitud',
            'norma_iso': 'ISO/IEC 25010',
            'valor_excelente': 98,
            'valor_bueno': 90,
            'valor_aceptable': 80,
            'valor_malo': 70,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente exactitud (98-100%)',
            'descripcion_bueno': 'Buena exactitud (90-97%)',
            'descripcion_aceptable': 'Aceptable (80-89%)',
            'descripcion_malo': 'Baja exactitud (70-79%)',
            'descripcion_critico': 'Crítico (<70%)',
            'interpretacion': 'Mayor porcentaje indica más resultados correctos'
        },
        {
            'codigo_formula': 'Uso',
            'nombre_formula': 'Tasa de Uso de Recursos',
            'norma_iso': 'ISO/IEC 9126',
            'valor_excelente': 80,
            'valor_bueno': 60,
            'valor_aceptable': 40,
            'valor_malo': 20,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente utilización (80-100%)',
            'descripcion_bueno': 'Buena utilización (60-79%)',
            'descripcion_aceptable': 'Aceptable (40-59%)',
            'descripcion_malo': 'Baja utilización (20-39%)',
            'descripcion_critico': 'Crítico (<20%)',
            'interpretacion': 'Mayor porcentaje indica mejor aprovechamiento de recursos'
        },
        {
            'codigo_formula': 'IM',
            'nombre_formula': 'Índice de Interoperabilidad Multiplataforma',
            'norma_iso': 'ISO/IEC 25010',
            'valor_excelente': 90,
            'valor_bueno': 75,
            'valor_aceptable': 60,
            'valor_malo': 40,
            'valor_critico': 0,
            'descripcion_excelente': 'Excelente interoperabilidad (90-100%)',
            'descripcion_bueno': 'Buena interoperabilidad (75-89%)',
            'descripcion_aceptable': 'Aceptable (60-74%)',
            'descripcion_malo': 'Interoperabilidad limitada (40-59%)',
            'descripcion_critico': 'Crítico (<40%)',
            'interpretacion': 'Mayor porcentaje indica mejor cobertura multiplataforma'
        }
    ]
    
    for ref_data in referencias_data:
        # Verificar si ya existe
        existing = ReferenciaNorma.query.filter_by(codigo_formula=ref_data['codigo_formula']).first()
        if not existing:
            ref = ReferenciaNorma(**ref_data)
            db.session.add(ref)
    
    db.session.commit()
    print(f"✓ Añadidas referencias para todas las 13 fórmulas")
