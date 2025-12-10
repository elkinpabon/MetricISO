"""
Migración 010: Agregar columna interpretacion_json a historico_calculos
"""

def upgrade(db):
    """Agrega la columna interpretacion_json"""
    try:
        from sqlalchemy import text
        
        # Verificar si la columna ya existe
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('historico_calculos')]
        
        if 'interpretacion_json' not in columns:
            with db.engine.connect() as connection:
                connection.execute(text(
                    'ALTER TABLE historico_calculos ADD COLUMN interpretacion_json TEXT'
                ))
                connection.commit()
            print("✓ Columna interpretacion_json agregada a historico_calculos")
        else:
            print("  - Columna interpretacion_json ya existe")
    
    except Exception as e:
        print(f"  ! Error al agregar columna: {str(e)}")
