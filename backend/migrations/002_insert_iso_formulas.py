"""
002_insert_iso_formulas.py
Migración: Validar que 13 fórmulas ISO existan
Se ejecuta automáticamente al iniciar la app
"""

def validate(db):
    """Valida que existan las 13 fórmulas ISO"""
    from app.models import FormulaISO
    
    formulas = FormulaISO.query.all()
    
    if len(formulas) < 13:
        print(f"❌ Solo hay {len(formulas)} fórmulas (se esperan 13)")
        return False
    
    print(f"✅ Las 13 fórmulas ISO existen")
    return True
