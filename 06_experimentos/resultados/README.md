# Resultados

Una fila por ejecución, con todas las métricas descritas en el README de la carpeta superior. Los ficheros `*_todas.csv` contienen todas las ejecuciones y los `*_resumen.csv`, la media y la desviación típica por lengua y nivel.

## `crf/` (modelo basado en rasgos)

- `crf_reserva_*`: reserva de tipos (10, 20, 30 y 50 %; 10 semillas), solo términos.
- `crf_dos_*`: la misma reserva con términos y entidades etiquetados por separado.
- `crf_ablacion_*`: ablación por familias de rasgos con la reserva del 20 %.
- `crf_cv_todas.csv`: validación cruzada aleatoria de 5 pliegues.
- `crf_sensibilidad.csv`: seis combinaciones de regularización (`c1`, `c2`) con la reserva del 20 % y tres semillas.
- `crf_convergencia.csv`: 200 frente a 1000 iteraciones en una partición.

## `bilstm/` (modelo neuronal)

- `bilstm_reserva_*`: reserva de tipos, tres semillas (las mismas particiones que las semillas 0-2 del CRF); incluye la época elegida en validación.
- `bilstm_cv_todas.csv`: validación cruzada aleatoria de 5 pliegues.

## `clasificadores/` (*baseline*)

Clasificadores por *token*, con los mismos rasgos que el CRF y sin secuencia.

- `clasificadores_todas.csv`: cinco clasificadores con validación cruzada aleatoria y con la reserva del 20 % (tres particiones).
- `clasificadores_spans.csv`: evaluación por unidad completa de la regresión logística y el árbol de decisión.

## `errores/`

- `crf_aciertos_por_termino.csv`, `crf_falsos_positivos_{en,es}.csv` y `crf_*_resumen.json`: análisis de errores del CRF (unidades reconocidas enteras, en parte o perdidas; términos espurios).
- `span_longitud_secuenciales.csv`: unidades monoléxicas y poliléxicas delimitadas exactamente por el CRF y el BiLSTM-CRF.
- `vocabulario_reservados.csv`: recuperación de los términos reservados según contengan o no palabras fuera del vocabulario de entrenamiento del BiLSTM-CRF.

## `predicciones/`

Predicciones de las ejecuciones de reserva de tipos y de validación cruzada de los dos modelos. Cada fichero tiene una fila por *token* con el documento, la oración, la posición y las etiquetas real (`gold`) y predicha (`pred`). No incluyen las palabras, para que no puedan reconstruirse los textos del corpus. Las predicciones del resto de las ejecuciones están disponibles a petición.
