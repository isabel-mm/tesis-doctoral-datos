"""Figura del cap. 6: F1 de término en validación por época del BiLSTM-CRF
(reserva de tipos, 3 particiones por nivel): images/11_bilstm_epocas.png.
Uso: python figuras_cap6_epocas.py <resultados> <carpeta_images>"""
import csv, sys, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

R, IMG = sys.argv[1], sys.argv[2]
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 17})
VERDES = ["#0B5149", "#12897B", "#4FA99C"]  # una por partición (sorteo)
MARCAS = ["o", "s", "^"]
GRIS = "#555"
coma = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")

def leer(lang, pct, seed):
    filas = list(csv.DictReader(open(f"{R}/bilstm/epocas/reserva_{lang}_p{pct}_s{seed}.csv", encoding="utf-8")))
    ep, f1, corte = [], [], None
    for r in filas:
        perd = r["perdida_media"]
        if perd == "" or math.isnan(float(perd)):  # pérdida no numérica: el entrenamiento diverge
            corte = int(r["epoca"]); break
        ep.append(int(r["epoca"])); f1.append(float(r["val_f1_termino"]))
    return ep, f1, corte

niveles = [10, 20, 30, 50]
fig, axes = plt.subplots(2, 4, figsize=(20, 9.6), sharey=True, sharex=True)
for i, lang in enumerate(("en", "es")):
    for j, pct in enumerate(niveles):
        ax = axes[i, j]
        for s in range(3):
            ep, f1, corte = leer(lang, pct, s)
            c = VERDES[s]
            ax.plot(ep, f1, color=c, lw=2, marker=MARCAS[s], ms=5)
            k = max(range(len(f1)), key=f1.__getitem__)
            ax.plot(ep[k], f1[k], MARCAS[s], ms=12, mfc=c, mec="white", mew=2, zorder=5)
            if corte:
                ax.plot(corte, 0.33, marker="x", ms=10, mew=2.2, color=c, clip_on=False, zorder=5)
        if i == 0:
            ax.set_title(f"{pct} % reservado", fontsize=18)
        ax.set_ylim(0.30, 0.90); ax.set_xlim(0.5, 12.5)
        ax.set_xticks([1, 3, 5, 7, 9, 11])
        ax.set_yticks([.3, .4, .5, .6, .7, .8, .9])
        ax.set_yticklabels([coma(v) for v in [.3, .4, .5, .6, .7, .8, .9]])
        ax.grid(color="#e3e3e3"); ax.set_axisbelow(True)
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
        if i == 1: ax.set_xlabel("Época")
    axes[i, 0].set_ylabel(f"{lang.upper()}\nF1 de término (validación)")

ley = [Line2D([], [], color=VERDES[s], lw=2, marker=MARCAS[s], ms=5, label=f"Partición {s + 1}") for s in range(3)]
ley += [Line2D([], [], ls="", marker="o", ms=11, mfc=GRIS, mec="white", mew=2, label="Época elegida (marca grande)"),
        Line2D([], [], ls="", marker="x", ms=10, mew=2.2, color=GRIS, label="Pérdida no numérica: el entrenamiento diverge")]
fig.legend(handles=ley, loc="lower center", ncol=5, frameon=False, fontsize=16)
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(f"{IMG}/11_bilstm_epocas.png", dpi=200); plt.close(fig)
print("ok")

# Versión simplificada (para lectores no especializados): solo el 20 % reservado.
fig, axes = plt.subplots(1, 2, figsize=(16, 6.6), sharey=True)
for ax, lang in zip(axes, ("en", "es")):
    for s in range(3):
        ep, f1, corte = leer(lang, 20, s)
        c = VERDES[s]
        ax.plot(ep, f1, color=c, lw=2.2, marker=MARCAS[s], ms=6)
        k = max(range(len(f1)), key=f1.__getitem__)
        ax.plot(ep[k], f1[k], MARCAS[s], ms=14, mfc=c, mec="white", mew=2, zorder=5)
    ax.set_title(lang.upper(), fontweight="bold", fontsize=20)
    ax.set_ylim(0.40, 0.85); ax.set_xlim(0.6, 7.4); ax.set_xticks(range(1, 8))
    ax.set_yticks([.4, .5, .6, .7, .8]); ax.set_yticklabels([coma(v) for v in [.4, .5, .6, .7, .8]])
    ax.set_xlabel("Época (pasadas completas por el conjunto de entrenamiento)")
    ax.grid(color="#e3e3e3"); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
axes[0].set_ylabel("F1 de término en la validación")
axes[0].annotate("época elegida:\nmejor resultado", xy=(1, 0.762), xytext=(2.3, 0.815), fontsize=15,
                 arrowprops={"arrowstyle": "->", "color": GRIS, "lw": 1.4}, color="#333")
axes[0].annotate("seguir entrenando\nno mejora el resultado", xy=(4, 0.655), xytext=(4.6, 0.43), fontsize=15,
                 arrowprops={"arrowstyle": "->", "color": GRIS, "lw": 1.4}, color="#333")
ley = [Line2D([], [], color=VERDES[s], lw=2.2, marker=MARCAS[s], ms=6, label=f"Partición {s + 1}") for s in range(3)]
ley += [Line2D([], [], ls="", marker="o", ms=13, mfc=GRIS, mec="white", mew=2, label="Época elegida")]
fig.legend(handles=ley, loc="lower center", ncol=4, frameon=False, fontsize=16)
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(f"{IMG}/11_bilstm_epocas_simple.png", dpi=200); plt.close(fig)
print("ok simple")
