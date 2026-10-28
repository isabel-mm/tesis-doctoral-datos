# Figuras

Figuras de datos de los capítulos 5, 6 y 7 en alta resolución, con la paleta de la tesis (morado para el CRF y verde para el BiLSTM-CRF), organizadas en una subcarpeta por capítulo.

- `cap5/`: `10_saturacion_terminologica.png`, `11_zipf_general_vs_termino.png`, `12_zipf_visual_simple.png`.
- `cap6/`: `01_holdout_tecla_barras.png` (F1 global), `10_holdout_termino_barras.png` (F1 de término), `confusion_matrices.png`, `13_acter_validacion.png`, `11_bilstm_epocas_simple.png` (F1 de término en validación por época, 20 % reservado), `14_recall_frecuencia.png` (recuperación de los términos reservados según la frecuencia del tipo) y `11_bilstm_epocas.png` (F1 de término en validación por época, todos los niveles de reserva; Figura 6.4 de la tesis).
- `cap7/`: `fig_categorias_glosario.png`.

## Scripts

Tal como se ejecutaron en el repositorio de trabajo de la tesis (las rutas remiten a él):

- `figuras_distribucion.py`: las tres figuras del capítulo 5, a partir de las salidas del análisis de distribución (recogidas en `cap5_distribucion_de_los_terminos/`).
- `figuras_modelos.py`: `confusion_matrices.png`, a partir de `cap6_reconocimiento_automatico/resultados/`.
- `figuras_categorias_acter.py`: `fig_categorias_glosario.png` y `13_acter_validacion.png`.
- Las dos figuras de barras del capítulo 6 las genera `cap6_reconocimiento_automatico/scripts/figuras_cap6_barras.py`.
- Las dos figuras de épocas las genera `cap6_reconocimiento_automatico/scripts/figuras_cap6_epocas.py`, a partir de los registros por época de `cap6_reconocimiento_automatico/resultados/bilstm/epocas/`.
- La figura de la recuperación según la frecuencia la genera `cap6_reconocimiento_automatico/scripts/figuras_cap6_frecuencia.py`, con las cifras de `cap6_reconocimiento_automatico/resultados/recall_frecuencia.txt`.
