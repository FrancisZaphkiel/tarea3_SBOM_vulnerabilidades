# SBOM y Análisis de Vulnerabilidades

## Descripción del Proyecto
El objetivo de este proyecto es generar un **SBOM** de las tecnologías (dependencias, librerías y componentes) de la organización **Checkly**. Se seleccionó esta organización debido a su alta actividad y volumen generoso de repositorios. 

El flujo de trabajo consiste en:
1.  **Filtrado:** Identificar repositorios con commits en el último mes.
2.  **Generación:** Crear los SBOMs de los repositorios activos.
3.  **Detección:** Analizar el código fuente y las dependencias en busca de vulnerabilidades (CVEs).
4.  **Evaluación:** Realizar un análisis cuantitativo en un Jupyter Notebook para categorizar hallazgos por severidad.

## Herramientas Utilizadas
* **Syft:** Generación de SBOM en formato JSON (CycloneDX).
* **Grype:** Escaneo de vulnerabilidades en las dependencias encontradas.
* **Trivy:** Análisis de seguridad integral (SAST y secretos) sobre el código fuente.
* **Pandas:** Procesamiento y limpieza de los datos extraídos.
* **Matplotlib / Seaborn:** Visualización de métricas de seguridad.

## Arquitectura del Proyecto
```text
.
├── compose.yml           # Orquestación del entorno (Docker)
├── Dockerfile            # Construcción de la imagen del proyecto
├── README.md             # Documentación principal
├── requirements.txt      # Dependencias del proyecto
├── extraction/           # Scripts para filtrar y clonar repositorios de GitHub
├── generation/           # Lógica de generación de SBOM con Syft
├── analysis/             # Scripts de escaneo con Grype/Trivy
└── notebook/             # Jupyter Notebook con el análisis cuantitativo
```

---

## Guía de Inicio Rápido (Docker)

Sigue estos pasos para poner en marcha el proyecto sin necesidad de instalar herramientas manualmente:

### 1. Requisitos previos
Tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).

### 2. Configurar credenciales
Crea un archivo llamado `.env` en la raíz del proyecto y añade tu token de GitHub para evitar límites de la API (es opcional):
```env
GITHUB_TOKEN=tu_token_aqui
```

### 3. Levantar el proyecto
Desde la terminal, en la carpeta del proyecto, ejecuta:
```bash
docker compose up --build
```
Este comando instalará automáticamente **Syft, Grype, Trivy** y todas las librerías necesarias.

### 4. Acceder al Análisis
Una vez que el comando termine de cargar, abre tu navegador en:
**[http://localhost:8888](http://localhost:8888)**

Desde ahí podrás abrir el archivo `notebook/analysis.ipynb` y ver los resultados gráficos.

---

## Ejecución Manual (Opcional)
En caso de preferir ejecutar los scripts uno por uno dentro del entorno Docker:
```bash
# Entrar al contenedor
docker exec -it sbom_analysis_app bash

# Ejecutar el flujo completo
python extraction/extract_repos.py   # Filtra y clona
python generation/generate_sbom.py   # Genera SBOM
python analysis/run_analysis.py      # Escanea vulnerabilidades
```