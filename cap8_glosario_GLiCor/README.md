# GLiCor: glosario bilingüe de lingüística de corpus

Los datos del glosario del capítulo 7 de la tesis: 261 entradas (151 términos y 110 entidades), cada una con sus denominaciones en inglés y en español. La forma más cómoda de consultarlo es su versión web: <https://isabel-mm.github.io/GLiCor/>.

## Documento

Las frecuencias son las apariciones anotadas de cada entrada en el corpus, sin sus secciones de referencias bibliográficas.

- `registro_normalizacion_glosario.pdf`: las decisiones con que se reúnen en una sola entrada las variantes, siglas, sinónimos y préstamos de cada concepto, el método con que se cuentan sus frecuencias y la comprobación de las formas que el glosario da como no documentadas.

## Datos

Están en formato JSON, el que lee la versión web. Se abren con cualquier editor de texto o con un navegador.

- `entries.json`: las 261 entradas. Para cada una: las denominaciones principales (`term_en`, `term_es`), la categoría temática (`category`), el tipo (`type`: término o entidad), las fuentes (`sources`), las frecuencias en cada subcorpus (`freq`, `docs`), los equivalentes (`equiv_en`, `equiv_es`), las relaciones con otras entradas (`relations_es`), todas sus formas (`forms`) y, si es el caso, la laguna terminológica (`gap`).
- `normalizacion.json`: el mismo registro de normalización que el PDF, en forma de datos: los tipos de decisión, las entradas unificadas con su criterio, las que se mantienen separadas y las formas que se cuentan de cada una.
