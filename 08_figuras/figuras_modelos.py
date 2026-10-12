"""
Figuras del cap. 6 con los resultados definitivos de la reanotación (2026-10-09):

  images/01_holdout_tecla_barras.png   F1 global de los dos modelos (reserva de tipos)
  images/10_holdout_termino_barras.png F1 de término de los dos modelos (reserva de tipos)
  images/confusion_matrices.png        matrices de confusión término/no término (CV de 5 pliegues)

CRF: media ± DT de 10 semillas; BiLSTM-CRF: media ± DT de 3 semillas (particiones
= tres primeras semillas del CRF; época elegida en validación).

Uso:  python3 tesis/reanotacion_2026-10/figuras_modelos.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager, ticker
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "colab_reanotacion/resultados"
IMG = ROOT / "tesis/maquetacion/images"

MORADO, CORAL = "#6A4C93", "#D9603B"
if any("Times New Roman" in f.name for f in font_manager.fontManager.ttflist):
    plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({"font.size": 13, "axes.spines.top": False, "axes.spines.right": False})


def coma(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")


def miles(n):
    return f"{int(n):,}".replace(",", ".")


def cargar():
    c = pd.read_csv(RES / "crf/crf_reserva_todas.csv")
    c = c[c.exp == "reserva"]
    b = pd.read_csv(RES / "bilstm/bilstm_reserva_todas.csv")
    return c, b


def barras(c, b, col, ylabel, salida):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), sharey=True)
    niveles = [10, 20, 30, 50]
    x = np.arange(len(niveles))
    w = 0.36
    for ax, lang in zip(axes, ["en", "es"]):
        for k, (df, color, lab) in enumerate([
                (c, MORADO, "CRF (27 rasgos; media ± desv. típica, 10 semillas)"),
                (b, CORAL, "BiLSTM-CRF (media ± desv. típica, 3 semillas)")]):
            g = df[df.lang == lang].groupby("pct")[col]
            m, s = g.mean().reindex(niveles).values, g.std().reindex(niveles).values
            pos = x + (k - 0.5) * w
            ax.bar(pos, m, w, color=color, label=lab, edgecolor="white", linewidth=0.8)
            ax.errorbar(pos, m, yerr=s, fmt="none", ecolor="#333333", capsize=4, linewidth=1.1)
            for p, v, e in zip(pos, m, s):
                ax.text(p, v + e + 0.015, coma(v), ha="center", va="bottom", fontsize=11)
        ax.set_title(lang.upper(), fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{n} %" for n in niveles])
        ax.set_xlabel("Tipos terminológicos excluidos del entrenamiento")
        ax.set_ylim(0, 1.08)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: coma(v, 1)))
        ax.grid(axis="y", color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)
    axes[0].set_ylabel(ylabel)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(IMG / salida, dpi=300, bbox_inches="tight")
    plt.close(fig)


def matrices():
    cv = {"CRF": pd.read_csv(RES / "crf/crf_cv_todas.csv"),
          "BiLSTM-CRF": pd.read_csv(RES / "bilstm/bilstm_cv_todas.csv")}
    fig, axes = plt.subplots(2, 2, figsize=(11, 10))
    for i, lang in enumerate(["en", "es"]):
        for j, (modelo, color) in enumerate([("CRF", MORADO), ("BiLSTM-CRF", CORAL)]):
            d = cv[modelo]
            s = d[d.lang == lang][["tn_termino", "fp_termino", "fn_termino", "tp_termino"]].sum()
            m = np.array([[s.tn_termino, s.fp_termino], [s.fn_termino, s.tp_termino]])
            ax = axes[i, j]
            cmap = LinearSegmentedColormap.from_list("c", ["#ffffff", color])
            # intensidad por fila (proporción sobre la clase real), para que se vean las dos filas
            ax.imshow(m / m.sum(axis=1, keepdims=True), cmap=cmap, vmin=0, vmax=1)
            for (r, k), v in np.ndenumerate(m):
                prop = v / m[r].sum()
                ax.text(k, r, miles(v), ha="center", va="center", fontsize=15, fontweight="bold",
                        color="white" if prop > 0.5 else "#222222")
            ax.set_xticks([0, 1]); ax.set_xticklabels(["No término", "Término"])
            ax.set_yticks([0, 1]); ax.set_yticklabels(["No término", "Término"])
            ax.set_xlabel("Predicho"); ax.set_ylabel("Real")
            ax.set_title(f"{modelo} ({lang.upper()})", fontweight="bold", color=color)
            for sp in ax.spines.values():
                sp.set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "confusion_matrices.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    c, b = cargar()
    barras(c, b, "f1_global", "F1 global (ponderado por etiqueta)", "01_holdout_tecla_barras.png")
    barras(c, b, "f1_termino", "F1 (específico de término)", "10_holdout_termino_barras.png")
    matrices()
    print("figuras guardadas en", IMG)


if __name__ == "__main__":
    main()
