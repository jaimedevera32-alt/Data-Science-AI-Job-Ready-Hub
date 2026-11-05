# Databricks notebook source
# MAGIC %md
# MAGIC ### ⚙️ Paso 1 · Credenciales de acceso al almacenamiento
# MAGIC Aquí definimos las credenciales necesarias para conectarnos a **Azure Data Lake Storage (ADLS)**, el servicio de almacenamiento en la nube donde están guardados los ficheros CSV.
# MAGIC
# MAGIC - **CONTAINER**: nombre del contenedor (carpeta raíz) dentro del almacenamiento.  
# MAGIC - **ADLS_ACCOUNT**: nombre de la cuenta de almacenamiento en Azure.  
# MAGIC - **ADLS_SAS_KEY**: clave de acceso (como una contraseña) que nos autoriza a leer los datos.
# MAGIC
# MAGIC > ⚠️ En un proyecto real estas credenciales nunca se escriben directamente en el código; se guardan de forma segura en un gestor de secretos.

# COMMAND ----------

CONTAINER = "datos"
# reemplazar con tus datos
ADLS_ACCOUNT = "..."
ADLS_SAS_KEY = "..."

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🗂️ Paso 2 · Ruta a la capa Bronze
# MAGIC Construimos la ruta completa (URL) que apunta a la carpeta **bronze** dentro del almacenamiento en la nube.
# MAGIC
# MAGIC La arquitectura Lakehouse organiza los datos en tres capas:
# MAGIC - **Bronze** → datos tal cual llegan, sin procesar.
# MAGIC - **Silver** → datos limpios y estructurados.
# MAGIC - **Gold** → datos listos para consumo (modelos, informes, dashboards).

# COMMAND ----------

BRONZE_PATH = f"abfss://{CONTAINER}@{ADLS_ACCOUNT}.dfs.core.windows.net/bronze"

# COMMAND ----------

# MAGIC %md
# MAGIC ### 🔑 Paso 3 · Opciones de conexión para Spark
# MAGIC Empaquetamos las credenciales en un diccionario (`DF_OPTIONS`) que luego pasaremos a Spark cada vez que necesite leer ficheros del almacenamiento.  
# MAGIC Así evitamos repetir las credenciales en cada lectura.

# COMMAND ----------

KEY = f"fs.azure.account.key.{ADLS_ACCOUNT}.dfs.core.windows.net"
DF_OPTIONS =  {KEY:ADLS_SAS_KEY}

# COMMAND ----------

# MAGIC %md
# MAGIC ### ✅ Paso 4 · Verificación del entorno
# MAGIC Simplemente imprime un mensaje para confirmar que el notebook de configuración se ha ejecutado correctamente y todas las variables están disponibles.

# COMMAND ----------

print("Entorno listo")