"""
Índice de terminologicidad del inventario sobre las apariciones ANOTADAS como unidad (2026-11-10).

TECLA ordena los candidatos contando todas las apariciones de cada forma, porque extrae antes
de que exista la anotación (cap. 5). El inventario revisado (cap. 6) se describe, en cambio,
con las apariciones que la revisión experta marcó como término o entidad: así «tipo» cuenta sus
usos terminológicos y no los de «tipo de texto», y «muestra» no suma las formas del verbo
«mostrar».

Mismas fórmulas que tesis/terminologicidad_glicor_2026-10/indice_T_glicor.py:
  freq      apariciones anotadas de la unidad (todas sus formas), sin las que quedan dentro
            de otra unidad anotada (la anotación no anida)
  df        documentos con al menos una aparición anotada
  TF-IDF    freq · (log2((N+1)/(df+1)) + 1)
  C-value   log2|a| · (f(a) − media de f(b) de las unidades b que la contienen), con
            f(a) = freq + apariciones de la forma dentro de unidades anotadas más largas, y
            f(b) = apariciones anotadas de b que contienen la forma de a (como en Frantzi, donde
            b es una cadena que contiene a; no se restan las variantes de b sin a, p. ej. BNC)
  NC-value  0,8 · C-value + 0,2 · Σ f_a(b) · peso(b): palabras de contexto (sustantivo,
            adjetivo o verbo, ±2) de las apariciones anotadas; peso(b) = proporción de los
            términos del inventario en cuyo contexto aparece b
  T         media de TF-IDF y NC-value normalizados por el máximo de la lengua

Incrustación (tablas de términos nucleares): cadenas = términos del inventario que contienen la
forma; incrustadas = apariciones de la forma dentro de términos anotados más largos; total =
freq + incrustadas.

Fuente: colab_reanotacion/datos_generados_sinbib/{en,es}_bio_tokens.csv (anotación definitiva, sin las
referencias bibliográficas, como el resto de cifras del inventario).
Salida: {en,es}_terminologicidad.csv en esta carpeta. No modifica la tesis.
Uso:    python3 tesis/terminologicidad_anotada_2026-11/indice_T_anotado.py
"""
import csv
from collections import Counter, defaultdict
from math import log2
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATOS = ROOT / "colab_reanotacion/datos_generados_sinbib"   # sin las referencias bibliográficas, como la tesis
FORMAS = ROOT.parent / "tesis_material_tribunal/cap3_anotacion/formas_por_entrada.csv"
PREVIO = ROOT.parent / "tesis-doctoral-datos/cap6_inventario_de_terminos"   # forma que representa a cada unidad
CONTEXT_POS = {"NOUN", "ADJ", "VERB"}
WINDOW = 2


def nombres(lang):
    name = {}
    for r in csv.DictReader(open(FORMAS, encoding="utf-8")):
        if r["lengua"].lower() == lang:
            name.setdefault(r["entrada"], r[f"denominacion_{lang}"] or r["forma"])
    return name


def frases(lang):
    cols = ["doc_id", "sentence_id", "token_id", "token", "lemma", "pos", "label_bio", "entrada"]
    d = pd.read_csv(DATOS / f"{lang}_bio_tokens.csv", usecols=cols, keep_default_na=False,
                    dtype={"token": str, "lemma": str})
    d = d.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable")
    for (doc, _), s in d.groupby(["doc_id", "sentence_id"], sort=False):
        yield doc, list(zip(s.token, s.lemma, s.pos, s.label_bio, s.entrada))


