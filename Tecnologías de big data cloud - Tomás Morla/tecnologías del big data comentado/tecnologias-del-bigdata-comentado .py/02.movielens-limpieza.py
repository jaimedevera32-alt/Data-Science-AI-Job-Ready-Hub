# Databricks notebook source
# MAGIC %md
# MAGIC # LIMPIEZA

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📎 Carga del notebook de configuración
# MAGIC `%run` ejecuta otro notebook como si fuera código de este mismo.  
# MAGIC Aquí cargamos el notebook `00.movielens-entorno` para tener disponibles las credenciales y rutas que definimos allí.

# COMMAND ----------

# MAGIC %run ./00.movielens-entorno

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔍 Comprobación de bases de datos disponibles
# MAGIC Lista todas las bases de datos existentes en el entorno de Databricks. Cuando creemos `movielens` podremos verla.

# COMMAND ----------

# MAGIC %sql
# MAGIC show databases;

# COMMAND ----------

# MAGIC %md
# MAGIC ## BRONZE

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📥 Carga del CSV de películas (Bronze)
# MAGIC Leemos el fichero `movies.csv` desde el almacenamiento en la nube y lo convertimos en un **Spark DataFrame** (una tabla distribuida en memoria).
# MAGIC
# MAGIC Opciones destacadas:
# MAGIC - `header=true` → la primera fila es la cabecera con los nombres de columna.
# MAGIC - `inferSchema=true` → Spark detecta automáticamente el tipo de cada columna (texto, número…).
# MAGIC - `escape="""` → necesario porque algunos títulos contienen comillas dentro del texto.

# COMMAND ----------

movies_path = f"{BRONZE_PATH}/movielens/movies/"
print(movies_path)
movies_raw = (spark.read
              .options(**DF_OPTIONS)
              .option("header","true")
              .option("escape","\"") # '"'
              .option("inferSchema","true")
              .csv(movies_path)
            )
