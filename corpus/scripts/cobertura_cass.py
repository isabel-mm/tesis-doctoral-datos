"""Cobertura de los 38 términos de CASS (inglés) y de sus equivalentes (español) en el
corpus sin bibliografías, con la misma función que tesis/reanotacion_2026-10/
adecuacion_reanotacion.py (secuencias de lemas o formas, dentro de la oración).
Salida: cobertura_cass_{en,es}.csv en esta carpeta.
Uso:    python3 tesis/sin_bibliografia_2026-11/cobertura_cass.py"""
import csv, sys
from pathlib import Path
import spacy
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tesis/reanotacion_2026-10"))
import adecuacion_reanotacion as A          # lee la anotación sin bibliografías por defecto
SEM = Path.home() / "Desktop/Repositorios/tesis-doctoral-datos/glosario_de_partida_CASS/cass_semilla_equivalentes.csv"
pares = [(r["termino_en"], r["equivalente_es"]) for r in csv.DictReader(open(SEM, encoding="utf-8"))]
for lang, model in (("en", "en_core_web_trf"), ("es", "es_dep_news_trf")):
    df = A.load(lang); nlp = spacy.load(model)
    if lang == "en":
        cov = A.coverage(df, lang, A.CASS, A.forms_en, nlp)
    else:
        es_of = dict((e.lower(), s) for e, s in pares)
        def slash(p):
            """«metadato/s» -> metadato, metadatos; «corpus de muestra/muestral» -> corpus de muestra, corpus muestral."""
            if "/" not in p: return [p]
            a, b = p.split("/", 1)
            if len(b) <= 2: return [a, a + b]
            head = a.rsplit(" ", 2)[0] if a.count(" ") >= 2 else a.rsplit(" ", 1)[0]
            return [a, f"{head} {b}"]
        def forms(term):
            s = es_of[term.lower()].replace("*", "")
            return [x.strip() for p in A.forms_es(s) for x in slash(p.strip()) if x.strip()]
        cov = A.coverage(df, lang, [e for e, _ in pares], forms, nlp)
    cov.to_csv(HERE / f"cobertura_cass_{lang}{__import__('os').environ.get('SUFIJO', '')}.csv", index=False)
    print(lang, f"{int(cov.cubierta.sum())}/{len(cov)}", "no cubiertas:", cov[~cov.cubierta].entrada.tolist(), flush=True)
