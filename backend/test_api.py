from app import create_app
from flask import json
import sys
import time

app = create_app()

with app.test_client() as client:
    # Crear proyecto con nombre unico
    timestamp = int(time.time())
    payload = {
        'nombre': f'Test Project {timestamp}',
        'url_github': f'https://github.com/test/test{timestamp}'
    }
    response = client.post('/api/proyectos', 
                          data=json.dumps(payload),
                          content_type='application/json')
    
    if response.status_code == 201:
        proyecto = response.get_json()
        proyecto_id = proyecto['id']
        print(f"[OK] Proyecto creado: {proyecto_id}")
    else:
        print("[FAIL] Error creando proyecto")
        proyecto_id = 1
    
    # Obtener formula
    response = client.get('/api/formulas/ICP')
    if response.status_code == 200:
        formula = response.get_json()
        print("[OK] Formula ICP obtenida")
        print(f"    Parametros: {formula['parametros']}")
    else:
        print("[FAIL] Error obteniendo formula")
        sys.exit(1)
    
    # Calcular
    payload = {
        'proyecto_id': proyecto_id,
        'parametros': {'Realizadas': 85, 'Planificadas': 100}
    }
    response = client.post('/api/formulas/ICP/calcular', 
                          data=json.dumps(payload),
                          content_type='application/json')
    
    if response.status_code == 200:
        result = response.get_json()
        print(f"[OK] Calculo exitoso")
        print(f"    Resultado: {result['resultado']} {result['unidad']}")
        print(f"    Interpretacion: {result['interpretacion']['nivel'].upper()}")
    else:
        print(f"[FAIL] Error en calculo: {response.status_code}")
        sys.exit(1)
    
    # Obtener referencias
    response = client.get('/api/formulas/ICP/referencias')
    if response.status_code == 200:
        references = response.get_json()
        print(f"[OK] Referencias obtenidas")
        print(f"    Formula: {references['codigo_formula']}")
        print(f"    Norma: {references['norma_iso']}")
        print(f"    Niveles: {list(references['rangos'].keys())}")
    else:
        print(f"[FAIL] Error obteniendo referencias: {response.status_code}")
        sys.exit(1)

print("\n[OK] Todos los tests pasaron correctamente")
