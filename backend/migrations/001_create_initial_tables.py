"""
001_create_initial_tables.py
Migración inicial: Crear tablas base de MetricISO
Se ejecuta automáticamente al iniciar la app
"""

def validate(db):
    """Valida que las tablas existan"""
    from app.models import Proyecto, MetricaBase, HistoricoCalculo, FormulaISO
    
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    required_tables = ['proyectos', 'metricas_base', 'historico_calculos', 'formulas_iso']
    missing = [t for t in required_tables if t not in tables]
    
    if missing:
        print(f"❌ Tablas faltantes: {missing}")
        return False
    
    print("✅ Todas las tablas existen")
    return True
