# Inventario terminológico

Inventario validado a partir de la extracción híbrida (capítulo 5 y Apéndice III de la tesis): 170 unidades en inglés y 147 en español.

Es el inventario tal como se validó, antes de la unificación por concepto. Las variantes de cada entrada (siglas, formas desarrolladas, sinónimos, préstamos) están en `04_anotacion/formas_por_entrada.csv`, y las 261 entradas unificadas del glosario, en `07_glicor/`.

## Ficheros

- `inventario_en.csv`, `inventario_es.csv`: una unidad por fila.
  - `unit`: la unidad; `tipo`: `termino` o `entidad`.
  - `freq`, `df`: frecuencia y número de documentos en que aparece.
  - `tfidf`, `cvalue`: TF-IDF y C-value.
  - `nc_frantzi`, `nc_validados`: NC-value según Frantzi et al. (2000), con dos conjuntos de términos de referencia: los primeros candidatos por C-value y los términos validados.
  - `context_factor`, `containers`, `containers_mean_freq`, `chains`, `nested`: magnitudes intermedias del cálculo (factor de contexto, candidatos que contienen a la unidad y apariciones incrustadas).
  - `*_norm`: valores normalizados por el máximo de los términos validados de la lengua.
  - `T`: índice de terminologicidad de la tesis, media del TF-IDF y el NC-value normalizados. `T_validados` y `T_cvalue` son variantes de comprobación.

Los números decimales usan punto.
