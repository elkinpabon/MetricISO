from flask import Flask
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

from app.models import db, FormulaISO
from app.views.routes import init_routes
from app.utils.formulas import FORMULAS_DEFINICION
from config import config

load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    CORS(app)
    
    with app.app_context():
        try:
            # Conectar a BD
            logger.info(f"Conectando a {app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}/{app.config['MYSQL_DB']}")
            
            # Crear tablas
            db.create_all()
            logger.info("Tablas sincronizadas")
            
            # Insertar fórmulas ISO
            _init_formulas()
            logger.info("Formulas ISO sincronizadas")
            logger.info("Backend iniciado correctamente")
            
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.error(f"Host: {app.config.get('MYSQL_HOST')}, Puerto: {app.config.get('MYSQL_PORT')}")
            raise
    
    init_routes(app)
    
    return app

def _init_formulas():
    """Inicializa las fórmulas ISO en la base de datos"""
    try:
        count = 0
        for formula_data in FORMULAS_DEFINICION:
            existe = FormulaISO.query.filter_by(codigo=formula_data['codigo']).first()
            if not existe:
                formula = FormulaISO(
                    codigo=formula_data['codigo'],
                    nombre=formula_data['nombre'],
                    descripcion=formula_data['descripcion'],
                    formula=formula_data['formula'],
                    unidad=formula_data['unidad'],
                    tipo=formula_data.get('tipo', 'General'),
                    norma_iso=formula_data.get('norma_iso', 'ISO/IEC 9126')
                )
                formula.set_parametros(formula_data['parametros'])
                db.session.add(formula)
                count += 1
            else:
                # Actualizar tipo y norma_iso en fórmulas existentes
                if formula_data.get('tipo') and existe.tipo == 'General':
                    existe.tipo = formula_data.get('tipo', 'General')
                    db.session.add(existe)
                    count += 1
                if formula_data.get('norma_iso') and existe.norma_iso == 'ISO/IEC 9126':
                    existe.norma_iso = formula_data.get('norma_iso', 'ISO/IEC 9126')
                    db.session.add(existe)
                    count += 1
        
        if count > 0:
            logger.info(f"Insertadas/Actualizadas {count} nuevas formulas")
        
        total = FormulaISO.query.count()
        logger.info(f"Total formulas en BD: {total}")
        
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Error con formulas: {e}")
        db.session.rollback()
        raise

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
