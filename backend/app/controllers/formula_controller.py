from flask import request, jsonify
from ..models import db, FormulaISO, HistoricoCalculo
from ..utils.formulas import CalculadoraISO
from datetime import datetime

class FormulaController:
    
    def listar(self):
        formulas = FormulaISO.query.all()
        return jsonify([f.to_dict() for f in formulas])
    
    def obtener(self, codigo):
        formula = FormulaISO.query.filter_by(codigo=codigo).first_or_404()
        return jsonify(formula.to_dict())
    
    def calcular(self, codigo):
        data = request.json
        proyecto_id = data.get('proyecto_id')
        parametros = data.get('parametros', {})
        
        try:
            metodo = getattr(CalculadoraISO, codigo)
            valores = list(parametros.values())
            resultado = metodo(*valores)
            
            historico = HistoricoCalculo(
                proyecto_id=proyecto_id,
                formula=codigo,
                resultado=resultado
            )
            historico.set_datos_entrada(parametros)
            db.session.add(historico)
            db.session.commit()
            
            return jsonify({
                'formula': codigo,
                'resultado': resultado,
                'fecha': datetime.utcnow().isoformat()
            })
        
        except AttributeError:
            return jsonify({'error': 'Fórmula no encontrada'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 400
