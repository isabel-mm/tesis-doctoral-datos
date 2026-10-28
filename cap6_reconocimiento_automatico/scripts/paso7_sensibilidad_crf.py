"""
paso7_sensibilidad_crf.py
─────────────────────────
Sensibilidad del CRF a la regularización (cap. 4: los valores c1 = 0,05 y
c2 = 0,01 se fijaron de antemano). Se reentrena el CRF con los 27 rasgos en la
reserva de tipos del 20 %, semillas 0-2 (las mismas particiones que el resto de
los experimentos), con c1 ∈ {0,05; 0,1; 0,5} y c2 ∈ {0,01; 0,1}. La combinación
de la tesis (0,05; 0,01) se recalcula también, como referencia.

Uso:    python3 colab_reanotacion/scripts/paso7_sensibilidad_crf.py [--jobs 3]
Salida: resultados/crf/crf_sensibilidad.csv
"""
import itertools
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn_crfsuite

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import crf_base as base  # noqa: E402
from metricas import metricas_completas  # noqa: E402
from paso2_crf import metricas_restringidas  # noqa: E402

DEST = HERE.parent / "resultados" / "crf" / "crf_sensibilidad.csv"
C1 = [0.05, 0.1, 0.5]
C2 = [0.01, 0.1]
DATA = {}


def cargar(lang):
    if lang not in DATA:
        df = base.attach_span_text(base.load_corpus(lang), solo_terminos=True)
        DATA[lang] = (base.build_sentences(df), np.array(sorted(df["_span_text"].dropna().unique())))
    return DATA[lang]


def ejecutar(t):
    lang, seed, c1, c2 = t
    t0 = time.time()
    sentences, span_types = cargar(lang)
    train, test, reservadas = base.split_by_type_holdout(sentences, span_types, 20, seed=seed)
    stats_get, stat_bounds = base.recompute_freq_stats(train)
    pmi_fn = base.compute_pmi_lookup(train)
    pmi_bounds = base.pmi_quartile_bounds(train, pmi_fn)
    Xtr, ytr = base.build_features_for_sentences(train, stats_get, stat_bounds, pmi_fn, pmi_bounds, lang)
    Xte, yte = base.build_features_for_sentences(test, stats_get, stat_bounds, pmi_fn, pmi_bounds, lang)
    crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=c1, c2=c2, max_iterations=200)
    crf.fit(Xtr, ytr)
    ypr = crf.predict(Xte)
    fila = {"lang": lang, "seed": seed, "c1": c1, "c2": c2}
    fila.update(metricas_completas(yte, ypr))
    fila.update(metricas_restringidas(test, yte, ypr, reservadas))
    fila["segundos"] = round(time.time() - t0, 1)
    print(f"{lang} s{seed} c1={c1} c2={c2}: F1 término={fila['f1_termino']:.3f} ({fila['segundos']:.0f}s)", flush=True)
    return fila


def main():
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
    hechas = pd.read_csv(DEST) if DEST.exists() else pd.DataFrame(columns=["lang", "seed", "c1", "c2"])
    ya = {(r.lang, int(r.seed), float(r.c1), float(r.c2)) for r in hechas.itertuples()}
    tareas = [t for t in itertools.product(["en", "es"], [0, 1, 2], C1, C2) if t not in ya]
    for lang in ("en", "es"):
        cargar(lang)  # se carga antes del fork para compartir los datos
    with Pool(jobs) as pool:
        for fila in pool.imap_unordered(ejecutar, tareas):
            hechas = pd.concat([hechas, pd.DataFrame([fila])], ignore_index=True)
            hechas.to_csv(DEST, index=False)


if __name__ == "__main__":
    main()
