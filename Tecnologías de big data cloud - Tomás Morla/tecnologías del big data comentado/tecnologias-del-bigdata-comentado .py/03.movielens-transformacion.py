# Databricks notebook source
# MAGIC %md
# MAGIC #TRANSFORMACIÓN
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Vamos a crear un modelo de recomendación de películas usando el algoritmo **ALS** usando la funcionalidad de **Spark MLLib**
# MAGIC
# MAGIC https://spark.apache.org/docs/latest/ml-collaborative-filtering.html

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📂 Carga de datos desde las tablas Silver
# MAGIC Recuperamos el DataFrame de películas directamente desde la tabla Silver que guardamos en el notebook anterior.  
# MAGIC Imprimimos cuántas películas hay en total como comprobación.

# COMMAND ----------

movies = spark.sql("select * from workspace.movielens.movies")
print(f"There are {movies.count()} movies in the datasets")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📂 Carga de valoraciones desde la tabla Silver
# MAGIC Recuperamos el DataFrame de valoraciones desde la tabla Silver.  
# MAGIC Estas valoraciones son los datos de entrada principales para entrenar el modelo de recomendación.

# COMMAND ----------

ratings = spark.sql("select * from workspace.movielens.ratings")
print(f"There are {ratings.count()} ratings in the datasets")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🎲 Semilla de aleatoriedad (reproducibilidad)
# MAGIC Fijamos un número llamado **semilla** (`seed = 42`) que controla todos los procesos aleatorios del entrenamiento.  
# MAGIC Gracias a esto, si ejecutamos el notebook dos veces obtendremos exactamente los mismos resultados, lo que facilita comparar experimentos.

# COMMAND ----------

seed = 42

# COMMAND ----------

# MAGIC %md
# MAGIC ### ✂️ División del dataset en entrenamiento y prueba
# MAGIC Dividimos las valoraciones en dos grupos:
# MAGIC - **Training (80%)**: los datos que el modelo usará para aprender.
# MAGIC - **Test (20%)**: los datos que reservamos para evaluar si el modelo funciona bien con datos que nunca ha visto.
# MAGIC
# MAGIC Esta separación es fundamental en Machine Learning: si evaluáramos con los mismos datos de entrenamiento, el modelo parecería mejor de lo que realmente es.

# COMMAND ----------

