"""
Propiedades distribucionales del inventario (cap. 5) sobre la anotación nueva
(proyección de GLiCor, 5 de octubre de 2026). Mismas medidas que
tesis/terminologicidad_2026-10/distribucion_terminos.py; cambia la fuente:

  - Términos: colab_reanotacion/datos_generados/{en,es}_bio_tokens_terms_only.csv.
    Un tipo de término es la ENTRADA de GLiCor (columna «entrada»): todas sus
    formas (flexión, variantes, siglas, préstamos) cuentan como un mismo tipo,
    como en el glosario y en la unidad de reserva de los modelos. Se calcula
    también por forma superficial en minúscula, para comparar.
  - Vocabulario general: {en,es}_bio_tokens.csv, tokens en minúscula sin
    puntuación (el texto ya está reparado).
  - Análisis de sensibilidad: ES sin los textos de Rojo.

Uso:    python3 tesis/reanotacion_2026-10/distribucion_reanotacion.py
Salida: en esta carpeta, {zipf_termino,zipf_general,saturacion}_{en,es}[_sinrojo].csv,
        zipf_exponentes.csv y resumen_distribucion.txt
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tesis/terminologicidad_2026-10"))
import distribucion_terminos as base  # noqa: E402

BIO = ROOT / "colab_reanotacion/datos_generados"


def term_spans(lang, unit="entrada", exclude=None):
    df = pd.read_csv(BIO / f"{lang}_bio_tokens_terms_only.csv",
                     usecols=["doc_id", "sentence_id", "token_id", "token", "label_bio", "entrada"],
                     keep_default_na=False)
    if exclude:
        df = df[~df.doc_id.str.contains(exclude, case=False, regex=False)]
    df = df.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable").reset_index(drop=True)
    doc_len = df.groupby("doc_id", sort=False).size()
    pos_in_doc = df.groupby("doc_id", sort=False).cumcount().values
    spans, cur = [], None
    for i, (doc, tok, lab, ent) in enumerate(zip(df.doc_id, df.token.str.lower(), df.label_bio, df.entrada)):
        if lab == "B-T":
            if cur:
                spans.append(cur)
            cur = [doc, pos_in_doc[i], ent, [tok]]
        elif lab == "I-T" and cur and cur[0] == doc:
            cur[3].append(tok)
        else:
            if cur:
                spans.append(cur)
            cur = None
    if cur:
        spans.append(cur)
    return [(d, p, e if unit == "entrada" else " ".join(t)) for d, p, e, t in spans], doc_len


def general(lang, exclude=None):
    cols = ["doc_id", "token", "is_punct"]
    g = pd.read_csv(BIO / f"{lang}_bio_tokens.csv", usecols=cols, keep_default_na=False)
    if exclude:
        g = g[~g.doc_id.str.contains(exclude, case=False, regex=False)]
    g = g[g.is_punct.astype(int) == 0].token.str.lower()
    return Counter(g)


def run(lang, rng, suffix="", exclude=None):
    lines = []
    spans, doc_len = term_spans(lang, exclude=exclude)
    freq = Counter(t for _, _, t in spans)
    zt = pd.DataFrame(freq.most_common(), columns=["tipo", "frecuencia"])
    zt.insert(0, "rango", range(1, len(zt) + 1))
    zt.to_csv(HERE / f"zipf_termino_{lang}{suffix}.csv", index=False)
    zgc = general(lang, exclude)
    zg = pd.DataFrame(zgc.most_common(), columns=["tipo", "frecuencia"])
    zg.insert(0, "rango", range(1, len(zg) + 1))
    zg.to_csv(HERE / f"zipf_general_{lang}{suffix}.csv", index=False)
    a_t, a_g = base.zipf_alpha(zt.frecuencia), base.zipf_alpha(zg.frecuencia)
    forms = Counter(t for _, _, t in term_spans(lang, unit="forma", exclude=exclude)[0])
    a_f = base.zipf_alpha(list(forms.values()))
    curves, x80 = base.saturation(spans, doc_len, len(zt), rng)
    mean = curves.mean(axis=0)
    pd.DataFrame({"pct_tokens": base.GRID, "pct_tipos_media": mean,
                  "pct_tipos_p05": np.percentile(curves, 5, axis=0),
                  "pct_tipos_p95": np.percentile(curves, 95, axis=0)}
                 ).to_csv(HERE / f"saturacion_{lang}{suffix}.csv", index=False)
    x0, x1, y0, y1 = base.plateau(base.GRID, mean)
    f = zt.frecuencia
    top = ", ".join(f"{t} {100 * n / f.sum():.1f} %" for t, n in zt.head(5)[["tipo", "frecuencia"]].values)
    lines += [
        f"=== {lang.upper()}{suffix} ===",
        f"tokens del corpus: {doc_len.sum()} | documentos: {len(doc_len)}",
        f"tipos de término (entradas): {len(zt)} | formas distintas: {len(forms)} | ocurrencias: {f.sum()}",
        f"cinco primeros: {top}",
        f"mediana: {f.median():g} | hápax: {100 * (f == 1).mean():.1f} % | <11: {100 * (f < 11).mean():.1f} %",
        f"exponente de Zipf: términos (entradas) {a_t:.3f} | términos (formas) {a_f:.3f} | "
        f"vocabulario general {a_g:.3f} ({len(zg)} tipos)",
        f"saturación 80 %: media de la curva {base.GRID[np.searchsorted(mean, 80)]:.1f} % del corpus; "
        f"por orden: mediana {np.median(x80):.1f} %, p5-p95 {np.percentile(x80, 5):.1f}-{np.percentile(x80, 95):.1f} %",
        f"meseta más larga (tolerancia 2 pp): {x0:.1f}-{x1:.1f} % del corpus, {y0:.1f} -> {y1:.1f} % del inventario",
        "",
    ]
    exp = dict(Lang=lang.upper() + suffix, Exponente_general=round(a_g, 3),
               Exponente_termino=round(a_t, 3), Exponente_termino_formas=round(a_f, 3),
               N_tipos_general=len(zg), N_tipos_termino=len(zt))
    return lines, exp


def main():
    rng = np.random.default_rng(base.SEED)
    lines, exps = [], []
    for lang, suffix, excl in (("en", "", None), ("es", "", None), ("es", "_sinrojo", "_Rojo, G.")):
        l, e = run(lang, rng, suffix, excl)
        lines += l
        exps.append(e)
        print("\n".join(l), flush=True)
    pd.DataFrame(exps).to_csv(HERE / "zipf_exponentes.csv", index=False)
    (HERE / "resumen_distribucion.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
