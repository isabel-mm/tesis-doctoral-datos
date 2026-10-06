# Criterios de anotación

Tomados del capítulo 3 de la tesis (§ «Anotación terminológica»).

La anotación del corpus se ha implementado en `Doccano` como un proyecto de etiquetado secuencial, en el que cada unidad terminológica se ha marcado con la etiqueta `term`. Los criterios aplicados, que son los mismos que guiaron la validación del inventario, son los siguientes. Ninguno de ellos basta por sí solo: una unidad se anota cuando el conjunto de los criterios indica que funciona como término en el texto.

- **Criterio de categoría gramatical.** Los términos son, de forma predominante, unidades nominales. Se anotan, por ello, los sustantivos y sintagmas nominales que responden a los patrones de la gramática terminológica, como *corpus*, *representatividad*, *corpus de referencia* o *natural language processing*. Se admiten, excepcionalmente, adjetivos que designan por sí solos un concepto del dominio, como *synchronic*, que se emplea como término para caracterizar un tipo de corpus. No se anotan, en cambio, los verbos, aunque pertenezcan a la misma familia que un término: se anota *lematización*, pero no *lematizar*.

- **Criterio de pertenencia al dominio.** Se anotan los conceptos de la lingüística de corpus y de las disciplinas de las que se nutre, como la estadística (*standard deviation*, *log-likelihood*), el procesamiento del lenguaje natural (*regular expression*, *named entity recognition*) o la lexicografía (*concordancia*). No se anota el léxico académico general, que aparece en cualquier disciplina científica (*análisis*, *método*, *resultado*, *data*), aunque sea muy frecuente en el corpus.

- **Criterio de estabilidad denominativa.** Se anotan las formas que la bibliografía emplea de manera constante para designar un concepto, y no las formulaciones ocasionales con que un autor lo parafrasea en un texto concreto. La frecuencia en el corpus no es, por sí sola, un requisito: *keyword* aparece 296 veces en 16 documentos, pero *z-score* o *inter-rater reliability* se anotan aunque aparezcan una sola vez, porque son denominaciones consolidadas en la disciplina.

- **Criterio de institucionalización.** Algunas expresiones nacen como descripciones o metáforas y terminan fijándose como denominación de un concepto. Se anotan cuando el discurso de la disciplina las emplea ya como tales, como *semantic prosody* (la tendencia de una palabra a aparecer en contextos con una determinada carga valorativa), *lexical bundles*, *web as corpus* o *word sketch*.

- **Criterio de relación con términos ya anotados.** Los términos de un dominio forman series. Se anotan las unidades que se relacionan con términos ya identificados, porque especifican el mismo núcleo (*corpus especializado*, *corpus general*, *corpus de referencia* o *corpus diacrónico*) o porque derivan de ellos (*lemma* y *lemmatisation*).

- **Criterio de variación.** Un mismo término puede presentarse con formas distintas, y se anotan todas: las siglas y sus formas desarrolladas (*part-of-speech tagging* y *`POS` tagging*), las variantes flexivas y las reordenaciones de sus componentes (*lingüística de corpus computacional* y *lingüística computacional de corpus*). Se anotan también los préstamos sin adaptar que el discurso en español emplea en lugar de una forma propia, como *keywords* o *wordlist*.

- **Criterio de delimitación.** Como la anotación `BIO` no admite solapamientos, cuando un término aparece dentro de una cadena terminológica más larga se anota la cadena entera, y no cada uno de los términos que contiene: en *reference corpus* se marca la cadena completa, aunque *corpus* sea también un término, y *corpus* solo se anota por separado cuando aparece de forma autónoma. Así, cada ocurrencia recibe una sola etiqueta y la unidad anotada es la que funciona como denominación en ese contexto. La relación entre los términos nucleares y las cadenas que los contienen no se pierde por ello: se analiza sobre el inventario en el la tesis.

- **Criterio de inclusión de recursos.** Se anotan también los nombres de los recursos con que trabaja la disciplina —corpus, herramientas y estándares—, como *BNC*, *CREA*, `Sketch Engine`, `FreeLing` o *XML*, porque forman parte del vocabulario especializado con que la lingüística de corpus se refiere a sus objetos de trabajo. En esta fase se anotan del mismo modo que el resto de las unidades; su naturaleza y su tratamiento se analizan sobre el inventario en el la tesis.

## Cómo se obtiene el *Gold Standard* final

El corpus se revisó texto a texto; el *Gold Standard* que usan los modelos se obtiene proyectando sobre el texto todas las formas de las entradas de GLiCor (`formas_por_entrada.csv`): flexión, variantes formales, siglas y formas desarrolladas, sinónimos y préstamos. La búsqueda sigue el método de recuento del glosario: se reparan los artefactos de la conversión desde PDF; la coincidencia es exacta, sin distinguir mayúsculas (ni tildes en español) y con límites de palabra; se aplican las exclusiones por contexto de cada forma, y no se cuentan las etiquetas de metadatos de los artículos («Palabras clave:», «Keywords:»). Cuando dos formas se solapan se anota la más larga (criterio de delimitación). Cada *span* conserva la entrada de GLiCor a la que pertenece.

## Ficheros

- `formas_por_entrada.csv`: todas las formas que se anotan, por entrada y lengua, con su relación (lema, sigla, sinónimo, préstamo…) y sus exclusiones.
- `apariciones_por_entrada_{en,es}.csv`: apariciones anotadas de cada entrada en cada subcorpus.

Los ficheros BIO completos (un *token* por fila) no se publican porque permiten reconstruir los textos, que están sujetos a derechos de autor; están disponibles a petición para la evaluación de la tesis.
