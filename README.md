# Material complementario de la tesis doctoral

**Modelo teórico-computacional para la extracción automática de términos: una aproximación desde las tecnologías del lenguaje**

Isabel Moyano Moreno · Universidad de Cádiz, 2026
Dirección: Prof. Dr. Miguel Casas Gómez y Prof. Dr. Mario Crespo Miguel

## Qué es este material

La tesis resume en tablas y figuras lo que aquí se ofrece completo: la relación de los textos del corpus, el inventario de términos, el registro de las decisiones del glosario y los resultados de todos los experimentos. Sirve para consultar con detalle lo que el texto resume y para comprobar sus cifras.

**No hace falta saber programar.** Los documentos principales están en PDF, y los datos, en tablas que se abren con una hoja de cálculo (Excel, LibreOffice Calc, Google Sheets). El código solo interesa a quien quiera repetir los experimentos.

## Por dónde empezar

| Si quiere… | Abra… |
|---|---|
| ver qué textos forman el corpus | [`cap3_corpus/registro_documental_corpus.pdf`](cap3_corpus/registro_documental_corpus.pdf) |
| ver los criterios con que se anotaron los términos | [`cap3_anotacion_de_terminos/README.md`](cap3_anotacion_de_terminos/README.md) |
| ver los 38 términos de partida (glosario CASS) y sus equivalentes en español | [`cap3_glosario_de_partida_CASS/cobertura_glosario_cass.pdf`](cap3_glosario_de_partida_CASS/cobertura_glosario_cass.pdf) |
| consultar todos los términos y entidades del corpus, con su frecuencia y su terminologicidad | [`cap5_inventario_de_terminos/inventario_bilingue.pdf`](cap5_inventario_de_terminos/inventario_bilingue.pdf) |
| consultar el glosario bilingüe GLiCor | su versión web: <https://isabel-mm.github.io/GLiCor/> |
| saber por qué el glosario agrupa, separa o nombra así cada entrada | [`cap7_glosario_GLiCor/registro_normalizacion_glosario.pdf`](cap7_glosario_GLiCor/registro_normalizacion_glosario.pdf) |
| consultar todos los resultados de los modelos de reconocimiento de términos | [`cap6_reconocimiento_automatico/resultados_completos.pdf`](cap6_reconocimiento_automatico/resultados_completos.pdf) |
| ver las figuras de la tesis en alta resolución | [`figuras/`](figuras/) |

## Documentos para leer (PDF)

Tienen el mismo formato que la tesis y pueden leerse por separado.

- **Registro documental del corpus** (`cap3_corpus/`, 11 págs.): la referencia bibliográfica de los 100 documentos del corpus, 50 en inglés y 50 en español, ordenados por lengua y tipo de publicación.
- **Cobertura del glosario de referencia** (`cap3_glosario_de_partida_CASS/`, 2 págs.): los 38 términos del glosario CASS que sirvieron de punto de partida de la anotación, con sus equivalentes en español y la fuente de cada uno.
- **Inventario bilingüe de términos y entidades** (`cap5_inventario_de_terminos/`, 18 págs.): todas las unidades validadas de cada lengua, ordenadas por terminologicidad, con sus frecuencias y medidas estadísticas.
- **Registro de normalización del glosario** (`cap7_glosario_GLiCor/`, 29 págs.): las decisiones con que se reúnen en una sola entrada las variantes, siglas y sinónimos de cada concepto, y el método con que se cuentan sus frecuencias.
- **Resultados completos e hiperparámetros** (`cap6_reconocimiento_automatico/`, 8 págs.): el entorno de trabajo, la configuración de los modelos y los resultados desglosados que el capítulo 6 resume.

## Datos en tablas (CSV)

Cada carpeta corresponde a un capítulo de la tesis y lleva su propio README, que explica qué contiene cada columna.

| Carpeta | Qué contiene | Capítulo |
|---|---|---|
| [`cap3_corpus/`](cap3_corpus/) | Los documentos del corpus: referencia, año, autoría, tipo y tamaño de cada uno; totales por lengua; pruebas de que el corpus es adecuado para estudiar la terminología del dominio (cobertura, crecimiento del vocabulario, dispersión, estabilidad). | 3 |
| [`cap3_glosario_de_partida_CASS/`](cap3_glosario_de_partida_CASS/) | Los términos de CASS y sus equivalentes, y cuántas veces aparece cada uno en el corpus. | 3 |
| [`cap3_anotacion_de_terminos/`](cap3_anotacion_de_terminos/) | Criterios de anotación; todas las formas que se anotan de cada entrada (siglas, variantes, sinónimos, préstamos); apariciones anotadas de cada entrada. | 3 |
| [`cap5_inventario_de_terminos/`](cap5_inventario_de_terminos/) | El inventario de términos y entidades de cada lengua con sus medidas: frecuencia, número de documentos, *TF-IDF*, *C-value*, *NC-value* e índice de terminologicidad. | 5 |
| [`cap5_distribucion_de_los_terminos/`](cap5_distribucion_de_los_terminos/) | Distribución de los términos: frecuencias ordenadas (ley de Zipf), curvas de saturación (cuántos términos nuevos aparecen al añadir textos) y estructura de las unidades. | 5 |
| [`cap6_reconocimiento_automatico/`](cap6_reconocimiento_automatico/) | Rasgos e hiperparámetros de los modelos y resultados de todas las ejecuciones: rendimiento, comparación con clasificadores sencillos, ablación por familias de rasgos, análisis de errores. | 4 y 6 |
| [`cap7_glosario_GLiCor/`](cap7_glosario_GLiCor/) | Las 261 entradas de GLiCor y su registro de normalización, en formato JSON (el que usa la versión web). | 7 |

