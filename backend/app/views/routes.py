from flask import Blueprint, jsonify, current_app
from ..controllers.proyecto_controller import ProyectoController
from ..controllers.formula_controller import FormulaController
from ..controllers.reporte_controller import generar_reporte_pdf
from flask import send_file

def init_routes(app):
    """Inicializa todas las rutas"""
    
    proyecto_bp = Blueprint('proyectos', __name__, url_prefix='/api/proyectos')
    formula_bp = Blueprint('formulas', __name__, url_prefix='/api/formulas')
    
    # Controllers
    proyecto_ctrl = ProyectoController(app.config)
    formula_ctrl = FormulaController()
    
    # Proyectos
    @proyecto_bp.route('', methods=['GET'])
    def listar_proyectos():
        return proyecto_ctrl.listar()
    
    @proyecto_bp.route('/<int:id>', methods=['GET'])
    def obtener_proyecto(id):
        return proyecto_ctrl.obtener(id)
    
    @proyecto_bp.route('', methods=['POST'])
    def crear_proyecto():
        return proyecto_ctrl.crear()
    
    @proyecto_bp.route('/<int:id>/analizar', methods=['POST'])
    def analizar_proyecto(id):
        return proyecto_ctrl.analizar(id)
    
    @proyecto_bp.route('/<int:id>', methods=['DELETE'])
    def eliminar_proyecto(id):
        return proyecto_ctrl.eliminar(id)
    
    @proyecto_bp.route('/<int:id>/historico', methods=['GET'])
    def get_historico(id):
        from ..models import HistoricoCalculo
        historico = HistoricoCalculo.query.filter_by(proyecto_id=id).order_by(HistoricoCalculo.fecha_calculo.desc()).all()
        return jsonify([h.to_dict() for h in historico])
    
    @proyecto_bp.route('/<int:id>/reporte-pdf', methods=['GET'])
    def descargar_reporte(id):
        """Genera y descarga un reporte PDF del proyecto"""
        pdf_buffer, error = generar_reporte_pdf(id)
        if error:
            return jsonify({'error': error}), 400
        
        from ..models import Proyecto
        proyecto = Proyecto.query.get(id)
        nombre_archivo = f"reporte_{proyecto.nombre.replace(' ', '_')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
    
    # Fórmulas
    @formula_bp.route('', methods=['GET'])
    def listar_formulas():
        return formula_ctrl.listar()
    
    @formula_bp.route('/<codigo>', methods=['GET'])
    def obtener_formula(codigo):
        return formula_ctrl.obtener(codigo)
    
    @formula_bp.route('/<codigo>/calcular', methods=['POST'])
    def calcular_formula(codigo):
        return formula_ctrl.calcular(codigo)
    
    @formula_bp.route('/<codigo>/referencias', methods=['GET'])
    def obtener_referencias_formula(codigo):
        return formula_ctrl.obtener_referencias(codigo)
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})
    
    app.register_blueprint(proyecto_bp)
    app.register_blueprint(formula_bp)
