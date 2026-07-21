#!/usr/bin/env python3
"""Guardián de la huella de flota de CLAUDE.md.

Impide que la sección «AGLAYA · Flota — el capitán» vuelva a afirmar ESTADO.
Un doc que pre-contesta una pregunta de estado hace que el hilo que lo lee no
vaya a mirar la fuente: ese es el fallo que este script existe para bloquear.

Alcance: SOLO esa sección. El resto del archivo tiene versiones y conteos
legítimos (el contrato de marca, las tools del MCP) y barrerlo entero
produciría rojos falsos, que es como muere un guardián.

Exención: los fragmentos entre acentos graves (`...`) y los bloques cercados.
Se exime el FRAGMENTO, no la línea: el doc tiene que poder nombrar los
patrones que prohíbe sin auto-delatarse, y el resto de esa misma línea se
sigue vigilando.

Sin dependencias: stdlib, como el MCP.

Uso:  python3 tools/guard_huella.py [ruta/a/CLAUDE.md]
Sale: 0 limpio · 1 huella con estado · 2 no se pudo comprobar.
"""

import re
import sys
from pathlib import Path

SECCION = "## AGLAYA · Flota — el capitán"

# Estrechas a propósito: solo las formas que ya nos han costado dinero.
# No intentan definir «estado» — intentan reconocer lo que rota solo.
REGLAS = [
    (
        "fecha-de-pase",
        r"\b\d{4}-\d{1,2}-\d{1,2}\b"
        r"|\b\d{1,2}[-/ ](?:ene|feb|mar|abr|may|jun|jul|ago|sept?|oct|nov|dic)\b",
        "una fecha caduca sola; el git log no",
    ),
    (
        "marca-de-progreso",
        r"\b\d+\s*/\s*\d+\b",
        "un N/N es un juicio congelado (fue un 7/7 lo que nadie volvió a mirar)",
    ),
    (
        "conteo",
        r"\b\d+\s+(?:tools?|herramientas|naves|repos?|nodos|kits|commits?|tags?|reglas|fuentes|servicios)\b",
        "cuenta lo que hay ahora, no lo que había al escribirlo",
    ),
    (
        "version-a-mano",
        r"\bv\d+\.\d+(?:\.\d+)?\b",
        "la versión la dicen `git tag` y la cabecera del contrato",
    ),
    (
        "precio",
        # Ojo: sin `\b` final tras el símbolo — `€` no es carácter de palabra y
        # el límite nunca casa. Ese fallo dejó pasar «2500 €» con el guardián en verde.
        r"[€$]\s*\d|\b\d+(?:[.,]\d+)?\s*[€$]|\b\d+(?:[.,]\d+)?\s*(?:eur|usd)\b",
        "la verdad comercial vive en el atlas, no aquí",
    ),
    (
        "sello-de-verificado",
        r"\bverificad[oa]s?\b|\bre-?verificaci[oó]n\b|\bsin\s+incidencias\b"
        r"|\bcerrad[oa]s?\s+(?:el|en|por)\b|\bcomprobad[oa]s?\s+(?:el|en)\b",
        "un sello dice que alguien miró un día, no que hoy sea cierto",
    ),
    (
        # Añadida tras el hallazgo del capitán: su ficha de esta nave llevaba doce
        # hex copiados a mano bajo «la paleta real, de vuestro CSS». Un valor de
        # marca tecleado en un doc es la misma avería que una fecha de pase.
        "valor-de-marca",
        r"#[0-9a-f]{3}(?:[0-9a-f]{3}(?:[0-9a-f]{2})?)?\b",
        "los valores de marca los sirve `aglaya-ds` (`get_token`, `list_tokens`), no un doc",
    ),
    (
        "estado-encendido",
        r"(?<!en )\bvivos?\b|\bencendid[oa]s?\b|\bapagad[oa]s?\b|\boperativ[oa]s?\b"
        r"|\bdesplegad[oa]s?\b|\bca[ií]d[oa]s?\b|\bsan[oa]s?\b|\bfuncionando\b",
        "«hoy está arriba» es exactamente lo que hay que ir a mirar",
    ),
]

REGLAS = [(nombre, re.compile(patron, re.IGNORECASE), porque) for nombre, patron, porque in REGLAS]

CERCADO = re.compile(r"```.*?```", re.DOTALL)
EN_LINEA = re.compile(r"`[^`\n]*`")


def enmascarar(texto: str) -> str:
    """Tapa los fragmentos entrecomillados conservando offsets y saltos."""

    def espacios(m: re.Match) -> str:
        return "".join("\n" if c == "\n" else " " for c in m.group(0))

    return EN_LINEA.sub(espacios, CERCADO.sub(espacios, texto))


def recortar_seccion(lineas: list[str]) -> tuple[int, int] | None:
    inicio = None
    for i, linea in enumerate(lineas):
        if linea.strip() == SECCION:
            inicio = i
            continue
        if inicio is not None and linea.startswith("## "):
            return inicio, i
    return (inicio, len(lineas)) if inicio is not None else None


def main() -> int:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "CLAUDE.md"
    if not ruta.is_file():
        print(f"guard-huella: no encuentro {ruta}", file=sys.stderr)
        return 2

    lineas = ruta.read_text(encoding="utf-8").splitlines()
    tramo = recortar_seccion(lineas)
    if tramo is None:
        print(
            f"guard-huella: no encuentro la sección «{SECCION}» en {ruta}.\n"
            "  O se renombró o se borró. Sin sección no hay nada que vigilar: fallo a propósito.",
            file=sys.stderr,
        )
        return 2

    inicio, fin = tramo
    hallazgos = []
    for offset, cruda in enumerate(lineas[inicio:fin]):
        limpia = enmascarar(cruda)
        for nombre, patron, porque in REGLAS:
            for m in patron.finditer(limpia):
                hallazgos.append((inicio + offset + 1, nombre, m.group(0).strip(), porque, cruda.strip()))

    if not hallazgos:
        print(f"guard-huella: OK — {ruta.name} líneas {inicio + 1}-{fin}, sin afirmaciones de estado.")
        return 0

    print(f"guard-huella: {len(hallazgos)} afirmación(es) de estado en la huella de flota de {ruta}\n", file=sys.stderr)
    for linea, nombre, encontrado, porque, contexto in hallazgos:
        print(f"  {ruta}:{linea}  [{nombre}]  → {encontrado!r}", file=sys.stderr)
        print(f"      {porque}", file=sys.stderr)
        print(f"      {contexto}\n", file=sys.stderr)
    print(
        "  Arréglalo borrando la afirmación y dejando en su lugar CON QUÉ se contesta esa\n"
        "  pregunta. Si el patrón lo nombra el propio doc, ponlo entre acentos graves —\n"
        "  no ensanches la exención.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
