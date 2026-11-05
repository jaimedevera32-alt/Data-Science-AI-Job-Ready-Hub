# Reto Día 01: Custom Transformer & Prevención de Data Leakage

## 📌 Contexto de Entrevista Técnica
En entrevistas de Machine Learning Engineer, uno de los errores eliminatorios más frecuentes es la **fuga de datos (Data Leakage)**: calcular estadísticas de preprocesamiento (medias, varianzas, percentiles) sobre el conjunto de test o antes de hacer el split de validación.

## 🎯 Objetivo
Implementa una clase `RobustOutlierCapper` compatible con el estándar de Scikit-Learn (`BaseEstimator`, `TransformerMixin`):
1. `fit(X, y=None)`: Calcula los percentiles 1% y 99% exclusivamente sobre el set de entrenamiento y los almacena en `self.lower_bound_` y `self.upper_bound_`.
2. `transform(X)`: Aplica el truncamiento (*clipping*) utilizando los límites aprendidos en `fit`.
3. Debe integrarse sin errores dentro de un `sklearn.pipeline.Pipeline`.

## ❓ Pregunta de Selección (Minutos 50 - 60)
* ¿Por qué aplicar `fit_transform` directamente sobre todo el dataset antes de `train_test_split` invalida las métricas de test?
* *Respuesta esperada:* Porque los parámetros del escalado o imputación incorporan información del conjunto de test que en producción no existiría en el momento de la inferencia, produciendo métricas de evaluación optimistas y fallos al desplegar en producción.

