"""Quita las bibliografías de tesis/bio/{en,es}_bio_tokens.csv (la fuente de las frecuencias del
índice T, tesis/terminologicidad_2026-10/recalculo_ncvalue.py). Igual que filtrar_bibliografia.py,
pero cada fila lleva en «path» el texto del que procede (relativo a repo_tesis), y los tokens se
buscan en ese texto tal cual. Salida: bio_sinbib/{en,es}_bio_tokens.csv en esta carpeta."""
import csv, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from tecla.corpus.cleaning import bibliography_spans
csv.field_size_limit(10**9)
(HERE / "bio_sinbib").mkdir(exist_ok=True)
for lang in ("en", "es"):
    with open(ROOT / f"tesis/bio/{lang}_bio_tokens.csv", encoding="utf-8", newline="") as fi, \
         open(HERE / f"bio_sinbib/{lang}_bio_tokens.csv", "w", encoding="utf-8", newline="") as fo:
        rd = csv.reader(fi); wr = csv.writer(fo); head = next(rd); wr.writerow(head)
        i_doc, i_path, i_tok = head.index("doc_id"), head.index("path"), head.index("token")
        cur = None; tot = drop = lost = docs_cut = 0
        for row in rd:
            if row[i_doc] != cur:
                cur = row[i_doc]; text = (ROOT / row[i_path]).read_text(encoding="utf-8", errors="replace")
                R = bibliography_spans(text, lang)
                docs_cut += bool(R); pos = 0
            tot += 1; tok = row[i_tok]; j = text.find(tok, pos)
            if j < 0: lost += 1; j = pos
            else: pos = j + len(tok)
            if any(a <= j < b for a, b in R): drop += 1; continue
            wr.writerow(row)
    print(lang, f"tokens {tot}, en bibliografías {drop} ({100*drop/tot:.1f} %), documentos con bibliografía {docs_cut}, no localizados {lost}", flush=True)
