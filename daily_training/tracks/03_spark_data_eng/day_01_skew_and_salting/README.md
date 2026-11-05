# Reto Día 01: Data Skew y Salting en Apache Spark

## 📌 Contexto de Entrevista Técnica
En entrevistas de Data Engineer (Netflix, Databricks, Amazon), el problema número 1 en clusters de Spark es el **Data Skew** (sesgo de datos). Ocurre cuando una clave de join o group-by concentra el 80% de los datos, provocando que un solo *task/executor* tarde horas mientras los demás terminan en segundos (Straggler Tasks / OOM Errors).

## 🎯 Objetivo
Implementa la técnica de **Salting** en PySpark (o simulación en Python para tests sin cluster):
1. Añadir una columna de "sal" aleatoria (`salt_key = concat(original_key, '_', random_int(0, N-1))`) a la tabla sesgada.
2. Replicar la tabla de dimensión multiplicando sus claves por cada valor de sal posible (`0` a `N-1`).
3. Realizar el join sobre `salted_key` para distribuir uniformemente los registros en los particionadores.

## ❓ Pregunta de Selección (Minutos 50 - 60)
* ¿Cuándo es preferible un `Broadcast Hash Join` sobre `Salting`?
* *Respuesta esperada:* Si una de las dos tablas es suficientemente pequeña (menor al umbral de `spark.sql.autoBroadcastJoinThreshold`, por defecto 10MB), el `Broadcast Join` envía la tabla completa a todos los ejecutores evitando completamente el shuffle y el problema del sesgo. Si ambas tablas son masivas y no caben en memoria del driver/ejecutores, el *salting* es la técnica indicada.

