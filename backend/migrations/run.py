"""
Migration Validator
Valida migraciones: python -m migrations.run
(Se ejecuta automáticamente al iniciar app/__init__.py)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

def validate_migrations():
    """Valida todas las migraciones"""
    app = create_app()
    
    with app.app_context():
        migrations = [
            '001_create_initial_tables',
            '002_insert_iso_formulas'
        ]
        
        all_valid = True
        for migration_name in migrations:
            try:
                module = __import__(f'migrations.{migration_name}', fromlist=['validate'])
                if hasattr(module, 'validate'):
                    print(f"🔍 Validando: {migration_name}...")
                    result = module.validate(db)
                    if not result:
                        all_valid = False
            except Exception as e:
                print(f"❌ {migration_name} - ERROR: {e}")
                all_valid = False
        
        return all_valid

if __name__ == '__main__':
    print("Validando migraciones...\n")
    success = validate_migrations()
    print()
    sys.exit(0 if success else 1)
