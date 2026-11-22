"""Mapeo exploratorio de las 8 líneas temáticas del corpus (cap. 3) sobre los 100 textos.
Léxicos semilla EN/ES por línea; densidad por 10 000 palabras; normalización por la media de la línea en su lengua.
Columnas: línea principal vacía si ninguna línea supera el umbral.
Una línea se asigna a un texto si su densidad relativa >= 1,25 (25 % por encima de la media); la principal es la de mayor densidad relativa."""
import re,unicodedata,glob,os,csv,statistics as st
BASE='../sin_bibliografia_2026-11/corpus_glicor_sinbib'
META=os.path.expanduser('~/Desktop/Repositorios/tesis-doctoral-datos/corpus/documentos_{}.csv')  # año, autoría, título, tipo
LINEAS=['L1 Historiografía','L2 Teoría y epistemología','L3 Muestreo y representatividad','L4 Diseño y construcción',
        'L5 Documentación y presentación','L6 Tipología','L7 Problemas metodológicos','L8 Anotación y herramientas']
LEX={'en':[
 r'histor\w*|pioneer\w*|forerunner|predecessor|brown corpus|\blob\b|survey of english usage|quirk|sinclair|firth|pre-?electronic|early corpus|first corpus|origins?|precursor\w*|chomsky\w*|decades? ago|twentieth century|1960s|1950s',
 r'theor\w*|epistem\w*|empiric\w*|rationalis\w*|introspect\w*|intuition\w*|paradigm\w*|corpus-driven|corpus-based|usage-based|hypothes\w*|philosoph\w*|scientific method|falsif\w*|definition of corpus linguistics',
 r'representativ\w*|sampl\w*|balanc\w*|population|stratif\w*|corpus size|saturation|sampling frame|proportion\w*|generaliz\w*|generalis\w*',
 r'design\w*|compil\w*|construct\w*|build\w*|collect\w*|transcri\w*|digiti[sz]\w*|\bocr\b|copyright|permission\w*|consent|recording\w*|data collection|source texts?',
 r'documentation|documented|metadata|reporting|report\w*|interface\w*|online|available|availability|access\w*|release\w*|licen[cs]\w*|user\w*|web ?site|download\w*|distribut\w*|manual',
 r'parallel|comparable|diachronic|synchronic|learner corp\w*|spoken|specialized|specialised|reference corp\w*|general corp\w*|monitor corp\w*|multilingual|monolingual|bilingual|typolog\w*|types of corp\w*|historical corp\w*',
 r'problem\w*|limitation\w*|bias\w*|challeng\w*|pitfall\w*|issues?|errors?|reliab\w*|validity|caveat\w*|drawback\w*|difficult\w*|shortcoming\w*|misleading|inconsisten\w*',
 r'annotat\w*|tag\w*|tagger\w*|pos\b|part-of-speech|pars\w*|lemmati[sz]\w*|lemma\w*|tokeni[sz]\w*|concordanc\w*|software|\bxml\b|\btei\b|tools?|quer\w*|cqp|sketch engine|antconc|wordsmith|script\w*|\br\b|python|algorithm\w*'],
'es':[
 r'histori\w*|antecedente\w*|pioner\w*|precursor\w*|corpus brown|\blob\b|survey of english usage|quirk|sinclair|firth|bello|cuervo|primeros? corpus|origen\w*|siglo xx|decada de 19\d0|chomsky\w*|predecesor\w*',
 r'teori\w*|teoric\w*|epistem\w*|empiri\w*|empirismo|racionalis\w*|introspecci\w*|intuici\w*|paradigma\w*|guiad\w* por (el )?corpus|basad\w* en (el )?corpus|corpus-driven|corpus-based|hipotesis|filosof\w*|metodo cientifico|disciplina',
 r'representativ\w*|muestr\w*|equilibr\w*|poblacion|estratific\w*|tamano|saturaci\w*|proporci\w*|generaliz\w*',
 r'disen\w*|compila\w*|construcci\w*|construir|recopila\w*|recogida|transcri\w*|digitaliz\w*|\bocr\b|derechos de autor|permiso\w*|consentimiento|grabaci\w*|fuentes? textual\w*',
 r'documentaci\w*|documentad\w*|metadatos?|interfaz\w*|interfaces|en linea|disponib\w*|acceso\w*|accesib\w*|usuari\w*|pagina web|sitio web|descarga\w*|distribu\w*|licencia\w*|consulta\w*',
 r'paralel\w*|comparable\w*|diacronic\w*|sincronic\w*|aprendient\w*|oral\w*|especializad\w*|de referencia|corpus general\w*|monitor|multilingu\w*|monolingu\w*|bilingu\w*|tipolog\w*|tipos de corpus',
 r'problema\w*|limitaci\w*|sesgo\w*|dificultad\w*|reto\w*|desafio\w*|error\w*|fiabil\w*|validez|inconvenient\w*|carencia\w*|deficiencia\w*|inconsistencia\w*',
 r'anota\w*|etiquet\w*|lematiz\w*|lema\w*|tokeniz\w*|analizador\w*|parser\w*|concordanc\w*|herramienta\w*|programa\w*|software|\bxml\b|\btei\b|algoritmo\w*|script\w*|python|sketch engine|antconc|wordsmith|cqp']}
