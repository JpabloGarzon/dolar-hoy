
SLUG = "notas"
NAV = "Calculadora de notas"
RESUMEN = "Calcula cuánto necesitas en el tercer corte para aprobar."


def generar():
    titulo = "Calculadora de notas"
    descripcion = (
        "Calcula la nota que necesitas en el último corte "
        "para aprobar tu materia."
    )

    cuerpo = """
<section class="notas-page">
    <p class="eyebrow">Herramienta académica</p>
    <h1>Calculadora de notas</h1>
    <p class="lead">
        Descubre cuánto necesitas sacar en el tercer corte
        para aprobar tu materia.
    </p>

    <form id="form-notas" class="notas-form">
        <div class="notas-cortes">
            <div class="notas-corte">
                <h2>Primer corte</h2>

                <label for="nota1">Nota obtenida</label>
                <input
                    id="nota1"
                    type="number"
                    min="0"
                    max="5"
                    step="0.01"
                    placeholder="Ej. 3.5"
                    required
                >

                <label for="porcentaje1">Porcentaje (%)</label>
                <input
                    id="porcentaje1"
                    type="number"
                    min="0"
                    max="100"
                    step="0.01"
                    placeholder="Ej. 30"
                    required
                >
            </div>

            <div class="notas-corte">
                <div>
                    <h2>Segundo corte</h2>

                    <label for="nota2">Nota obtenida</label>
                    <input
                        id="nota2"
                        type="number"
                        min="0"
                        max="5"
                        step="0.01"
                        placeholder="Ej. 2.8"
                        required
                    >

                    <label for="porcentaje2">Porcentaje (%)</label>
                    <input
                        id="porcentaje2"
                        type="number"
                        min="0"
                        max="100"
                        step="0.01"
                        placeholder="Ej. 30"
                        required
                    >
                </div>
            </div>
        </div>

        <p id="suma-porcentajes" class="notas-ayuda">
            El porcentaje del tercer corte se calculará automáticamente.
        </p>

        <button class="notas-boton" type="submit">
            Calcular nota necesaria
        </button>

        <button class="notas-limpiar" type="reset">
            Limpiar campos
        </button>
    </form>

    <p class="notas-pie">
        El cálculo utiliza el promedio ponderado de los tres cortes.
        Verifica las reglas de aproximación y las condiciones
        de aprobación de tu institución.
    </p>
</section>

<div id="resultado-notas" class="notas-modal-fondo" hidden>
    <div
        class="notas-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="estado-notas"
        aria-describedby="detalle-notas"
    >
        <button
            type="button"
            id="cerrar-notas"
            class="notas-cerrar"
            aria-label="Cerrar"
        >&times;</button>

        <p id="estado-notas" class="notas-modal-titulo"></p>

        <div class="notas-numero" id="nota-necesaria">—</div>

        <p id="detalle-notas" class="notas-modal-detalle"></p>

        <button type="button" id="aceptar-notas" class="notas-boton">
            Entendido
        </button>
    </div>
</div>
"""

    css = """
.notas-page {
    max-width: 780px;
    margin: 0 auto;
}

.notas-form {
    margin-top: 28px;
    padding: 24px;
    background: var(--card, #fff);
    border: 1px solid var(--border, #e5e7eb);
    border-radius: 18px;
}

.notas-page label {
    display: block;
    margin: 12px 0 7px;
    font-weight: 600;
}

.notas-page input {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 12px;
    color: #172033;
    background: #fff;
    border: 1px solid #d1d5db;
    border-radius: 10px;
    font: inherit;
}

.notas-cortes {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
}

.notas-corte {
    min-width: 0;
    padding: 15px;
    border: 1px solid var(--border, #e5e7eb);
    border-radius: 12px;
}

.notas-corte h2 {
    margin: 0;
    font-size: 1.05rem;
}

.notas-boton,
.notas-limpiar {
    width: 100%;
    box-sizing: border-box;
    padding: 13px;
    margin-top: 12px;
    border-radius: 10px;
    cursor: pointer;
    font: inherit;
    font-weight: 600;
}

.notas-boton {
    color: white;
    background: #2563eb;
    border: 1px solid #2563eb;
}

.notas-limpiar {
    color: #374151;
    background: white;
    border: 1px solid #d1d5db;
}

.notas-ayuda,
.notas-pie {
    color: #6b7280;
    font-size: .92rem;
    line-height: 1.6;
}

/* Fondo oscuro detrás de la ventana emergente */
.notas-modal-fondo {
    position: fixed;
    inset: 0;
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    box-sizing: border-box;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
}

.notas-modal-fondo[hidden] {
    display: none;
}

/* Ventana emergente compacta */
.notas-modal {
    position: relative;
    width: 100%;
    max-width: 370px;
    max-height: 90vh;
    overflow-y: auto;
    box-sizing: border-box;
    padding: 28px 22px 22px;
    border: 1px solid var(--border, #374151);
    border-radius: 18px;
    background: var(--card, #151a22);
    color: var(--text, #f3f4f6);
    text-align: center;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
    animation: notas-aparecer .2s ease-out;
}

.notas-cerrar {
    position: absolute;
    top: 7px;
    right: 12px;
    width: 32px;
    height: 32px;
    border: 0;
    border-radius: 8px;
    background: transparent;
    color: inherit;
    font-size: 27px;
    line-height: 1;
    cursor: pointer;
}

.notas-cerrar:hover {
    background: rgba(127, 127, 127, .15);
}

.notas-modal-titulo {
    margin: 8px 18px 12px;
    font-size: 18px;
    font-weight: 700;
}

.notas-modal .notas-numero {
    margin: 8px 0;
    font-size: clamp(42px, 12vw, 58px);
    line-height: 1.2;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.notas-modal-detalle {
    margin: 12px 0 20px;
    font-size: 14px;
    line-height: 1.6;
    color: var(--muted, #a1a1aa);
}

.notas-modal .notas-boton {
    margin-top: 0;
}

@keyframes notas-aparecer {
    from {
        opacity: 0;
        transform: translateY(8px) scale(.97);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@media (max-width: 600px) {
    .notas-cortes {
        grid-template-columns: 1fr;
    }

    .notas-form {
        padding: 16px;
    }

    .notas-modal {
        max-width: 340px;
        padding: 26px 18px 18px;
    }
}

@media (prefers-reduced-motion: reduce) {
    .notas-modal {
        animation: none;
    }
}
"""

    js = """
(() => {
    const form = document.getElementById("form-notas");
    if (!form) return;

    const resultado = document.getElementById("resultado-notas");
    const estado = document.getElementById("estado-notas");
    const numero = document.getElementById("nota-necesaria");
    const detalle = document.getElementById("detalle-notas");
    const sumaTexto = document.getElementById("suma-porcentajes");

    const cerrarNotas = document.getElementById("cerrar-notas");
    const aceptarNotas = document.getElementById("aceptar-notas");

    const valor = id =>
        Number(document.getElementById(id).value);

    let elementoAnterior = null;

    function abrirModal() {
        elementoAnterior = document.activeElement;
        resultado.hidden = false;
        aceptarNotas.focus();
    }

    function cerrarModal() {
        resultado.hidden = true;

        if (elementoAnterior && elementoAnterior.focus) {
            elementoAnterior.focus();
        }
    }

    cerrarNotas.addEventListener("click", cerrarModal);
    aceptarNotas.addEventListener("click", cerrarModal);

    resultado.addEventListener("click", event => {
        if (event.target === resultado) {
            cerrarModal();
        }
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !resultado.hidden) {
            cerrarModal();
        }
    });

    form.addEventListener("submit", event => {
        event.preventDefault();

        if (!form.reportValidity()) return;

        const minima = 3.0;
        const nota1 = valor("nota1");
        const nota2 = valor("nota2");
        const p1 = valor("porcentaje1");
        const p2 = valor("porcentaje2");

        // Calcular automáticamente el porcentaje restante.
        const p3 = 100 - p1 - p2;

        if (p1 + p2 >= 100) {
            sumaTexto.textContent =
                "Los porcentajes del primer y segundo corte " +
                "deben sumar menos del 100%.";

            return;
        }

        if (p1 + p2 < 0 || p3 <= 0) {
            sumaTexto.textContent =
                "Ingresa porcentajes válidos para los dos primeros cortes.";

            return;
        }

        sumaTexto.textContent =
            `Porcentaje del tercer corte: ${p3.toFixed(2)}%`;

        const aporte1 = nota1 * p1 / 100;
        const aporte2 = nota2 * p2 / 100;

        const necesaria =
            (minima - aporte1 - aporte2) / (p3 / 100);

        if (necesaria <= 0) {
            estado.textContent = "¡Ya alcanzaste la meta!";
            numero.textContent = "0.00";

            detalle.textContent =
                "Ya alcanzas matemáticamente la nota mínima para aprobar. " +
                "No te descuides y verifica si tu institución exige " +
                "una nota mínima obligatoria en el tercer corte.";

        } else if (necesaria > 5) {
            estado.textContent = "¡Atención!";
            numero.textContent = necesaria.toFixed(2);

            detalle.textContent =
                "La nota necesaria supera el máximo de 5.0. " +
                "Consulta con tu docente qué opciones tienes.";

        } else if (necesaria < 3) {
            estado.textContent = "¡No te preocupes!";
            numero.textContent = necesaria.toFixed(2);

            detalle.textContent =
                "Necesitas menos de 3.0 en el tercer corte para pasar. " +
                "Pero no te descuides: sigue esforzándote y apunta " +
                "a sacar una buena nota.";

        } else {
            estado.textContent = "Esta es tu meta para pasar";
            numero.textContent = necesaria.toFixed(2);

            detalle.textContent =
                "Esta es la nota que necesitas en el tercer corte " +
                "para alcanzar tu objetivo. ¡Prepárate y da lo mejor!";
        }

        abrirModal();
    });

    form.addEventListener("reset", () => {
        resultado.hidden = true;

        sumaTexto.textContent =
            "El porcentaje del tercer corte se calculará automáticamente.";
    });
})();
"""

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "cuerpo": cuerpo,
        "css": css,
        "js": js,
    }