def compute(lang):
    name = nombres(lang)
    sents = list(frases(lang))
    docs = {d for d, _ in sents}
    N = len(docs)
    spans = []                       # (frase, inicio, fin, entrada)
    clase = {}
    for si, (doc, toks) in enumerate(sents):
        i = 0
        while i < len(toks):
            lab = toks[i][3]
            if lab.startswith("B-"):
                j = i + 1
                while j < len(toks) and toks[j][3].startswith("I-"):
                    j += 1
                e = toks[i][4]
                spans.append((si, i, j, e))
                clase.setdefault(e, "termino" if lab == "B-T" else "entidad")
                i = j
            else:
                i += 1

    forms = defaultdict(Counter)     # formas anotadas de cada unidad (tuplas en minúscula)
    freq, docs_of = Counter(), defaultdict(set)
    for si, i, j, e in spans:
        forms[e][tuple(t[0].lower() for t in sents[si][1][i:j])] += 1
        freq[e] += 1
        docs_of[e].add(sents[si][0])
    units = sorted(freq)

    # apariciones de la forma de a dentro de unidades anotadas más largas
    nested_all, nested_term = Counter(), Counter()
    containers, chains = defaultdict(set), defaultdict(set)
    hits_in = defaultdict(Counter)   # hits_in[a][b]: apariciones de b que contienen la forma de a
    span_forms = [(e, tuple(t[0].lower() for t in sents[si][1][i:j])) for si, i, j, e in spans]
    for a in units:
        fa = set(forms[a])
        la = {len(f) for f in fa}
        for b, fb in span_forms:
            if b == a:
                continue
            hits = sum(1 for n in la if n < len(fb)
                       for k in range(len(fb) - n + 1) if fb[k:k + n] in fa)
            if hits:
                nested_all[a] += hits
                hits_in[a][b] += 1
                containers[a].add(b)
                if clase[b] == "termino":
                    nested_term[a] += hits
                    chains[a].add(b)

    f_c = {a: freq[a] + nested_all[a] for a in units}
    tfidf = {a: freq[a] * (log2((N + 1) / (len(docs_of[a]) + 1)) + 1) for a in units}
    length = {a: len(forms[a].most_common(1)[0][0]) for a in units}
    cvalue = {}
    for a in units:
        ll = 1.0 if length[a] == 1 else log2(length[a])
        tb = containers.get(a)
        cvalue[a] = ll * (f_c[a] - (sum(hits_in[a][b] for b in tb) / len(tb) if tb else 0))

    ctx = defaultdict(Counter)
    for si, i, j, e in spans:
        toks = sents[si][1]
        for k in list(range(max(0, i - WINDOW), i)) + list(range(j, min(len(toks), j + WINDOW))):
            if toks[k][2] in CONTEXT_POS:
                ctx[e][toks[k][1].lower()] += 1
    ref = [a for a in units if clase[a] == "termino"]
    t_b = Counter()
    for r in ref:
        t_b.update(ctx[r].keys())
    weight = {b: c / len(ref) for b, c in t_b.items()}
    ncvalue = {a: 0.8 * cvalue[a] + 0.2 * sum(f * weight.get(b, 0.0) for b, f in ctx[a].items())
               for a in units}

    previo = pd.read_csv(PREVIO / f"inventario_{lang}.csv").set_index("unit")["forma"].to_dict()
    rows = []
    for a in units:
        n = name[a]
        rows.append(dict(unit=n, entrada=a, tipo=clase[a],
                         forma=previo.get(n, " ".join(forms[a].most_common(1)[0][0])),
                         freq=freq[a], f_cvalue=f_c[a], df=len(docs_of[a]), tfidf=tfidf[a], cvalue=cvalue[a],
                         nc_frantzi=ncvalue[a], context_factor=(ncvalue[a] - 0.8 * cvalue[a]) / 0.2,
                         containers=len(containers.get(a, ())), chains=len(chains.get(a, ())),
                         nested=nested_term[a], total=freq[a] + nested_term[a]))
    out = pd.DataFrame(rows)
    for col in ("tfidf", "cvalue", "nc_frantzi"):
        out[col + "_norm"] = out[col] / out[col].max()
    out["T"] = (out.tfidf_norm + out.nc_frantzi_norm) / 2
    out = out.sort_values("T", ascending=False)
    out.to_csv(HERE / f"{lang}_terminologicidad.csv", index=False)
    print(f"{lang}: {N} documentos, {(out.tipo == 'termino').sum()} términos, "
          f"{(out.tipo == 'entidad').sum()} entidades")
    return out


if __name__ == "__main__":
    for lang in ("en", "es"):
        compute(lang)
