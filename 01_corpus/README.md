# Corpus

Corpus comparable de 100 textos académicos sobre lingüística de corpus: 50 en inglés y 50 en español (artículos de revista, libros y manuales, y capítulos de libro).

## Ficheros

- `referencias_corpus.csv`: referencia bibliográfica de cada documento, con su lengua, tipo y enlace (DOI o URL) cuando existe. Es el Apéndice I de la tesis.
- `documentos_en.csv`, `documentos_es.csv`: un documento por fila.
  - `documento`: identificador (nombre del fichero de texto); `año`, `autoría`, `título`, `fuente`, `tipo`.
  - `tokens`, `oraciones`: tamaño según el análisis de spaCy (`en_core_web_trf`, `es_dep_news_trf`), sin espacios en blanco.
  - `tipos_alfabéticos`, `TTR`: formas distintas (en minúsculas) de los *tokens* alfabéticos y su proporción sobre esos *tokens*.
  - `spans_término`, `spans_entidad`: apariciones anotadas de términos y de entidades (nombres de recursos, herramientas y estándares).
  - `entradas_término_distintas`, `entradas_entidad_distintas`: entradas distintas de GLiCor anotadas en el documento.
- `estadisticos_subcorpus.csv`: totales por subcorpus.

Las pruebas de adecuación terminológica del capítulo 3 (cobertura, Heaps, dispersión DP y estabilidad) se añadirán con las cifras definitivas.
