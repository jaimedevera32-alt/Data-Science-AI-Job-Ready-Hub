# 📦 Guía de Datasets Pesados (>100 MB)

Para mantener el repositorio dentro de los límites estrictos de GitHub (<100 MB por archivo y <1-2 GB total) y permitir clones rápidos, los siguientes archivos pesados se mantienen **únicamente en tu almacenamiento local** y están excluidos del control de versiones mediante `.gitignore`.

> [!NOTE]
> **Tus archivos locales están 100% seguros e intactos en tu disco.** Git simplemente no los sube a GitHub para evitar errores de subida.

---

## Detalle de Datasets Excluidos

| Módulo / Asignatura | Archivo | Tamaño Original | Fuente / Origen |
| :--- | :--- | :--- | :--- |
| **Open Data** (Carlos Ortega) | `datamarket_productos_de_supermercados_v2.csv` | ~2.36 GB | Datamarket Supermercados España |
| **Spark** (Pablo Villacorta) | `yellow_tripdata_2015-01.zip` | ~484.7 MB | NYC Taxi & Limousine Commission (TLC) Trip Data |
| **Spark** (Pablo Villacorta) | `flights-jan-apr-2018.csv` | ~311.5 MB | Bureau of Transportation Statistics (BTS) Flight Delays |
| **Visualización avanzada** (Pedro Concejero) | `data.csv` | ~234.3 MB | Dataset de visualización de eventos / series temporales |
| **Open Data** (Carlos Ortega) | `LosAngeles_Crime_Data_from_2020_to_Present.csv` | ~169.3 MB | Data.gov / City of Los Angeles Open Data Portal |

---

## 🎧 Podcasts y Archivos de Audio

En las carpetas del Máster existen 34 archivos de audio (`.m4a`, ~1.18 GB en total) que corresponden a podcasts explicativos de los temas.
* Para no saturar el límite de GitHub ni agotar cuotas de ancho de banda de Git LFS, se mantienen en local.
* En la plataforma de entrenamiento (`daily_training/`), los conceptos clave de estos audios se integran en formato de tarjetas de estudio (*flashcards*) y resúmenes conceptuales en Markdown.

---

## 💡 Cómo trabajar en local

1. Si estás trabajando directamente en tu máquina local, los archivos ya están en sus respectivas carpetas y tus notebooks los leerán sin ninguna modificación.
2. Si clonas este repositorio en un nuevo equipo, puedes descargar los datasets completos desde sus fuentes públicas o generar un subconjunto (*sample*) de las primeras 5.000 filas para validar el código.

