import json
import urllib.parse
import urllib.request
from datetime import datetime

SLUG = "dolar"
NAV = "Dólar hoy"
RESUMEN = "TRM del dólar en Colombia, conversor de dólares a pesos e historial."

URL = "https://www.datos.gov.co/resource/32sa-8pi3.json?" + urllib.parse.urlencode(
    {"$order": "vigenciadesde DESC", "$limit": 31}
)

CSS = """
.valor{font-size:clamp(2rem,10vw,3.2rem);font-weight:800;line-height:1.1;overflow-wrap:anywhere}
.cambio{font-weight:600;margin-top:.25rem}
.sube{color:var(--up)}
.baja{color:var(--down)}
svg{width:100%;height:auto;display:block}
.line{fill:none;stroke:var(--accent);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.area{fill:var(--accent);opacity:.12}
.dot{fill:var(--accent)}
.lbl{fill:var(--muted);font-size:11px}
.tw{overflow-x:auto}
table{width:100%;border-collapse:collapse}
th,td{padding:.6rem .4rem;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th:not(:first-child),td:not(:first-child){text-align:right}
"""

JS = """
(function(){
var TRM=__TRM__;
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
"""


def fmt(v, dec=2):
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def parse_fecha(s):
    return datetime.strptime(s[:10], "%Y-%m-%d")


def fdate(dt):
    return dt.strftime("%d/%m/%Y")


def _grafica(serie):
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


def generar():
    with urllib.request.urlopen(URL, timeout=30) as r:
        crudo = json.load(r)

    datos = []
    for d in crudo:
        datos.append(
            {
                "desde": parse_fecha(d["vigenciadesde"]),
                "hasta": parse_fecha(d["vigenciahasta"]) if d.get("vigenciahasta") else None,
                "valor": float(d["valor"]),
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

    serie = list(reversed(datos[:30]))

    cuerpo = f"""
<h1>Dólar hoy en Colombia</h1>
<p class="muted">{vigencia}</p>

<section class="card hero">
<div class="muted">TRM (pesos por 1 dólar)</div>
<div class="valor">${fmt(actual['valor'])}</div>
<div class="cambio {cls}">{flecha} {signo}{fmt(cambio)} ({fmt(pct)}%) frente a la TRM anterior</div>
</section>

<section class="card">
<h2>Conversor</h2>
<div class="conv">
<div><label for="usd">Dólares (USD)</label><input id="usd" inputmode="decimal" autocomplete="off" placeholder="100"></div>
<div><label for="cop">Pesos (COP)</label><input id="cop" inputmode="decimal" autocomplete="off" placeholder="Pesos"></div>
</div>
<p class="muted nota">Calculado con la TRM vigente. Bancos y casas de cambio pueden aplicar otro valor.</p>
</section>

<section class="card">
<h2>Evolución reciente</h2>
{_grafica(serie)}
</section>

<section class="card">
<h2>Historial</h2>
<div class="tw"><table>
<tr><th>Fecha</th><th>TRM</th><th>Cambio</th></tr>
{filas}
</table></div>
</section>

<p class="muted nota">Fuente: Superintendencia Financiera de Colombia (datos.gov.co).</p>
"""

    return {
        "titulo": f"Dólar hoy en Colombia (TRM): ${fmt(actual['valor'])}",
        "descripcion": f"TRM del dólar hoy en Colombia: ${fmt(actual['valor'])} COP. Conversor de dólares a pesos e historial reciente.",
        "cuerpo": cuerpo,
        "destacado": ("TRM hoy", f"${fmt(actual['valor'])}", f"{flecha} {signo}{fmt(pct)}%"),
        "css": CSS,
        "js": JS.replace("__TRM__", f"{actual['valor']:.2f}"),
    }