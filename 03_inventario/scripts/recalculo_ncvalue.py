"""
Recálculo de TF-IDF, C-value, NC-value y terminologicidad (2026-10-03).

Sustituye a las cifras de las Tablas 5.x y del Apéndice III, que procedían
de cálculos anteriores a la reparación del corpus EN y de una implementación
del NC-value que no seguía a Frantzi et al. (2000).

Fuente: los CSV de tokens del corpus anotado (tesis/bio/{en,es}_bio_tokens.csv),
los mismos que describe el cap. 3 (1.448.283 tokens EN; 954.943 ES).

Procedimiento (fórmulas del cap. 4, ec. cvalue y ncvalue):
  1. Candidatos: patrones POS de TECLA (tecla/extractor/grammar.yaml) aplicados
     frase a frase, más los términos validados del Apéndice III. Se descartan
     los candidatos de frecuencia < 2 (umbral por defecto de TECLA).
  2. Frecuencia y DF: ocurrencias de la secuencia de formas (en minúscula) en
     el corpus, incluidas las que forman parte de candidatos más largos.
  3. TF-IDF = f · (log2((N+1)/(DF+1)) + 1), como en TECLA.
  4. C-value (Frantzi): log2|a| · f(a), o log2|a| · (f(a) - media de f(b) de
     los candidatos b que contienen a). Para |a| = 1 se toma log2|a| = 1,
     convención de TECLA (si no, todo término unipalabra valdría 0).
  5. NC-value (Frantzi): 0,8 · C-value(a) + 0,2 · Σ_b f_a(b) · weight(b),
     donde b son los sustantivos, adjetivos y verbos (lema) a ±2 tokens de
     cada ocurrencia de a dentro de la frase; f_a(b) es el número de veces
     que b aparece junto a a; weight(b) = t(b)/n, con t(b) el número de
     términos de referencia junto a los que aparece b y n el total de
     términos de referencia.
     Términos de referencia: Frantzi los toma de los primeros puestos de la
     lista ordenada por C-value. Se calculan dos variantes:
       - "frantzi": los n primeros candidatos por C-value (n = nº de términos
         validados de la lengua);
       - "validados": los términos validados del Apéndice III.
  6. Normalización por el máximo entre los términos validados de cada lengua;
     terminologicidad = media de TF-IDF y NC-value normalizados.

Uso:  python3 tesis/terminologicidad_2026-10/recalculo_ncvalue.py
Salida: {en,es}_terminologicidad.csv en esta misma carpeta.
"""

import re
import sys
from collections import Counter, defaultdict
from math import log2
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tecla.extractor.linguistic_filter import extract_candidates  # noqa: E402

OUT = Path(__file__).resolve().parent
APENDICE = ROOT / "tesis/maquetacion/chapters/anexo_terminos_entidades.tex"
GRAMMAR = ROOT / "tecla/extractor/grammar.yaml"
CONTEXT_POS = {"NOUN", "ADJ", "VERB"}
WINDOW = 2
MIN_FREQ = 2


# Formas del corpus que corresponden a una unidad pero que la tokenización ha
# alterado: "Tweepy7" es Tweepy con la llamada de nota 7 pegada.
FORM_ALIASES = {"Tweepy": [("tweepy7",)]}

# Formas en minúscula de las siglas del inventario (CREA, TTR...). En el corpus,
# un token escrito todo en minúscula con esa forma (crea, del verbo crear) no
# cuenta como la sigla.
ACRONYMS = set()


def norm(tok):
    """Comparación sin distinguir mayúsculas, salvo homógrafos en minúscula de siglas."""
    low = tok.lower()
    return low + "_lc" if low in ACRONYMS and tok.islower() else low


def name_norm(tok):
    return tok.lower()


def tokenize_name(name):
    """Tokenizaciones posibles: guion separado (spaCy EN) o unido (ES); puntos separados (Val.Es.Co)."""
    split = tuple(name_norm(t) for t in re.split(r"\s+|(-)", name) if t)
    joined = tuple(name_norm(t) for t in name.split())
    dots = tuple(name_norm(t) for t in re.split(r"\s+|(-)|(\.)", name) if t)
    return {split, joined, dots}


