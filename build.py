import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

URL = "https://www.datos.gov.co/resource/32sa-8pi3.json?" + urllib.parse.urlencode(
    {"$order": "vigenciadesde DESC", "$limit": 31}
)


def fmt(v, dec=2):
    # 3912.34 -> 3.912,34 (formato colombiano)
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def parse_fecha(s):
    # Valida que sea una fecha real; si viene algo raro, el script falla en vez de publicarlo
    return datetime.strptime(s[:10], "%Y-%m-%d")


def fdate(dt):
    return dt.strftime("%d/%m/%Y")


with urllib.request.urlopen(URL, timeout=30) as r:
    crudo = json.load(r)

datos = []
for d in crudo:
    datos.append(
        {
            "desde": parse_fecha(d["vigenciadesde"]),
            "hasta": parse_fecha(d["vigenciahasta"]) if d.get("vigenciahasta") else None,
            "valor": float(d["valor"]),  # si no es un número, falla
        }
    )

actual, previo = datos[0], datos[1]
cambio = actual["valor"] - previo["valor"]
pct = cambio / previo["valor"] * 100
cls = "sube" if cambio > 0 else "baja" if cambio < 0 else ""
flecha = "▲" if cambio > 0 else "▼" if cambio < 0 else "■"
signo = "+" if cambio > 0 else ""

if actual["hasta"]:
    vigencia = f"Vigente del {fdate(actual['desde'])} al {fdate(actual['hasta'])}"
else:
    vigencia = f"Vigente desde {fdate(actual['desde'])}"

filas = ""
for i, d in enumerate(datos[:30]):
    c = d["valor"] - datos[i + 1]["valor"]
    k = "sube" if c > 0 else "baja" if c < 0 else ""
    f = "▲" if c > 0 else "▼" if c < 0 else "■"
    s = "+" if c > 0 else ""
    filas += (
        f"<tr><td>{fdate(d['desde'])}</td><td>${fmt(d['valor'])}</td>"
        f'<td class="{k}">{f} {s}{fmt(c)}</td></tr>'
    )


def grafica(serie):
    W, H, pl, pr, pt, pb = 360, 180, 10, 10, 26, 28
    vals = [d["valor"] for d in serie]
    vmin, vmax = min(vals), max(vals)
    rango = (vmax - vmin) or 1
    n = len(vals)
    pts = []
    for i, v in enumerate(vals):
        x = pl + i * (W - pl - pr) / max(n - 1, 1)
        y = pt + (vmax - v) / rango * (H - pt - pb)
        pts.append((x, y))
    linea = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    base = H - pb
    area = f"{pts[0][0]:.1f},{base} {linea} {pts[-1][0]:.1f},{base}"
    xl, yl = pts[-1]
    return (
        f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Gráfica de la TRM de las últimas {n} fechas">'
        f'<polygon class="area" points="{area}"/>'
        f'<polyline class="line" points="{linea}"/>'
        f'<circle class="dot" cx="{xl:.1f}" cy="{yl:.1f}" r="4"/>'
        f'<text class="lbl" x="{pl}" y="14">Máx ${fmt(vmax)}</text>'
        f'<text class="lbl" x="{W - pr}" y="14" text-anchor="end">Mín ${fmt(vmin)}</text>'
        f'<text class="lbl" x="{pl}" y="{H - 8}">{fdate(serie[0]["desde"])}</text>'
        f'<text class="lbl" x="{W - pr}" y="{H - 8}" text-anchor="end">{fdate(serie[-1]["desde"])}</text>'
        f"</svg>"
    )


serie = list(reversed(datos[:30]))

