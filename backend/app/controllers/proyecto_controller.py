from flask import request, jsonify
from ..models import db, Proyecto, MetricaBase, HistoricoCalculo
from ..utils.github_analyzer import GitHubAnalyzer
import os
import shutil

class ProyectoController:
    
    def __init__(self, config):
        self.config = config
    
    def listar(self):
        proyectos = Proyecto.query.all()
        return jsonify([p.to_dict() for p in proyectos])
    
    def obtener(self, id):
        proyecto = Proyecto.query.get_or_404(id)
        data = proyecto.to_dict()
        metrica = MetricaBase.query.filter_by(proyecto_id=id).first()
        if metrica:
            data['metrica_base'] = metrica.to_dict()
        historico = HistoricoCalculo.query.filter_by(proyecto_id=id).all()
        data['historico'] = [h.to_dict() for h in historico]
        return jsonify(data)
    
    def crear(self):
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
    
    def analizar(self, id):
        proyecto = Proyecto.query.get_or_404(id)
        proyecto.estado = 'procesando'
        db.session.commit()
        
        try:
            repos_dir = self.config['REPOS_DIR']
            proyecto_dir = os.path.join(repos_dir, str(proyecto.id))
            
            analyzer = GitHubAnalyzer(proyecto.url_github, self.config.get('GITHUB_TOKEN'))
            resultado = analyzer.analyze(proyecto_dir)
            
            if resultado['commits']:
                proyecto.total_commits = resultado['commits']['total_commits']
            if resultado['loc']:
                proyecto.total_loc = resultado['loc']['total_lineas']
            
            proyecto.complejidad_ciclomatica = resultado['complejidad_ciclomatica']
            proyecto.estado = 'completado'
            db.session.commit()
            
            metrica = MetricaBase(
                proyecto_id=proyecto.id,
                commits_totales=resultado['commits']['total_commits'] if resultado['commits'] else 0,
                commits_mes=resultado['commits']['commits_mes'] if resultado['commits'] else 0,
                commits_semana=resultado['commits']['commits_semana'] if resultado['commits'] else 0,
                lineas_codigo=resultado['loc']['total_lineas'] if resultado['loc'] else 0,
                complejidad=resultado['complejidad_ciclomatica']
            )
            db.session.add(metrica)
            db.session.commit()
            
            return jsonify({'mensaje': 'Análisis completado', 'proyecto': proyecto.to_dict(), 'metrica': metrica.to_dict()})
        
        except Exception as e:
            proyecto.estado = 'error'
            db.session.commit()
            return jsonify({'error': str(e)}), 500
    
    def eliminar(self, id):
        proyecto = Proyecto.query.get_or_404(id)
        repos_dir = self.config['REPOS_DIR']
        proyecto_dir = os.path.join(repos_dir, str(proyecto.id))
        if os.path.exists(proyecto_dir):
            shutil.rmtree(proyecto_dir)
        
        db.session.delete(proyecto)
        db.session.commit()
        
        return jsonify({'mensaje': 'Eliminado'}), 200
