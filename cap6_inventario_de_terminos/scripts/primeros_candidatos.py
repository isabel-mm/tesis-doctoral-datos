"""
Nota del cap. 5 (índice de terminologicidad): proporción de unidades validadas entre los
100 primeros candidatos según el índice T, el TF-IDF y el NC-value por separado, y número de
candidatos que contienen *corpus*. Mismo cálculo que recalculo_ncvalue.compute, pero con el
NC-value de todos los candidatos (no solo de las unidades validadas).

Uso:  python3 primeros_candidatos.py            (sin bibliografías)
      CONBIB=1 python3 primeros_candidatos.py   (con bibliografías, para validar con la tesis)
"""
import os
from collections import Counter, defaultdict
from math import log2
import indice_T_sinbib as it
rc = it.rc
CONBIB = os.environ.get("CONBIB") == "1"
if CONBIB:
    import importlib; importlib.reload(rc)   # load_sentences original (tesis/bio, con bibliografías)
    it.ROOT_DATOS = "datos_generados"


def run(lang):
    rc.FORM_ALIASES.clear(); rc.FORM_ALIASES["Tweepy"] = [("tweepy7",)]
    if CONBIB:
        import pandas as pd
        orig = pd.read_csv
        it.pd.read_csv = lambda p, *a, **k: orig(str(p).replace("datos_generados_sinbib", "datos_generados"), *a, **k)
        terms, ents = it.glicor_units(lang); it.pd.read_csv = orig
    else:
        terms, ents = it.glicor_units(lang)
    docs = rc.load_sentences(lang); n_docs = len(docs)
    rc.ACRONYMS.clear()
    rc.ACRONYMS.update(t.lower() for n in terms + ents for t in rc.re.split(r"[\s-]+", n) if len(t) > 1 and t.isupper())
    cands = rc.extract_candidates(docs, language=lang, grammar_path=rc.GRAMMAR)
    cand_freq = Counter(tuple(rc.norm(t) for t in c["term"].split()) for c in cands)
    keys = {k for k, f in cand_freq.items() if f >= rc.MIN_FREQ}
    names = terms + ents
    variants = {n: rc.tokenize_name(n) | set(rc.FORM_ALIASES.get(n, [])) for n in names}
    for v in variants.values():
        keys |= v
    max_len = max(len(k) for k in keys)
    freq, docs_of = Counter(), defaultdict(set)
    for doc_id, _, _, _, k, _ in rc.ngrams(docs, max_len):
        if k in keys:
            freq[k] += 1; docs_of[k].add(doc_id)
    unit = {n: max(v, key=lambda k: freq[k]) for n, v in variants.items()}
    keys = {k for k in keys if freq[k] > 0} | set(unit.values())
    tfidf = {k: freq[k] * (log2((n_docs + 1) / (len(docs_of[k]) + 1)) + 1) for k in keys}
    containers = defaultdict(set)
    for b in keys:
        for n in range(1, len(b)):
            for i in range(len(b) - n + 1):
                if b[i:i + n] in keys:
                    containers[b[i:i + n]].add(b)
    cvalue = {}
    for a in keys:
        loglen = 1.0 if len(a) == 1 else log2(len(a)); tb = containers.get(a)
        cvalue[a] = loglen * (freq[a] - (sum(freq[b] for b in tb) / len(tb) if tb else 0))
    top_c = set(sorted(keys, key=lambda k: -cvalue[k])[:len(terms)])
    ctx = defaultdict(Counter)
    for doc_id, si, i, n, k, sent in rc.ngrams(docs, max_len):
        if k not in keys:
            continue
        lo, hi = max(0, i - rc.WINDOW), min(len(sent), i + n + rc.WINDOW)
        for j in list(range(lo, i)) + list(range(i + n, hi)):
            if sent[j]["pos"] in rc.CONTEXT_POS:
                ctx[k][sent[j]["lemma"].lower()] += 1
    t_b = Counter()
    for r in top_c:
        t_b.update(ctx[r].keys())
    weight = {b: c / len(top_c) for b, c in t_b.items()}
    nc = {a: 0.8 * cvalue[a] + 0.2 * sum(f * weight.get(b, 0.0) for b, f in ctx[a].items()) for a in keys}
    mt, mn = max(tfidf.values()), max(nc.values())
    T = {k: (tfidf[k] / mt + nc[k] / mn) / 2 for k in keys}
    defs = {"todas las formas": set(k for n in names for k in variants[n] if k in keys),
            "formas de términos": set(k for n in terms for k in variants[n] if k in keys),
            "una por unidad": set(unit.values()),
            "una por término": set(unit[n] for n in terms)}
    res = {}
    for d, valid in defs.items():
        res[d] = (f"{100 * len(valid) / len(keys):.1f} %",
                  {nombre: sum(k in valid for k in sorted(keys, key=lambda k: -sc[k])[:100])
                   for nombre, sc in (("T", T), ("TF-IDF", tfidf), ("NC-value", nc))})
    valid = defs["todas las formas"]; base = len(valid) / len(keys)
    corpus_key = unit[[n for n in terms if n.lower() == "corpus"][0]]
    print(f"{lang}{' (con bibliografías)' if CONBIB else ''}: {len(keys)} candidatos, {len(valid)} validados "
          f"({100 * base:.1f} %) | validados entre los 100 primeros: {res} | "
          f"candidatos que contienen 'corpus': {len(containers[corpus_key])}", flush=True)


for lang in ("en", "es"):
    run(lang)
