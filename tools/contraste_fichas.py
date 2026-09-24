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


# Toda la familia de funciones de color de CSS, no solo las que hoy usa el
# mapa de fichas. Con `var|color-mix|rgba?` a secas, un `hsl()` escrito en una
# ficha no se extraía siquiera — y entonces no había pareja que reportar como
# sin medir: desaparecía un paso antes que `badge/brand`. Las funciones que no
# son de color (`translate()`, `clamp()`) quedan fuera a propósito: la prosa de
# las specs las nombra y no forman pareja.
_INICIO_COLOR = re.compile(
    r"\b(?:var|rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\(|#[0-9a-fA-F]{3,6}"
)


def _colores_en(texto: str) -> list:
    """Los colores que nombra una cadena de spec, también dentro de la prosa.

    Los paréntesis se cuentan, no se recortan con una regex. Una regex de
    `[^)]*` corta `color-mix(in srgb, var(--color-brand) 10%, transparent)` en
    el primer `)` —el del `var()`— y devuelve un valor que ya no resuelve. Eso
    hizo desaparecer la ficha `badge/brand` de la salida entera: ni ok ni BAJO,
    y en claro daba 1.72.
    """
    fuera = []
    i = 0
    while True:
        m = _INICIO_COLOR.search(texto, i)
        if not m:
            return fuera
        if m.group().startswith("#"):
            fuera.append(m.group())
            i = m.end()
            continue
        profundidad, j = 0, m.end() - 1
        while j < len(texto):
            if texto[j] == "(":
                profundidad += 1
            elif texto[j] == ")":
                profundidad -= 1
                if profundidad == 0:
                    break
            j += 1
        fuera.append(texto[m.start() : j + 1])
        i = j + 1


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


def _es_token_no_cromatico(valor: str, tokens: dict, visto=()) -> bool:
    """¿Es un token que existe y cuyo valor NO INTENTA ser un color? Una
    tipografía o un tracking viajan en la misma cadena que los colores y no
    forman pareja.

    Lo que decide es la FORMA del valor final, no que este guion sepa leerlo.
    Antes bastaba con que `_rgb` fallara: un token de color escrito en una forma
    desconocida —`--color-muted: hsl(0 0% 71%)`— se daba por «no cromático» y su
    pareja desaparecía sin aviso. Medido por el vigilante sobre `bbee786`: de 22
    parejas se pasaba a 19, con 0 avisos y el mismo `rc`. Ahora ese caso se
    imprime, que es lo único que un instrumento no puede dejar de hacer.
    """
    m = re.fullmatch(r"var\((--[\w-]+)\)", valor.strip())
    if not m or m.group(1) not in tokens or m.group(1) in visto:
        return False
    destino = tokens[m.group(1)].strip()
    if re.fullmatch(r"var\(--[\w-]+\)", destino):
        return _es_token_no_cromatico(destino, tokens, visto + (m.group(1),))
    # Huele a color y no se deja leer -> hay una pareja sin medir, y se dice.
    return not _INICIO_COLOR.search(destino)


def main() -> int:
    todas = "--todas" in sys.argv
    modos = _bloques()
    bajos = []
    sin_resolver = []
    print(f"suelo: {SUELO} · valores leídos en vivo de {CSS.relative_to(RAIZ)}\n")
    for ruta, tinta, fondo in _parejas():
        for modo, tokens in modos.items():
            cf = _rgb(fondo, tokens)
            ct = _rgb(tinta, tokens)
            if not cf or not ct:
                # Nada se salta callando. Un valor que no resuelve es de una de
                # dos clases, y solo una es inocente:
                #   · un token que EXISTE y no es color (`var(--font-mono)`,
                #     `var(--tracking-widest)`) — la spec los nombra al lado de
                #     los colores y no hay pareja que medir;
                #   · cualquier otra cosa — una forma que este guion no
                #     entiende, y entonces hay una pareja SIN MEDIR.
                # La segunda se imprime y hace que esto no salga con 0. Antes se
                # hacía `continue` con las dos, y así desapareció `badge/brand`,
                # que en claro daba 1.72.
                for valor, papel in ((tinta, "tinta"), (fondo, "fondo")):
                    if _rgb(valor, tokens):
                        continue
                    if _es_token_no_cromatico(valor, tokens):
                        continue
                    sin_resolver.append((ruta, modo, papel, valor))
                    print(f"  SIN RESOLVER {modo:6}  {ruta}")
                    print(f"         {papel} {valor} — este guion no sabe leer esa forma")
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
    if sin_resolver:
        print(f"FICHAS: {len(sin_resolver)} valor(es) sin medir — hay parejas sin comprobar")
    if bajos:
        print(f"FICHAS: {len(bajos)} pareja(s) por debajo de {SUELO}")
    if bajos or sin_resolver:
        return 1
    print(f"FICHAS: todas las parejas llegan a {SUELO} en los dos modos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