**Cómo abrir un CSV en Excel con la configuración española.** Si las columnas aparecen juntas o los decimales salen mal, no abra el fichero con doble clic: use *Datos → Obtener datos → Desde texto/CSV* y elija como origen *UTF-8*, como delimitador la *coma* y, como configuración regional, una que use el *punto* como separador decimal (por ejemplo, *Inglés (Estados Unidos)*). LibreOffice Calc pregunta todo esto al abrir el fichero.

## Código

Las carpetas `scripts/` contienen el código, en Python, con que se han obtenido los datos y los resultados, tal como se ejecutó. La lista de librerías necesarias está en `cap6_reconocimiento_automatico/scripts/requirements.txt`. TECLA, la librería de extracción terminológica desarrollada en la tesis (capítulo 8), tiene su propio repositorio: <https://github.com/isabel-mm/TECLA>.

## Qué no se publica

Los **textos del corpus** son publicaciones académicas sujetas a derechos de autor, por lo que no se distribuyen; el registro documental permite localizar cada uno. Por la misma razón no se publican los ficheros de anotación palabra a palabra, que permitirían reconstruir los textos. Las predicciones de los modelos se publican sin las palabras: solo con la posición de cada palabra y sus etiquetas. Ambos están disponibles a petición para la evaluación de la tesis.

## Términos técnicos que aparecen en los ficheros

- ***Token***: cada palabra o signo del texto tal como aparece; es la unidad con que se mide el tamaño del corpus.
- **Tipo**: cada unidad distinta, con independencia de cuántas veces aparezca. *Corpus* es un tipo con miles de apariciones.
- **Entrada**: una entrada de GLiCor, que reúne todas las formas de un mismo concepto (singular y plural, sigla y forma desarrollada, sinónimos).
- **Término y entidad**: la tesis distingue los términos, que designan conceptos (*corpus de referencia*), de las entidades, nombres propios de corpus, herramientas y estándares (*BNC*, *Sketch Engine*, *XML*).
- **Etiquetas `B-T`, `I-T` y `O`**: forma de marcar los términos palabra a palabra. `B-T` señala la primera palabra de un término; `I-T`, las siguientes, y `O`, las palabras que no forman parte de ningún término. En *el corpus de referencia*, *el* es `O`, *corpus* es `B-T` y *de* y *referencia* son `I-T`. `B-E` e `I-E` hacen lo mismo con las entidades.
- **Unidad** (*span*): un término completo, de su primera a su última palabra.
- **Precisión, recuperación y F₁**: la precisión es la proporción de lo que el modelo marca como término que realmente lo es; la recuperación, la proporción de los términos del texto que el modelo encuentra, y el F₁, una media de las dos. La tesis usa como medida principal el **F₁ de término**.
- **Reserva de tipos**: el procedimiento de evaluación de la tesis. Se aparta al azar una parte de los términos (el 10, 20, 30 o 50 %) y se evalúa a los modelos con textos que los contienen, de modo que tienen que reconocer términos que nunca han visto.
- **Semilla o repetición**: cada uno de los sorteos de la reserva de tipos. El experimento se repite con varios sorteos y se da la media.
- **Validación cruzada**: la evaluación habitual, que reparte las oraciones al azar entre entrenamiento y prueba. La tesis la usa como contraste, porque sobreestima lo que los modelos han aprendido.
- **CRF**: el modelo basado en rasgos, que reconoce los términos a partir de 27 propiedades lingüísticas y estadísticas de cada palabra.
- **BiLSTM-CRF**: el modelo neuronal, que aprende por sí mismo sus representaciones de las palabras a partir del corpus.
- ***Baseline***: los clasificadores sencillos con que se comparan los modelos.
- **Ablación**: experimento en que se retira una familia de rasgos y se mide cuánto empeora el modelo, para saber qué aporta cada una.
- ***TF-IDF***, ***C-value***, ***NC-value*** e **índice de terminologicidad**: medidas estadísticas de hasta qué punto una unidad es característica del dominio; el índice de terminologicidad de la tesis combina el *TF-IDF* y el *NC-value*.

## Licencia y cita

Los datos se publican con licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) y el código, con licencia MIT (véase `LICENSE.md`). Para citar este material, véase `CITATION.cff`.

---

*English summary.* Supplementary material for the PhD thesis "A theoretical-computational model for automatic term extraction: an approach from language technologies" (Universidad de Cádiz, 2026). Readable PDF documents (corpus record, terminological inventory, glossary normalisation record, seed glossary coverage and full experimental results) and the underlying CSV data: corpus metadata and statistics, seed glossaries, annotation criteria and forms, terminological inventory, term distribution data, model features, hyperparameters and full results, and the data of the bilingual glossary GLiCor. The corpus texts and token-level annotation are not distributed for copyright reasons.
