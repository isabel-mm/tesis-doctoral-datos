"""
paso8_convergencia_crf.py
─────────────────────────
¿Converge el CRF con el tope de 200 iteraciones de la tesis? Se reentrena en la
reserva del 20 %, semilla 0, con 200 y con 1000 iteraciones (c1 = 0,05; c2 = 0,01)
y se registra en qué iteración se detiene L-BFGS y el F1 de término resultante.

Uso:    python3 colab_reanotacion/scripts/paso8_convergencia_crf.py
Salida: resultados/crf/crf_convergencia.csv
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn_crfsuite

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import crf_base as base  # noqa: E402
from metricas import metricas_completas  # noqa: E402
from paso2_crf import metricas_restringidas  # noqa: E402

DEST = HERE.parent / "resultados" / "crf" / "crf_convergencia.csv"
filas = []
for lang in ("en", "es"):
    df = base.attach_span_text(base.load_corpus(lang), solo_terminos=True)
    sentences = base.build_sentences(df)
    span_types = np.array(sorted(df["_span_text"].dropna().unique()))
    train, test, reservadas = base.split_by_type_holdout(sentences, span_types, 20, seed=0)
    stats_get, stat_bounds = base.recompute_freq_stats(train)
    pmi_fn = base.compute_pmi_lookup(train)
    pmi_bounds = base.pmi_quartile_bounds(train, pmi_fn)
    Xtr, ytr = base.build_features_for_sentences(train, stats_get, stat_bounds, pmi_fn, pmi_bounds, lang)
    Xte, yte = base.build_features_for_sentences(test, stats_get, stat_bounds, pmi_fn, pmi_bounds, lang)
    for it in (200, 1000):
        t0 = time.time()
        crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.05, c2=0.01, max_iterations=it)
        crf.fit(Xtr, ytr)
        ypr = crf.predict(Xte)
        log = crf.training_log_
        fila = {"lang": lang, "max_iter": it, "iteraciones_hechas": log.last_iteration.get("num"),
                "perdida_final": log.last_iteration.get("loss")}
        m = metricas_completas(yte, ypr)
        fila.update({k: m[k] for k in ("p_termino", "r_termino", "f1_termino", "f1_span_exacto")})
        fila["res_r_termino"] = metricas_restringidas(test, yte, ypr, reservadas).get("res_r_termino")
        fila["segundos"] = round(time.time() - t0, 1)
        filas.append(fila)
        print(fila, flush=True)
        pd.DataFrame(filas).to_csv(DEST, index=False)
