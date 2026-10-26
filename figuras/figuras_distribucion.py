"""
Figuras de distribución del cap. 5 (saturación, Zipf log-log y 10 primeros
términos) a partir de las salidas de distribucion_reanotacion.py.

Uso:    python3 tesis/reanotacion_2026-10/figuras_distribucion.py
Salida: tesis/maquetacion/images/{10_saturacion_terminologica,
        11_zipf_general_vs_termino,12_zipf_visual_simple}.png
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IMG = ROOT / "tesis/maquetacion/images"
COL = {"en": "#6A4C93", "es": "#12897B"}
INK, MUTED, GRID = "#1f2937", "#6b7280", "#dddddd"
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 15,
                     "axes.edgecolor": "#cccccc", "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.linewidth": 1.5})
N_TOP = 10
ENTRIES = {e["slug"]: e for e in json.load(open(ROOT / "colab_reanotacion/datos/glicor/entradas.json"))}


def fmt(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def miles(n):
    return f"{int(n):,}".replace(",", " ")


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=1)
    ax.set_axisbelow(True)


def saturacion():
    fig, ax = plt.subplots(figsize=(10, 5.7), dpi=224)
    for lang in ("en", "es"):
        s = pd.read_csv(HERE / f"saturacion_{lang}.csv")
        ax.fill_between(s.pct_tokens, s.pct_tipos_p05, s.pct_tipos_p95, color=COL[lang], alpha=0.15, lw=0, step="post")
        ax.plot(s.pct_tokens, s.pct_tipos_media, color=COL[lang], lw=2.5, label=lang.upper())
        x80 = s.pct_tokens.values[np.searchsorted(s.pct_tipos_media.values, 80)]
        ax.plot([x80, x80], [0, 80], ls=":", color=COL[lang], lw=1.3)
        ax.text(x80 + 1, 3, f"{fmt(x80)} %", color=COL[lang], fontsize=14)
    ax.axhline(80, color=GRID, lw=1)
    ax.text(60, 76, "80 % del inventario", color=MUTED, fontsize=13)
    ax.set(xlim=(0, 100), ylim=(0, 102), xlabel="% del corpus recorrido", ylabel="% de los tipos de término")
    style(ax)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(IMG / "10_saturacion_terminologica.png")


def zipf():
    exp = pd.read_csv(HERE / "zipf_exponentes.csv").set_index("Lang")
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), dpi=224)
    for ax, lang in zip(axes, ("en", "es")):
        g = pd.read_csv(HERE / f"zipf_general_{lang}.csv")
        t = pd.read_csv(HERE / f"zipf_termino_{lang}.csv")
        ax.loglog(g.rango, g.frecuencia, color=COL["en"], lw=2, label="Vocabulario general")
        ax.loglog(t.rango, t.frecuencia, color=COL["es"], lw=2.8, label="Inventario terminológico")
        e = exp.loc[lang.upper()]
        ax.set_title(f"{lang.upper()}  (α general = {fmt(e.Exponente_general, 2)} · "
                     f"α términos = {fmt(e.Exponente_termino, 2)})", fontweight="bold", color=INK, fontsize=15)
        ax.set_xlabel("Rango (log)")
        style(ax)
    axes[0].set_ylabel("Frecuencia (log)")
    axes[0].legend(frameon=False, loc="upper right", fontsize=13)
    fig.tight_layout()
    fig.savefig(IMG / "11_zipf_general_vs_termino.png")


def top12():
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 8.5), dpi=224)
    for ax, lang in zip(axes, ("en", "es")):
        t = pd.read_csv(HERE / f"zipf_termino_{lang}.csv")
        head, rest = t.head(N_TOP), t.iloc[N_TOP:]
        labels = [ENTRIES[s][f"term_{lang}"] for s in head.tipo]
        labels.append(f"+{len(rest)} términos más\n({round(rest.frecuencia.mean())} apariciones de media cada uno)")
        vals = list(head.frecuencia) + [rest.frecuencia.mean()]
        y = np.arange(len(vals))[::-1]
        ax.barh(y, vals, color=[COL[lang]] * N_TOP + ["#bbbbbb"], height=0.65)
        for yi, v in zip(y, vals):
            ax.text(v + max(vals) * 0.015, yi, miles(round(v)), va="center", fontsize=12, color=INK)
        ax.set_yticks(y, labels, fontsize=13)
        ax.set_xlim(0, max(vals) * 1.15)
        ax.set_title(lang.upper(), fontweight="bold", color=INK)
        ax.set_xlabel("Apariciones en el corpus")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.grid(axis="x", color=GRID)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(IMG / "12_zipf_visual_simple.png")


if __name__ == "__main__":
    saturacion()
    zipf()
    top12()
