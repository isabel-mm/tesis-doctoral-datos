# Experimentos

Datos del capítulo 8 de la tesis (y del diseño experimental del capítulo 4). Para una lectura de conjunto, empiece por `resultados_completos.pdf`, que reúne en tablas el entorno de trabajo, los hiperparámetros y los resultados desglosados. Los términos técnicos se explican en el README principal.

La tesis compara dos modelos de reconocimiento de términos, uno por cada respuesta posible a la pregunta de si hacen falta rasgos o basta con la distribución de las palabras en el texto, y un *baseline* de clasificadores que deciden sobre cada palabra por separado:

1. **Modelo de aprendizaje automático basado en rasgos**: un CRF que recibe, para cada palabra, 27 rasgos lingüísticos y estadísticos (`rasgos_crf.csv`).
2. **Modelo neuronal basado en distribuciones**: un BiLSTM-CRF que no recibe rasgos y aprende sus propias representaciones de las palabras a partir del corpus.

3. **Baseline**: cinco clasificadores clásicos (regresión logística, SVM lineal, Naive Bayes, árbol de decisión y Random Forest) con los mismos 27 rasgos que el CRF, pero sin tener en cuenta la secuencia.

Los hiperparámetros están en `hiperparametros.csv`.

## Protocolo de evaluación

- **Reserva de tipos** (protocolo principal): se reserva al azar un 10, 20, 30 o 50 % de las entradas de término de GLiCor; toda oración que contenga alguna de ellas va al conjunto de prueba, y el resto, al de entrenamiento. Así ningún término evaluado se ha visto al entrenar, y todas las formas de un mismo concepto caen en la misma partición. Se repite con 10 semillas, las mismas para el CRF y el BiLSTM-CRF; los dos modelos se comparan partición a partición con la prueba de Wilcoxon y la corrección de Holm.
- **Sin fuga de datos**: los rasgos estadísticos (frecuencia, frecuencia documental, TF-IDF, dispersión contextual, PMI) se calculan solo con las oraciones de entrenamiento de cada partición.
- **Dos etiquetas**: misma reserva, pero con términos y entidades etiquetados por separado (`B-T/I-T` y `B-E/I-E`).
- **Ablación**: se reentrena el CRF sin cada una de las 9 familias de rasgos, con 10 repeticiones en cada nivel de reserva y, como contraste, con la validación cruzada. Se mide cuánto cambia el F1 de término y cuánto cambia la recuperación de los términos reservados, los que el modelo no ha visto.
- **Validación externa en ACTER** (inglés): reserva del 20 % de los tipos con las mismas 10 semillas y *leave-one-domain-out* (LODO), con el CRF y el BiLSTM-CRF (cinco semillas por dominio).
- **Validación cruzada estándar** de 5 pliegues, con particiones aleatorias, como contraste: mide cuánto se sobrestima el rendimiento cuando las apariciones de un mismo término se reparten entre entrenamiento y prueba.

## Métricas

Para cada ejecución se guardan, sobre el conjunto de prueba completo y, por separado, sobre los *tokens* de las entradas reservadas (`res_*`, términos nunca vistos) y sobre el resto (`vis_*`):

- por etiqueta (`bt`, `it`, `o`; `be`, `ie` con dos etiquetas): verdaderos positivos, falsos positivos, falsos negativos, verdaderos negativos, soporte, precisión, recuperación y F1;
- término frente a palabra: los mismos recuentos y medidas; `f1_termino` es la métrica principal de la tesis;
- medias macro y ponderada (`f1_global`) y exactitud;
- por *span* de término: coincidencia exacta y parcial, y *spans* exactos, parciales, perdidos y espurios.

## Código

`scripts/` contiene el código completo: generación de la anotación (`paso1_generar_bio.py`, `glicor_match.py`), CRF (`crf_base.py`, `paso2_crf.py`), BiLSTM-CRF (`paso3_bilstm.py`), análisis de errores (`paso4_errores.py`), análisis de palabras fuera de vocabulario (`paso5_vocabulario.py`), *baseline* (`paso6_clasificadores.py`), sensibilidad y convergencia del CRF (`paso7_sensibilidad_crf.py`, `paso8_convergencia_crf.py`), recuperación por frecuencia del tipo (`paso9_recall_frecuencia.py`), tipología y tabla de errores (`paso10_tipologia_errores.py`, `paso11_tabla_errores.py`), figuras de barras del capítulo 8 (`figuras_cap6_barras.py`), figuras de épocas del BiLSTM-CRF (`figuras_cap6_epocas.py`) y métricas (`metricas.py`).

Los resultados de todas las ejecuciones están en `resultados/` (véase su README).