display(movies_raw.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔬 Inspección del esquema de movies
# MAGIC `printSchema()` muestra la estructura del DataFrame: nombres de columnas y tipos de datos detectados.  
# MAGIC Es un paso de verificación para asegurarnos de que la carga ha funcionado como esperábamos.

# COMMAND ----------

movies_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📥 Carga del CSV de valoraciones (Bronze)
# MAGIC Leemos `ratings.csv` y lo convertimos en DataFrame.  
# MAGIC Este fichero es el más grande del dataset: contiene más de 100.000 valoraciones de usuarios.

# COMMAND ----------

ratings_path = f"{BRONZE_PATH}/movielens/ratings/"
ratings_raw = spark.read.options(**DF_OPTIONS).option("header","true").option("inferSchema","true").csv(ratings_path)
display(ratings_raw.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔬 Inspección del esquema de ratings
# MAGIC Verificamos que las columnas `userId`, `movieId`, `rating` y `timestamp` se han cargado con los tipos correctos.

# COMMAND ----------

ratings_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📥 Carga del CSV de enlaces (Bronze)
# MAGIC Leemos `links.csv`, que contiene los identificadores de cada película en bases de datos externas (IMDb y TMDb).

# COMMAND ----------

links_path = f"{BRONZE_PATH}/movielens/links/"
links_raw = spark.read.options(**DF_OPTIONS).option("header","true").csv(links_path)

display(links_raw.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔬 Inspección del esquema de links
# MAGIC Verificamos la estructura del DataFrame de enlaces.

# COMMAND ----------

links_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📥 Carga del CSV de tráilers (Bronze)
# MAGIC Leemos `trailers.csv`, que asocia cada película con uno o varios vídeos de YouTube.

# COMMAND ----------

trailers_path = f"{BRONZE_PATH}/movielens/trailers/"
trailers_raw = spark.read.options(**DF_OPTIONS).option("header","true").option("inferSchema","true").csv(trailers_path)
display(trailers_raw.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔬 Inspección del esquema de trailers
# MAGIC Verificamos la estructura del DataFrame de tráilers.

# COMMAND ----------

trailers_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧹 Limpieza de películas (Bronze → Silver)
# MAGIC Este es el paso de limpieza más elaborado del dataset. Hacemos tres cosas:
# MAGIC
# MAGIC 1. **Separamos título y año**: la columna `title` contiene ambos mezclados (ej: `"Toy Story (1995)"`). Usamos una **expresión regular** (una especie de plantilla de búsqueda de texto) para extraerlos en columnas separadas: `title` y `year`.
# MAGIC 2. **Separamos los géneros**: la columna `genres` tiene los géneros separados por `|` (ej: `"Action|Comedy"`). Los convertimos en una lista real para poder filtrar fácilmente después.
# MAGIC 3. **Ajustamos el tipo de `movieId`**: lo convertimos a número entero largo (`bigint`) para que coincida con el resto de tablas.
# MAGIC
# MAGIC > 💡 `@udf` significa *User Defined Function*: una función Python que Spark puede aplicar fila a fila sobre todo el DataFrame.

# COMMAND ----------

import re
from pyspark.sql.functions import col,split

@udf("array<string>")
def parse_title(t:str):
    titleRegex = re.compile(r'^(.+)\((\d{4})\)$')
    m = titleRegex.search(t.strip())
    if m:
        title,year= m.groups()
        return [title.strip(),year.strip()]
    else:
        return [t,None]
    

movies_std = movies_raw.select(
    col("movieId").cast("bigint"),
    parse_title(col("title"))[0].alias("title"),
    parse_title(col("title"))[1].cast("integer").alias("year"),
    split("genres",'\|').alias("genres")
)

display(movies_std)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔎 Revisión de películas sin año
# MAGIC Comprobamos si hay películas a las que no se les ha podido extraer el año (por ejemplo, títulos con un formato inusual).  
# MAGIC Esto nos ayuda a detectar casos que la limpieza no ha resuelto correctamente.

# COMMAND ----------

display(movies_std.where(col("year").isNull()))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧹 Eliminación del valor "(no genres listed)"
# MAGIC Algunas películas tienen el texto literal `"(no genres listed)"` como género.  
# MAGIC Con `array_remove` lo eliminamos de la lista para dejar el campo limpio (lista vacía en su lugar).

# COMMAND ----------

from pyspark.sql.functions import array_remove

movies_std = movies_std.withColumn("genres",array_remove(col("genres"),"(no genres listed)"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔎 Verificación tras la limpieza de géneros
# MAGIC Volvemos a revisar las películas sin año para confirmar que no hemos introducido nuevos problemas con la transformación anterior.

# COMMAND ----------

display(movies_std.where(col("year").isNull()))

# COMMAND ----------

display(movies_std)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧹 Limpieza de valoraciones (Bronze → Silver)
# MAGIC Ajustamos los tipos de datos del DataFrame de ratings:
# MAGIC - `userId` y `movieId` → números enteros largos (`bigint`).
# MAGIC - `rating` → número decimal (`double`).
# MAGIC - `timestamp` → convertimos el número Unix (segundos desde 1970) a una fecha y hora legible.  
# MAGIC
# MAGIC > 💡 `from_unixtime` convierte el número a texto de fecha, y `to_timestamp` lo convierte al tipo fecha de Spark.

# COMMAND ----------

from pyspark.sql.functions import to_timestamp, from_unixtime
ratings_std = ratings_raw.select(
    col("userId").cast("bigint"),
    col("movieId").cast("bigint"),
    col("rating").cast("double"),    
    to_timestamp(from_unixtime("timestamp")).alias("timestamp")
)
display(ratings_std)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧹 Limpieza de enlaces (Bronze → Silver)
# MAGIC Limpiamos el DataFrame de links y, además, **construimos URLs completas** para IMDb y TMDb concatenando el ID con la URL base de cada plataforma.  
# MAGIC Así será mucho más fácil enlazar directamente a la ficha de cada película desde la aplicación.

# COMMAND ----------

from pyspark.sql.functions import concat,lit

links_std = links_raw.select(
    col("movieId").cast("bigint"),
    col("imdbId"),    
    concat(lit("http://www.imdb.com/title/tt"),col("imdbId"),lit("/")).alias("imdbUrl"),
    col("tmdbId"),    
    concat(lit("https://www.themoviedb.org/movie/"),col("tmdbId"),lit("/")).alias("tmdbUrl")
)

display(links_std)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧹 Limpieza de tráilers (Bronze → Silver)
# MAGIC Igual que con los links, construimos la URL completa de cada tráiler en YouTube a partir del `youtubeId`.  
# MAGIC De este modo podemos embeber el vídeo directamente en la aplicación sin cálculos adicionales.

# COMMAND ----------

from pyspark.sql.functions import *

trailers_std = trailers_raw.select(
    col("movieId").cast("bigint"),
    col("youtubeId"),    
    concat(lit("https://www.youtube.com/embed/"),col("youtubeId"),lit("/")).alias("youtubeUrl")
)
display(trailers_std)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🗄️ Creación de la base de datos
# MAGIC Antes de guardar ningún dato, necesitamos un lugar donde organizarlos.  
# MAGIC Esta instrucción SQL crea una **base de datos** llamada `movielens` dentro del catálogo de Databricks (si aún no existe).  
# MAGIC Será el contenedor donde luego registraremos todas las tablas del proyecto.

# COMMAND ----------

# MAGIC %sql
# MAGIC create database if not exists workspace.movielens;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 💾 Guardado en la capa Silver (formato Delta)
# MAGIC Guardamos los cuatro DataFrames limpios como **tablas Delta** en el catálogo de Databricks.
# MAGIC
# MAGIC - **Formato Delta**: es un formato especial de almacenamiento optimizado para big data. Permite actualizaciones eficientes, control de versiones y consultas muy rápidas.  
# MAGIC - `mode("overwrite")` → si la tabla ya existe, se sobreescribe completamente.  
# MAGIC - `saveAsTable` → registra la tabla en el catálogo para poder consultarla con SQL.

# COMMAND ----------

format = "delta"

movies_std.write.format(format).mode("overwrite").saveAsTable("workspace.movielens.movies")
ratings_std.write.format(format).mode("overwrite").saveAsTable("workspace.movielens.ratings")
links_std.write.format(format).mode("overwrite").saveAsTable("workspace.movielens.links")
trailers_std.write.format(format).mode("overwrite").saveAsTable("workspace.movielens.trailers")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔍 Prueba de consulta SQL sobre la tabla limpia
# MAGIC Hacemos una consulta de ejemplo sobre la tabla `movies` ya guardada en Silver:  
# MAGIC buscamos todas las películas de acción del año 1999.  
# MAGIC
# MAGIC Esto demuestra que los datos están correctamente guardados y que podemos consultarlos con SQL estándar, incluyendo búsquedas dentro de arrays (columna `genres`).

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from workspace.movielens.movies 
# MAGIC where year = 1999 and array_contains(genres, "Action");