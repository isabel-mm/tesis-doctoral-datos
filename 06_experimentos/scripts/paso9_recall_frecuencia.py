import gzip, csv, json, glob, re, sys, statistics as st
from collections import defaultdict, Counter
R = sys.argv[1]
BANDS = [("raros (≤10)", 0, 10), ("medios (11–100)", 11, 100), ("frecuentes (>100)", 101, 10**9)]
def band(n):
    for name, lo, hi in BANDS:
        if lo <= n <= hi: return name
freq = {}
for lang in ("en", "es"):
    c = Counter()
    for f in sorted(glob.glob(f"{R}/crf/pred/cv_{lang}_f[0-9].csv.gz")):
        for row in csv.DictReader(gzip.open(f, "rt", encoding="utf-8")):
            if row["gold"] == "B-T" and row["entrada"]: c[row["entrada"]] += 1
    freq[lang] = c
    bt = Counter(band(n) for n in c.values())
    print(lang, "tipos:", len(c), {k: bt[k] for k, *_ in BANDS})
res = defaultdict(list)  # (model,lang,pct,band) -> recalls por semilla
for model, pat in (("CRF", f"{R}/crf/pred/reserva_*_todas.csv.gz"), ("BiLSTM", f"{R}/bilstm/pred/reserva_*.csv.gz")):
    for f in sorted(glob.glob(pat)):
        m = re.search(r"reserva_(en|es)_p(\d+)_s(\d+)", f); lang, pct, seed = m[1], int(m[2]), m[3]
        rv = set(json.load(open(f"{R}/crf/reservadas/reserva_{lang}_p{pct}_s{seed}_todas.json", encoding="utf-8")))
        tot = Counter(); hit = Counter()
        ent = None
        if model == "BiLSTM":
            ent = {}
            for r2 in csv.DictReader(gzip.open(f"{R}/crf/pred/reserva_{lang}_p{pct}_s{seed}_todas.csv.gz", "rt", encoding="utf-8")):
                ent[(r2["doc_id"], r2["sentence_id"], r2["i"])] = r2["entrada"]
        for row in csv.DictReader(gzip.open(f, "rt", encoding="utf-8")):
            e = row.get("entrada", "") if ent is None else ent.get((row["doc_id"], row["sentence_id"], row["i"]), "")
            if row["gold"] != "O" and e in rv:
                b = band(freq[lang].get(e, 0)); tot[b] += 1; hit[b] += row["pred"] != "O"
        for name, *_ in BANDS:
            if tot[name]: res[(model, lang, pct, name)].append((hit[name] / tot[name], tot[name]))
for k in sorted(res):
    v = res[k]; print(*k, "n=%d" % len(v), "recall %.3f" % st.mean(x for x, _ in v), "tokens/semilla %.0f" % st.mean(n for _, n in v))
