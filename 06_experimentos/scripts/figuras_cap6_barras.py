"""Figuras de barras del cap. 6 (F1 de término y F1 global con reserva de tipos):
images/10_holdout_termino_barras.png e images/01_holdout_tecla_barras.png.
Uso: python figuras_cap6_barras.py <resultados> <carpeta_images>"""
import csv, sys, statistics as st
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R, IMG = sys.argv[1], sys.argv[2]
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 19})
MORADO, CORAL = "#6A4C93", "#D9603B"
def cargar(f, col):
    d = defaultdict(list)
    for r in csv.DictReader(open(f, encoding="utf-8")):
        d[(r["lang"], int(float(r["pct"])))].append(float(r[col]))
    return d
coma = lambda x: f"{x:.2f}".replace(".", ",")
def figura(col, ylabel, salida):
    crf = cargar(f"{R}/crf/crf_reserva_todas.csv", col)
    bil = cargar(f"{R}/bilstm/bilstm_reserva_todas.csv", col)
    fig, axes = plt.subplots(1, 2, figsize=(20.7, 8.4), sharey=True)
    niveles = [10, 20, 30, 50]; w = 0.36
    for ax, lang in zip(axes, ("en", "es")):
        for k, (d, color, dx) in enumerate(((crf, MORADO, -w/2), (bil, CORAL, w/2))):
            m = [st.mean(d[(lang, n)]) for n in niveles]; s = [st.stdev(d[(lang, n)]) for n in niveles]
            xs = [i + dx for i in range(4)]
            ax.bar(xs, m, w, color=color, edgecolor="white", yerr=s, capsize=5, error_kw={"elinewidth": 1.2, "ecolor": "#333"})
            for x, mi, si in zip(xs, m, s):
                ax.text(x, mi + si + 0.015, coma(mi), ha="center", va="bottom", fontsize=17)
        ax.set_title(lang.upper(), fontweight="bold", fontsize=23)
        ax.set_xticks(range(4)); ax.set_xticklabels([f"{n} %" for n in niveles])
        ax.set_xlabel("Tipos terminológicos reservados")
        ax.set_ylim(0, 1.08); ax.set_yticks([0, .2, .4, .6, .8, 1.0])
        ax.set_yticklabels([coma(v)[:3] for v in [0, .2, .4, .6, .8, 1.0]])
        ax.grid(axis="y", color="#ddd"); ax.set_axisbelow(True)
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    axes[0].set_ylabel(ylabel)
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=MORADO, label="CRF (27 rasgos; media ± desv. típica, 10 repeticiones)"),
                        Patch(color=CORAL, label="BiLSTM-CRF (media ± desv. típica, 3 repeticiones)")],
               loc="lower center", ncol=2, frameon=False, fontsize=19)
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    fig.savefig(f"{IMG}/{salida}", dpi=200); plt.close(fig)
figura("f1_termino", "F1 (específico de término)", "10_holdout_termino_barras.png")
figura("f1_global", "F1 global (ponderado por etiqueta)", "01_holdout_tecla_barras.png")
print("ok")
