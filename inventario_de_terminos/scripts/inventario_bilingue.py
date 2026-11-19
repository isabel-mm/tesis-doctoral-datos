"""Inventario bilingüe de términos y entidades (material complementario, carpeta
inventario_de_terminos): reconstruye el documento con las tablas de
apendice_glicor.py y los valores de {en,es}_terminologicidad.csv sin bibliografías.
2026-11-10: lee los CSV calculados sobre las apariciones anotadas (carpeta superior).
Uso: python3 tesis/terminologicidad_anotada_2026-11/inventario_bilingue/generar.py"""
import csv, re, subprocess, os
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent; DATA = HERE.parent; ROOT = DATA.parents[1]
MAQ = ROOT / "tesis/maquetacion"
FORMAS = ROOT.parent / "tesis_material_tribunal/cap3_anotacion/formas_por_entrada.csv"
CATS_T = [("Metodología y diseño", "MET-DI"), ("Procesamiento lingüístico", "PROC-LIN"),
          ("Estadística y léxico", "EST-LEX"), ("Tecnología y formatos", "TEC-FOR")]
CATS_E = [("Recursos y corpus", "REC-COR"), ("Herramientas y software", "HER-SOFT"),
          ("Estándares y formatos técnicos", "EST-FOR"), ("Anotación y procesamiento lingüístico", "ANOT-PROC")]
dec = lambda x: f"{x:.4f}".replace(".", "{,}")
esc = lambda s: re.sub(r"([&%#_$])", r"\\\1", str(s))
cat_of = {}
for r in csv.DictReader(open(FORMAS, encoding="utf-8")):
    L = r["lengua"].lower(); cat_of[(L, r[f"denominacion_{L}"] or r["forma"])] = r["categoria"]

def body(lang, tipo):
    d = pd.read_csv(DATA / f"{lang}_terminologicidad.csv"); d = d[d.tipo == tipo].copy()
    d["cat"] = [cat_of[(lang, u)] for u in d.unit]
    lines = []
    for nombre, codigo in (CATS_T if tipo == "termino" else CATS_E):
        g = d[d.cat == nombre].sort_values("T", ascending=False)
        if g.empty: continue
        if lines: lines.append(r"\midrule")
        lines += [rf"\multicolumn{{7}}{{l}}{{\textbf{{{nombre} (\texttt{{{codigo}}})}}}} \\", r"\midrule"]
        for _, r in g.iterrows():
            f = r"\texttt" if nombre == "Herramientas y software" else r"\textit"
            lines.append(f"{f}{{{esc(r.forma)}}} & {r.freq} & {r.df} & {dec(r.tfidf_norm)} & "
                         f"{dec(r.cvalue_norm)} & {dec(r.nc_frantzi_norm)} & {dec(r['T'])} \\\\")
    return "\n".join(lines) + "\n", len(d)

def table(lang, tipo, caption):
    rows, n = body(lang, tipo); col = "Término" if tipo == "termino" else "Entidad"
    head = rf"\textbf{{{col}}} & \textbf{{Frec.}} & \textbf{{DF}} & \textbf{{\textit{{TF-IDF}}}} & \textbf{{\textit{{C-value}}}} & \textbf{{\textit{{NC-value}}}} & \textbf{{Terminologicidad}} \\"
    return (r"""{\footnotesize\setlength{\tabcolsep}{4pt}
\begin{longtable}{@{} >{\raggedright\arraybackslash}p{3.6cm} r r r r r r @{}}
\toprule
""" + head + r"""
\midrule
\endfirsthead
\multicolumn{7}{l}{\textit{(continuación)}}\\
\toprule
""" + head + r"""
\midrule
\endhead
\midrule
\multicolumn{7}{r}{\textit{Continúa en la página siguiente\ldots}}\\
\endfoot
\endlastfoot
""" + rows + r"""\bottomrule
\caption{""" + caption.replace("NN", str(n)) + r"""}
\end{longtable}}
""")

