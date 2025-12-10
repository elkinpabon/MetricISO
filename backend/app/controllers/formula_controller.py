from flask import request, jsonify
from ..models import db, FormulaISO, HistoricoCalculo, ReferenciaNorma
from ..utils.formulas import CalculadoraISO
from sqlalchemy import exc
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FormulaController:
    
    def listar(self):
        try:
            formulas = FormulaISO.query.all()
            return jsonify([f.to_dict() for f in formulas])
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error listando fórmulas: {str(e)}")
            return jsonify({'error': 'Error interno'}), 500
    
    def obtener(self, codigo):
        try:
            formula = FormulaISO.query.filter_by(codigo=codigo).first_or_404()
            return jsonify(formula.to_dict())
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error obteniendo fórmula: {str(e)}")
            return jsonify({'error': 'Error interno'}), 500
    
    def calcular(self, codigo):
        try:
            data = request.json
            proyecto_id = data.get('proyecto_id')
            parametros = data.get('parametros', {})
            
            # Calcular resultado
            metodo = getattr(CalculadoraISO, codigo)
            valores = list(parametros.values())
            resultado = metodo(*valores)
            
            # Obtener referencias de la norma para interpretar resultado
            formula = FormulaISO.query.filter_by(codigo=codigo).first()
            referencia = ReferenciaNorma.query.filter_by(codigo_formula=codigo).first()
            
            # Preparar interpretación
            interpretacion = None
            if referencia:
                interpretacion = self._interpretar_resultado(resultado, referencia)
            
            # Guardar en histórico
            historico = HistoricoCalculo(
                proyecto_id=proyecto_id,
                formula=codigo,
                resultado=resultado,
                fecha_calculo=datetime.now()
            )
            historico.set_datos_entrada(parametros)
            if interpretacion:
                historico.set_interpretacion(interpretacion)
            db.session.add(historico)
            db.session.commit()
            
            respuesta = {
                'formula': codigo,
                'nombre': formula.nombre if formula else codigo,
                'resultado': round(resultado, 2),
                'unidad': formula.unidad if formula else '',
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parametros_entrada': parametros
            }
            
            # Agregar interpretación si existe referencia
            if referencia:
                respuesta['referencia'] = referencia.to_dict()
                respuesta['interpretacion'] = interpretacion
            
            return jsonify(respuesta), 200
        
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except AttributeError:
            logger.error(f"Fórmula no encontrada: {codigo}")
            return jsonify({'error': f'Fórmula {codigo} no existe'}), 404
        except Exception as e:
            logger.error(f"Error calculando fórmula {codigo}: {str(e)}")
            db.session.rollback()
            return jsonify({'error': f'Error: {str(e)}'}), 500
    
    def _interpretar_resultado(self, resultado, referencia):
        """Interpreta el resultado según los rangos de referencia"""
        if referencia.valor_excelente is not None and resultado >= referencia.valor_excelente:
            return {
                'nivel': 'excelente',
                'descripcion': referencia.descripcion_excelente,
                'color': '#00AA00',
                'recomendacion': 'Excelente desempeño. Mantener prácticas actuales.'
            }
        elif referencia.valor_bueno is not None and resultado >= referencia.valor_bueno:
            return {
                'nivel': 'bueno',
                'descripcion': referencia.descripcion_bueno,
                'color': '#88DD00',
                'recomendacion': 'Buen desempeño. Sin cambios urgentes.'
            }
        elif referencia.valor_aceptable is not None and resultado >= referencia.valor_aceptable:
            return {
                'nivel': 'aceptable',
                'descripcion': referencia.descripcion_aceptable,
                'color': '#FFDD00',
                'recomendacion': 'Desempeño aceptable. Considerar mejoras.'
            }
        elif referencia.valor_malo is not None and resultado >= referencia.valor_malo:
            return {
                'nivel': 'malo',
                'descripcion': referencia.descripcion_malo,
                'color': '#FF8800',
                'recomendacion': 'Desempeño bajo. Se requieren mejoras.'
            }
        else:
            return {
                'nivel': 'critico',
                'descripcion': referencia.descripcion_critico,
                'color': '#DD0000',
                'recomendacion': 'Desempeño crítico. Acción inmediata requerida.'
            }
    
    def obtener_referencias(self, codigo):
        """Obtiene los parámetros de referencia para una fórmula"""
        try:
            referencia = ReferenciaNorma.query.filter_by(codigo_formula=codigo).first()
            if not referencia:
                return jsonify({}), 200
            
            return jsonify(referencia.to_dict()), 200
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error obteniendo referencias: {str(e)}")
            return jsonify({'error': f'Error: {str(e)}'}), 500
