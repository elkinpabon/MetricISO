import os
import subprocess
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
            Repo.clone_from(self.repo_url, target_dir, depth=1)
            self.repo = Repo(target_dir)
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
            now = datetime.now()
            
            week_ago = now - timedelta(days=7)
            commits_week = sum(1 for c in commits if datetime.fromtimestamp(c.committed_date) > week_ago)
            
            month_ago = now - timedelta(days=30)
            commits_month = sum(1 for c in commits if datetime.fromtimestamp(c.committed_date) > month_ago)
            
            return {
                'total_commits': total,
                'commits_semana': commits_week,
                'commits_mes': commits_month
            }
        except Exception as e:
            print(f"Error en commits: {e}")
            return None
    
    def count_loc(self):
        if not self.local_path:
            return None
        try:
            result = subprocess.run(
                f'(Get-ChildItem -Path "{self.local_path}" -Include *.py,*.js,*.java,*.cpp,*.c -Recurse | Measure-Object -Line).Lines',
                shell=True, capture_output=True, text=True
            )
            total_lines = int(result.stdout.strip()) if result.stdout.strip() else 0
            return {'total_lineas': total_lines, 'archivos': 0}
        except:
            return {'total_lineas': 0, 'archivos': 0}
    
    def calculate_cyclomatic_complexity(self):
        if not self.local_path:
            return 0
        try:
            result = subprocess.run(
                f'(Select-String -Path "{self.local_path}/*.py", "{self.local_path}/*.js" -Pattern "if|for|while|switch|case|catch" -Recurse | Measure-Object).Count',
                shell=True, capture_output=True, text=True
            )
            complexity = int(result.stdout.strip()) if result.stdout.strip() else 0
            return complexity / 100 + 1
        except:
            return 0
    
    def analyze(self, target_dir):
        self.clone_repository(target_dir)
        
        commits_data = self.analyze_commits()
        loc_data = self.count_loc()
        complexity = self.calculate_cyclomatic_complexity()
        
        return {
            'commits': commits_data,
            'loc': loc_data,
            'complejidad_ciclomatica': complexity
        }
