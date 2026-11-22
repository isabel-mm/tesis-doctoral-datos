# Glosario de referencia (CASS)

Los 38 términos del glosario del centro CASS (Lancaster) que sirvieron de punto de partida de la anotación y de referencia para comprobar que el corpus cubre la terminología del dominio (capítulo 3 de la tesis).

## Documento

- `cobertura_glosario_cass.pdf`: los 38 términos, sus equivalentes en español y la fuente de cada equivalente, en el formato de la tesis.

## Datos

- `cass_semilla_equivalentes.csv`: un término por fila.
  - `termino_en`: el término de CASS; `equivalente_es`: el equivalente con que se buscó en el subcorpus español; `fuente_equivalente`: el banco de datos terminológico de donde procede (*Propuesta*, si no figura en ninguno y se propone a partir del uso en publicaciones académicas).
- `cobertura_cass_en.csv`, `cobertura_cass_es.csv`: presencia de cada término (o de su equivalente) en cada subcorpus.
  - `entrada`: el término; `ocurrencias`: veces que aparece; `documentos`: en cuántos de los 50 documentos; `densidad_pct`: porcentaje que suponen sus apariciones sobre el total de *tokens* del subcorpus; `cubierta`: si aparece al menos una vez (`True`) o no (`False`).
