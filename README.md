# Material complementario de la tesis doctoral

**Modelo teórico-computacional para la extracción automática de términos: una aproximación desde las tecnologías del lenguaje**

Isabel Moyano Moreno · Universidad de Cádiz, 2026
Dirección: Prof. Dr. Miguel Casas Gómez y Prof. Dr. Mario Crespo Miguel

Este repositorio reúne los datos y resultados en que se basa la tesis, para que el tribunal y cualquier lector puedan consultarlos y comprobarlos. El nombre de cada carpeta indica el capítulo de la tesis al que corresponde, y cada una lleva, cuando hace falta, su propio README. TECLA (capítulo 8) tiene su propio repositorio.

## Contenido

| Carpeta | Qué contiene | En la tesis |
|---|---|---|
| `cap3_corpus/` | Registro documental del corpus: los 100 documentos (50 EN, 50 ES) con su referencia bibliográfica, en CSV y en PDF (`registro_documental_corpus.pdf`); estadísticos por documento y por subcorpus; pruebas de adecuación terminológica (cobertura, Heaps, dispersión DP, estabilidad) | Cap. 3 |
| `cap3_glosarios_semilla/` | Los 38 términos semilla de CASS con sus equivalentes en español y su fuente; cobertura de ambos listados en el corpus; versión legible en `cobertura_glosario_cass.pdf` | Cap. 3 |
| `cap3_anotacion/` | Criterios de anotación; formas que se anotan de cada entrada de GLiCor; apariciones anotadas por entrada | Cap. 3 |
| `cap5_inventario/` | Inventario terminológico validado: términos y entidades, categoría, frecuencia, frecuencia documental, TF-IDF, C-value, NC-value e índice de terminologicidad *T*; versión legible en `inventario_bilingue.pdf` | Cap. 5 |
| `cap5_distribucion/` | Datos de Zipf (vocabulario terminológico y general) y curvas de saturación | Cap. 5 |
| `cap6_experimentos/` | Rasgos del modelo basado en rasgos, hiperparámetros, protocolo de evaluación, código y resultados de todas las ejecuciones con todas sus métricas: *baseline*, CRF, BiLSTM-CRF, ablación, análisis de errores y de palabras fuera de vocabulario; entorno computacional, hiperparámetros y resultados completos por etiqueta en `resultados_completos.pdf` | Caps. 4 y 6 |
| `cap7_glicor/` | Datos del glosario bilingüe GLiCor: 261 entradas y registro de normalización (`normalizacion.json` y, en versión legible, `registro_normalizacion_glosario.pdf`) | Cap. 7 |
| `figuras/` | Figuras de la tesis en alta resolución, en una subcarpeta por capítulo | Caps. 5, 6 y 7 |

**Recursos relacionados**

- TECLA, la librería de extracción terminológica desarrollada en la tesis: <https://github.com/isabel-mm/TECLA>
- GLiCor, versión digital del glosario: <https://isabel-mm.github.io/GLiCor/>

## Qué no se publica

Los **textos del corpus** son publicaciones académicas sujetas a derechos de autor, por lo que no se distribuyen; `cap3_corpus/referencias_corpus.csv` permite localizar cada uno. Por la misma razón no se publican los ficheros de anotación **token a token** (BIO), que permitirían reconstruir los textos. Las predicciones de los modelos se publican sin las palabras: solo con la posición de cada *token* y sus etiquetas. Ambos están disponibles a petición para la evaluación de la tesis.

## Formato

Todos los datos tabulares están en CSV (UTF-8, separador coma). Los números decimales usan punto.

## Licencia y cita

Los datos se publican con licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) y el código, con licencia MIT (véase `LICENSE.md`). Para citar este material, véase `CITATION.cff`.

---

*English summary.* Supplementary material for the PhD thesis "A theoretical-computational model for automatic term extraction: an approach from language technologies" (Universidad de Cádiz, 2026): corpus metadata and statistics, seed glossaries, terminological inventory, annotation criteria, term distribution data, experimental setup, code and full results, and the data of the bilingual glossary GLiCor. The corpus texts and token-level annotation are not distributed for copyright reasons.
