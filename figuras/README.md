# Figuras

Figuras de datos de los capítulos 6, 7 y 8 en alta resolución, con la paleta de la tesis (morado para el CRF y verde para el BiLSTM-CRF), organizadas en una subcarpeta por capítulo.

- `cap6/`: `10_saturacion_terminologica.png`, `11_zipf_general_vs_termino.png`, `12_zipf_visual_simple.png`.
- `cap7/`: `fig_categorias_glosario.png`.
- `cap8/`: `baseline_cv_reserva.png` (clasificadores por *token*: validación cruzada frente a reserva del 20 %), `10_holdout_termino_barras.png` (F1 de término de los dos modelos, diez repeticiones), `11_bilstm_epocas_simple.png` (F1 de término en validación por época, reserva del 20 %, diez particiones), `14_recall_frecuencia.png` (recuperación de los términos reservados según la frecuencia del tipo) y `13_acter_validacion.png` (ACTER: reserva del 20 % y LODO). Las cuatro últimas se obtienen de los resultados de `reconocimiento_automatico/resultados/`.

## Scripts

Tal como se ejecutaron en el repositorio de trabajo de la tesis (las rutas remiten a él):

- `figuras_distribucion.py`: las tres figuras del capítulo 6, a partir de las salidas del análisis de distribución (recogidas en `distribucion_de_los_terminos/`).
- `figuras_categorias_acter.py`: `fig_categorias_glosario.png` y `13_acter_validacion.png`.
- Las dos figuras de barras del capítulo 8 las genera `reconocimiento_automatico/scripts/figuras_cap6_barras.py`.
- Las dos figuras de épocas las genera `reconocimiento_automatico/scripts/figuras_cap6_epocas.py`, a partir de los registros por época de `reconocimiento_automatico/resultados/bilstm/epocas/`.
- La figura de la recuperación según la frecuencia la genera `reconocimiento_automatico/scripts/figuras_cap6_frecuencia.py`, con las cifras de `reconocimiento_automatico/resultados/recall_frecuencia.txt`.