(training, test) = ratings.randomSplit([0.8, 0.2], seed=seed)
print(f"Training: {training.count()}")
print(f"Test: {test.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 👁️ Previsualización de los conjuntos de datos
# MAGIC Mostramos las primeras filas de cada conjunto para verificar que la división ha funcionado correctamente.

# COMMAND ----------

display(training.limit(5))
display(test.limit(5))

# COMMAND ----------

# DBTITLE 1,Cell 12
# MAGIC %md
# MAGIC ### 🤖 Configuración del algoritmo ALS
# MAGIC Creamos una instancia del algoritmo **ALS** (*Alternating Least Squares*), el método que usaremos para generar recomendaciones.
# MAGIC
# MAGIC **¿Cómo funciona ALS?**  
# MAGIC Imagina una tabla enorme donde las filas son usuarios y las columnas son películas. La mayoría de celdas están vacías (los usuarios no han visto todas las películas). ALS "rellena" esas celdas prediciendo qué puntuación daría cada usuario a cada película que no ha visto.
# MAGIC
# MAGIC Parámetros principales:
# MAGIC - `setUserCol / setItemCol / setRatingCol` → indica qué columnas contienen usuarios, películas y valoraciones.
# MAGIC - `setMaxIter(5)` → número máximo de veces que el algoritmo ajusta sus cálculos.
# MAGIC - `setColdStartStrategy("drop")` → descarta predicciones para usuarios o películas sin historial suficiente.
# MAGIC - `setRegParam(0.1)` → parámetro de regularización: evita que el modelo "memorice" los datos en lugar de aprender patrones generales.

# COMMAND ----------

# DBTITLE 1,Cell 12
from pyspark.ml.recommendation import ALS

als = (ALS() 
    .setUserCol("userId") 
    .setItemCol("movieId") 
    .setRatingCol("rating") 
    .setMaxIter(5) 
    .setSeed(seed) 
    .setColdStartStrategy("drop") 
    .setRegParam(0.1) 
    .setNonnegative(True)
)

# COMMAND ----------

# MAGIC %md
# MAGIC Puesto que lo que estamos intentando predecir es la valoración de un usuario para cada película, es un problema de regresión y por lo tanto vamos a usar **RMSE** como nuestra métrica de evaluación.
# MAGIC
# MAGIC Además vamos a configurar un grid para hacer la búsqueda de hyperparametros. En este caso, es un grid muy pequeño, de tan solo dos parametros para evitar entrenar muchos modelos

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📁 Creación del volumen temporal para MLlib
# MAGIC Crea un espacio de almacenamiento temporal en Databricks que necesita el algoritmo para guardar ficheros intermedios durante el proceso de entrenamiento con validación cruzada.

# COMMAND ----------

spark.sql("CREATE VOLUME IF NOT EXISTS workspace.default.sparkml_temp")

# COMMAND ----------

# MAGIC %md
# MAGIC ### ⚙️ Configuración previa del entorno ML
# MAGIC Antes de usar las funciones de Machine Learning de Spark, configuramos una ruta temporal donde el algoritmo podrá escribir ficheros intermedios durante el entrenamiento.  
# MAGIC Esto es necesario por una limitación del entorno gratuito de Databricks.

# COMMAND ----------

import os

# Configure temp path for Spark MLlib in serverless
os.environ["SPARKML_TEMP_DFS_PATH"] = "/Volumes/workspace/default/sparkml_temp"

# COMMAND ----------

# DBTITLE 1,Cell 14
# MAGIC %md
# MAGIC ### 🏋️ Entrenamiento con validación cruzada
# MAGIC Entrenamos el modelo probando diferentes configuraciones para encontrar la mejor.
# MAGIC
# MAGIC - **ParamGridBuilder**: define qué valores probar para el parámetro `rank` (5 y 10). El `rank` controla la "complejidad" del modelo: cuántos factores ocultos usa para representar a usuarios y películas.
# MAGIC - **CrossValidator**: divide el conjunto de entrenamiento en 3 partes, entrena con 2 y evalúa con 1, rotando. Así obtiene una estimación más fiable del rendimiento que si usara una sola división.
# MAGIC - **RegressionEvaluator con RMSE**: mide el error como la diferencia media entre la puntuación real y la predicha. Cuanto más bajo, mejor.
# MAGIC
# MAGIC > 💡 Este proceso entrena 6 modelos en total (2 valores de rank × 3 folds). Puede tardar unos minutos.

# COMMAND ----------

# DBTITLE 1,Cell 14
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator

rmse_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="rating", metricName="rmse")

grid = (ParamGridBuilder().addGrid(als.rank, [5, 10]).build())

cv = CrossValidator(numFolds=3, estimator=als, estimatorParamMaps=grid, evaluator=rmse_evaluator, seed=seed)          

cv_model = cv.fit(training)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔍 Tipo del modelo resultante
# MAGIC Muestra el tipo de objeto que ha devuelto el CrossValidator.  
# MAGIC Sirve como comprobación rápida de que el entrenamiento ha finalizado correctamente.

# COMMAND ----------

type(cv_model)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 📊 Métricas de los modelos entrenados
# MAGIC Muestra el error (RMSE) obtenido por cada configuración probada durante la validación cruzada.  
# MAGIC El valor más bajo corresponde al mejor modelo.

# COMMAND ----------

cv_model.avgMetrics

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🏆 Selección del mejor modelo
# MAGIC Recuperamos el modelo con menor error de los que se han entrenado y mostramos con qué valor de `rank` se ha conseguido.

# COMMAND ----------

best_model = cv_model.bestModel
print(f"El mejor modelo se ha entrenado con rank = {best_model.rank}")

# COMMAND ----------

