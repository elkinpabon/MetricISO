from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

db = SQLAlchemy()

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)
    url_github = db.Column(db.String(512), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    estado = db.Column(db.String(50), default='pendiente')
    
    total_commits = db.Column(db.Integer, default=0)
    total_loc = db.Column(db.Integer, default=0)
    complejidad_ciclomatica = db.Column(db.Float, default=0.0)
    
    metricas = db.relationship('MetricaBase', backref='proyecto', lazy=True, cascade='all, delete-orphan')
    historico = db.relationship('HistoricoCalculo', backref='proyecto', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        # Formatear fechas como strings legibles
        fecha_creacion = self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None
        fecha_actualizacion = self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_actualizacion else None
        return {
            'id': self.id,
            'nombre': self.nombre,
            'url_github': self.url_github,
            'fecha_creacion': fecha_creacion,
            'fecha_actualizacion': fecha_actualizacion,
            'estado': self.estado,
            'total_commits': self.total_commits,
            'total_loc': self.total_loc,
            'complejidad_ciclomatica': round(self.complejidad_ciclomatica, 2) if self.complejidad_ciclomatica else 0
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
    ultimos_commits = db.Column(db.Text, default='[]')  # Almacenar como JSON string
    
    fecha_calculo = db.Column(db.DateTime, server_default=db.func.now())
    
    def set_ultimos_commits(self, commits_list):
        """Almacena la lista de últimos commits como JSON"""
        self.ultimos_commits = json.dumps(commits_list)
    
    def get_ultimos_commits(self):
        """Recupera la lista de últimos commits desde JSON"""
        if self.ultimos_commits:
            return json.loads(self.ultimos_commits)
        return []
    
    def to_dict(self):
        # Formatear fecha como string legible
        fecha_calculo = self.fecha_calculo.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_calculo else None
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'commits_totales': self.commits_totales,
            'commits_mes': self.commits_mes,
            'commits_semana': self.commits_semana,
            'lineas_codigo': self.lineas_codigo,
            'lineas_comentarios': self.lineas_comentarios,
            'complejidad': round(self.complejidad, 2) if self.complejidad else 0,
            'tiempo_promedio_commit': round(self.tiempo_promedio_commit, 2) if self.tiempo_promedio_commit else 0,
            'ultimos_commits': self.get_ultimos_commits(),
            'fecha_calculo': fecha_calculo
        }

class HistoricoCalculo(db.Model):
    __tablename__ = 'historico_calculos'
    
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    
    formula = db.Column(db.String(50), nullable=False)
    datos_entrada = db.Column(db.Text)
    resultado = db.Column(db.Float)
    interpretacion_json = db.Column(db.Text)
    fecha_calculo = db.Column(db.DateTime, server_default=db.func.now())
    
    def set_datos_entrada(self, datos):
        self.datos_entrada = json.dumps(datos)
    
    def get_datos_entrada(self):
        if self.datos_entrada:
            return json.loads(self.datos_entrada)
        return {}
    
    def set_interpretacion(self, interp):
        self.interpretacion_json = json.dumps(interp)
    
    def get_interpretacion(self):
        if self.interpretacion_json:
            return json.loads(self.interpretacion_json)
        return {}
    
    def to_dict(self):
        # Formatear fecha como string legible
        fecha_calculo = self.fecha_calculo.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_calculo else None
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'formula': self.formula,
            'datos_entrada': self.get_datos_entrada(),
            'resultado': self.resultado,
            'interpretacion': self.get_interpretacion(),
            'fecha_calculo': fecha_calculo
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
    tipo = db.Column(db.String(100), default='General')
    norma_iso = db.Column(db.String(100), default='ISO/IEC 9126')
    
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
            'unidad': self.unidad,
            'tipo': self.tipo,
            'norma_iso': self.norma_iso
        }

class ReferenciaNorma(db.Model):
    """Tabla de referencia con parámetros buenos, malos y aceptables por fórmula"""
    __tablename__ = 'referencias_normas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_formula = db.Column(db.String(50), nullable=False)
    nombre_formula = db.Column(db.String(255), nullable=False)
    norma_iso = db.Column(db.String(100), nullable=False)
    
    # Valores de referencia
    valor_excelente = db.Column(db.Float)  # Verde
    valor_bueno = db.Column(db.Float)      # Verde claro
    valor_aceptable = db.Column(db.Float)  # Amarillo
    valor_malo = db.Column(db.Float)       # Naranja
    valor_critico = db.Column(db.Float)    # Rojo
    
    descripcion_excelente = db.Column(db.String(255))
    descripcion_bueno = db.Column(db.String(255))
    descripcion_aceptable = db.Column(db.String(255))
    descripcion_malo = db.Column(db.String(255))
    descripcion_critico = db.Column(db.String(255))
    
    interpretacion = db.Column(db.Text)  # Guía de interpretación
    
    def to_dict(self):
        # Construir rangos en función de los valores disponibles
        # Los valores están en orden: excelente >= bueno >= aceptable >= malo >= critico
        # Esto significa que cada nivel define el mínimo para estar en ese nivel
        rangos = {}
        
        # Excelente: desde valor_excelente en adelante
        if self.valor_excelente is not None:
            rangos['excelente'] = {
                'min': self.valor_excelente,
                'max': None,
                'descripcion': self.descripcion_excelente,
                'color': '#00AA00'
            }
        
        # Bueno: desde valor_bueno hasta valor_excelente
        if self.valor_bueno is not None:
            rangos['bueno'] = {
                'min': self.valor_bueno,
                'max': self.valor_excelente,
                'descripcion': self.descripcion_bueno,
                'color': '#88DD00'
            }
        
        # Aceptable: desde valor_aceptable hasta valor_bueno
        if self.valor_aceptable is not None:
            rangos['aceptable'] = {
                'min': self.valor_aceptable,
                'max': self.valor_bueno,
                'descripcion': self.descripcion_aceptable,
                'color': '#FFDD00'
            }
        
        # Malo: desde valor_malo hasta valor_aceptable
        if self.valor_malo is not None:
            rangos['malo'] = {
                'min': self.valor_malo,
                'max': self.valor_aceptable,
                'descripcion': self.descripcion_malo,
                'color': '#FF8800'
            }
        
        # Crítico: desde 0 hasta valor_malo
        if self.valor_critico is not None:
            rangos['critico'] = {
                'min': self.valor_critico,
                'max': self.valor_malo,
                'descripcion': self.descripcion_critico,
                'color': '#DD0000'
            }
        
        return {
            'id': self.id,
            'codigo_formula': self.codigo_formula,
            'nombre_formula': self.nombre_formula,
            'norma_iso': self.norma_iso,
            'rangos': rangos,
            'interpretacion': self.interpretacion
        }
