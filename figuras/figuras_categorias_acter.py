"""Figuras con la paleta de la tesis (morados y verdes):
- images/fig_categorias_glosario.png (cap. 7): entradas de GLiCor por categoría (glosario_GLiCor/entries.json, 261 entradas).
- images/13_acter_validacion.png (cap. 6): F1 de término en ACTER (Tabla tab:acter_results).
Uso: python figuras_categorias_acter.py <carpeta_images>"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
IMG = sys.argv[1]
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 19, "hatch.color": "white", "hatch.linewidth": 1.2})
MORADO, VERDE = "#6A4C93", "#12897B"
CATS = [("Metodología y\ndiseño\n(MET-DI)", "#0B5149"), ("Procesamiento\nlingüístico\n(PROC-LIN)", "#12897B"),
        ("Estadística y\nléxico\n(EST-LEX)", "#4FA99C"), ("Tecnología y\nformatos\n(TEC-FOR)", "#8CCBC2"),
        ("Recursos y\ncorpus\n(REC-COR)", "#3D2A5C"), ("Herramientas y\nsoftware\n(HER-SOFT)", "#6A4C93"),
        ("Estándares y\nformatos\ntécnicos", "#A23E68"), ("Anotación y\nprocesamiento\nlingüístico", "#B9A6D9")]
X = [0, 1, 2, 3, 4.6, 5.6, 6.6, 7.6]
coma = lambda v, d: f"{v:.{d}f}".replace(".", ",")
def ejes(ax, ylabel, ymax):
    ax.set_xticks(X); ax.set_xticklabels([c for c, _ in CATS], fontsize=16)
    ax.set_ylabel(ylabel); ax.set_ylim(0, ymax)
    ax.axvline(3.8, color="#999", ls=":", lw=1.5)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5"); ax.set_axisbelow(True)
    ax.text(1.5, -0.30, "TÉRMINOS", transform=ax.get_xaxis_transform(), ha="center", fontweight="bold", fontsize=18)
    ax.text(6.1, -0.30, "ENTIDADES", transform=ax.get_xaxis_transform(), ha="center", fontweight="bold", fontsize=18)
# --- cap. 7: glosario
G = [56, 39, 52, 4, 58, 42, 9, 1]
fig, ax = plt.subplots(figsize=(18.3, 8.6))
for x, (_, col), n in zip(X, CATS, G):
    v = 100 * n / 261
    ax.bar(x, v, 0.7, color=col, edgecolor="white")
    ax.text(x, v + 0.4, f"{coma(v, 1)} %\n(n = {n})", ha="center", va="bottom", fontsize=15)
ejes(ax, "% sobre el total de entradas", 30)
fig.tight_layout(); fig.savefig(f"{IMG}/fig_categorias_glosario.png", dpi=200); plt.close(fig)
# --- cap. 6: ACTER
res = {"crf": [0.805, 0.784, 0.772, 0.717], "bil": [0.868, 0.849, 0.785, 0.754]}
lodo = {"crf": [0.374, 0.478, 0.137, 0.528], "bil": [0.333, 0.204, 0.189, 0.160]}
fig, axes = plt.subplots(1, 2, figsize=(20.7, 8.4), sharey=True); w = 0.36
for ax, d, labels, xl, tit in ((axes[0], res, ["10 %", "20 %", "30 %", "50 %"], "Tipos terminológicos reservados", "Reserva de tipos"),
                               (axes[1], lodo, ["corp\n(corrupción)", "equi\n(doma clásica)", "htfl\n(insuf. cardíaca)", "wind\n(eólica)"], "Dominio de ACTER evaluado", "LODO (dominio excluido)")):
    for vals, col, dx in ((d["crf"], MORADO, -w/2), (d["bil"], VERDE, w/2)):
        xs = [i + dx for i in range(4)]
        ax.bar(xs, vals, w, color=col, edgecolor="white", linewidth=1.5)
        for x, v in zip(xs, vals): ax.text(x, v + 0.015, coma(v, 3), ha="center", va="bottom", fontsize=16)
    ax.set_title(tit, fontweight="bold", fontsize=22); ax.set_xticks(range(4)); ax.set_xticklabels(labels)
    ax.set_xlabel(xl); ax.set_ylim(0, 1.08); ax.set_yticks([0, .2, .4, .6, .8, 1.0])
    ax.set_yticklabels([coma(v, 1) for v in [0, .2, .4, .6, .8, 1.0]])
    ax.grid(axis="y", color="#ddd"); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
axes[0].set_ylabel("F1 (específico de término)")
fig.legend(handles=[Patch(color=MORADO, label="CRF (27 rasgos)"), Patch(color=VERDE, label="BiLSTM-CRF")], loc="lower center", ncol=2, frameon=False, fontsize=19)
fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(f"{IMG}/13_acter_validacion.png", dpi=200); plt.close(fig)
print("ok")
