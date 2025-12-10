from flask import request, jsonify
from ..models import db, Proyecto, MetricaBase, HistoricoCalculo
from ..utils.github_analyzer import GitHubAnalyzer
from sqlalchemy import exc
import os
import shutil
import stat
import logging

logger = logging.getLogger(__name__)

class ProyectoController:
    
    def __init__(self, config):
        self.config = config
    
    def listar(self):
        try:
            proyectos = Proyecto.query.all()
            return jsonify([p.to_dict() for p in proyectos])
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error listando proyectos: {str(e)}")
            return jsonify({'error': 'Error interno'}), 500
    
    def obtener(self, id):
        try:
            proyecto = Proyecto.query.get_or_404(id)
            data = proyecto.to_dict()
            logger.info(f"Datos del proyecto: {data}")
            
            # Obtener métricas
            metrica = MetricaBase.query.filter_by(proyecto_id=id).first()
            if metrica:
                data['metrica_base'] = metrica.to_dict()
                logger.info(f"Métricas encontradas: {data['metrica_base']}")
            else:
                # Retornar estructura vacía si no hay métricas
                data['metrica_base'] = {
                    'proyecto_id': id,
                    'commits_totales': data.get('total_commits', 0),
                    'commits_mes': 0,
                    'commits_semana': 0,
                    'lineas_codigo': data.get('total_loc', 0),
                    'complejidad': 1.0,
                    'tiempo_promedio_commit': 0.0
                }
                logger.info(f"Sin métricas, usando valores por defecto: {data['metrica_base']}")
            
            # Obtener histórico
            historico = HistoricoCalculo.query.filter_by(proyecto_id=id).all()
            data['historico'] = [h.to_dict() for h in historico]
            logger.info(f"Histórico cargado: {len(data['historico'])} registros")
            
            logger.info(f"Respuesta completa: {data}")
            return jsonify(data)
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error obteniendo proyecto: {str(e)}")
            return jsonify({'error': 'Error interno'}), 500
    
    def crear(self):
        try:
            data = request.json
            if not data.get('nombre') or not data.get('url_github'):
                return jsonify({'error': 'Nombre y URL requeridos'}), 400
            
            existe = Proyecto.query.filter_by(nombre=data['nombre']).first()
            if existe:
                return jsonify({'error': 'Proyecto existe'}), 400
            
            proyecto = Proyecto(nombre=data['nombre'], url_github=data['url_github'], estado='pendiente')
            db.session.add(proyecto)
            db.session.commit()
            
            return jsonify(proyecto.to_dict()), 201
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error creando proyecto: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Error interno'}), 500
    
    def analizar(self, id):
        proyecto = None
        try:
            proyecto = Proyecto.query.get_or_404(id)
            proyecto.estado = 'procesando'
            db.session.commit()
            
            repos_dir = self.config['REPOS_DIR']
            proyecto_dir = os.path.join(repos_dir, str(proyecto.id))
            
            analyzer = GitHubAnalyzer(proyecto.url_github, self.config.get('GITHUB_TOKEN'))
            resultado = analyzer.analyze(proyecto_dir)
            
            if resultado['commits']:
                proyecto.total_commits = resultado['commits']['commits_totales']
                # Actualizar fechas del repositorio si están disponibles
                if resultado['commits'].get('fecha_creacion_repo'):
                    from datetime import datetime
                    proyecto.fecha_creacion = datetime.strptime(resultado['commits']['fecha_creacion_repo'], '%Y-%m-%d %H:%M:%S')
                if resultado['commits'].get('fecha_ultima_modificacion'):
                    from datetime import datetime
                    proyecto.fecha_actualizacion = datetime.strptime(resultado['commits']['fecha_ultima_modificacion'], '%Y-%m-%d %H:%M:%S')
            
            if resultado['loc']:
                proyecto.total_loc = resultado['loc']['total_lineas']
            
            proyecto.complejidad_ciclomatica = resultado['complejidad_ciclomatica']
            proyecto.estado = 'analizado'
            db.session.commit()
            
            metrica = MetricaBase(
                proyecto_id=proyecto.id,
                commits_totales=resultado['commits']['commits_totales'] if resultado['commits'] else 0,
                commits_mes=resultado['commits'].get('commits_mes', 0) if resultado['commits'] else 0,
                commits_semana=resultado['commits'].get('commits_semana', 0) if resultado['commits'] else 0,
                lineas_codigo=resultado['loc']['total_lineas'] if resultado['loc'] else 0,
                complejidad=resultado['complejidad_ciclomatica'],
                tiempo_promedio_commit=resultado['commits'].get('tiempo_promedio', 0) if resultado['commits'] else 0
            )
            
            # Guardar últimos commits
            if resultado['commits'] and resultado['commits'].get('ultimos_commits'):
                metrica.set_ultimos_commits(resultado['commits']['ultimos_commits'])
            
            db.session.add(metrica)
            db.session.commit()
            
            return jsonify({'mensaje': 'Análisis completado exitosamente', 'proyecto': proyecto.to_dict()}), 200
            
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB en análisis: {str(e)}")
            db.session.rollback()
            if proyecto:
                proyecto.estado = 'error'
                db.session.commit()
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error analizando proyecto {id}: {str(e)}")
            db.session.rollback()
            if proyecto:
                proyecto.estado = 'error'
                db.session.commit()
            return jsonify({'error': f'Error en análisis: {str(e)}'}), 500
    
    def eliminar(self, id):
        try:
            proyecto = Proyecto.query.get_or_404(id)
            repos_dir = self.config['REPOS_DIR']
            proyecto_dir = os.path.join(repos_dir, str(proyecto.id))
            
            # Intentar eliminar el directorio del proyecto
            if os.path.exists(proyecto_dir):
                try:
                    # En Windows, a veces los archivos Git quedan bloqueados
                    # Intenta cambiar permisos y luego eliminar
                    import stat
                    for root, dirs, files in os.walk(proyecto_dir, topdown=False):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                os.chmod(filepath, stat.S_IWRITE)
                                os.remove(filepath)
                            except Exception as e:
                                logger.warning(f"No se pudo eliminar {filepath}: {e}")
                        for dir in dirs:
                            dirpath = os.path.join(root, dir)
                            try:
                                os.chmod(dirpath, stat.S_IWRITE)
                                os.rmdir(dirpath)
                            except Exception as e:
                                logger.warning(f"No se pudo eliminar dir {dirpath}: {e}")
                    os.rmdir(proyecto_dir)
                except Exception as e:
                    logger.warning(f"Limpieza parcial de {proyecto_dir}: {e}")
            
            # Eliminar del BD aunque no se haya limpiado completamente
            db.session.delete(proyecto)
            db.session.commit()
            
            return jsonify({'mensaje': 'Proyecto eliminado'}), 200
        except exc.OperationalError as e:
            logger.error(f"Error de conexión DB: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Error temporal de conexión. Reintentar.'}), 503
        except Exception as e:
            logger.error(f"Error eliminando proyecto: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Error interno'}), 500
