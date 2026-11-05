# Reto Día 01: Optimización de Bucle Python a Vectorización NumPy/Pandas

## 📌 Contexto de Entrevista Técnica
En entrevistas para puestos de Data Scientist / Machine Learning Engineer es clásico recibir un fragmento de código con bucles `for` lentos sobre DataFrames (`.iterrows()` o bucles anidados) y pedirte optimizarlo reduciendo la complejidad temporal de minutos a milisegundos.

## 🎯 Objetivo
Dado un DataFrame con millones de registros de transacciones con `amount` y `category`, queremos calcular una columna calculada de `adjusted_amount`:
- Si la categoría es 'LUXURY', se aplica un recargo del 15% (`amount * 1.15`).
- Si la categoría es 'ESSENTIAL', se aplica un descuento del 5% (`amount * 0.95`).
- Para cualquier otra categoría, el monto se mantiene igual.

Debes implementar la función `vectorized_adjusted_amount(df)` evitando completamente bucles `for` e `iterrows()`, usando `numpy.select` o máscaras booleanas.

## ❓ Pregunta de Selección (Minutos 50 - 60)
* ¿Por qué `.iterrows()` o `.apply()` es lento en Pandas comparado con `np.select` o `np.where`?
* *Respuesta esperada:* `.iterrows()` convierte cada fila en una `pd.Series`, generando overhead de Python object creation en cada iteración y saltándose el GIL y las optimizaciones de bajo nivel en C/BLAS de NumPy.

