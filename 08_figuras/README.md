# Figuras

Figuras de datos de los capítulos 5, 6 y 7 en alta resolución, con la paleta de la tesis (morado para el CRF y verde para el BiLSTM-CRF).

- Capítulo 5: `10_saturacion_terminologica.png`, `11_zipf_general_vs_termino.png`, `12_zipf_visual_simple.png`.
- Capítulo 6: `01_holdout_tecla_barras.png` (F1 global), `10_holdout_termino_barras.png` (F1 de término), `confusion_matrices.png`, `13_acter_validacion.png`.
- Capítulo 7: `fig_categorias_glosario.png`.

## Scripts

Tal como se ejecutaron en el repositorio de trabajo de la tesis (las rutas remiten a él):

- `figuras_distribucion.py`: las tres figuras del capítulo 5, a partir de las salidas del análisis de distribución (recogidas en `05_distribucion/`).
- `figuras_modelos.py`: `confusion_matrices.png`, a partir de `06_experimentos/resultados/`.
- `figuras_categorias_acter.py`: `fig_categorias_glosario.png` y `13_acter_validacion.png`.
- Las dos figuras de barras del capítulo 6 las genera `06_experimentos/scripts/figuras_cap6_barras.py`.
