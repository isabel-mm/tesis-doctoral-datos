"""
Propiedades estructurales del inventario (cap. 5, §sec:propiedades_estructurales)
sobre la anotación nueva (proyección de GLiCor, 5 de octubre de 2026).

Unidad: cada entrada de término de GLiCor presente en el subcorpus (146 EN,
142 ES). Para cada una se toma su denominación principal en esa lengua si
está documentada en el subcorpus (si no, su forma anotada más frecuente, que
suele ser un préstamo) y la secuencia de categorías (UPOS) más frecuente de
esa forma, contada solo en sus apariciones en minúscula (en los títulos, las
mayúsculas llevan a etiquetar como PROPN nombres comunes). Para los patrones,
un participio (VERB) que modifica al núcleo cuenta como ADJ; PROPN cuenta
como NOUN salvo en las palabras que la denominación principal escribe con
mayúscula (Zipf), porque en los términos es casi siempre un error de
etiquetado (préstamos y títulos); y en español
«del» y «de + determinante» cuentan como «de».

  - Composición: monoléxica si esa forma es un solo token.
  - Patrones: los de la gramática terminológica (tecla/extractor/grammar.yaml).
  - Incrustación: una aparición de la entrada A está incrustada si alguna de
    sus formas anotadas aparece, como secuencia contigua de tokens, dentro de
    un span anotado de otra entrada de término B (la anotación toma la cadena
    más larga, así que esas apariciones no figuran como spans de A). Cadenas =
    número de entradas B distintas que la contienen. Se excluye «type»: GLiCor
    solo lo cuenta en el sentido de type frente a token, y sus formas dentro de
    otros términos («text types») son la palabra general.

Uso:    python3 tesis/reanotacion_2026-10/estructura_reanotacion.py
Salida: estructura_{en,es}.csv, nucleares_{en,es}.csv y resumen_estructura.txt
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BIO = ROOT / "colab_reanotacion/datos_generados"
ENTRIES = {e["slug"]: e for e in json.load(open(ROOT / "colab_reanotacion/datos/glicor/entradas.json"))}
CONTENT = {"NOUN", "PROPN", "ADJ"}
NO_NESTING = {"type"}


def spans(lang):
    df = pd.read_csv(BIO / f"{lang}_bio_tokens_terms_only.csv",
                     usecols=["doc_id", "sentence_id", "token_id", "token", "pos", "label_bio", "entrada"],
                     keep_default_na=False)
    df = df.sort_values(["doc_id", "sentence_id", "token_id"], kind="stable")
    out, cur = [], None
    for doc, sid, tok, pos, lab, ent in zip(df.doc_id, df.sentence_id, df.token, df.pos, df.label_bio, df.entrada):
        if lab == "B-T":
            if cur:
                out.append(cur)
            cur = [ent, [tok], [pos], (doc, sid)]
        elif lab == "I-T" and cur and cur[3] == (doc, sid):
            cur[1].append(tok)
            cur[2].append(pos)
        else:
            if cur:
                out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return [(e, tuple(x.lower() for x in t), tuple(p), t[-1].islower() or len(t) == 1 and t[0].islower())
            for e, t, p, _ in out]


def key(s):
    return " ".join(s.lower().replace("-", " - ").split())


def normalise(toks, pos, lang):
    """Participios modificadores como ADJ; en español, del / de + DET como «de»."""
    toks, pos = list(toks), list(pos)
    if lang == "en":
        pos = [("ADJ" if p == "VERB" and i < len(pos) - 1 else p) for i, p in enumerate(pos)]
    else:
        pos = [("ADJ" if p == "VERB" and i > 0 else p) for i, p in enumerate(pos)]
        out_t, out_p, i = [], [], 0
        while i < len(toks):
            if toks[i] == "del":
                out_t.append("de"); out_p.append("ADP")
            elif toks[i] == "de" and i + 1 < len(toks) and pos[i + 1] == "DET":
                out_t.append("de"); out_p.append("ADP"); i += 1
            else:
                out_t.append(toks[i]); out_p.append(pos[i])
            i += 1
        toks, pos = out_t, out_p
    return tuple(toks), tuple(pos)


def pattern(toks, pos, lang, principal=""):
    caps = {w.lower() for w in principal.split() if w[:1].isupper()}
    pos = tuple("NOUN" if p == "PROPN" and t not in caps else p for t, p in zip(toks, pos))
    toks, pos = normalise(toks, pos, lang)
    prep = "of" if lang == "en" else "de"
    if len(toks) == 1:
        return "Monoléxico"
    if any("-" in t for t in toks):
        return "Compuesto con guion"
    if all(p == "PROPN" for p in pos):
        return "PROPN PROPN+"
    if all(p == "NOUN" for p in pos):
        return "N N+"
    if pos[0] == "NOUN" and all(p == "ADJ" for p in pos[1:]):
        return "N ADJ+"
    if prep in toks:
        i = toks.index(prep)
        left, right = pos[:i], pos[i + 1:]
        if left and right and all(p == "NOUN" for p in left):
            if all(p == "NOUN" for p in right):
                return f"N+ {prep} N+"
            if right[0] == "NOUN" and all(p == "ADJ" for p in right[1:]):
                return f"N+ {prep} N ADJ+"
    if pos[-1] == "NOUN" and all(p in CONTENT for p in pos):
        return "(ADJ|N|PROPN)* N"
    return "Otros"


def contains(big, small):
    n = len(small)
    return any(big[i:i + n] == small for i in range(len(big) - n + 1))


def main():
    lines = []
    for lang in ("en", "es"):
        sp = spans(lang)
        by_entry = defaultdict(list)
        for e, t, p, low in sp:
            by_entry[e].append((t, p, low))
        rows = []
        for e, occ in by_entry.items():
            principal = key(ENTRIES[e][f"term_{lang}"])
            attested = [t for t, _, _ in occ if key(" ".join(t)) == principal]
            form = attested[0] if attested else Counter(t for t, _, _ in occ).most_common(1)[0][0]
            cand = [p for t, p, low in occ if t == form and low] or [p for t, p, _ in occ if t == form]
            pos = Counter(cand).most_common(1)[0][0]
            rows.append(dict(entrada=e, denominacion=ENTRIES[e][f"term_{lang}"], forma=" ".join(form),
                             pos=" ".join(pos), n_tokens=len(form), patron=pattern(form, pos, lang, ENTRIES[e][f"term_{lang}"]),
                             principal_documentada=bool(attested),
                             frec_autonoma=len(occ), formas=len({t for t, _, _ in occ})))
        st = pd.DataFrame(rows).sort_values("frec_autonoma", ascending=False)
        # incrustación
        forms = {e: {t for t, _, _ in occ} for e, occ in by_entry.items()}
        nested, chains = Counter(), defaultdict(set)
        for b, t, _, _ in sp:
            for a, fa in forms.items():
                if a == b or a in NO_NESTING:
                    continue
                k = sum(1 for f in fa if len(f) < len(t) and contains(t, f))
                if k:
                    nested[a] += 1
                    chains[a].add(b)
        st["frec_incrustada"] = st.entrada.map(nested).fillna(0).astype(int)
        st["cadenas"] = st.entrada.map(lambda e: len(chains.get(e, ())))
        st["frec_total"] = st.frec_autonoma + st.frec_incrustada
        st.to_csv(HERE / f"estructura_{lang}.csv", index=False)
        nuc = st[st.cadenas > 0].sort_values(["cadenas", "frec_total"], ascending=False)
        nuc.to_csv(HERE / f"nucleares_{lang}.csv", index=False)
        n = len(st)
        mono = (st.n_tokens == 1).sum()
        total_occ = st.frec_total.sum()
        lines += [f"=== {lang.upper()} === entradas de término: {n}",
                  f"monoléxicos {mono} ({100 * mono / n:.1f} %) | poliléxicos {n - mono} ({100 * (n - mono) / n:.1f} %)",
                  "patrones: " + "; ".join(f"{k} {v} ({100 * v / n:.1f} %)" for k, v in st.patron.value_counts().items()),
                  f"nucleares: {len(nuc)} ({100 * len(nuc) / n:.1f} %); incrustadas = "
                  f"{100 * st.frec_incrustada.sum() / st.frec_autonoma.sum():.1f} % de las apariciones anotadas "
                  f"({100 * st.frec_incrustada.sum() / total_occ:.1f} % del total con incrustadas)",
                  nuc[["denominacion", "frec_total", "frec_autonoma", "frec_incrustada", "cadenas"]].to_string(index=False),
                  ""]
    (HERE / "resumen_estructura.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
