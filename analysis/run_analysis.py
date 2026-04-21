import os
import subprocess

# Configuración
CLONE_DIR = 'cloned_repos'
SBOM_DIR = 'sboms'
RESULTS_DIR = 'analysis_results'

# Ejecuta Grype utilizando los SBOMs generados como entrada
def run_grype(sbom_dir, results_dir):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_sbom_dir = os.path.join(base_path, sbom_dir)
    full_results_dir = os.path.join(base_path, results_dir, 'grype')

    if not os.path.exists(full_sbom_dir):
        print(f"[ERROR] El directorio {full_sbom_dir} no existe.")
        return

    os.makedirs(full_results_dir, exist_ok=True)

    sboms = [f.name for f in os.scandir(full_sbom_dir) if f.is_file() and f.name.endswith('.json')]
    
    if not sboms:
        print("[ERROR] No se encontraron SBOMs para analizar. Por favor ejecuta la generación primero.")
        return

    print(f"\nIniciando análisis de dependencias (SCA) con Grype para {len(sboms)} SBOMs...")

    for sbom in sboms:
        sbom_path = os.path.join(full_sbom_dir, sbom)
        repo_name = sbom.replace('_sbom.json', '')
        result_path = os.path.join(full_results_dir, f"{repo_name}_grype.json")

        if os.path.exists(result_path):
            print(f"El reporte de Grype para {repo_name} ya existe. Omitiendo.")
            continue

        print(f"Analizando dependencias de {repo_name} con Grype...")
        try:
            # grype sbom:ruta_al_sbom -o json > ruta_resultado.json
            with open(result_path, 'w') as out_file:
                subprocess.run(['grype', f"sbom:{sbom_path}", '-o', 'json'], check=True, stdout=out_file, stderr=subprocess.DEVNULL)
            print(f"[OK] Reporte Grype generado: {repo_name}_grype.json")
        except subprocess.CalledProcessError:
            # Grype puede devolver un código de salida distinto de 0 en algunas configuraciones o si hay errores, pero se asume que el JSON se creó
            if os.path.exists(result_path) and os.path.getsize(result_path) > 0:
                print(f"[OK] Reporte Grype generado (con advertencias): {repo_name}_grype.json")
            else:
                print(f"[ERROR] Falló la ejecución de Grype en {repo_name}")
        except FileNotFoundError:
            print("[ERROR] El comando 'grype' no está instalado o no se encuentra en el PATH del sistema.")
            break

# Ejecuta Trivy sobre el código fuente clonado para realizar SAST y buscar secretos
def run_trivy(clone_dir, results_dir):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_clone_dir = os.path.join(base_path, clone_dir)
    full_results_dir = os.path.join(base_path, results_dir, 'trivy')

    if not os.path.exists(full_clone_dir):
        print(f"[ERROR] El directorio {full_clone_dir} no existe.")
        return

    os.makedirs(full_results_dir, exist_ok=True)

    repos = [f.name for f in os.scandir(full_clone_dir) if f.is_dir()]
    
    if not repos:
        print("[ERROR] No se encontraron repositorios para analizar.")
        return

    print(f"\nIniciando análisis estático y de secretos con Trivy para {len(repos)} repositorios...")

    for repo in repos:
        repo_path = os.path.join(full_clone_dir, repo)
        result_path = os.path.join(full_results_dir, f"{repo}_trivy.json")

        if os.path.exists(result_path):
            print(f"El reporte de Trivy para {repo} ya existe. Omitiendo.")
            continue

        print(f"Ejecutando Trivy en {repo}...")
        try:
            cmd = ['trivy', 'fs', '--scanners', 'vuln,secret', '-f', 'json', '-o', result_path, repo_path]
            # Se usa check=False porque trivy puede devolver un código no nulo si encuentra vulnerabilidades críticas
            subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(result_path) and os.path.getsize(result_path) > 0:
                print(f"[OK] Reporte Trivy generado: {repo}_trivy.json")
            else:
                print(f"[ERROR] No se generó reporte Trivy para {repo}.")
        except FileNotFoundError:
            print("[ERROR] El comando 'trivy' no está instalado o no se encuentra en el PATH del sistema.")
            break

if __name__ == "__main__":
    run_grype(SBOM_DIR, RESULTS_DIR)
    run_trivy(CLONE_DIR, RESULTS_DIR)
    print("\nProceso de análisis de vulnerabilidades completado.")
