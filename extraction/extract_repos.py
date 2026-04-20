import os
import requests
import subprocess
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

# Configuración
ORG_NAME = 'checkly'
GITHUB_API_URL = 'https://api.github.com'
CLONE_DIR = 'cloned_repos'
DAYS_LIMIT = 30

# Obtiene repositorios de la organización que han recibido commits en los últimos 'days_limit' días.
def get_recent_repos(org, days_limit):
    date_limit = datetime.now(timezone.utc) - timedelta(days=days_limit)
    date_str = date_limit.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    print(f"Buscando repositorios de '{org}' con actividad desde {date_str}...")
    
    repos = []
    page = 1
    per_page = 100
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Si hay un token en las variables de entorno, usarlo para evitar límites de API
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'token {github_token}'

    while True:
        url = f"{GITHUB_API_URL}/orgs/{org}/repos?sort=pushed&direction=desc&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error al obtener repositorios: {response.status_code}")
            if response.status_code == 403:
                print("Posible límite de tasa (rate limit) de la API de GitHub superado. Considera configurar la variable de entorno GITHUB_TOKEN.")
            break
            
        page_repos = response.json()
        if not page_repos:
            break
            
        for repo in page_repos:
            pushed_at_str = repo.get('pushed_at')
            if not pushed_at_str:
                continue
                
            pushed_at = datetime.strptime(pushed_at_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            if pushed_at >= date_limit:
                repos.append(repo)
            else:
                # Como están ordenados por fecha de push descendente, si encontramos uno más antiguo, podemos detenernos
                return repos
                
        page += 1
        
    return repos

# Clona una lista de repositorios en el directorio destino.
def clone_repositories(repos, target_dir):
    # Usar ruta absoluta basada en el directorio del script, ubicándolo en la raíz del proyecto
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_target_dir = os.path.join(base_path, target_dir)

    if not os.path.exists(full_target_dir):
        os.makedirs(full_target_dir)
        
    print(f"\nSe encontraron {len(repos)} repositorios para clonar en '{full_target_dir}'.")
    
    for repo in repos:
        repo_name = repo['name']
        clone_url = repo['clone_url']
        repo_path = os.path.join(full_target_dir, repo_name)
        
        if os.path.exists(repo_path):
            print(f"El repositorio {repo_name} ya existe en {repo_path}. Omitiendo clonación.")
            continue
            
        print(f"Clonando {repo_name}...")
        try:
            # Usar subprocess.run para ejecutar git clone
            subprocess.run(['git', 'clone', clone_url, repo_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[OK] {repo_name} clonado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Error al clonar {repo_name}: {e}")

if __name__ == "__main__":
    recent_repos = get_recent_repos(ORG_NAME, DAYS_LIMIT)
    
    if recent_repos:
        clone_repositories(recent_repos, CLONE_DIR)
        print("\n¡Proceso de extracción completado!")
    else:
        print("\nNo se encontraron repositorios con actividad reciente.")
