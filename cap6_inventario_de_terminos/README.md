# Inventario terminológico

Unidades del inventario validado (GLiCor) presentes en cada subcorpus, con sus valores de terminologicidad (capítulo 6 de la tesis): 200 unidades en inglés (145 términos y 55 entidades) y 247 en español (140 términos y 107 entidades). Todas las cifras se calculan sin las secciones de referencias bibliográficas de los documentos (capítulo 3). Una unidad está presente en un subcorpus si aparece anotada en él con alguna de sus formas.

Las unidades se validaron durante la anotación del corpus (capítulo 3 de la tesis) y se unificaron por concepto en las 261 entradas del glosario, que están en `cap7_glosario_GLiCor/`. Las formas de cada entrada (siglas, formas desarrolladas, sinónimos, préstamos) están en `cap3_anotacion_de_terminos/formas_por_entrada.csv`.

## Ficheros

- `inventario_bilingue.pdf`: el inventario completo en forma de tablas, con los términos y las entidades de cada lengua ordenados por terminologicidad.

- `inventario_en.csv`, `inventario_es.csv`: una unidad por fila, ordenadas por terminologicidad.
  - `unit`: la unidad (denominación de la entrada en esa lengua); `forma`: la forma del corpus sobre la que se calculan los valores, que es la más frecuente entre sus formas anotadas, con su grafía original (en las entidades cuya forma más frecuente no es una forma registrada del glosario, la denominación); `tipo`: `termino` o `entidad`; `categoria`: categoría temática (capítulo 6).
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
- `indice_T_sinbib.py`: aplica ese cálculo a las unidades de GLiCor presentes en cada subcorpus, con las formas anotadas en el corpus y sin las referencias bibliográficas (`indice_T_glicor.py` es la versión anterior, sobre los textos completos).
- `forma_representante_sinbib.py`: añade la columna `forma` (`forma_representante.py`, versión anterior).
- `primeros_candidatos.py`: proporción de unidades validadas entre los 100 primeros candidatos según el índice, el TF-IDF y el NC-value (nota del capítulo 6).
- `resumen_T.py`: cifras del capítulo 6 (correlaciones de Spearman, peso del factor de contexto, medianas).
- `inventario_bilingue.py`: genera y compila `inventario_bilingue.pdf` con los valores sin referencias bibliográficas (`apendice_glicor.py`, versión anterior de sus tablas).
