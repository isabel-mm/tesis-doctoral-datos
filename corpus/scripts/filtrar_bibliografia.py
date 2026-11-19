"""
Versión de la anotación sin las bibliografías (opción B, 7-nov-2026).

El cap. 3 dice que las secciones de referencias se eliminan antes de anotar y
de contar frecuencias, pero los textos de colab_reanotacion/datos/corpus las
conservaban. Este script localiza, en cada documento, las listas de referencias y el índice
final (tecla.corpus.cleaning.bibliography_spans, la misma función de TECLA) y
escribe los ficheros BIO sin los tokens que caen dentro de ellos. Los tokens se sitúan en el texto reparado (glicor_match.clean, el mismo
que usa paso1_generar_bio.py) buscándolos uno tras otro, en orden.

Entrada:  colab_reanotacion/datos_generados/{en,es}_bio_tokens[_terms_only].csv
Salida:   colab_reanotacion/datos_generados_sinbib/ (mismos nombres) y,
          en esta carpeta, resumen_por_documento.csv
Uso:      python3 tesis/sin_bibliografia_2026-11/filtrar_bibliografia.py
"""
import csv, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "colab_reanotacion/scripts"))
from tecla.corpus.cleaning import bibliography_spans
from glicor_match import clean
csv.field_size_limit(10**9)
SRC = ROOT / "colab_reanotacion/datos_generados"; DST = ROOT / "colab_reanotacion/datos_generados_sinbib"
CORPUS = ROOT / "colab_reanotacion/datos/corpus"
DST.mkdir(exist_ok=True)

def bib_ranges(raw, lang):
    """Tramos de las bibliografías (y del índice final) en el texto reparado."""
    return [(len(clean(raw[:a])), len(clean(raw[:b]))) for a, b in bibliography_spans(raw, lang)]

resumen = []
for lang in ("en", "es"):
    for kind in ("bio_tokens", "bio_tokens_terms_only"):
        src = SRC / f"{lang}_{kind}.csv"; dst = DST / src.name
        with open(src, encoding="utf-8", newline="") as fi, open(dst, "w", encoding="utf-8", newline="") as fo:
            rd = csv.reader(fi); wr = csv.writer(fo)
            head = next(rd); wr.writerow(head)
            i_doc, i_path, i_tok, i_lab = head.index("doc_id"), head.index("path"), head.index("token"), head.index("label_bio")
            cur = None; text = ""; L = None; pos = 0; kept = dropped = tdrop = 0; lost = 0
            def close():
                if cur and kind == "bio_tokens":
                    resumen.append({"lengua": lang.upper(), "doc_id": cur, "tokens": kept + dropped, "tokens_bibliografia": dropped,
                                    "inicios_de_termino_en_bibliografia": tdrop, "tokens_no_localizados": lost})
            for row in rd:
                if row[i_doc] != cur:
                    close()
                    cur = row[i_doc]; raw = (CORPUS / lang / row[i_path]).read_text(encoding="utf-8", errors="replace")
                    R = bib_ranges(raw, lang); text = clean(raw); pos = 0; kept = dropped = tdrop = lost = 0
                tok = row[i_tok]; j = text.find(tok, pos)
                if j < 0: lost += 1; j = pos          # no debería ocurrir; se conserva la posición
                else: pos = j + len(tok)
                if any(a <= j < b for a, b in R):
                    dropped += 1; tdrop += row[i_lab].startswith("B")
                    continue
                kept += 1; wr.writerow(row)
            close()
        print(lang, kind, "hecho", flush=True)
with open(HERE / "resumen_por_documento.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(resumen[0])); w.writeheader(); w.writerows(resumen)
for lang in ("EN", "ES"):
    rs = [r for r in resumen if r["lengua"] == lang]
    t = sum(r["tokens"] for r in rs); b = sum(r["tokens_bibliografia"] for r in rs)
    print(lang, f"tokens {t}, en bibliografías {b} ({100*b/t:.1f} %), documentos con bibliografía {sum(1 for r in rs if r['tokens_bibliografia'])}, "
          f"inicios de término eliminados {sum(r['inicios_de_termino_en_bibliografia'] for r in rs)}, tokens no localizados {sum(r['tokens_no_localizados'] for r in rs)}")