doc = r"""\setcounter{chapter}{1}
\section{Términos}
Los términos listados en esta sección designan conceptos, procesos, propiedades y metodologías centrales al dominio de la lingüística de corpus. Se presentan agrupados por categoría temática dentro de cada lengua, siguiendo una clasificación común de cuatro categorías ---Metodología y diseño (\texttt{MET-DI}), Procesamiento lingüístico (\texttt{PROC-LIN}), Estadística y léxico (\texttt{EST-LEX}) y Tecnología y formatos (\texttt{TEC-FOR})--- aplicada de manera idéntica al inglés y al español para facilitar la comparación interlingüística directa entre ambos inventarios. Dentro de cada categoría, las unidades se ordenan por terminologicidad. Todas las cifras se calculan sin las secciones de referencias bibliográficas de los documentos. Las frecuencias y las métricas se calculan sobre las apariciones que la revisión experta anotó como término o entidad, con todas las formas de cada unidad (la que figura en la tabla es la más frecuente), y no sobre todas las apariciones de la forma en el texto, que es lo que cuenta la extracción con TECLA para ordenar los candidatos (capítulo 5 de la tesis): así, una forma que también funciona en la lengua general, como \textit{muestra} (también del verbo \textit{mostrar}), solo cuenta sus usos terminológicos. El glosario (capítulo 7 de la tesis) recuenta las formas de cada concepto con el método descrito en el registro de normalización del glosario (carpeta \texttt{cap7\_glosario\_GLiCor} de este material), por lo que algunas cifras pueden diferir ligeramente entre ambos.

\subsection{Términos en inglés}
Léxico especializado organizado en las cuatro categorías comunes: Metodología y diseño (\textit{corpus linguistics}, \textit{representativeness}, \textit{query}, \textit{natural language processing}), Procesamiento lingüístico (\textit{annotation}, \textit{\texttt{POS} tagging}, \textit{token}, \textit{lemma}, \textit{parsing}), Estadística y léxico (\textit{frequency}, \textit{probability}, \textit{collocation}, \textit{keyword}) y Tecnología y formatos (\textit{metadata}, \textit{encoding}). \textit{Unicode} se clasifica como entidad y figura en la sección de estándares técnicos.

""" + table("en", "termino", r"Términos del inventario presentes en el subcorpus inglés (NN unidades), agrupados por categoría temática. DF = frecuencia de documento.\label{tab:anexo_terminos_en}") + r"""
\subsection{Términos en español}
Léxico especializado organizado en las mismas categorías: Metodología y diseño (\textit{corpus}, \textit{lingüística de corpus}, \textit{consulta}, \textit{concordancia}), Procesamiento lingüístico (\textit{anotación}, \textit{lema}, \textit{clase de palabras}, \textit{alineación}), Estadística y léxico (\textit{frecuencia}, \textit{muestra}, \textit{frecuencia normalizada}, \textit{colocación}) y Tecnología y formatos (\textit{codificación}, \textit{metadatos}).

""" + table("es", "termino", r"Términos del inventario presentes en el subcorpus español (NN unidades), agrupados por categoría temática. Mismas categorías que la Tabla~\ref{tab:anexo_terminos_en}.\label{tab:anexo_terminos_es}") + r"""
\section{Entidades}
Las entidades listadas en esta sección son denominaciones propias de recursos específicos, herramientas computacionales, proyectos de investigación y estándares técnicos relevantes para la lingüística de corpus. Se presentan agrupadas por categoría temática dentro de cada lengua ---Recursos y corpus (\texttt{REC-COR}), Herramientas y software (\texttt{HER-SOFT}), Estándares y formatos técnicos (\texttt{EST-FOR}) y Anotación y procesamiento lingüístico (\texttt{ANOT-PROC})---, con idéntica clasificación en inglés y en español. Las dos últimas categorías (capítulo 7 de la tesis, §~7.2) reúnen nombres propios que podrían tomarse por términos: los estándares y formatos (\textit{XML}, \textit{HTML}, \textit{SGML}, \textit{TEI}, \textit{UTF-8}, \textit{Unicode}, \textit{EAGLES}, \textit{Universal Dependencies}, \textit{Universal POS}) y el algoritmo de Lesk. Por la misma razón, \texttt{UKB}, nombre propio de un programa, figura en Herramientas y software. Dentro de cada categoría, las unidades se ordenan por terminologicidad.

\subsection{Entidades en inglés}
Incluye corpus de referencia de amplia circulación internacional (\textit{BNC}, \textit{Brown Corpus}, \textit{Penn Treebank}, \textit{COCA}) y herramientas de análisis y procesamiento (\texttt{CLAWS}, \texttt{Sketch Engine}, \texttt{WordSmith Tools}, \texttt{TreeTagger}, \texttt{AntConc}).

""" + table("en", "entidad", r"Entidades del inventario presentes en el subcorpus inglés (NN unidades), agrupadas por categoría temática.\label{tab:anexo_entidades_en}") + r"""
\subsection{Entidades en español}
Incluye una concentración marcada de corpus nacionales hispanohablantes (\textit{CREA}, \textit{CORDE}, \textit{PRESEEA}, \textit{CORPES XXI}, \textit{IULA}, \textit{Val.Es.Co}) que refleja la tradición historiográfica de la lingüística de corpus en español; también herramientas y plataformas de procesamiento (\texttt{FreeLing}, \texttt{Sketch Engine}, \texttt{BootCaT}, \texttt{TreeTagger}, \texttt{AntConc}).

""" + table("es", "entidad", r"Entidades del inventario presentes en el subcorpus español (NN unidades), agrupadas por categoría temática. Mismas categorías que la Tabla~\ref{tab:anexo_entidades_en}.\label{tab:anexo_entidades_es}")

main = (MAQ / "main.tex").read_text(encoding="utf-8")
pre = main[:main.index(r"\begin{document}")]
tex = pre + r"""\begin{document}
\pagestyle{plain}
\begin{center}{\Large\bfseries Inventario bilingüe de términos y entidades}\\[0.5em]{\normalsize Material complementario de la tesis doctoral \textit{Modelo teórico-computacional para la extracción automática de términos: una aproximación desde las tecnologías del lenguaje}. Isabel Moyano Moreno, Universidad de Cádiz, 2026.}\end{center}
\vspace{1em}
""" + doc + "\n\\end{document}\n"
(HERE / "inventario_bilingue.tex").write_text(tex, encoding="utf-8")
env = dict(os.environ, TEXINPUTS=f".:{MAQ}//:")
r = subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-bibtex-", "inventario_bilingue.tex"], cwd=HERE, env=env, capture_output=True, text=True)
print("latexmk", r.returncode)
