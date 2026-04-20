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
├── extraction/           # Scripts para filtrar y clonar repositorios de GitHub
├── generation/           # Lógica de generación de SBOM con Syft
├── analysis/             # Scripts de escaneo con Grype/Trivy
└── notebook/             # Jupyter Notebook con el análisis cuantitativo