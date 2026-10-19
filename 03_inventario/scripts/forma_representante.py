"""Añade a {en,es}_terminologicidad.csv la columna «forma»: la forma del corpus que representa
a cada unidad en el cálculo (la más frecuente entre sus formas anotadas), con el mismo recuento
que recalculo_ncvalue.py (formas en minúscula; siglas en minúscula no cuentan como la sigla)."""
import re
from collections import Counter
import pandas as pd
import indice_T_glicor as ig

rc = ig.rc
for lang in ("en", "es"):
    rc.FORM_ALIASES.clear()
    rc.FORM_ALIASES["Tweepy"] = [("tweepy7",)]
    terms, ents = ig.glicor_units(lang)
    names = terms + ents
    rc.ACRONYMS.clear()
    rc.ACRONYMS.update(t.lower() for n in names for t in re.split(r"[\s-]+", n) if len(t) > 1 and t.isupper())
    alias = {n: rc.tokenize_name(n) | set(rc.FORM_ALIASES.get(n, [])) for n in names}
    keys = set().union(*alias.values())
    mx = max(map(len, keys))
    freq = Counter()
    for d in rc.load_sentences(lang):
        for sent in d["sentences"]:
            forms = [rc.norm(t["text"]) for t in sent]
            for n in range(1, mx + 1):
                for i in range(len(forms) - n + 1):
                    k = tuple(forms[i:i + n])
                    if k in keys:
                        freq[k] += 1
    best = {n: max(alias[n], key=lambda k: freq[k]) for n in names}
    out = pd.read_csv(f"{lang}_terminologicidad.csv")
    out["forma"] = [" ".join(best[u]).replace(" - ", "-").replace(" ’", "’").replace(" '", "'") for u in out.unit]
    out["freq_forma"] = [freq[best[u]] for u in out.unit]
    # siglas con puntos (Val.Es.Co): el script original las cuenta sobre el documento entero
    out.loc[out.freq != out.freq_forma, "forma"] = out.unit
    out.to_csv(f"{lang}_terminologicidad.csv", index=False)
    print(lang, "discrepancias freq:", (out.freq != out.freq_forma).sum())
