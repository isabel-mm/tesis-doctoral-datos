"""Tipología de errores (Tabla tab:errores_apariciones del cap. 6): reparto de los errores en % del total
(apariciones de términos reservados no reconocidas enteras + falsos positivos), media de los cuatro niveles
de reserva, particiones 0-2 comunes a CRF y BiLSTM-CRF, sin el tipo corpus.
Uso: python paso10_tipologia_errores.py <resultados>"""
import csv, gzip, json, sys
from collections import Counter, defaultdict
R = sys.argv[1]
def spans(labels):
    out=[]; start=None
    for i,l in enumerate(labels+["O"]):
        if l=="B-T" or l=="O" or (l=="I-T" and start is None):
            if start is not None: out.append((start,i)); start=None
            if l in ("B-T","I-T"): start=i
    return out
def load(f):
    sents=defaultdict(list)
    for r in csv.DictReader(gzip.open(f,"rt",encoding="utf-8")):
        sents[(r["doc_id"],r["sentence_id"])].append(r)
    return sents
res={}
for pct in (10,20,30,50):
 for lang in ("en","es"):
    for model in ("CRF","BiLSTM"):
        c=Counter(); ex=defaultdict(Counter); inv_forms=set()
        for seed in "012":
            crf=load(f"{R}/crf/pred/reserva_{lang}_p{pct}_s{seed}_todas.csv.gz")
            rv=set(json.load(open(f"{R}/crf/reservadas/reserva_{lang}_p{pct}_s{seed}_todas.json",encoding="utf-8")))
            if model=="BiLSTM":
                bp={}
                for r in csv.DictReader(gzip.open(f"{R}/bilstm/pred/reserva_{lang}_p{pct}_s{seed}.csv.gz","rt",encoding="utf-8")):
                    bp[(r["doc_id"],r["sentence_id"],r["i"])]=r["pred"]
            for key,rows in crf.items():
                rows.sort(key=lambda r:int(r["i"]))
                toks=[r["token"].lower() for r in rows]
                gold=[r["gold"] for r in rows]
                pred=[r["pred"] if model=="CRF" else bp.get((key[0],key[1],r["i"]),"O") for r in rows]
                gs=spans(gold); ps=spans(pred)
                for a,b in gs: inv_forms.add(" ".join(toks[a:b]))
                for a,b in gs:
                    e=rows[a]["entrada"]
                    if e not in rv or e=="corpus": continue
                    g=" ".join(toks[a:b])
                    ov=[(x,y) for x,y in ps if x<b and y>a]
                    if (a,b) in ps: k="exacto"; p=g
                    elif not ov: k="omitido_mono" if b-a==1 else "omitido_poli"; p=""
                    else:
                        x,y=ov[0]; p=" ".join(toks[x:y])
                        if x>=a and y<=b: k="defecto"
                        elif x<=a and y>=b: k="exceso"
                        else: k="solapamiento"
                    c[k]+=1; ex[k][(g,p)]+=1
                c["pred_total"]+=len(ps)
                for x,y in ps:
                    if not any(a<y and b>x for a,b in gs):
                        p=" ".join(toks[x:y]); c["fp"]+=1; ex["fp"][p]+=1
        res[(pct,lang,model)]=(c,ex,inv_forms)


import statistics as st
K=("defecto","exceso","solapamiento","omitido_mono","omitido_poli","fp")
for lang in ("en","es"):
  for model in ("CRF","BiLSTM"):
    pc=defaultdict(list); tot_err=[]
    for pct in (10,20,30,50):
        c,ex,inv=res[(pct,lang,model)]
        e=sum(c[k] for k in K); tot_err.append(e)
        for k in K: pc[k].append(100*c[k]/e)
    print(lang,model," ".join(f"{k}={st.mean(v):.1f}" for k,v in pc.items()), "| errores por nivel:", tot_err)