def clean_latex(s):
    s = re.sub(r"\\[a-zA-Z]+\{", "", s).replace("{", "").replace("}", "")
    return s.replace("\\", "").replace("~", " ").strip()


def appendix_units():
    """Unidades validadas del Apéndice III: longtable 1-2 términos EN/ES, 3-4 entidades EN/ES."""
    text = APENDICE.read_text(encoding="utf-8")
    tables = re.findall(r"\\begin\{longtable\}(.*?)\\end\{longtable\}", text, re.S)
    out = []
    for body in tables[:4]:
        names = []
        for line in body.splitlines():
            parts = [p.strip() for p in line.rstrip("\\ ").split("&")]
            if len(parts) in (6, 7) and re.match(r"^\d", parts[1]):
                names.append(clean_latex(parts[0]))
        out.append(names)
    return {"en": (out[0], out[2]), "es": (out[1], out[3])}


def load_sentences(lang):
    cols = ["doc_id", "sentence_id", "token_id", "token", "lemma", "pos"]
    df = pd.read_csv(ROOT / f"tesis/bio/{lang}_bio_tokens.csv", usecols=cols,
                     dtype={"token": str, "lemma": str}, keep_default_na=False)
    df = df.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable")
    docs = []
    for doc_id, d in df.groupby("doc_id", sort=False):
        sents = []
        for _, s in d.groupby("sentence_id", sort=False):
            sents.append([{"text": t, "lemma": l, "pos": p}
                          for t, l, p in zip(s.token, s.lemma, s.pos)])
        docs.append({"doc_id": doc_id, "sentences": sents})
    return docs


def ngrams(docs, max_len):
    """Recorre todas las secuencias de hasta max_len formas normalizadas por frase."""
    for d in docs:
        for si, sent in enumerate(d["sentences"]):
            forms = [norm(t["text"]) for t in sent]
            for n in range(1, max_len + 1):
                for i in range(len(forms) - n + 1):
                    yield d["doc_id"], si, i, n, tuple(forms[i:i + n]), sent


