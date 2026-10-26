"""Figura del cap. 6: recuperación de los términos reservados según la frecuencia del tipo
(reserva del 20 %, media de las repeticiones): images/14_recall_frecuencia.png.
Las cifras son las de la Tabla tab:recall_frecuencia (resultados/recall_frecuencia.txt).
Uso: python figuras_cap6_frecuencia.py <carpeta_images>"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
IMG = sys.argv[1]
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 19})
MORADO, VERDE = "#6A4C93", "#12897B"
coma = lambda x: f"{x:.3f}".replace(".", ",")
coma1 = lambda x: f"{x:.1f}".replace(".", ",")
datos = {  # franja: (porcentaje de tipos, CRF, BiLSTM-CRF)
    "EN": [(15, 0.285, 0.197), (50, 0.198, 0.302), (35, 0.257, 0.355)],
    "ES": [(30, 0.170, 0.090), (49, 0.266, 0.321), (20, 0.344, 0.441)],
}
franjas = ["Raros\n(≤ 10)", "Medios\n(11–100)", "Frecuentes\n(> 100)"]
fig, axes = plt.subplots(1, 2, figsize=(18, 7.8), sharey=True)
w = 0.36
for ax, lang in zip(axes, ("EN", "ES")):
    for k, (col, dx) in enumerate(((MORADO, -w/2), (VERDE, w/2))):
        vals = [d[k + 1] for d in datos[lang]]
        xs = [i + dx for i in range(3)]
        ax.bar(xs, vals, w, color=col, edgecolor="white")
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.008, coma(v), ha="center", va="bottom", fontsize=16)
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{f}\n{d[0]} % de los tipos" for f, d in zip(franjas, datos[lang])])
    ax.set_title(lang, fontweight="bold", fontsize=23)
    ax.set_ylim(0, 0.5); ax.set_yticks([0, .1, .2, .3, .4, .5])
    ax.set_yticklabels([coma1(v) for v in [0, .1, .2, .3, .4, .5]])
    ax.grid(axis="y", color="#ddd"); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.set_xlabel("Frecuencia del tipo en el corpus")
axes[0].set_ylabel("Recuperación de los términos reservados")
fig.legend(handles=[Patch(color=MORADO, label="CRF"), Patch(color=VERDE, label="BiLSTM-CRF")],
           loc="lower center", ncol=2, frameon=False, fontsize=19)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(f"{IMG}/14_recall_frecuencia.png", dpi=200); plt.close(fig)
print("ok")