# MAGIC %md
# MAGIC Las métricas anteriores han sido calculadas con un pequeños subconjunto de datos al hacer validación cruzada.
# MAGIC
# MAGIC Vamos a evaluar nuestro modelo contra el conjunto de **test**

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🧪 Evaluación final sobre el conjunto de test
# MAGIC Usamos el mejor modelo para predecir las valoraciones del conjunto de **test** (que el modelo nunca ha visto) y calculamos el RMSE final.  
# MAGIC Este es el indicador más honesto del rendimiento real del modelo.

# COMMAND ----------

predictions= best_model.transform(test)
rmse = rmse_evaluator.evaluate(predictions)
print(f"ALS RMSE: {rmse:.3}")

# COMMAND ----------

# MAGIC %md
# MAGIC Nuestro error final es de **0.882**

# COMMAND ----------

# MAGIC %md
# MAGIC Este tipo de modelos crear las recomendaciones como resultado, por lo tanto vamos a volver a entrenarlo, esta vez, con todas las valoraciones.
# MAGIC
# MAGIC Voy a añadir datos de un usuario ficticio con id 0, incluyendo algunas valoraciones de películas.
# MAGIC
# MAGIC Para ello creamos un DataFrame a partir de una lista python

# COMMAND ----------

# MAGIC %md
# MAGIC ### 👤 Creación de un usuario ficticio con sus valoraciones
# MAGIC Para poder ver recomendaciones personalizadas, creamos un usuario ficticio (userId = 0) y le asignamos puntuaciones máximas (5 estrellas) a 8 películas conocidas.  
# MAGIC A partir de estas preferencias, el modelo inferirá qué otras películas podrían gustarle.

# COMMAND ----------

from datetime import datetime
myUserId = 0
now = datetime.now()
myRatedMovies = [
     (myUserId, 1214, 5, now), # Alien
     (myUserId, 480,  5, now), # Jurassic Park
     (myUserId, 260, 5, now),  # Star Wars: Episode IV - A New Hope
     (myUserId, 541, 5, now),  # Blade Runner
     (myUserId, 2571, 5, now), # Matrix, The
     (myUserId, 296,  5, now), # Pulp Fiction
     (myUserId, 356,  5, now), # Forrest Gump     
     (myUserId, 593, 5, now),  # Silence of the Lambs, The
]

myRatingsDF = spark.createDataFrame(myRatedMovies, ['userId', 'movieId','rating','timestamp'])
display(myRatingsDF)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔄 Reentrenamiento con todos los datos + usuario ficticio
# MAGIC Unimos las valoraciones reales con las del usuario ficticio y reentrenamos el modelo desde cero usando todos los datos disponibles.  
# MAGIC Esta vez usamos `rank=10` (el mejor encontrado en la validación cruzada) y no reservamos datos de test, porque ya no necesitamos evaluar: queremos el mejor modelo posible para generar recomendaciones.

# COMMAND ----------

allratings = ratings.unionByName(myRatingsDF)
als.setRank(10)
best_model = als.fit(allratings)

# COMMAND ----------

# MAGIC %md
# MAGIC # SERVICIO LAKEHOUSE

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC En esta primera versión, vamos a servir las recomendaciones directamente desde nuestro lakehouse
# MAGIC
# MAGIC Configuramos la ruta para escribir los datos en la capa **gold**
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🗄️ Creación de la base de datos de recomendaciones
# MAGIC Creamos una base de datos separada llamada `recommender` donde guardaremos las recomendaciones generadas.  
# MAGIC Separarla de `movielens` es una buena práctica: los datos de origen y los resultados del modelo quedan organizados de forma independiente.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS workspace.recommender;

# COMMAND ----------

# MAGIC %md
# MAGIC Creamos 10 recomendaciones (peliculas) para todos los usuarios

# COMMAND ----------

# DBTITLE 1,Cell 33
user_recs = (best_model.recommendForAllUsers(10))

# COMMAND ----------

