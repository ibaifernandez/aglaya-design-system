#!/usr/bin/env python3
"""contraste_fichas.py — mide, en LOS DOS MODOS, cada pareja tinta/fondo que
declaran las fichas de `components/components.json`, que es lo que el MCP
`aglaya-ds` sirve a las demás naves.

PARA QUÉ. La ficha del `codetag` pedía tinta `#000` sobre fondo
`var(--color-text)`. En oscuro eso es negro sobre casi blanco; en claro,
`--color-text` vale `#000000` y la pareja daba **1.0 exacto**: invisible. Una
nave que siguiera la ficha pintaba un componente ilegible, y aquí nadie se
enteraba.

CÓMO. Los valores NO se teclean: se leen de `colors_and_type.css` en vivo, del
bloque `:root` para el modo oscuro y de `[data-theme="light"]` para el claro,
resolviendo `var()`, `rgba()` con alfa compuesto sobre su fondo y
`color-mix(in srgb, X N%, transparent)`. Si el CSS cambia un valor, esto
persigue el nuevo sin tocar una línea.

QUÉ ES UNA PAREJA. El fondo de un componente es el suyo si lo declara, y si no
el de la superficie en la que vive (`--color-bg`). La tinta es cualquier color
que la ficha nombre en un campo de texto — incluidos los que van dentro de la
prosa de la spec, que es donde esta casa escribe la mitad de sus fichas.

EL SUELO. 4.5 para texto, el de AA. Las fichas no declaran tamaño de forma
fiable, así que no se aplica la excepción de texto grande: un suelo más bajo
habría que justificarlo ficha a ficha, y eso es exactamente lo que nadie va a
hacer al añadir la siguiente.

Uso:  python3 tools/contraste_fichas.py [--todas]
      --todas imprime también las parejas que pasan.
Sale: 0 si ninguna pareja baja del suelo · 1 si alguna baja.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSS = RAIZ / "colors_and_type.css"
FICHAS = RAIZ / "components" / "components.json"
SUELO = 4.5

_COMENTARIO = re.compile(r"/\*.*?\*/", re.DOTALL)
# Campos cuyo valor es tinta. El resto de claves de una spec (padding, font,
# signature…) no pintan texto.
_CLAVES_TINTA = ("color", "title", "body", "label", "placeholder", "value", "text")
_CLAVES_FONDO = ("background",)


def _bloques() -> dict:
    """Los dos mapas de tokens del CSS, leídos en vivo. Los comentarios se
    quitan ANTES de buscar el bloque: dentro de `:root` hay comentarios largos,
    y un `}` dentro de uno cerraría el bloque antes de tiempo."""
    css = _COMENTARIO.sub("", CSS.read_text(encoding="utf-8"))
    modos = {}
    for modo, patron in (
        ("oscuro", r":root\s*\{(.*?)\n\}"),
        ("claro", r'\[data-theme="light"\]\s*\{(.*?)\n\}'),
    ):
        m = re.search(patron, css, re.DOTALL)
        if not m:
            raise SystemExit(f"no encuentro el bloque de tokens del modo {modo} en {CSS}")
        modos[modo] = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)))
    # El modo claro redefine solo lo que cambia; lo demás lo hereda de :root.
    heredado = dict(modos["oscuro"])
    heredado.update(modos["claro"])
    modos["claro"] = heredado
    return modos


def _rgb(valor: str, tokens: dict, visto=()) -> tuple | None:
    """(r, g, b, alfa) de un valor CSS, resolviendo var() y color-mix().
    Devuelve None si el valor no es un color (p. ej. `none`, `transparent`)."""
    v = valor.strip()
    m = re.fullmatch(r"var\((--[\w-]+)\)", v)
    if m:
        if m.group(1) in visto or m.group(1) not in tokens:
            return None
        return _rgb(tokens[m.group(1)], tokens, visto + (m.group(1),))
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        partes = [p.strip() for p in m.group(1).split(",")]
        if len(partes) >= 3:
            r, g, b = (int(float(p)) for p in partes[:3])
            a = float(partes[3]) if len(partes) > 3 else 1.0
            return (r, g, b, a)
    # color-mix(in srgb, <color> N%, transparent) — el resto del mapa de
    # componentes no usa otras formas, y una forma nueva se ve porque sale sin
    # resolver en vez de colarse con un número inventado.
    m = re.fullmatch(
        r"color-mix\(in srgb,\s*(.+?)\s+([\d.]+)%,\s*transparent\)", v, re.DOTALL
    )
    if m:
        base = _rgb(m.group(1), tokens, visto)
        if base:
            return (base[0], base[1], base[2], base[3] * float(m.group(2)) / 100)
    return None


def _componer(color: tuple, fondo: tuple) -> tuple:
    """Un color con alfa sobre su fondo, que es lo que el ojo ve."""
    a = color[3]
    return tuple(round(color[i] * a + fondo[i] * (1 - a)) for i in range(3)) + (1.0,)


def _lum(c: tuple) -> float:
    def canal(x):
        x /= 255
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

    return 0.2126 * canal(c[0]) + 0.7152 * canal(c[1]) + 0.0722 * canal(c[2])


def _contraste(tinta: tuple, fondo: tuple) -> float:
    a, b = sorted((_lum(tinta), _lum(fondo)), reverse=True)
    return (a + 0.05) / (b + 0.05)


_COLOR_SUELTO = re.compile(
    r"var\(--[\w-]+\)|color-mix\(in srgb,[^)]*\)[^,)]*\)?|#[0-9a-fA-F]{3,6}"
    r"|rgba?\([^)]*\)"
)


def _colores_en(texto: str) -> list:
    """Los colores que nombra una cadena de spec, también dentro de la prosa."""
    fuera = []
    for bruto in _COLOR_SUELTO.findall(texto):
        # color-mix se recorta mal con una regex simple cuando anida var():
        # se rescata el paréntesis que falta.
        if bruto.startswith("color-mix") and bruto.count("(") > bruto.count(")"):
            bruto += ")" * (bruto.count("(") - bruto.count(")"))
        fuera.append(bruto)
    return fuera


def _parejas() -> list:
    """(ruta, tinta, fondo) de cada ficha, heredando el fondo del componente."""
    fichas = json.loads(FICHAS.read_text(encoding="utf-8"))
    parejas = []

    def recorre(nodo, ruta, fondo):
        if isinstance(nodo, dict):
            propio = next(
                (nodo[k] for k in _CLAVES_FONDO if isinstance(nodo.get(k), str)), None
            )
            if propio:
                cols = _colores_en(propio)
                if cols:
                    fondo = cols[0]
            for k, v in nodo.items():
                if isinstance(v, (dict, list)):
                    recorre(v, f"{ruta}/{k}", fondo)
                elif isinstance(v, str) and any(t in k for t in _CLAVES_TINTA):
                    for col in _colores_en(v):
                        parejas.append((f"{ruta}/{k}", col, fondo))
        elif isinstance(nodo, list):
            for i, v in enumerate(nodo):
                nombre = v.get("name") or v.get("id") or i if isinstance(v, dict) else i
                recorre(v, f"{ruta}[{nombre}]", fondo)

    recorre(fichas, "", "var(--color-bg)")
    return parejas


def main() -> int:
    todas = "--todas" in sys.argv
    modos = _bloques()
    bajos = []
    print(f"suelo: {SUELO} · valores leídos en vivo de {CSS.relative_to(RAIZ)}\n")
    for ruta, tinta, fondo in _parejas():
        for modo, tokens in modos.items():
            cf = _rgb(fondo, tokens)
            ct = _rgb(tinta, tokens)
            if not cf or not ct:
                continue
            # El fondo con alfa se compone sobre el lienzo del modo.
            lienzo = _rgb("var(--color-bg)", tokens)
            if cf[3] < 1:
                cf = _componer(cf, lienzo)
            if ct[3] < 1:
                ct = _componer(ct, cf)
            r = _contraste(ct, cf)
            ok = r >= SUELO
            if not ok:
                bajos.append((ruta, modo, tinta, fondo, r))
            if todas or not ok:
                print(f"  {'ok ' if ok else 'BAJO'} {modo:6} {r:6.2f}  {ruta}")
                print(f"         tinta {tinta} sobre fondo {fondo}")
    print()
    if bajos:
        print(f"FICHAS: {len(bajos)} pareja(s) por debajo de {SUELO}")
        return 1
    print(f"FICHAS: todas las parejas llegan a {SUELO} en los dos modos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
