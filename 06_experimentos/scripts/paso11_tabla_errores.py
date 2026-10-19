"""Tabla de errores para el material complementario: una fila por error ante los términos reservados
(apariciones no reconocidas enteras) y por falso positivo, para CRF y BiLSTM-CRF, los cuatro niveles de
reserva y las particiones 0-2 comunes a los dos modelos. No incluye el texto de las oraciones.
Uso: python paso11_tabla_errores.py <resultados> <salida.csv>"""
import csv, gzip, json, sys
from collections import defaultdict
R, OUT = sys.argv[1], sys.argv[2]
def spans(labels):
    out = []; start = None
    for i, l in enumerate(labels + ["O"]):
        if l == "B-T" or l == "O" or (l == "I-T" and start is None):
            if start is not None: out.append((start, i)); start = None
            if l in ("B-T", "I-T"): start = i
    return out
def load(f):
    sents = defaultdict(list)
    for r in csv.DictReader(gzip.open(f, "rt", encoding="utf-8")):
        sents[(r["doc_id"], r["sentence_id"])].append(r)
    return sents
cols = ["lengua", "modelo", "reserva_pct", "particion", "documento", "oracion", "entrada_glicor",
        "termino_esperado", "n_tokens_termino", "prediccion", "tipo_error"]
w = csv.DictWriter(open(OUT, "w", encoding="utf-8", newline=""), fieldnames=cols); w.writeheader()
n = 0
for lang in ("en", "es"):
    for pct in (10, 20, 30, 50):
        for seed in "012":
            crf = load(f"{R}/crf/pred/reserva_{lang}_p{pct}_s{seed}_todas.csv.gz")
            rv = set(json.load(open(f"{R}/crf/reservadas/reserva_{lang}_p{pct}_s{seed}_todas.json", encoding="utf-8")))
            bp = {}
            for r in csv.DictReader(gzip.open(f"{R}/bilstm/pred/reserva_{lang}_p{pct}_s{seed}.csv.gz", "rt", encoding="utf-8")):
                bp[(r["doc_id"], r["sentence_id"], r["i"])] = r["pred"]
            for model in ("CRF", "BiLSTM-CRF"):
                for (doc, sid), rows in crf.items():
                    rows.sort(key=lambda r: int(r["i"]))
                    toks = [r["token"] for r in rows]; gold = [r["gold"] for r in rows]
                    pred = [r["pred"] if model == "CRF" else bp.get((doc, sid, r["i"]), "O") for r in rows]
                    gs, ps = spans(gold), spans(pred)
                    base = dict(lengua=lang.upper(), modelo=model, reserva_pct=pct, particion=seed, documento=doc, oracion=sid)
                    for a, b in gs:
                        e = rows[a]["entrada"]
                        if e not in rv or (a, b) in ps: continue
                        ov = [(x, y) for x, y in ps if x < b and y > a]
                        if not ov: t = "omisión de un término monoléxico" if b - a == 1 else "omisión de un término poliléxico"; p = ""
                        else:
                            x, y = ov[0]; p = " ".join(toks[x:y])
                            t = ("delimitación por defecto" if x >= a and y <= b else
                                 "delimitación por exceso" if x <= a and y >= b else "solapamiento parcial")
                        w.writerow({**base, "entrada_glicor": e, "termino_esperado": " ".join(toks[a:b]),
                                    "n_tokens_termino": b - a, "prediccion": p, "tipo_error": t}); n += 1
                    for x, y in ps:
                        if not any(a < y and b > x for a, b in gs):
                            w.writerow({**base, "entrada_glicor": "", "termino_esperado": "", "n_tokens_termino": "",
                                        "prediccion": " ".join(toks[x:y]), "tipo_error": "falso positivo"}); n += 1
print(n, "filas")
