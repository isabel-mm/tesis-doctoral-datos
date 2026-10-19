# Inventario terminológico

Unidades del inventario validado (GLiCor) presentes en cada subcorpus, con sus valores de terminologicidad (capítulo 5 y Apéndice III de la tesis): 202 unidades en inglés (146 términos y 56 entidades) y 250 en español (142 términos y 108 entidades). Una unidad está presente en un subcorpus si aparece anotada en él con alguna de sus formas.

Las unidades se validaron durante la anotación del corpus (capítulo 3 de la tesis) y se unificaron por concepto en las 261 entradas del glosario, que están en `07_glicor/`. Las formas de cada entrada (siglas, formas desarrolladas, sinónimos, préstamos) están en `04_anotacion/formas_por_entrada.csv`.

## Ficheros

- `inventario_en.csv`, `inventario_es.csv`: una unidad por fila, ordenadas por terminologicidad.
  - `unit`: la unidad (denominación de la entrada en esa lengua); `forma`: la forma del corpus sobre la que se calculan los valores, que es la más frecuente entre sus formas anotadas, con su grafía original (en las entidades cuya forma más frecuente no es una forma registrada del glosario, la denominación); `tipo`: `termino` o `entidad`; `categoria`: categoría temática (capítulo 5).
  - `freq`, `df`: frecuencia de esa forma y número de documentos en que aparece.
  - `tfidf`, `cvalue`: TF-IDF y C-value.
  - `nc_frantzi`, `nc_validados`: NC-value según Frantzi et al. (2000), con dos conjuntos de términos de referencia: los primeros candidatos por C-value y los términos del inventario.
  - `context_factor`, `containers`, `containers_mean_freq`, `chains`, `nested`: magnitudes intermedias del cálculo (factor de contexto, candidatos que contienen a la unidad y apariciones incrustadas).
  - `*_norm`: valores normalizados por el máximo entre las unidades de la lengua.
  - `T`: índice de terminologicidad de la tesis, media del TF-IDF y el NC-value normalizados. `T_validados` y `T_cvalue` son variantes de comprobación.

Los números decimales usan punto.

## Scripts

En `scripts/`, tal como se ejecutaron en el repositorio de trabajo de la tesis (las rutas remiten a él):

- `recalculo_ncvalue.py`: cálculo de TF-IDF, C-value, NC-value y del índice T.
- `indice_T_glicor.py`: aplica ese cálculo a las unidades de GLiCor presentes en cada subcorpus, con las formas anotadas en el corpus.
- `forma_representante.py`: añade la columna `forma`.
- `resumen_T.py`: cifras del capítulo 5 (correlaciones de Spearman, peso del factor de contexto, medianas).
- `apendice_glicor.py`: genera las tablas del Apéndice III.