def compute(lang, term_names, entity_names):
    docs = load_sentences(lang)
    n_docs = len(docs)
    ACRONYMS.clear()
    ACRONYMS.update(t.lower() for n in term_names + entity_names
                    for t in re.split(r"[\s-]+", n) if len(t) > 1 and t.isupper())

    # 1. Candidatos
    cands = extract_candidates(docs, language=lang, grammar_path=GRAMMAR)
    cand_freq = Counter(tuple(norm(t) for t in c["term"].split()) for c in cands)
    keys = {k for k, f in cand_freq.items() if f >= MIN_FREQ}
    names = term_names + entity_names
    variants = {n: tokenize_name(n) | set(FORM_ALIASES.get(n, [])) for n in names}
    for v in variants.values():
        keys |= v
    max_len = max(len(k) for k in keys)

    # 2. Frecuencia y DF de todos los candidatos
    freq = Counter()
    docs_of = defaultdict(set)
    for doc_id, _, _, _, k, _ in ngrams(docs, max_len):
        if k in keys:
            freq[k] += 1
            docs_of[k].add(doc_id)
    # Siglas con puntos internos (Val.Es.Co): spaCy corta la frase en cada
    # punto, así que se cuentan sobre el documento entero.
    dotted = {k for v in variants.values() for k in v if "." in k and len(k) > 1}
    for d in docs:
        forms = [norm(t["text"]) for sent in d["sentences"] for t in sent]
        for k in dotted:
            for i in range(len(forms) - len(k) + 1):
                if tuple(forms[i:i + len(k)]) == k:
                    freq[k] += 1
                    docs_of[k].add(d["doc_id"])
    # cada unidad validada se queda con la tokenización que aparece en el corpus
    unit = {n: max(v, key=lambda k: freq[k]) for n, v in variants.items()}
    keys = {k for k in keys if freq[k] > 0} | set(unit.values())

    # 3. TF-IDF
    tfidf = {k: freq[k] * (log2((n_docs + 1) / (len(docs_of[k]) + 1)) + 1)
             for k in keys}

    # 4. C-value
    containers = defaultdict(set)
    for b in keys:
        for n in range(1, len(b)):
            for i in range(len(b) - n + 1):
                if b[i:i + n] in keys:
                    containers[b[i:i + n]].add(b)
    cvalue = {}
    for a in keys:
        loglen = 1.0 if len(a) == 1 else log2(len(a))
        tb = containers.get(a)
        cvalue[a] = loglen * (freq[a] - (sum(freq[b] for b in tb) / len(tb) if tb else 0))

    # 5. Contexto (f_a(b)) y posiciones de las unidades validadas
    n_ref = len(term_names)
    top_c = set(sorted(keys, key=lambda k: -cvalue[k])[:n_ref])
    need = top_c | set(unit.values())
    ctx = defaultdict(Counter)
    occ = defaultdict(list)
    for doc_id, si, i, n, k, sent in ngrams(docs, max_len):
        if k not in need:
            continue
        occ[k].append((doc_id, si, i))
        lo, hi = max(0, i - WINDOW), min(len(sent), i + n + WINDOW)
        for j in list(range(lo, i)) + list(range(i + n, hi)):
            if sent[j]["pos"] in CONTEXT_POS:
                ctx[k][sent[j]["lemma"].lower()] += 1

    def ncvalue(ref):
        t_b = Counter()
        for r in ref:
            t_b.update(ctx[r].keys())
        weight = {b: c / len(ref) for b, c in t_b.items()}
        return {a: 0.8 * cvalue[a]
                + 0.2 * sum(f * weight.get(b, 0.0) for b, f in ctx[a].items())
                for a in unit.values()}

    nc_frantzi = ncvalue(top_c)
    nc_valid = ncvalue({unit[n] for n in term_names})

    # 6. Incrustación entre términos validados (cadenas del propio inventario)
    term_keys = {unit[n] for n in term_names}
    inc = {}
    for n in term_names:
        a = unit[n]
        chains = [b for b in term_keys if len(b) > len(a)
                  and any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1))]
        if not chains:
            continue
        covered = set()
        for b in chains:
            offs = [i for i in range(len(b) - len(a) + 1) if b[i:i + len(a)] == a]
            for doc_id, si, i in occ[b]:
                for o in offs:
                    covered.add((doc_id, si, i + o))
        nested = sum(1 for o in occ[a] if o in covered)
        inc[n] = dict(chains=len(chains), nested=nested, autonomous=freq[a] - nested)

    rows = []
    for name, k in unit.items():
        rows.append(dict(unit=name, tipo="termino" if name in term_names else "entidad",
                         freq=freq[k], df=len(docs_of[k]),
                         tfidf=tfidf[k], cvalue=cvalue[k],
                         nc_frantzi=nc_frantzi[k], nc_validados=nc_valid[k],
                         context_factor=(nc_frantzi[k] - 0.8 * cvalue[k]) / 0.2,
                         containers=len(containers.get(k, ())),
                         containers_mean_freq=(sum(freq[b] for b in containers[k]) / len(containers[k])
                                               if containers.get(k) else 0.0),
                         chains=inc.get(name, {}).get("chains", 0),
                         nested=inc.get(name, {}).get("nested", 0)))
    out = pd.DataFrame(rows)
    # normalización por el máximo entre todas las unidades de la lengua
    for col in ("tfidf", "cvalue", "nc_frantzi", "nc_validados"):
        out[col + "_norm"] = out[col] / out[col].max()
    out["T"] = (out.tfidf_norm + out.nc_frantzi_norm) / 2
    out["T_validados"] = (out.tfidf_norm + out.nc_validados_norm) / 2
    out["T_cvalue"] = (out.tfidf_norm + out.cvalue_norm) / 2
    out = out.sort_values("T", ascending=False)
    out.to_csv(OUT / f"{lang}_terminologicidad.csv", index=False)
    print(f"{lang}: {len(keys)} candidatos, {n_docs} documentos, "
          f"{len(term_names)} términos y {len(entity_names)} entidades, "
          f"{(out.freq == 0).sum()} sin ocurrencias: "
          f"{list(out[out.freq == 0].unit)}")
    return out


if __name__ == "__main__":
    for lang, (terms, entities) in appendix_units().items():
        compute(lang, terms, entities)
