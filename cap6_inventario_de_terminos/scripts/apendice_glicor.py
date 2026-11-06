"""Regenera las cuatro tablas del Apéndice III (términos y entidades, EN y ES) con las unidades
de GLiCor presentes en cada subcorpus y los valores de {en,es}_terminologicidad.csv de esta carpeta.
Agrupa por categoría temática y, dentro de cada una, ordena por terminologicidad."""
import csv
import re
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AP = ROOT / "tesis/maquetacion/chapters/anexo_terminos_entidades.tex"
FORMAS = ROOT.parent / "tesis_material_tribunal/cap3_anotacion/formas_por_entrada.csv"
CATS_T = [("Metodología y diseño", "MET-DI"), ("Procesamiento lingüístico", "PROC-LIN"),
          ("Estadística y léxico", "EST-LEX"), ("Tecnología y formatos", "TEC-FOR")]
CATS_E = [("Recursos y corpus", "REC-COR"), ("Herramientas y software", "HER-SOFT"),
          ("Estándares y formatos técnicos", None), ("Anotación y procesamiento lingüístico", None)]
LABELS = {("en", "termino"): "tab:anexo_terminos_en", ("es", "termino"): "tab:anexo_terminos_es",
          ("en", "entidad"): "tab:anexo_entidades_en", ("es", "entidad"): "tab:anexo_entidades_es"}


def dec(x):
    return f"{x:.4f}".replace(".", "{,}")


def esc(s):
    return re.sub(r"([&%#_$])", r"\\\1", s)


cat_of = {}
for r in csv.DictReader(open(FORMAS, encoding="utf-8")):
    cat_of[(r["lengua"].lower(), r[f"denominacion_{r['lengua'].lower()}"] or r["forma"])] = r["categoria"]


def body(lang, tipo):
    d = pd.read_csv(HERE / f"{lang}_terminologicidad.csv")
    d = d[d.tipo == tipo].copy()
    d["cat"] = [cat_of[(lang, u)] for u in d.unit]
    lines = []
    for nombre, codigo in (CATS_T if tipo == "termino" else CATS_E):
        g = d[d.cat == nombre].sort_values("T", ascending=False)
        if g.empty:
            continue
        if lines:
            lines.append(r"\midrule")
        cab = f"{nombre} (\\texttt{{{codigo}}})" if codigo else nombre
        lines += [rf"\multicolumn{{7}}{{l}}{{\textbf{{{cab}}}}} \\", r"\midrule"]
        for _, r in g.iterrows():
            f = r"\texttt" if nombre == "Herramientas y software" else r"\textit"
            lines.append(f"{f}{{{esc(r.forma)}}} & {r.freq} & {r.df} & {dec(r.tfidf_norm)} & "
                         f"{dec(r.cvalue_norm)} & {dec(r.nc_frantzi_norm)} & {dec(r['T'])} \\\\")
    return "\n".join(lines) + "\n", len(d)


text = AP.read_text(encoding="utf-8")
for (lang, tipo), label in LABELS.items():
    rows, n = body(lang, tipo)
    i = text.index(rf"\label{{{label}}}")
    b = text.index(r"\endlastfoot", i) + len(r"\endlastfoot") + 1
    e = text.index(r"\end{longtable}", b)
    text = text[:b] + rows + text[e:]
    # cifra del pie de tabla
    c0 = text.rindex(r"\caption{", 0, i)
    cap = text[c0:i]
    new = re.sub(r"\(\d+ unidades\)", f"({n} unidades)", cap)
    new = new.replace("validados del subcorpus en", "del inventario presentes en el subcorpus").replace(
        "validadas del subcorpus en", "del inventario presentes en el subcorpus")
    text = text[:c0] + new + text[i:]
    print(lang, tipo, n)
text = text.replace("Dentro de cada categoría se conserva el orden de presentación del cuerpo del capítulo.",
                    "Dentro de cada categoría, las unidades se ordenan por terminologicidad.")
AP.write_text(text, encoding="utf-8")
