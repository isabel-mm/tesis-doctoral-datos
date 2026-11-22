# Inventario terminológico

Unidades del inventario validado (GLiCor) presentes en cada subcorpus, con sus valores de terminologicidad (capítulo 6 de la tesis): 200 unidades en inglés (145 términos y 55 entidades) y 247 en español (140 términos y 107 entidades). Todas las cifras se calculan sin las secciones de referencias bibliográficas de los documentos (capítulo 3). Una unidad está presente en un subcorpus si aparece anotada en él con alguna de sus formas.

Las unidades se validaron durante la anotación del corpus (capítulo 3 de la tesis) y se unificaron por concepto en las 261 entradas del glosario, que están en `cap8_glosario_GLiCor/`. Las formas de cada entrada (siglas, formas desarrolladas, sinónimos, préstamos) están en `cap4_anotacion_de_terminos/formas_por_entrada.csv`.

Las cifras se calculan sobre las apariciones que la revisión experta anotó como término o entidad, con todas las formas de cada unidad, y no sobre todas las apariciones de la forma en el texto, que es lo que cuenta TECLA al ordenar los candidatos antes de la revisión (capítulo 5). Así, una forma que también funciona en la lengua general, como *muestra* (también del verbo *mostrar*) o *tipo* (*este tipo de análisis*), solo cuenta sus usos terminológicos.

## Ficheros

- `inventario_bilingue.pdf`: el inventario completo en forma de tablas, con los términos y las entidades de cada lengua agrupados por categoría y ordenados por terminologicidad.

- `inventario_en.csv`, `inventario_es.csv`: una unidad por fila, ordenadas por terminologicidad.
  - `unit`: la unidad (denominación de la entrada en esa lengua); `forma`: su forma anotada más frecuente, que es la que figura en las tablas; `tipo`: `termino` o `entidad`; `categoria`: categoría temática (capítulo 6).
  - `freq`: número de apariciones anotadas de la unidad (todas sus formas); `df`: número de documentos en que se anota.
  - `tfidf`: TF-IDF, `freq · (log2((N+1)/(df+1)) + 1)`, con N = 50 documentos.
  - `cvalue`: C-value de Frantzi et al. (2000): a la frecuencia de la unidad, sumadas las apariciones de su forma dentro de unidades anotadas más largas, se le resta la media de las apariciones de esas unidades que la contienen.
  - `nc_frantzi`: NC-value, `0,8 · C-value + 0,2 · factor de contexto`; el factor (`context_factor`) pondera las palabras de contexto (sustantivos, adjetivos y verbos a dos posiciones) de las apariciones anotadas por la proporción de términos del inventario en cuyo contexto aparecen.
  - `containers`: unidades anotadas que contienen la forma; `chains`: términos del inventario que la contienen (cadenas terminológicas); `nested`: apariciones de la unidad incrustadas en esos términos; `total`: `freq + nested` (tablas de términos nucleares del capítulo 6).
  - `*_norm`: valores normalizados por el máximo entre las unidades de la lengua.
  - `T`: índice de terminologicidad de la tesis, media del TF-IDF y el NC-value normalizados.

Los números decimales usan punto.

## Scripts

En `scripts/`, tal como se ejecutaron en el repositorio de trabajo de la tesis (las rutas remiten a él):

- `indice_T_anotado.py`: cálculo de TF-IDF, C-value, NC-value y del índice T sobre las apariciones anotadas, sin las referencias bibliográficas.
- `resumen_T_anotado.py`: cifras del capítulo 6 (correlaciones de Spearman, peso del factor de contexto, medianas, incrustación).
- `inventario_bilingue.py`: genera `inventario_bilingue.pdf`.
- `primeros_candidatos.py`: proporción de unidades validadas entre los 100 primeros candidatos de TECLA según el índice, el TF-IDF y el NC-value (nota del capítulo 5); se calcula sobre las formas, porque ordena candidatos antes de la revisión.
- `recalculo_ncvalue.py`, `indice_T_sinbib.py`, `forma_representante_sinbib.py`, `resumen_T.py`: cálculo anterior sobre las formas, conservado como referencia.
