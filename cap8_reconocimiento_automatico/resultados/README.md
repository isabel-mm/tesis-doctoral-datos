# Resultados

Una fila por ejecución, con todas las métricas descritas en el README de la carpeta superior. Los ficheros `*_todas.csv` contienen todas las ejecuciones y los `*_resumen.csv`, la media y la desviación típica por lengua y nivel.

## `crf/` (modelo basado en rasgos)

- `crf_reserva_*`: reserva de tipos (10, 20, 30 y 50 %; 10 semillas), solo términos.
- `crf_dos_*`: la misma reserva con términos y entidades etiquetados por separado.
- `crf_ablacion_todas.csv`, `crf_ablacion_resumen.csv`: ablación por familias de rasgos en los cuatro niveles de reserva (10 semillas, las mismas que `crf_reserva_*`). `delta_f1_termino` es la variación del F1 de término al retirar la familia, y `delta_recall_reservadas`, la de la recuperación de los términos reservados (un valor negativo indica que la familia aporta).
- `crf_ablacion_pruebas.csv`: pruebas estadísticas de la ablación (tabla de ablación del capítulo 8 de la tesis). Para cada familia, lengua, nivel y medida: la diferencia media en puntos, su desviación típica, cuántas de las 10 repeticiones son negativas y el valor *p* de una prueba *t*, sin corregir y con la corrección de Holm para comparaciones múltiples.
- `crf_ablacv_*`: la misma ablación con la validación cruzada de 5 pliegues.
- `crf_cv_todas.csv`: validación cruzada aleatoria de 5 pliegues.
- `crf_sensibilidad.csv`: seis combinaciones de regularización (`c1`, `c2`) con la reserva del 20 % y tres semillas.
- `crf_convergencia.csv`: 200 frente a 1000 iteraciones en una partición.

## `bilstm/` (modelo neuronal)

- `bilstm_reserva_*`: reserva de tipos, diez semillas (las mismas particiones que el CRF); incluye la época elegida en validación.
- `bilstm_cv_todas.csv`: validación cruzada aleatoria de 5 pliegues.
- `epocas/`: registro por época de cada ejecución (`reserva_<lengua>_p<nivel>_s<semilla>.csv` y `cv_<lengua>_f<pliegue>.csv`): pérdida media y métricas en el conjunto de validación. Una pérdida vacía indica que el entrenamiento divergió (valor no numérico); ocurre en algunas ejecuciones en inglés, siempre después de la época elegida.

## `comparacion/`

- `pruebas_crf_bilstm.csv`: comparación del CRF y el BiLSTM-CRF partición a partición (diez particiones por lengua y nivel): diferencia media, intervalo de confianza, victorias de cada modelo y valor *p* de la prueba de Wilcoxon, sin corregir y con la corrección de Holm sobre las ocho comparaciones (dos lenguas y cuatro niveles). La columna `diferencia_b_menos_a` es `modelo_b` menos `modelo_a`.

## `acter/`

Validación externa en la parte inglesa de ACTER, sin entidades nombradas.

- `acter_reserva_todas.csv`: reserva de tipos (CRF en los cuatro niveles; CRF y BiLSTM-CRF con el 20 %, diez semillas).
- `acter_lodo_todas.csv`: *leave-one-domain-out*; el CRF es determinista y el BiLSTM-CRF se entrena con cinco semillas por dominio.
- `acter_lodo_pruebas.csv`: prueba *t* de una muestra del BiLSTM-CRF frente al CRF en cada dominio, con la corrección de Holm.

## `clasificadores/` (*baseline*)

Clasificadores por *token*, con los mismos rasgos que el CRF y sin secuencia.

- `clasificadores_todas.csv`: cinco clasificadores con validación cruzada aleatoria y con la reserva del 20 % (tres particiones).
- `clasificadores_spans.csv`: evaluación por unidad completa de la regresión logística y el árbol de decisión.

## `errores/`

- `crf_aciertos_por_termino.csv`, `crf_falsos_positivos_{en,es}.csv` y `crf_*_resumen.json`: análisis de errores del CRF (unidades reconocidas enteras, en parte o perdidas; términos espurios).
- `apariciones_reservadas.csv.gz`: cada aparición de un término reservado en la prueba, para el CRF y el BiLSTM-CRF, en todas las particiones (también ACTER): el término esperado (`entrada`, `forma_esperada`), lo que predijo el modelo (`forma_predicha`), el resultado (`exacta`, `por_defecto`, `por_exceso`, `solapamiento` u `omitida`), si contiene alguna palabra desconocida (`con_oov`) y la frecuencia del tipo. Se identifican el documento y la oración, pero no se incluye su texto.
- `falsos_positivos.csv.gz`: unidades propuestas por cada modelo que no coinciden con ningún término, por partición.
- `analisis_por_nivel.csv`: medias por modelo, lengua y nivel de las proporciones de apariciones reconocidas enteras o en parte, de la delimitación exacta de monoléxicos y poliléxicos, de la recuperación de los términos reservados con y sin palabras desconocidas y por franja de frecuencia, y del reparto de errores sin la entrada `corpus` (`errsc_pct_*`), que es el que recoge la tabla de errores del capítulo 8.

## `predicciones/`

Predicciones de las ejecuciones de reserva de tipos y de validación cruzada de los dos modelos (las del BiLSTM-CRF, en las diez particiones de cada nivel). Cada fichero tiene una fila por *token* con el documento, la oración, la posición y las etiquetas real (`gold`) y predicha (`pred`). No incluyen las palabras, para que no puedan reconstruirse los textos del corpus. Las predicciones del resto de las ejecuciones están disponibles a petición.

## `recall_frecuencia.txt`

Recuperación de los términos reservados según la frecuencia del tipo (raros, ≤ 10 apariciones; medios, 11–100; frecuentes, > 100), por modelo, lengua y nivel (media de diez particiones). La figura `figuras/cap8/14_recall_frecuencia.png` muestra la reserva del 20 %.
