"""
Tests de adecuación terminológica del corpus (cap. 3, §evaluacion) sobre los
tokens de la reanotación (spaCy trf, 5 de octubre de 2026). Mismo método que
tesis/representatividad_2026-09/tests_representatividad.py y que los scripts de
cobertura de resultados_experimentos/06_glosario_semilla; cambian los datos:

  - Cobertura: CASS (38 términos) sobre el subcorpus inglés y Rojo (2021, 89
    entradas) sobre el español, con y sin el libro que contiene el glosario.
    Coincidencia de secuencias de lemas (o de formas) en minúscula, dentro de
    la misma oración; en español, sin diacríticos. Los lemas de las entradas se
    obtienen con los mismos modelos que el corpus (en_core_web_trf,
    es_dep_news_trf).
  - Saturación: ley de Heaps sobre los lemas alfabéticos, en el orden original
    de los documentos y en 50 órdenes aleatorios.
  - Dispersión: DP de Gries de los 50 tipos de término más frecuentes.
  - Estabilidad: bootstrap de documentos (B = 200), top-30.
  Tipo de término = unidad normalizada (columna «entrada»), como en el cap. 5.

Uso:    python3 tesis/reanotacion_2026-10/adecuacion_reanotacion.py
Salida: adecuacion_resultados.csv, adecuacion_dp_top50.csv,
        cobertura_cass_en.csv, cobertura_rojo_es.csv
"""
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import spacy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# Anotación sin las bibliografías (tesis/sin_bibliografia_2026-11): las secciones de
# referencias no forman parte del discurso especializado (cap. 3). TESIS_BIO permite
# usar otra carpeta, p. ej. colab_reanotacion/datos_generados (con bibliografías).
BIO = Path(__import__("os").environ.get("TESIS_BIO", ROOT / "colab_reanotacion/datos_generados_sinbib"))
SEMILLA = ROOT / "resultados_experimentos/06_glosario_semilla"
BOOK = "ES::2021_Rojo, G._Introducción a la lingüística de corpus en español"
SEED = 42
N_ORDERS, B, TOP_DP, TOP_STAB = 50, 200, 50, 30

CASS = [
    "corpus", "text", "annotation", "keyword", "type", "tagging", "sample", "XML",
    "token", "corpus-based", "markup", "diachronic", "metadata", "representativeness",
    "reference corpus", "concordance", "node", "collocation", "balance", "synchronic",
    "frequency list", "encoding", "lemma", "comparability", "significance test",
    "markup language", "concordancer", "corpus construction", "corpus-driven",
    "statistical significance", "lexis", "lemmatisation", "monitor corpus",
    "sampling frame", "type-token ratio", "key word in context (KWIC)",
    "colligation", "sample corpus",
]
EXTRA_EN = {  # mismas formas adicionales que regenerar_cobertura_cass.py
    "corpus-based": ["corpus base", "corpus based", "corpusbased"],
    "corpus-driven": ["corpus drive", "corpus driven", "corpusdriven"],
    "type-token ratio": ["type token ratio"],
    "key word in context (KWIC)": ["kwic", "key word in context", "keyword in context"],
}


def norm(s, lang):
    s = str(s).lower()
    if lang == "es":
        s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return s


def load(lang):
    cols = ["doc_id", "sentence_id", "token_id", "token", "lemma", "is_alpha", "label_bio", "entrada"]
    return pd.read_csv(BIO / f"{lang}_bio_tokens_terms_only.csv", usecols=cols,
                       keep_default_na=False, low_memory=False)


# ---------- cobertura
def coverage(df, lang, entries, forms_of, nlp):
    d = df.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable")
    arrs = [d.lemma.map(lambda x: norm(x, lang)).values, d.token.map(lambda x: norm(x, lang)).values]
    doc, sent = d.doc_id.values, d.sentence_id.values

    def starts(seq):
        n, found = len(seq), set()
        for arr in arrs:
            for i in np.flatnonzero(arr == seq[0]):
                if i + n <= len(arr) and doc[i] == doc[i + n - 1] and sent[i] == sent[i + n - 1] \
                        and all(arr[i + j] == seq[j] for j in range(1, n)):
                    found.add((i, n))
        return found

    rows = []
    for e in entries:
        cands = set()
        for f in forms_of(e):
            seqs = {tuple(norm(t.lemma_, lang) for t in nlp(f) if not t.is_space),
                    tuple(norm(w, lang) for w in f.replace("-", " - ").split()),
                    tuple(norm(w, lang) for w in f.replace("-", " ").split())}
            for seq in seqs:
                if seq:
                    cands |= starts(list(seq))
        # de la secuencia más larga a la más corta, sin solapamientos
        used, spans = set(), []
        for i, n in sorted(cands, key=lambda x: (-x[1], x[0])):
            rng_ = set(range(i, i + n))
            if used.isdisjoint(rng_):
                used |= rng_
                spans.append(i)
        ds = {doc[i] for i in spans}
        rows.append(dict(entrada=e, ocurrencias=len(spans), documentos=len(ds),
                         densidad_pct=100 * len(spans) / len(d), cubierta=len(ds) > 0,
                         cubierta_sin_libro=len(ds - {BOOK}) > 0, solo_en_libro=ds == {BOOK}))
    return pd.DataFrame(rows)


