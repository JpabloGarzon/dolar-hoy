import os
from html import escape

import layout
from paginas import dolar

PAGINAS = [dolar]  # aquí se irán sumando las páginas nuevas

# Tarjetas "Próximamente" solo para mostrar la visión del sitio.
# Bórralas (deja la lista vacía) antes de pedir publicidad.
PROXIMAMENTE = [
    ("notas", "Calculadora de notas", "Calcula cuánto necesitas en el próximo corte para pasar."),
    ("pico-y-placa", "Pico y placa", "Consulta la restricción de hoy en tu ciudad."),
]

SALIDA = "docs"


def escribir(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def tarjeta(slug, titulo, resumen, destacado=None, activa=True):
    badge = ""
    if destacado:
        etiqueta, valor, cambio = destacado
        cls = "sube" if cambio.startswith("▲") else "baja" if cambio.startswith("▼") else ""
        badge = (
            f'<div class="badge"><span class="muted">{escape(etiqueta)}</span>'
            f"<strong>{escape(valor)}</strong>"
            f'<span class="chip {cls}">{escape(cambio)}</span></div>'
        )
    cuerpo = (
        f'<div class="ico">{layout.icono(slug)}</div>'
        f"<h2>{escape(titulo)}</h2>"
        f'<p class="muted">{escape(resumen)}</p>{badge}'
    )
    if activa:
        return f'<a class="tool card enlace" href="{slug}/">{cuerpo}</a>'
    return f'<div class="tool card soon">{cuerpo}<span class="tag">Próximamente</span></div>'


def pagina_inicio(resultados):
    tarjetas = "".join(
        tarjeta(p.SLUG, p.NAV, p.RESUMEN, resultados[p.SLUG].get("destacado"))
        for p in PAGINAS
    )
    tarjetas += "".join(
        tarjeta(slug, titulo, resumen, activa=False)
        for slug, titulo, resumen in PROXIMAMENTE
    )
    return f"""
<section class="hero-home">
<p class="eyebrow">Colombia · cada día</p>
<h1>Lo que necesitas saber hoy, <span class="resalta">sin vueltas</span>.</h1>
<p class="lead">Herramientas gratuitas de consulta diaria, hechas para usarse desde el celular.</p>
</section>
<div class="grid">{tarjetas}</div>
"""


def main():
    # Primero se genera cada página; si alguna fuente de datos falla, el script se detiene.
    resultados = {p.SLUG: p.generar() for p in PAGINAS}
    menu = [(p.SLUG, p.NAV) for p in PAGINAS]

    escribir(
        f"{SALIDA}/index.html",
        layout.render(
            titulo=f"{layout.NOMBRE_SITIO}: herramientas de consulta diaria",
            descripcion="Herramientas gratuitas de consulta diaria para Colombia.",
            cuerpo=pagina_inicio(resultados),
            raiz="",
            menu=menu,
        ),
    )

    for p in PAGINAS:
        d = resultados[p.SLUG]
        escribir(
            f"{SALIDA}/{p.SLUG}/index.html",
            layout.render(
                titulo=d["titulo"],
                descripcion=d["descripcion"],
                cuerpo=d["cuerpo"],
                raiz="../",
                menu=menu,
                activa=p.SLUG,
                css=d.get("css", ""),
                js=d.get("js", ""),
            ),
        )
        print("Listo:", p.SLUG)


main()