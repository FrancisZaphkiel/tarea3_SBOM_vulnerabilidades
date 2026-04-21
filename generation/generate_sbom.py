import os
import subprocess

# Configuración
CLONE_DIR = 'cloned_repos'
SBOM_DIR = 'sboms'

# Genera SBOMs utilizando Syft para cada repositorio clonado en formato CycloneDX JSON.
def generate_sboms(clone_dir, sbom_dir):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_clone_dir = os.path.join(base_path, clone_dir)
    full_sbom_dir = os.path.join(base_path, sbom_dir)

    if not os.path.exists(full_clone_dir):
        print(f"[ERROR] El directorio {full_clone_dir} no existe. Por favor ejecuta la extracción primero.")
        return

    if not os.path.exists(full_sbom_dir):
        os.makedirs(full_sbom_dir)

    # Listar directorios de repositorios
    repos = [f.name for f in os.scandir(full_clone_dir) if f.is_dir()]
    
    if not repos:
        print("[ERROR] No se encontraron repositorios clonados.")
        return

    print(f"Se generarán SBOMs para {len(repos)} repositorios...")

    for repo in repos:
        repo_path = os.path.join(full_clone_dir, repo)
        sbom_path = os.path.join(full_sbom_dir, f"{repo}_sbom.json")

        if os.path.exists(sbom_path):
            print(f"El SBOM para {repo} ya existe. Omitiendo.")
            continue

        print(f"Generando SBOM para {repo}...")
        try:
            # Ejecutar syft para generar el SBOM
            cmd = ['syft', f"dir:{repo_path}", '-o', f"cyclonedx-json={sbom_path}"]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[OK] SBOM generado: {repo}_sbom.json")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Error al generar SBOM para {repo}: {e}")
        except FileNotFoundError:
            print("[ERROR] El comando 'syft' no está instalado o no se encuentra en el PATH del sistema.")
            break

if __name__ == "__main__":
    generate_sboms(CLONE_DIR, SBOM_DIR)
    print("\nProceso de generación de SBOM completado.")