def forms_en(term):
    base = term.split(" (")[0]
    return [base] + EXTRA_EN.get(term, [])


def forms_es(entry):
    out = []
    m = re.match(r"^(.*?)\s*\((.*)\)\s*$", entry)
    parts = [m.group(1), *re.split(r",\s*", m.group(2))] if m else [entry]
    for p in parts:
        out += [q for q in re.split(r"\s+o\s+", p) if q.strip()]
    return out


# ---------- saturación, dispersión, estabilidad
def heaps_beta(lemmas):
    seen, xs, ys = set(), [], []
    step = max(1, len(lemmas) // 5000)
    for i, l in enumerate(lemmas, 1):
        seen.add(l)
        if i % step == 0:
            xs.append(i)
            ys.append(len(seen))
    beta, logk = np.polyfit(np.log(xs), np.log(ys), 1)
    return beta, float(np.exp(logk)), len(seen)


def term_spans(df):
    per_doc = defaultdict(Counter)
    for doc, g in df.groupby("doc_id", sort=False):
        for lab, ent in zip(g.label_bio, g.entrada):
            if lab == "B-T":
                per_doc[ent][doc] += 1
    return per_doc


def gries_dp(counts, share):
    F = sum(counts.values())
    return 0.5 * sum(abs(counts.get(d, 0) / F - s) for d, s in share.items())


def run(lang, df):
    docs = list(dict.fromkeys(df.doc_id))
    alpha = df[df.is_alpha.astype(int) == 1]
    lem_by_doc = {d: g.lemma.astype(str).str.lower().tolist() for d, g in alpha.groupby("doc_id", sort=False)}
    beta0, k0, V = heaps_beta([l for d in docs for l in lem_by_doc.get(d, [])])
    rng = random.Random(SEED)
    betas = []
    for _ in range(N_ORDERS):
        order = docs[:]
        rng.shuffle(order)
        betas.append(heaps_beta([l for d in order for l in lem_by_doc.get(d, [])])[0])
    sizes = df.groupby("doc_id").size()
    share = (sizes / sizes.sum()).to_dict()
    spans = term_spans(df)
    freq = {t: sum(c.values()) for t, c in spans.items()}
    top = sorted(freq, key=freq.get, reverse=True)[:TOP_DP]
    dps = {t: gries_dp(spans[t], share) for t in top}
    top30 = set(sorted(freq, key=freq.get, reverse=True)[:TOP_STAB])
    rng = random.Random(SEED)
    kept = []
    for _ in range(B):
        sample = Counter(rng.choice(docs) for _ in docs)
        bf = {t: sum(c.get(d, 0) * n for d, n in sample.items()) for t, c in spans.items()}
        btop = set(sorted(bf, key=bf.get, reverse=True)[:TOP_STAB])
        kept.append(len(btop & top30) / TOP_STAB)
    res = dict(lengua=lang.upper(), tokens=len(df), tipos_lema=V,
               heaps_beta_orden_original=round(beta0, 3),
               heaps_beta_media_ordenes=round(float(np.mean(betas)), 3),
               heaps_beta_dt_ordenes=round(float(np.std(betas)), 3),
               tipos_termino=len(spans),
               dp_top50_media=round(float(np.mean(list(dps.values()))), 3),
               dp_top50_prop_menor_0_4=round(sum(v < 0.4 for v in dps.values()) / len(dps), 3),
               dp_top50_un_documento=sum(len(spans[t]) == 1 for t in top),
               estabilidad_top30_media=round(float(np.mean(kept)), 3))
    dp_rows = [dict(lengua=lang.upper(), termino=t, frecuencia=freq[t], documentos=len(spans[t]),
                    dp=round(dps[t], 3)) for t in top]
    return res, dp_rows


def main():
    out, dp_out = [], []
    for lang in ("en", "es"):
        df = load(lang)
        if lang == "en":
            nlp = spacy.load("en_core_web_trf")
            cov = coverage(df, lang, CASS, forms_en, nlp)
            cov.to_csv(HERE / "cobertura_cass_en.csv", index=False)
        else:
            nlp = spacy.load("es_dep_news_trf")
            entries = pd.read_csv(SEMILLA / "cobertura_glosario_rojo_es.csv").entrada.tolist()
            cov = coverage(df, lang, entries, forms_es, nlp)
            cov.to_csv(HERE / "cobertura_rojo_es.csv", index=False)
        r, d = run(lang, df)
        r.update(cobertura=f"{cov.cubierta.sum()}/{len(cov)}",
                 cobertura_sin_libro=f"{cov.cubierta_sin_libro.sum()}/{len(cov)}" if lang == "es" else "")
        print(r, flush=True)
        if lang == "es":
            print("solo en el libro:", cov[cov.solo_en_libro].entrada.tolist())
            print("no cubiertas:", cov[~cov.cubierta].entrada.tolist())
        else:
            print("no cubiertos:", cov[~cov.cubierta].entrada.tolist())
        out.append(r)
        dp_out += d
    pd.DataFrame(out).to_csv(HERE / "adecuacion_resultados.csv", index=False)
    pd.DataFrame(dp_out).to_csv(HERE / "adecuacion_dp_top50.csv", index=False)


if __name__ == "__main__":
    main()
