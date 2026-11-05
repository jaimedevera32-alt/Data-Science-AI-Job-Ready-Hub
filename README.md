# 🚀 Data-Science-AI-Job-Ready-Hub
> **Plataforma de entrenamiento interactivo diario (1h/día) & Hub de Especialización Técnica**
> *De los fundamentos del Máster UCM (Data Science, Big Data & Business Analytics) al dominio de Agentes de IA y Retos Técnicos de Selección.*

---

## 🎯 Visión y Objetivos

Este repositorio no es un simple archivador de apuntes: es un **entorno de entrenamiento práctico y continuo** diseñado para preparar perfiles de alto nivel en **Data Science, Data Engineering, MLOps e Inteligencia Artificial Generativa / Agentes**.

### Metodología de 1 Hora al Día (1h/day)
Cada día se divide en una rutina de 60 minutos enfocada en resolución activa de problemas:
```
┌─────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐
│  15 min: TEORÍA │  ──►  │   35 min: CODING KATA  │  ──►  │  10 min: AI INTERVIEW  │
│ Flash conceptual│       │ Reto técnico + pytest  │       │ Simulación con Agente  │
└─────────────────┘       └────────────────────────┘       └────────────────────────┘
```

1. **Minutos 0 - 15 (Flash Conceptual):** Revisión de la base matemática, algorítmica o arquitectónica.
2. **Minutos 15 - 50 (Coding Challenge):** Implementación de código en Python/SQL/Spark/Agentes con validación mediante tests unitarios (`pytest`).
3. **Minutos 50 - 60 (Simulación de Entrevista):** Revisión de complejidad (Big O), casos borde, escalabilidad a producción y preguntas típicas de selección técnica.

---

## 🗺️ Estructura del Repositorio

El repositorio se divide en dos grandes ejes:

### 1. 🎓 Módulos del Máster UCM (`Curriculum Base`)
Los 17 módulos formativos organizados con sus notebooks, scripts, presentaciones y ejercicios prácticos:
* **Python (Básica y Avanzada):** POO, programación funcional, decoradores, generadores y buenas prácticas.
* **Bases de Datos (SQL y NoSQL):** Modelado relacional, consultas analíticas avanzadas, MongoDB, Cassandra, Snowflake.
* **Business Intelligence & Visualización:** Tableau, visualización científica, dashboards de impacto de negocio.
* **Estadística & Modelización Predictiva:** Inferencia, contrastes de hipótesis, regresión lineal y logística, series temporales.
* **Machine Learning & Deep Learning:** Árboles, ensambles (XGBoost, LightGBM), redes neuronales, Computer Vision y NLP.
* **Big Data & Cloud:** Apache Spark (PySpark), arquitecturas distribuidas, Hadoop, GCP/AWS.
* **Text Mining & Redes Sociales:** Extracción de información, embeddings, grafos y análisis de comunidades.
* **TFM:** Proyecto final integrador.

### 2. ⚡ Plataforma de Entrenamiento Diario (`daily_training/`)
Ubicada en [`daily_training/`](file:///c:/Users/jaime/Desktop/UCM%20-%20Data%20Science%2C%20Big%20Data%20%26%20Business%20Analytics/daily_training), contiene los 5 tracks de preparación para procesos de selección:

| Track | Foco Principal | Tecnologías & Competencias |
| :--- | :--- | :--- |
| **01. Python & Algos** | Algoritmia para Data & Optimización | Vectorización NumPy/Pandas, Big-O, estructuras de datos |
| **02. SQL Mastery** | Analítica de Negocio & Data Warehousing | CTEs recursivas, Window functions, DuckDB, PostgreSQL |
| **03. Data Engineering** | Pipelines Escalables & Big Data | PySpark, optimización de joins, salting, streaming vs batch |
| **04. ML & MLOps** | Modelos en Producción | Feature pipelines, validación sin fuga (data leakage), FastAPI |
| **05. AI Agents & Skills** | **Track Diferenciador 2025/2026** | Patrones ReAct, Tool Calling, MCP, RAG avanzado, Evals |

---

## 🛠️ Cómo Iniciar el Entrenamiento Diario

### 1. Requisitos Previos
Clona el repositorio e instala las dependencias de la plataforma de retos:
```bash
git clone https://github.com/jaimedevera32-alt/Data-Science-AI-Job-Ready-Hub.git
cd Data-Science-AI-Job-Ready-Hub
pip install -r daily_training/requirements.txt
```

### 2. Lanzar la Plataforma Interactiva
Ejecuta el asistente de retos diarios:
```bash
python daily_training/runner.py
```

Podrás seleccionar el track a entrenar, ver el enunciado del reto, iniciar el cronómetro de 60 minutos y correr los tests automáticos:
```bash
# Ejemplo: ejecutar tests del reto del día en Python
pytest daily_training/tracks/01_python_algos/day_01_vectorization_pandas/test_challenge.py
```

---

## 📦 Gestión de Datos y Datasets Pesados

Para optimizar el tamaño del repositorio y cumplir con los límites de GitHub (<100MB por archivo):
* Los datasets de gran tamaño (>100MB) y podcasts de audio se conservan en local y están listados en [DATASETS_README.md](file:///c:/Users/jaime/Desktop/UCM%20-%20Data%20Science%2C%20Big%20Data%20%26%20Business%20Analytics/DATASETS_README.md).
* Los retos de la plataforma utilizan datos sintéticos o bases de datos ligeras en memoria ([DuckDB](https://duckdb.org/)) para que cualquier desarrollador pueda ejecutarlos al instante tras clonar el repositorio.

---

## 👤 Autor
* **Jaime de Vera** - [GitHub](https://github.com/jaimedevera32-alt)

