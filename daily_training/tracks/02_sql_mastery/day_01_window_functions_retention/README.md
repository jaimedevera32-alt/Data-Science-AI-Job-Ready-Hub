# Reto Día 01: Window Functions & MoM Growth en SQL

## 📌 Contexto de Entrevista Técnica
En entrevistas de Product Data Scientist y Analytics Engineer (Meta, Uber, Spotify) es un estándar evaluar `WINDOW FUNCTIONS` (`LAG`, `LEAD`, `ROW_NUMBER`, `SUM OVER`) para calcular métricas de retención, cohortes y crecimiento mensual interanual.

## 🎯 Objetivo
Tenemos una tabla `monthly_revenue` con columnas:
* `month_date` (DATE)
* `product_category` (VARCHAR)
* `revenue` (DECIMAL)

Escribe una consulta SQL que devuelva:
1. `month_date`
2. `product_category`
3. `revenue`
4. `prev_month_revenue`: El revenue del mes anterior para esa misma categoría.
5. `mom_growth_pct`: El porcentaje de crecimiento respecto al mes anterior redondeado a 2 decimales: `((revenue - prev) / prev) * 100`.

## ❓ Pregunta de Selección (Minutos 50 - 60)
* ¿Cuál es la diferencia entre `RANK()`, `DENSE_RANK()` y `ROW_NUMBER()` cuando hay empates?
* *Respuesta esperada:* `ROW_NUMBER()` asigna números únicos consecutivos sin importar empates. `RANK()` asigna la misma posición a valores empatados y salta las siguientes posiciones (1, 2, 2, 4). `DENSE_RANK()` asigna la misma posición y no salta posiciones (1, 2, 2, 3).