def norm(t): return ''.join(c for c in unicodedata.normalize('NFD',t.lower()) if unicodedata.category(c)!='Mn')
filas=[]
META_={l:{unicodedata.normalize('NFC',r['documento']):r for r in csv.DictReader(open(META.format(l),encoding='utf8'))} for l in ('en','es')}
for lang in ('en','es'):
    pats=[re.compile(p) for p in LEX[lang]]
    for f in sorted(glob.glob(f'{BASE}/{lang}/**/*.txt',recursive=True)):
        t=norm(open(f,encoding='utf8',errors='ignore').read()); n=len(t.split())
        doc=unicodedata.normalize('NFC',os.path.basename(f)[:-4]); m=META_[lang][doc]
        filas.append(dict(lengua=lang,documento=doc,anio=m['año'],autor=m['autoría'],titulo=m['título'],genero=m['tipo'],palabras=n,
                          dens=[len(p.findall(t))/n*1e4 for p in pats]))
for lang in ('en','es'):
    F=[r for r in filas if r['lengua']==lang]
    medias=[st.mean(r['dens'][i] for r in F) for i in range(8)]
    for r in F:
        r['rel']=[r['dens'][i]/medias[i] for i in range(8)]
        r['lineas']=[i for i in range(8) if r['rel'][i]>=1.25]
        r['principal']=max(range(8),key=lambda i:r['rel'][i])
with open('mapeo_lineas_tematicas.csv','w',newline='',encoding='utf8') as fh:
    w=csv.writer(fh); w.writerow(['lengua','documento','año','autoría','título','tipo','palabras','línea principal','líneas asignadas']+[f'{l} (rel.)' for l in LINEAS])
    for r in filas: w.writerow([r['lengua'].upper(),r['documento'],r['anio'],r['autor'],r['titulo'],r['genero'],r['palabras'],(LINEAS[r['principal']] if r['lineas'] else ''),'; '.join(LINEAS[i][:2] for i in r['lineas'])]+[f'{x:.2f}' for x in r['rel']])
import json; json.dump(filas,open('mapeo.json','w'),ensure_ascii=False)
for lang in ('en','es'):
    F=[r for r in filas if r['lengua']==lang]
    print(f'\n== {lang.upper()} ({len(F)} textos)')
    for i,l in enumerate(LINEAS):
        print(f'{l:35s} principal: {sum(r["principal"]==i for r in F):2d}   asignada: {sum(i in r["lineas"] for r in F):2d}')
    print('líneas por texto (media):',round(st.mean(len(r['lineas']) for r in F),2))