# DBTITLE 1,Cell 33
# MAGIC %md
# MAGIC ### 🎯 Generación de recomendaciones para todos los usuarios
# MAGIC Pedimos al modelo que genere las **10 mejores recomendaciones** para cada usuario del dataset.  
# MAGIC Internamente, el modelo calcula qué películas no ha visto cada usuario y predice qué puntuación les daría.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🛠️ Generación manual de recomendaciones (workaround)
# MAGIC La función automática del modelo no está disponible en la edición gratuita de Databricks, así que calculamos las recomendaciones "a mano" siguiendo estos pasos:
# MAGIC
# MAGIC 1. **Extraemos los factores latentes**: el modelo ALS representa a cada usuario y cada película como un vector de números (sus "gustos" en un espacio abstracto).
# MAGIC 2. **Multiplicamos las matrices**: `puntuación = factores_usuario · factores_película`. Esta operación matemática predice la afinidad de cada usuario con cada película.
# MAGIC 3. **Seleccionamos el Top 10**: para cada usuario, nos quedamos con las 10 películas con mayor puntuación predicha.
# MAGIC
# MAGIC > 💡 Este proceso usa **NumPy** para hacer los cálculos con matrices de forma eficiente, y luego convierte el resultado de vuelta a un DataFrame de Spark.

# COMMAND ----------

# ============================================================
# 5. GENERACION DE RECOMENDACIONES (compatible con UC)
# ============================================================

# 1. Obtén los factores latentes del modelo directamente
#    (matrices U e I, sin higher-order functions)
user_factors = best_model.userFactors   # DataFrame: id, features
item_factors = best_model.itemFactors   # DataFrame: id, features

# 2. Sácalos del contexto UC con TempViews
user_factors.createOrReplaceTempView("tv_user_factors")
item_factors.createOrReplaceTempView("tv_item_factors")
ratings.createOrReplaceTempView("tv_ratings")

# 3. Reconstruye las recomendaciones manualmente en Pandas
#    multiplicando los vectores de factores latentes
import numpy as np
import pandas as pd

user_factors_pd = spark.sql("SELECT * FROM tv_user_factors").toPandas()
item_factors_pd = spark.sql("SELECT * FROM tv_item_factors").toPandas()

# Matrices de factores
U = np.array(user_factors_pd["features"].tolist())   # (n_users, rank)
I = np.array(item_factors_pd["features"].tolist())   # (n_items, rank)

# Scores = U · I^T  →  (n_users, n_items)
scores = U @ I.T

# 4. Obtén el top-10 por usuario
user_ids = user_factors_pd["id"].tolist()
item_ids = item_factors_pd["id"].tolist()
TOP_N    = 10

rows = []
for i, uid in enumerate(user_ids):
    top_indices = np.argpartition(scores[i], -TOP_N)[-TOP_N:]
    top_indices = top_indices[np.argsort(scores[i][top_indices])[::-1]]
    for idx in top_indices:
        rows.append({
            "userId":  uid,
            "movieId": item_ids[idx],
            "score":   float(scores[i][idx])
        })

recs_pd = pd.DataFrame(rows)

user_recs = spark.createDataFrame(recs_pd)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 👁️ Previsualización de las recomendaciones
# MAGIC Mostramos las recomendaciones generadas para verificar que el formato es correcto antes de guardarlas.

# COMMAND ----------

display(user_recs)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 💾 Guardado de las recomendaciones (capa Gold)
# MAGIC Guardamos la tabla de recomendaciones en formato Delta dentro de la base de datos `recommender`.  
# MAGIC Esta es la capa **Gold**: datos completamente procesados y listos para ser consumidos por aplicaciones o usuarios finales.

# COMMAND ----------

format = "delta"

user_recs.write.format(format).mode("overwrite").saveAsTable("workspace.recommender.user_recommendations")


# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔍 Consulta de verificación
# MAGIC Consultamos las primeras 10 filas de la tabla de recomendaciones recién guardada para confirmar que todo se ha guardado correctamente.

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from workspace.recommender.user_recommendations
# MAGIC limit 10