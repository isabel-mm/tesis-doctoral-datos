"""
paso4_errores.py
────────────────
Análisis de errores a partir de las predicciones guardadas (no reentrena).
Por defecto usa la ejecución de la tesis: CRF, reserva del 20 %, semilla 42,
todos los rasgos (ablacion_<lang>_p20_s42_todas).

Para cada span de término gold: exacto / parcial (error de frontera) / perdido;
para cada span predicho que no solapa ningún gold: espurio. Se desglosa por
entrada reservada (nunca vista) frente a vista, y por longitud del span
(monoléxico / poliléxico).

Salidas en $RESULTADOS/errores/: <id>_spans.csv y <id>_resumen.json

Uso:  python paso4_errores.py [modelo] [id_ejecucion]
      python paso4_errores.py crf ablacion_en_p20_s42_todas
      python paso4_errores.py bilstm reserva_en_p20_s0
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from metricas import spans_termino  # noqa: E402

RES = Path(os.environ.get("RESULTADOS", HERE.parent / "resultados"))
OUT = RES / "errores"
OUT.mkdir(parents=True, exist_ok=True)


def analizar(modelo: str, rid: str):
    pred = pd.read_csv(RES / modelo / "pred" / f"{rid}.csv.gz", keep_default_na=False)
    res_file = RES / "crf" / "reservadas" / f"{rid}.json"
    reservadas = set(json.loads(res_file.read_text())) if res_file.exists() else set()
    if not reservadas and modelo == "bilstm":
        # el BiLSTM usa las mismas particiones que el CRF con la misma semilla y nivel
        alt = RES / "crf" / "reservadas" / f"{rid}_todas.json"
        reservadas = set(json.loads(alt.read_text())) if alt.exists() else set()
    filas = []
    for (doc, sid), g in pred.groupby(["doc_id", "sentence_id"], sort=False):
        g = g.sort_values("i")
        gold, prd = g["gold"].tolist(), g["pred"].tolist()
        toks = g["token"].tolist() if "token" in g else [""] * len(g)
        ents = g["entrada"].tolist() if "entrada" in g else [""] * len(g)
        gs, ps = spans_termino(gold), spans_termino(prd)
        pset = set(ps)
        for a, b in gs:
            sol = [(c, d) for c, d in ps if c < b and d > a]
            res = "perdido" if not sol else ("exacto" if (a, b) in pset else "parcial")
            filas.append({"doc_id": doc, "sentence_id": sid, "span": " ".join(map(str, toks[a:b])),
                          "entrada": ents[a], "n_tokens": b - a, "reservada": ents[a] in reservadas,
                          "tipo": "gold", "resultado": res,
                          "prediccion": " | ".join(" ".join(map(str, toks[c:d])) for c, d in sol)})
        for c, d in ps:
            if not any(a < d and b > c for a, b in gs):
                filas.append({"doc_id": doc, "sentence_id": sid, "span": " ".join(map(str, toks[c:d])),
                              "entrada": "", "n_tokens": d - c, "reservada": None,
                              "tipo": "predicho", "resultado": "espurio", "prediccion": ""})
    df = pd.DataFrame(filas)
    df.to_csv(OUT / f"{modelo}_{rid}_spans.csv", index=False)
    gold = df[df.tipo == "gold"].copy()
    gold["forma"] = gold["n_tokens"].map(lambda n: "monoléxico" if n == 1 else "poliléxico")
    resumen = {
        "modelo": modelo, "ejecucion": rid,
        "spans_gold": int(len(gold)), "spans_espurios": int((df.resultado == "espurio").sum()),
        "global": dict(Counter(gold["resultado"])),
        "por_reserva": {("reservada" if k else "vista"): dict(Counter(v["resultado"]))
                        for k, v in gold.groupby("reservada")},
        "por_forma": {k: dict(Counter(v["resultado"])) for k, v in gold.groupby("forma")},
        "reservadas_por_forma": {k: dict(Counter(v["resultado"]))
                                 for k, v in gold[gold.reservada == True].groupby("forma")},  # noqa: E712
        "espurios_mas_frecuentes": Counter(df[df.resultado == "espurio"]["span"].str.lower()).most_common(30),
    }
    (OUT / f"{modelo}_{rid}_resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1))
    print(json.dumps({k: resumen[k] for k in ("global", "por_reserva", "por_forma")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    modelo = sys.argv[1] if len(sys.argv) > 1 else "crf"
    if len(sys.argv) > 2:
        analizar(modelo, sys.argv[2])
    else:
        for lang in ("en", "es"):
            analizar("crf", f"ablacion_{lang}_p20_s42_todas")
