"""Cifras del texto (caps. 5-6) sobre el índice T y la incrustación, calculadas con
{en,es}_terminologicidad.csv de esta carpeta (apariciones anotadas)."""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr
HERE = Path(__file__).resolve().parent
for lg in ("en", "es"):
    d = pd.read_csv(HERE / f"{lg}_terminologicidad.csv")
    t = d[d.tipo == "termino"].copy()
    share = (0.2 * t.context_factor / t.nc_frantzi).median()
    s = d.sort_values("T", ascending=False)["T"].values
    saltos = [(s[i] - s[i + 1]) / s[i] for i in range(len(s) - 1) if s[i + 1] > 0]
    grandes = [i + 1 for i, x in enumerate(saltos) if x > 0.40]
    print(f"== {lg}: {len(t)} términos, {len(d) - len(t)} entidades")
    print(f"  Spearman TF-IDF/NC (términos) {spearmanr(t.tfidf, t.nc_frantzi)[0]:.3f} | NC/C {spearmanr(t.nc_frantzi, t.cvalue)[0]:.3f}")
    print(f"  contexto (mediana) {100 * share:.1f} % | mediana T términos {t['T'].median():.4f}, entidades {d[d.tipo == 'entidad']['T'].median():.4f}")
    print(f"  saltos >40 % en puestos {grandes}")
    nuc = t[t.chains > 0]
    print(f"  incrustación: {len(nuc)} términos nucleares ({100 * len(nuc) / len(t):.1f} %); "
          f"apariciones incrustadas {100 * t.nested.sum() / t.total.sum():.1f} % del total de apariciones de término")
    print("  nucleares:", nuc.sort_values("chains", ascending=False)[["forma", "total", "freq", "nested", "chains"]].head(12).to_string(index=False))
    # pares en que TF-IDF y NC-value ordenan al revés (para el ejemplo del texto)
    t = t.sort_values("T", ascending=False).head(40)
    best = []
    for i, a in t.iterrows():
        for j, b in t.iterrows():
            if a.freq < b.freq and a.df > b.df + 10 and a.tfidf < b.tfidf and a.nc_frantzi > b.nc_frantzi:
                best.append((a.forma, a.freq, a.df, b.forma, b.freq, b.df))
    print("  ejemplos TF-IDF/NC opuestos:", best[:6])
