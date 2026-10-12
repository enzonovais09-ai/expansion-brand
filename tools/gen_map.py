import base64, subprocess, os
from PIL import Image
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def b64(p): return "data:image/png;base64,"+base64.b64encode(open(p,"rb").read()).decode()
LB=b64("logo-black.png"); LW=b64("logo-white.png")
OUT="map3"
CSS="""*{margin:0;padding:0;box-sizing:border-box}
body{background:transparent;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;color:#0A0A0A}
.cv{position:relative;overflow:hidden;background:#0A0A0A}
.cv.clear{background:transparent}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:100px 100px;background-position:-1px -1px}
.bleed{position:absolute;font-weight:700;letter-spacing:-.045em;line-height:.8;color:#FFFFFF;opacity:.05;white-space:nowrap}
.tick{font-size:15px;letter-spacing:.22em;text-transform:uppercase;color:#FF2600;font-weight:500}
.meta{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#CFCAC3}"""
def render(name,w,h,inner,scale=2,clear=False):
    W=max(w,620); H=max(h,620)
    html=f"<!doctype html><meta charset=utf-8><style>{CSS}</style><body><div class='cv{" clear" if clear else ""}' style='width:{w}px;height:{h}px'>{inner}</div></body>"
    p=os.path.abspath(f"{OUT}/{name}")
    open(p+".html","w").write(html)
    subprocess.run([CH,"--headless=new","--disable-gpu","--hide-scrollbars",f"--window-size={W},{H}",f"--force-device-scale-factor={scale}","--default-background-color=00000000","--virtual-time-budget=1200",f"--screenshot={p}.png","file://"+p+".html"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    Image.open(p+".png").crop((0,0,w*scale,h*scale)).save(p+".png",optimize=True)
    os.remove(p+".html")

def cover(name,label,code,tick,title,sub,ts=96,logo_col=False):
    # v2: sem título (o Notion já mostra o nome da página). Tudo dentro da faixa central que o Notion exibe.
    col=(f'<img src="{LW}" style="width:96px">' if logo_col else f'<span style="font-size:{72 if len(code)<=2 else 58}px;font-weight:700;letter-spacing:-.04em;color:#FFFFFF;line-height:1">{code}</span>')
    inner=f"""<div class=grid></div>
<div class=bleed style="font-size:330px;left:-14px;top:175px;opacity:.06">EXPANSION</div>
<div style="position:absolute;right:80px;top:0;bottom:0;width:150px;background:#D00001;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px">
  <span style="font-size:11px;letter-spacing:.2em;color:#FFFFFF;font-weight:500">{label}</span>{col}
  <span style="font-size:11px;letter-spacing:.2em;color:#FFFFFF;font-weight:500">EXP©</span></div>
<div style="position:absolute;left:90px;top:214px;display:flex;align-items:center;gap:16px">
  <img src="{LW}" style="height:20px"><span style="width:28px;height:1px;background:rgba(255,255,255,.35)"></span><span class=tick style="font-size:13px">{tick}</span></div>
<div class=meta style="position:absolute;right:262px;top:218px;font-size:11px">© Expansion Co. 2026</div>"""
    render(name,1500,600,inner)

def icon(name,code,logo=False):
    fs=150 if len(code)<=2 else 110
    body=(f'<img src="{LW}" style="position:absolute;left:30px;top:80px;width:200px">' if logo else
          f'<div style="position:absolute;left:24px;top:22px;font-size:{fs}px;font-weight:700;letter-spacing:-.05em;color:#FFFFFF;line-height:1">{code}</div>')
    render(name,280,280,f'<div style="position:absolute;inset:0;background:#0A0A0A"></div>{body}<div style="position:absolute;right:0;bottom:0;width:70px;height:70px;background:#D00001"></div>')

def banner(name,n,title,tick):
    # v2: faixa fina (1500x80) pra não dominar a página em largura total
    inner=f"""<div style="position:absolute;left:0;top:0;bottom:0;width:88px;background:#D00001;display:flex;align-items:center;justify-content:center"><span style="font-size:34px;font-weight:700;letter-spacing:-.03em;color:#FFFFFF">{n}</span></div>
<div style="position:absolute;left:116px;top:50%;transform:translateY(-50%);font-size:34px;font-weight:700;letter-spacing:-.02em;text-transform:uppercase;line-height:1;color:#FFFFFF">{title}</div>
<div class=meta style="position:absolute;right:24px;top:50%;transform:translateY(-50%);font-size:11px">Expansion Map</div>
"""
    render(name,1500,80,inner)

def ticker(name,words):
    inner=f"""<div style="position:absolute;left:0;right:0;top:0;height:1px;background:rgba(138,133,128,.45)"></div>
<div style="position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);display:flex;justify-content:space-between;padding:0 4px;font-size:15px;letter-spacing:.3em;text-transform:uppercase;font-weight:500">{''.join(f'<span style="color:{"#FF2600" if i==0 else "#8A8580"}">{w}</span>' for i,w in enumerate(words))}</div>"""
    render(name,1500,50,inner,clear=True)

cover("capa-map","MAPA","","Expansion Co. · Sistema","Expansion Map","Do modelo à escala, em 4 fases",logo_col=True)
cover("capa-ct","PÁGINA","CT","Expansion Map · Conteúdo","Expansion Funnel","Ideias, roteiros e métricas do seu conteúdo")
cover("capa-00","PÁGINA","00","Expansion Map · Onboarding","Comece aqui","O que é o mapa e como usar")
cover("capa-fn","PÁGINA","FN","Expansion Map · Diagnóstico","Seu funil de expansão","Onde você está e para onde vai",ts=80)
cover("capa-faq","PÁGINA","?","Expansion Map · Suporte","Dúvidas frequentes","Respostas rápidas pras dúvidas comuns",ts=84)
for i,t in enumerate(["Modelo & Oferta","Aquisição & Conversão","Vendas & Agendamento","Alavancagem & Mão de Obra"],1):
    cover(f"capa-f{i}","FASE",f"F{i}",f"Expansion Map · Fase {i} de 4",t,"",ts=96 if len(t)<16 else 78 if len(t)<22 else 66)
cover("capa-r7","PÁGINA","R7","Expansion Map · Recursos","Recursos de 7 dígitos","Materiais de apoio pra cada fase",ts=80)
icon("icone-map","",logo=True)
for c in ["CT","00","FN","?","F1","F2","F3","F4","R7"]:
    icon("icone-"+{"?":"faq"}.get(c,c.lower()),c)
banner("faixa-01-conteudo","01","Conteúdo","Expansion Map<br>© Expansion Co.")
banner("faixa-02-comece","02","Comece aqui","Expansion Map<br>© Expansion Co.")
banner("faixa-03-fases","03","As 4 fases","Expansion Map<br>© Expansion Co.")
banner("faixa-04-recursos","04","Recursos","Expansion Map<br>© Expansion Co.")
ticker("rodape-ticker",["Expansion","Map","©","2026"])
