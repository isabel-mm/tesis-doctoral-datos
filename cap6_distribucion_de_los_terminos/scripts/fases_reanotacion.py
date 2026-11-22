"""
Procedencia de las unidades del Gold Standard por fase de anotación (cap. 3,
Tabla tab:fases_anotacion) sobre la anotación nueva (solo términos).

Fase 1 = unidades normalizadas que contienen un término semilla de CASS (38;
Apéndice II, Tabla tab:glosario_cass), en cualquiera de sus formas inglesas.
Fases 2-3 = el resto. Tipo = unidad normalizada (columna «entrada»).
Se cuentan además los tipos de baja frecuencia (<= 10 apariciones) y los hápax
de las fases 2-3, que corresponden característicamente a la validación manual.

Uso:    python3 tesis/reanotacion_2026-10/fases_reanotacion.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# Anotación sin las bibliografías (tesis/sin_bibliografia_2026-11): las secciones de
# referencias no forman parte del discurso especializado (cap. 3). TESIS_BIO permite
# usar otra carpeta, p. ej. colab_reanotacion/datos_generados (con bibliografías).
BIO = Path(__import__("os").environ.get("TESIS_BIO", ROOT / "colab_reanotacion/datos_generados_sinbib"))
G = ROOT / "colab_reanotacion/datos/glicor"
CASS = ["corpus", "text", "annotation", "keyword", "type", "tagging", "sample", "XML", "token",
        "corpus-based", "markup", "diachronic", "metadata", "representativeness", "reference corpus",
        "concordance", "node", "collocation", "balance", "synchronic", "frequency list", "encoding",
        "lemma", "comparability", "significance test", "markup language", "concordancer",
        "corpus construction", "corpus-driven", "statistical significance", "lexis", "lemmatisation",
        "monitor corpus", "sampling frame", "type-token ratio", "KWIC", "colligation", "sample corpus"]


def en_forms():
    norm = json.load(open(G / "normalizacion.json"))
    forms = defaultdict(set)
    for e in json.load(open(G / "entradas.json")):
        forms[e["slug"]].add(e["term_en"].lower())
    for slug, d in norm["formas_contadas"].items():
        if isinstance(d, dict):
            forms[slug] |= {f.lower() for f in d.get("en", [])}
    for e in norm["entradas"]:
        for f in e.get("formas", {}).get("en", []):
            forms[e["slug"]] |= {c.lower() for c in f.get("cuenta", [])} | {f["forma"].lower()}
    return forms


def main():
    forms = en_forms()
    seed_entries, unmatched = {}, []
    for s in CASS:
        hit = [slug for slug, fs in forms.items() if s.lower() in fs]
        if hit:
            seed_entries[s] = hit[0]
        else:
            unmatched.append(s)
    print("semilla sin unidad normalizada:", unmatched)
    print("semilla -> unidad:", seed_entries)
    phase1 = set(seed_entries.values())
    for lang in ("en", "es"):
        df = pd.read_csv(BIO / f"{lang}_bio_tokens_terms_only.csv", usecols=["label_bio", "entrada"],
                         keep_default_na=False)
        freq = Counter(df.entrada[df.label_bio == "B-T"])
        n_t, n_o = len(freq), sum(freq.values())
        p1 = {e: f for e, f in freq.items() if e in phase1}
        rest = {e: f for e, f in freq.items() if e not in phase1}
        low = sum(f <= 10 for f in rest.values())
        hapax = sum(f == 1 for f in rest.values())
        print(f"{lang.upper()}: total {n_t} tipos / {n_o} apariciones")
        print(f"  fase 1: {len(p1)} ({100*len(p1)/n_t:.1f} %) tipos, {sum(p1.values())} ({100*sum(p1.values())/n_o:.1f} %) apariciones")
        print(f"  fases 2-3: {len(rest)} ({100*len(rest)/n_t:.1f} %) tipos, {sum(rest.values())} ({100*sum(rest.values())/n_o:.1f} %) apariciones")
        print(f"  fases 2-3 con <= 10 apariciones: {low} ({100*low/len(rest):.1f} %), hápax {hapax}")


if __name__ == "__main__":
    main()
