"""Figura: textos por línea temática (EN/ES); tramo oscuro = línea principal, claro = línea secundaria."""
import json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.rcParams.update({'font.family':'Times New Roman','font.size':10})
F=json.load(open('mapeo.json'))
LINEAS=['Historiografía','Teoría y epistemología','Muestreo y representatividad','Diseño y construcción',
        'Documentación y presentación','Tipología','Problemas metodológicos','Anotación y herramientas']
COL={'en':('#6A4C93','#B9A6D9'),'es':('#12897B','#8CCBC2')}
fig,ax=plt.subplots(figsize=(6.3,5.0))
h=0.38
for j,lang in enumerate(('en','es')):
    R=[r for r in F if r['lengua']==lang]
    for i in range(8):
        y=7-i + (h/2+0.02 if lang=='en' else -h/2-0.02)
        p=sum(r['principal']==i and i in r['lineas'] for r in R)
        s=sum(i in r['lineas'] for r in R)-p
        ax.barh(y,p,h,color=COL[lang][0],edgecolor='white',linewidth=1)
        ax.barh(y,s,h,left=p,color=COL[lang][1],edgecolor='white',linewidth=1)
        ax.text(p+s+0.3,y,str(p+s),va='center',fontsize=8.5,color='#333333')
ax.set_yticks(range(8)); ax.set_yticklabels([f'L{8-k}. {LINEAS[7-k]}' for k in range(8)])
ax.set_xlabel('Número de textos (de 50 por lengua)')
ax.set_xlim(0,18); ax.xaxis.grid(True,color='#e6e6e6',linewidth=0.6); ax.set_axisbelow(True)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#999999'); ax.spines['bottom'].set_color('#999999')
leg=[Patch(color=COL['en'][0],label='EN: línea principal'),Patch(color=COL['en'][1],label='EN: línea secundaria'),
     Patch(color=COL['es'][0],label='ES: línea principal'),Patch(color=COL['es'][1],label='ES: línea secundaria')]
ax.legend(handles=[leg[0],leg[2],leg[1],leg[3]],loc='lower left',bbox_to_anchor=(-0.02,1.0),fontsize=8.5,frameon=False,ncol=2)
fig.tight_layout(); fig.savefig('lineas_tematicas.pdf'); fig.savefig('lineas_tematicas.png',dpi=200)
