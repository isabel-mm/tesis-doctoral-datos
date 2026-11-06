"""Cifras del cap. 5 sobre el índice T, para un par de CSV ({en,es}_terminologicidad.csv).
Uso: python3 resumen_T.py <carpeta>"""
import sys
import pandas as pd
from scipy.stats import spearmanr
carpeta = sys.argv[1]
for lg in ("en", "es"):
    d = pd.read_csv(f"{carpeta}/{lg}_terminologicidad.csv")
    t = d[d.tipo == "termino"]
    share = (0.2 * t.context_factor / t.nc_frantzi).median()
    rho_tn = spearmanr(t.tfidf, t.nc_frantzi)[0]
    rho_nc = spearmanr(t.nc_frantzi, t.cvalue)[0]
    s = d.sort_values("T", ascending=False)["T"].values
    saltos = [(s[i] - s[i + 1]) / s[i] for i in range(len(s) - 1) if s[i + 1] > 0]
    grandes = [i + 1 for i, x in enumerate(saltos) if x > 0.40]
    mono = (t.unit.str.split().str.len() == 1).mean()
    print(f"{lg}: {len(t)} términos, {len(d) - len(t)} entidades | Spearman TF-IDF/NC {rho_tn:.3f} | "
          f"NC/C {rho_nc:.3f} | contexto {100 * share:.1f} % | mediana T términos {t['T'].median():.4f}, "
          f"entidades {d[d.tipo == 'entidad']['T'].median():.4f} | saltos >40 % en puestos {grandes} | "
          f"monoléxicos {100 * mono:.1f} %")