plantilla = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Dólar hoy en Colombia (TRM): $__HOY__</title>
<meta name="description" content="TRM del dólar hoy en Colombia: $__HOY__ COP. Conversor de dólares a pesos e historial reciente.">
<style>
:root{--bg:#f6f7f9;--card:#fff;--text:#1b1f24;--muted:#5d6672;--line:#e3e6ea;--accent:#0b6bcb;--up:#c0392b;--down:#1e8e5a}
@media (prefers-color-scheme:dark){:root{--bg:#0f1318;--card:#171d24;--text:#e8ecf1;--muted:#9aa5b1;--line:#27303a;--accent:#5aa9ff;--up:#ff7b6b;--down:#4cd08c}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.5}
.wrap{max-width:720px;margin:0 auto;padding:1rem}
h1{font-size:clamp(1.4rem,5vw,2rem);margin:.5rem 0 .25rem}
h2{font-size:clamp(1.1rem,4vw,1.35rem);margin:0 0 .75rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem;margin-top:1rem}
.valor{font-size:clamp(2rem,10vw,3.2rem);font-weight:800;line-height:1.1;overflow-wrap:anywhere}
.muted{color:var(--muted);font-size:.9rem;margin:0}
.cambio{font-weight:600;margin-top:.25rem}
.sube{color:var(--up)}
.baja{color:var(--down)}
.conv{display:grid;gap:.75rem}
@media(min-width:560px){.conv{grid-template-columns:1fr 1fr}}
label{display:block;font-size:.85rem;color:var(--muted);margin-bottom:.25rem}
input{width:100%;font-size:1.2rem;padding:.75rem;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--text);min-height:48px}
input:focus{outline:2px solid var(--accent);outline-offset:1px}
.nota{margin-top:.75rem}
svg{width:100%;height:auto;display:block}
.line{fill:none;stroke:var(--accent);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.area{fill:var(--accent);opacity:.12}
.dot{fill:var(--accent)}
.lbl{fill:var(--muted);font-size:11px}
.tw{overflow-x:auto}
table{width:100%;border-collapse:collapse}
th,td{padding:.6rem .4rem;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th:not(:first-child),td:not(:first-child){text-align:right}
footer{margin:1.5rem 0 2rem}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>Dólar hoy en Colombia</h1>
<p class="muted">__VIGENCIA__</p>
</header>
<main>
<section class="card">
<div class="muted">TRM (pesos por 1 dólar)</div>
<div class="valor">$__HOY__</div>
<div class="cambio __CLS__">__FLECHA__ __SIGNO____CAMBIO__ (__PCT__%) frente a la TRM anterior</div>
</section>

<section class="card">
<h2>Conversor</h2>
<div class="conv">
<div><label for="usd">Dólares (USD)</label><input id="usd" inputmode="decimal" autocomplete="off" placeholder="100"></div>
<div><label for="cop">Pesos (COP)</label><input id="cop" inputmode="decimal" autocomplete="off" placeholder="319.444"></div>
</div>
<p class="muted nota">Calculado con la TRM vigente. Bancos y casas de cambio pueden aplicar otro valor.</p>
</section>

<section class="card">
<h2>Evolución reciente</h2>
__GRAFICA__
</section>

<section class="card">
<h2>Historial</h2>
<div class="tw"><table>
<tr><th>Fecha</th><th>TRM</th><th>Cambio</th></tr>
__FILAS__
</table></div>
</section>
</main>
<footer class="muted">Fuente: Superintendencia Financiera de Colombia (datos.gov.co). Actualizado: __ACT__ UTC.</footer>
</div>
<script>
(function(){
var TRM=__TRMJS__;
var usd=document.getElementById("usd"),cop=document.getElementById("cop");
var nf=new Intl.NumberFormat("es-CO",{maximumFractionDigits:2});
function num(s,esCop){
  s=s.trim();
  if(esCop){s=s.split(".").join("");}
  else if(s.indexOf(",")>-1||s.split(".").length>2){s=s.split(".").join("");}
  s=s.replace(",",".");
  var n=parseFloat(s);
  return isFinite(n)&&n>=0?n:null;
}
usd.addEventListener("input",function(){var n=num(usd.value,false);cop.value=n===null?"":nf.format(n*TRM);});
cop.addEventListener("input",function(){var n=num(cop.value,true);usd.value=n===null?"":nf.format(n/TRM);});
})();
</script>
</body>
</html>"""

html = (
    plantilla.replace("__HOY__", fmt(actual["valor"]))
    .replace("__VIGENCIA__", vigencia)
    .replace("__CLS__", cls)
    .replace("__FLECHA__", flecha)
    .replace("__SIGNO__", signo)
    .replace("__CAMBIO__", fmt(cambio))
    .replace("__PCT__", fmt(pct))
    .replace("__GRAFICA__", grafica(serie))
    .replace("__FILAS__", filas)
    .replace("__ACT__", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    .replace("__TRMJS__", f"{actual['valor']:.2f}")
)

os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Listo: docs/index.html generado. TRM:", fmt(actual["valor"]))