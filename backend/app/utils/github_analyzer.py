import os
import subprocess
import re
from datetime import datetime, timedelta
from git import Repo
import requests

class GitHubAnalyzer:
    """Analiza repositorios GitHub"""
    
    def __init__(self, repo_url, token=None):
        self.repo_url = repo_url
        self.token = token
        self.local_path = None
        self.repo = None
    
    def extract_repo_info(self):
        if 'github.com/' in self.repo_url:
            parts = self.repo_url.split('github.com/')[-1].replace('.git', '').split('/')
            return {'owner': parts[0], 'name': parts[1] if len(parts) > 1 else ''}
        return None
    
    def clone_repository(self, target_dir):
        try:
            self.local_path = target_dir
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            # Clonar SIN depth para obtener todo el historial
            Repo.clone_from(self.repo_url, target_dir)
            self.repo = Repo(target_dir)
            print(f"Repositorio clonado en: {target_dir}")
            return True
        except Exception as e:
            print(f"Error clonando: {e}")
            return False
    
    def analyze_commits(self):
        if not self.repo:
            return None
        try:
            commits = list(self.repo.iter_commits())
            total = len(commits)
            print(f"Total commits encontrados: {total}")
            
            now = datetime.now()
            
            week_ago = now - timedelta(days=7)
            commits_week = sum(1 for c in commits if datetime.fromtimestamp(c.committed_date) > week_ago)
            
            month_ago = now - timedelta(days=30)
            commits_mes = sum(1 for c in commits if datetime.fromtimestamp(c.committed_date) > month_ago)
            
            # Calcular tiempo promedio entre commits
            if len(commits) > 1:
                fechas = sorted([datetime.fromtimestamp(c.committed_date) for c in commits])
                tiempos = [(fechas[i+1] - fechas[i]).total_seconds() / 3600 for i in range(len(fechas)-1)]
                tiempo_promedio = sum(tiempos) / len(tiempos)
            else:
                tiempo_promedio = 0.0
            
            # Extraer fechas del repositorio
            # Fecha de creación = primer commit (el más antiguo)
            # Fecha de última modificación = último commit (el más reciente)
            fecha_creacion_repo = None
            fecha_ultima_modificacion = None
            
            if commits:
                # Ordenar commits por fecha
                commits_sorted = sorted(commits, key=lambda c: c.committed_date)
                # Primer commit (más antiguo)
                fecha_creacion_repo = datetime.fromtimestamp(commits_sorted[0].committed_date).strftime('%Y-%m-%d %H:%M:%S')
                # Último commit (más reciente)
                fecha_ultima_modificacion = datetime.fromtimestamp(commits_sorted[-1].committed_date).strftime('%Y-%m-%d %H:%M:%S')
            
            # Extraer últimos 10 commits
            ultimos_commits = []
            for i, commit in enumerate(commits[:10]):
                ultimos_commits.append({
                    'hash': commit.hexsha[:8],
                    'author': commit.author.name if commit.author else 'Unknown',
                    'message': commit.message.strip()[:100],  # Primeros 100 caracteres
                    'fecha': datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
                })
            
            print(f"Commits semana: {commits_week}, mes: {commits_mes}, promedio: {tiempo_promedio:.2f}h")
            print(f"Primer commit: {fecha_creacion_repo}")
            print(f"Último commit: {fecha_ultima_modificacion}")
            
            return {
                'commits_totales': total,
                'commits_semana': commits_week,
                'commits_mes': commits_mes,
                'tiempo_promedio': tiempo_promedio,
                'ultimos_commits': ultimos_commits,
                'fecha_creacion_repo': fecha_creacion_repo,
                'fecha_ultima_modificacion': fecha_ultima_modificacion
            }
        except Exception as e:
            print(f"Error en commits: {e}")
            return None
    
    def count_loc(self):
        if not self.local_path:
            return None
        try:
            total_lines = 0
            file_count = 0
            extensions = {'.py', '.js', '.java', '.cpp', '.c', '.ts', '.jsx', '.tsx', '.go', '.rs'}
            
            for root, dirs, files in os.walk(self.local_path):
                # Ignorar carpetas .git y node_modules
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__', 'dist', 'build'}]
                
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = len(f.readlines())
                                total_lines += lines
                                file_count += 1
                        except:
                            pass
            
            print(f"LOC encontradas: {total_lines} en {file_count} archivos")
            return {'total_lineas': total_lines, 'archivos': file_count}
        except Exception as e:
            print(f"Error contando LOC: {e}")
            return {'total_lineas': 0, 'archivos': 0}
    
    def calculate_cyclomatic_complexity(self):
        """Calcula complejidad ciclomática por función/método"""
        if not self.local_path:
            return 1.0
        try:
            import re
            
            complexities = []
            
            for root, dirs, files in os.walk(self.local_path):
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__', 'dist', 'build'}]
                
                for file in files:
                    if file.endswith('.py'):
                        self._analyze_python_file(os.path.join(root, file), complexities)
                    elif file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                        self._analyze_js_file(os.path.join(root, file), complexities)
                    elif file.endswith('.java'):
                        self._analyze_java_file(os.path.join(root, file), complexities)
            
            avg_complexity = sum(complexities) / len(complexities) if complexities else 1.0
            print(f"Complejidad ciclomática promedio: {avg_complexity:.2f}")
            return avg_complexity
        except Exception as e:
            print(f"Error calculando complejidad: {e}")
            return 1.0
    
    def _analyze_python_file(self, filepath, complexities):
        """Analiza complejidad ciclomática en archivos Python"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            current_complexity = 1
            in_function = False
            indent_level = 0
            
            for line in lines:
                stripped = line.lstrip()
                current_indent = len(line) - len(stripped)
                
                # Detectar definición de función
                if stripped.startswith('def '):
                    if in_function and current_complexity > 1:
                        complexities.append(current_complexity)
                    current_complexity = 1
                    in_function = True
                    indent_level = current_indent
                
                # Contar puntos de decisión dentro de la función
                if in_function and current_indent > indent_level:
                    decision_keywords = ['if ', 'elif ', 'for ', 'while ', 'try:', 'except', 'and ', 'or ']
                    for keyword in decision_keywords:
                        if keyword in stripped:
                            current_complexity += 1
                
                # Detectar fin de función (siguiente función o fin de indentación)
                if in_function and stripped and not stripped.startswith('#') and current_indent == indent_level and not stripped.startswith('def'):
                    if current_complexity > 1:
                        complexities.append(current_complexity)
                    in_function = False
            
            # Registrar última función
            if in_function and current_complexity > 1:
                complexities.append(current_complexity)
        except:
            pass
    
    def _analyze_js_file(self, filepath, complexities):
        """Analiza complejidad ciclomática en archivos JavaScript/TypeScript"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Contar funciones
            function_pattern = r'function\s+\w+|=>\s*\{|function\s*\('
            functions = len(re.findall(function_pattern, content))
            
            if functions > 0:
                # Contar puntos de decisión
                decision_count = len(re.findall(r'\bif\b|\belse\b|\bswitch\b|\bcase\b|\bfor\b|\bwhile\b|\bcatch\b|\btry\b|\b\|\|\b|\b&&\b|\?\s*:', content))
                avg_complexity_per_function = 1 + (decision_count / functions)
                complexities.append(avg_complexity_per_function)
        except:
            pass
    
    def _analyze_java_file(self, filepath, complexities):
        """Analiza complejidad ciclomática en archivos Java"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Contar métodos
            method_pattern = r'(public|private|protected)?\s+\w+\s+\w+\s*\('
            methods = len(re.findall(method_pattern, content))
            
            if methods > 0:
                # Contar puntos de decisión
                decision_count = len(re.findall(r'\bif\b|\belse\b|\bswitch\b|\bcase\b|\bfor\b|\bwhile\b|\bcatch\b|\btry\b|\b\|\|\b|\b&&\b|\?', content))
                avg_complexity_per_method = 1 + (decision_count / methods)
                complexities.append(avg_complexity_per_method)
        except:
            pass

    
    
    def analyze(self, target_dir):
        """Ejecuta análisis completo del repositorio"""
        try:
            print(f"Iniciando análisis de: {self.repo_url}")
            
            if not self.clone_repository(target_dir):
                return {
                    'commits': None,
                    'loc': None,
                    'complejidad_ciclomatica': 0
                }
            
            commits = self.analyze_commits()
            loc = self.count_loc()
            complexity = self.calculate_cyclomatic_complexity()
            
            return {
                'commits': commits,
                'loc': loc,
                'complejidad_ciclomatica': complexity
            }
        except Exception as e:
            print(f"Error en análisis: {e}")
            return {
                'commits': None,
                'loc': None,
                'complejidad_ciclomatica': 0
            }
