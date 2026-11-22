"""Figura del README: F1 de término con validación cruzada (términos ya vistos) frente a la
reserva del 10 % de los tipos (términos nuevos). Cifras de la tesis (cap. 7, tabla de F1 de término)."""
import matplotlib.pyplot as plt
from matplotlib import font_manager
MORADO, VERDE, TINTA, GRIS = "#6A4C93", "#12897B", "#222222", "#6b6b6b"
datos = {"Inglés": {"CRF": (0.854, 0.628), "BiLSTM-CRF": (0.990, 0.722)},
         "Español": {"CRF": (0.838, 0.660), "BiLSTM-CRF": (0.983, 0.736)}}
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 12})
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
for ax, (lengua, d) in zip(axes, datos.items()):
    for modelo, color in (("CRF", MORADO), ("BiLSTM-CRF", VERDE)):
        a, b = d[modelo]
        ax.plot([0, 1], [a, b], color=color, lw=2.2, solid_capstyle="round", zorder=2)
        ax.scatter([0, 1], [a, b], s=70, color=color, edgecolor="white", linewidth=2, zorder=3)
        ax.text(-0.06, a, f"{a:.2f}".replace(".", ","), ha="right", va="center", color=TINTA, fontsize=11)
        ax.text(1.06, b, f"{b:.2f}  {modelo}".replace(".", ",", 1), ha="left", va="center", color=TINTA, fontsize=11)
    ax.set_title(lengua, fontsize=13, fontweight="bold", color=TINTA)
    ax.set_xlim(-0.45, 1.75); ax.set_ylim(0.55, 1.03)
    ax.set_xticks([0, 1], ["Validación cruzada\n(términos ya vistos)", "Reserva del 10 %\n(términos nuevos)"], color=TINTA)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bbbbbb"); ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", length=0, colors=GRIS); ax.grid(axis="y", color="#e6e6e6", lw=0.8); ax.set_axisbelow(True)
    ax.set_yticks([0.6, 0.7, 0.8, 0.9, 1.0], ["0,6", "0,7", "0,8", "0,9", "1,0"])
axes[0].set_ylabel("F$_1$ de término", color=TINTA)
fig.suptitle("La evaluación habitual mide, sobre todo, memoria", fontsize=15, fontweight="bold", color=TINTA, x=0.02, ha="left")
fig.text(0.02, 0.9, "F$_1$ de término de los dos modelos cuando los términos de la prueba se han visto en el entrenamiento y cuando no",
         fontsize=11, color=GRIS, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig("figuras/memoria_frente_a_generalizacion.png", dpi=200, facecolor="white")
