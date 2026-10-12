"""
paso5_vocabulario.py
────────────────────
¿De dónde procede la ventaja del BiLSTM-CRF sobre los términos reservados?

Los dos modelos se evalúan sobre las mismas particiones de reserva de tipos,
pero el BiLSTM-CRF representa las palabras (vocabulario de entrenamiento) y el
CRF no. Este análisis separa las apariciones de los términos reservados en dos
grupos, según que todas sus palabras estén en el vocabulario de entrenamiento
del BiLSTM-CRF («sin palabras fuera de vocabulario») o que alguna no lo esté
(«con alguna palabra fuera de vocabulario», OOV), y compara en cada grupo la recuperación de los dos modelos:

  - por token: proporción de tokens de término reservados que el modelo
    etiqueta como término (B-T o I-T), como la recuperación restringida del cap. 6;
  - por aparición: proporción de apariciones reservadas reconocidas exactamente
    (mismos límites y etiquetas B-T/I-T).

Usa las predicciones ya guardadas (sin reentrenar) y reproduce la partición y
el vocabulario de paso3_bilstm.py (entrenamiento sin el conjunto de validación).

Uso:    python3 colab_reanotacion/scripts/paso5_vocabulario.py
Salida: resultados/errores/vocabulario_reservados.csv (por ejecución) y resumen en pantalla.
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paso3_bilstm as B  # noqa: E402

RES = HERE.parent / "resultados"
OUT = RES / "errores"
OUT.mkdir(exist_ok=True)


def apariciones(oraciones, reservadas):
    """Una fila por token de las oraciones de prueba, con la aparición reservada a la que pertenece."""
    filas, span = [], -1
    for o in oraciones:
        actual = None
        for i, (tok, lab, ent) in enumerate(zip(o["tokens"], o["labels"], o["entradas"])):
            if lab == "B-T" or (lab == "I-T" and actual is None):
                span += 1
                actual = span if ent in reservadas else None
            elif lab == "O":
                actual = None
            filas.append((o["doc_id"], o["sentence_id"], i, tok, lab, actual))
    return pd.DataFrame(filas, columns=["doc_id", "sentence_id", "i", "tok", "gold", "span"])


def main():
    filas = []
    for lang in ("en", "es"):
        oraciones, entradas = B.cargar(lang)
        for pct in (10, 20, 30, 50):
            for seed in (0, 1, 2):
                train, test, reservadas = B.particion_reserva(oraciones, entradas, pct, seed)
                train, _ = B.separar_validacion(train, seed, por_entradas=True)
                vocab = {t for o in train for t in o["tokens"]}
                df = apariciones(test, reservadas)
                rid = f"reserva_{lang}_p{pct}_s{seed}"
                pb = pd.read_csv(RES / "bilstm" / "pred" / f"{rid}.csv.gz")
                pc = pd.read_csv(RES / "crf" / "pred" / f"{rid}_todas.csv.gz", usecols=["doc_id", "sentence_id", "i", "gold", "pred"])
                key = ["doc_id", "sentence_id", "i"]
                df = df.merge(pb[key + ["pred"]].rename(columns={"pred": "bilstm"}), on=key) \
                       .merge(pc[key + ["pred"]].rename(columns={"pred": "crf"}), on=key)
                r = df[df.span.notna()].copy()
                r["en_vocab"] = r.tok.isin(vocab)
                grupo = r.groupby("span").en_vocab.all().map({True: "sin palabras fuera de vocabulario", False: "con alguna palabra fuera de vocabulario"})
                r["grupo"] = r.span.map(grupo)
                for g, sub in r.groupby("grupo"):
                    fila = {"lang": lang, "pct": pct, "seed": seed, "grupo": g,
                            "apariciones": sub.span.nunique(), "tokens": len(sub)}
                    for m in ("bilstm", "crf"):
                        fila[f"r_token_{m}"] = (sub[m] != "O").mean()
                        exacta = sub.assign(ok=sub[m] == sub.gold).groupby("span").ok.all()
                        fila[f"r_aparicion_{m}"] = exacta.mean()
                    filas.append(fila)
                print(rid, "ok", flush=True)
    res = pd.DataFrame(filas)
    res.to_csv(OUT / "vocabulario_reservados.csv", index=False)
    tot = res.groupby(["lang", "grupo"]).apply(lambda g: pd.Series({
        "apariciones": g.apariciones.sum(),
        "% apariciones": None,
        **{c: (g[c] * g.apariciones).sum() / g.apariciones.sum() for c in
           ["r_token_bilstm", "r_token_crf", "r_aparicion_bilstm", "r_aparicion_crf"]}}))
    tot["% apariciones"] = tot.apariciones / tot.groupby(level=0).apariciones.transform("sum")
    print(tot.round(3).to_string())


if __name__ == "__main__":
    main()
