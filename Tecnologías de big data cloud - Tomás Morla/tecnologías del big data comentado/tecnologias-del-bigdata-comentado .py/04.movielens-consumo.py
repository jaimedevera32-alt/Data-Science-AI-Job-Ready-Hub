# Databricks notebook source
# MAGIC %md
# MAGIC # CONSUMO

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🖥️ Función para mostrar recomendaciones visualmente
# MAGIC Definimos una función `display_recs` que recibe una lista de recomendaciones y las muestra en el notebook de forma visual:  
# MAGIC - Un **vídeo embebido** del tráiler de YouTube de cada película.  
# MAGIC - Un enlace a su ficha en **IMDb** y en **TMDb**.
# MAGIC
# MAGIC Usamos `HTML` de IPython para renderizar contenido web directamente dentro del notebook.

# COMMAND ----------

from IPython.display import HTML
    
def display_recs(recs):
    html = ""
    for rec in recs:        
        html += f'''<p><iframe src="{rec['youtubeUrl']}"></iframe></p>'''
        html += f'''<p><a href="{rec['imdbUrl']}">{rec['title']}</a></p>'''
        html += f'''<p><a href="{rec['tmdbUrl']}">{rec['title']}</a></p>'''
    display(HTML(html))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔗 Función para recuperar recomendaciones enriquecidas
# MAGIC Definimos la función `get_recs(user_id)` que, dado un `userId`, consulta la tabla de recomendaciones y la **cruza con otras tablas** para añadir información adicional:
# MAGIC
# MAGIC - `movies` → título y año de la película.
# MAGIC - `links` → URLs de IMDb y TMDb.
# MAGIC - `trailers` → URL del tráiler en YouTube.
# MAGIC
# MAGIC El resultado se ordena por puntuación (de mayor a menor) para mostrar primero las recomendaciones más relevantes.

# COMMAND ----------

def get_recs(user_id:int):
   recs = spark.sql(f"""
               SELECT r.*,
                     m.title,
                     m.year,
                     l.imdbUrl,
                     l.tmdbUrl,
                     t.youtubeUrl
               FROM (select * FROM workspace.recommender.user_recommendations WHERE userId={user_id}) r
               LEFT JOIN workspace.movielens.movies m ON r.movieId=m.movieId   
               LEFT JOIN workspace.movielens.links l ON r.movieId=l.movieId
               LEFT JOIN workspace.movielens.trailers t ON r.movieId=t.movieId  
               ORDER BY r.score DESC 
   """)
   return recs.collect()
   

# COMMAND ----------

# MAGIC %md
# MAGIC Mostramos las recomendaciones

# COMMAND ----------

display_recs(get_recs(user_id=1))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🎬 Mostrar recomendaciones para el usuario 30
# MAGIC Llamamos a las dos funciones anteriores para mostrar las recomendaciones del usuario con `userId = 30`.  
# MAGIC Prueba a cambiar el número por cualquier otro `userId` del dataset para ver recomendaciones diferentes.

# COMMAND ----------

display_recs(get_recs(user_id=30))