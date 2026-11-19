"""
Índice de terminologicidad sobre las unidades de GLiCor presentes en cada subcorpus (2026-10-19).

Mismo cálculo que tesis/terminologicidad_2026-10/recalculo_ncvalue.py (TF-IDF, C-value,
NC-value de Frantzi, T = media de TF-IDF y NC-value normalizados); solo cambia la lista
de unidades: en lugar de las del Apéndice III, las entradas de GLiCor que aparecen
anotadas en cada subcorpus (EN: 146 términos + 56 entidades; ES: 142 + 108). Las formas
de cada entrada son las secuencias anotadas en el corpus (incluidas las flexionadas), y la
entrada se representa por la más frecuente, como hace el script original.

Salida: {en,es}_terminologicidad.csv en esta carpeta. No modifica la tesis.

COPIA (7-nov-2026) en tesis/sin_bibliografia_2026-11: unidades de datos_generados_sinbib y
frecuencias de bio_sinbib/ (ambas sin las secciones de referencias bibliográficas).
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tesis/terminologicidad_2026-10"))
import recalculo_ncvalue as rc  # noqa: E402

rc.OUT = HERE


def _load_sentences_sinbib(lang):
    cols = ["doc_id", "sentence_id", "token_id", "token", "lemma", "pos"]
    df = pd.read_csv(HERE / f"bio_sinbib/{lang}_bio_tokens.csv", usecols=cols,
                     dtype={"token": str, "lemma": str}, keep_default_na=False)
    df = df.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable")
    docs = []
    for doc_id, d in df.groupby("doc_id", sort=False):
        sents = [[{"text": t, "lemma": l, "pos": p} for t, l, p in zip(s.token, s.lemma, s.pos)]
                 for _, s in d.groupby("sentence_id", sort=False)]
        docs.append({"doc_id": doc_id, "sentences": sents})
    return docs


rc.load_sentences = _load_sentences_sinbib
FORMAS = ROOT.parent / "tesis_material_tribunal/cap3_anotacion/formas_por_entrada.csv"


def glicor_units(lang):
    d = pd.read_csv(ROOT / f"colab_reanotacion/datos_generados_sinbib/{lang}_bio_tokens.csv",
                    usecols=["token", "label_bio", "entrada"], keep_default_na=False)
    spans, lab = defaultdict(set), {}
    toks, labs, ents = list(d.token), list(d.label_bio), list(d.entrada)
    i = 0
    while i < len(toks):
        if labs[i].startswith("B-"):
            j = i + 1
            while j < len(toks) and labs[j].startswith("I-"):
                j += 1
            spans[ents[i]].add(tuple(rc.name_norm(t) for t in toks[i:j]))
            lab.setdefault(ents[i], labs[i])
            i = j
        else:
            i += 1
    name = {}
    for r in csv.DictReader(open(FORMAS, encoding="utf-8")):
        if r["lengua"].lower() == lang and r["entrada"] in lab:
            name.setdefault(r["entrada"], r[f"denominacion_{lang}"] or r["forma"])
    terms, entities = [], []
    for e, l in lab.items():
        n = name[e]
        # el corpus del cap. 3 usa el apóstrofo curvo (Zipf ’s law); la anotación, el recto
        rc.FORM_ALIASES[n] = list(spans[e] | {tuple(t.replace("'", "’") for t in k) for k in spans[e]})
        (terms if l == "B-T" else entities).append(n)
    return terms, entities


if __name__ == "__main__":
    for lang in ("en", "es"):
        rc.FORM_ALIASES.clear()
        rc.FORM_ALIASES["Tweepy"] = [("tweepy7",)]
        t, e = glicor_units(lang)
        assert len(set(t + e)) == len(t + e), "denominaciones repetidas"
        rc.compute(lang, t, e)
