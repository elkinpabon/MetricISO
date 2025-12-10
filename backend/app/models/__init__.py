from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    url_github = db.Column(db.String(512), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = db.Column(db.String(50), default='pendiente')
    
    total_commits = db.Column(db.Integer, default=0)
    total_loc = db.Column(db.Integer, default=0)
    complejidad_ciclomatica = db.Column(db.Float, default=0.0)
    
    metricas = db.relationship('MetricaBase', backref='proyecto', lazy=True, cascade='all, delete-orphan')
    historico = db.relationship('HistoricoCalculo', backref='proyecto', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'url_github': self.url_github,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat(),
            'estado': self.estado,
            'total_commits': self.total_commits,
            'total_loc': self.total_loc,
            'complejidad_ciclomatica': self.complejidad_ciclomatica
        }

class MetricaBase(db.Model):
    __tablename__ = 'metricas_base'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    
    commits_totales = db.Column(db.Integer, default=0)
    commits_mes = db.Column(db.Integer, default=0)
    commits_semana = db.Column(db.Integer, default=0)
    
    lineas_codigo = db.Column(db.Integer, default=0)
    lineas_comentarios = db.Column(db.Integer, default=0)
    complejidad = db.Column(db.Float, default=0.0)
    
    tiempo_promedio_commit = db.Column(db.Float, default=0.0)
    
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'commits_totales': self.commits_totales,
            'commits_mes': self.commits_mes,
            'commits_semana': self.commits_semana,
            'lineas_codigo': self.lineas_codigo,
            'lineas_comentarios': self.lineas_comentarios,
            'complejidad': self.complejidad,
            'tiempo_promedio_commit': self.tiempo_promedio_commit,
            'fecha_calculo': self.fecha_calculo.isoformat()
        }

class HistoricoCalculo(db.Model):
    __tablename__ = 'historico_calculos'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    
    formula = db.Column(db.String(50), nullable=False)
    datos_entrada = db.Column(db.Text)
    resultado = db.Column(db.Float)
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_datos_entrada(self, datos):
        self.datos_entrada = json.dumps(datos)
    
    def get_datos_entrada(self):
        if self.datos_entrada:
            return json.loads(self.datos_entrada)
        return {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'formula': self.formula,
            'datos_entrada': self.get_datos_entrada(),
            'resultado': self.resultado,
            'fecha_calculo': self.fecha_calculo.isoformat()
        }

class FormulaISO(db.Model):
    __tablename__ = 'formulas_iso'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    formula = db.Column(db.String(512), nullable=False)
    parametros = db.Column(db.Text)
    unidad = db.Column(db.String(50))
    
    def set_parametros(self, params):
        self.parametros = json.dumps(params)
    
    def get_parametros(self):
        if self.parametros:
            return json.loads(self.parametros)
        return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'formula': self.formula,
            'parametros': self.get_parametros(),
            'unidad': self.unidad
        }
