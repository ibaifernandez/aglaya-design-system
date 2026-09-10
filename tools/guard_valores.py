#!/usr/bin/env python3
"""Guardián de los valores de marca.

La avería que persigue: un valor de marca **copiado a mano** fuera del archivo
que lo declara. El día que el rojo se mueva, esa copia sigue pintando el rojo
viejo — y lo peor es dónde suele estar: en los specimens, que son justo lo que
alguien abre para ver «cuál es el rojo». Una copia en un sitio así no es un
descuido: es una segunda fuente de la verdad que nadie declaró.

QUÉ CUBRE Y QUÉ NO — léelo antes de darlo por vigilado
------------------------------------------------------
Este guardián se llamó «de valores» cuando solo perseguía colores, y el nombre
prometía el canon entero. Una guarda que promete más de lo que cumple es peor
que una pequeña y declarada, porque quien la aplica cree haber comprobado. Así
que la cobertura se declara aquí, token a token, y no se deduce del nombre.

El criterio de admisión de una familia es uno solo y está **medido**, no
razonado: que su literal sea AUTO-IDENTIFICABLE — que en este repo no pueda
significar otra cosa.

VIGILADAS:
  · color        hex, y también rgb()/rgba() — `rgba(252,252,252,.72)` es
                 `--color-muted` y hasta hoy no lo veía nadie. Incluye los
                 valores de los MODOS (`[data-theme="light"]`), que redefinen
                 los mismos tokens con otros valores.
  · tracking     unidad `em`. Medido: las 94 apariciones de un valor `em`
                 fuera del canon son letter-spacing. Ninguna otra cosa.
  · font         por el NOMBRE DE FAMILIA, no por el valor entero. El valor
                 entero solo caza 7 de 54 copias: las pilas de fallback
                 difieren (`'Space Mono', monospace` contra el canónico
                 `'Space Mono', ui-monospace, monospace`). Perseguir el valor
                 completo habría dado la familia por cubierta cazando un
                 octavo — la misma enfermedad que este bloque documenta.
  · dur          unidad `ms`.   · ease  `cubic-bezier(...)`.
  · bp, radius   unidad `px`.

NO VIGILADAS, y por qué:
  · space, layout, text, bp-max, layout-max — unidad `rem`. El mismo literal
    significa legítimamente cosas distintas: `--space-12` vale `3rem` y
    `clamp(3rem, 9vw, 9rem)` es un tamaño de letra, no un espaciado. Separarlos
    exige saber en qué propiedad CSS cae el valor, y eso es un parser de CSS
    — en un repo que ya tiene tres y una doctrina de no añadir el cuarto.
    Vigilarlas sin eso daría el rojo falso que desactiva un guardián.
  · radius-none/sm/md/lg (`0`), tracking-normal (`0`), space-0 (`0`),
    shadow-none (`none`) — el literal no identifica nada. Perseguir «0» es
    perseguir todos los archivos.
  · text-*, glow-*, aura-*, fg-*, color-border-brand — compuestos de otros
    tokens (`var(--font-display)`, `color-mix(... var(--color-brand) ...)`).
    Sus partes ya están vigiladas por el token al que apuntan; el compuesto no
    añade un valor nuevo que copiar.

Dos formas, las dos vistas en este repo:

1. **valor-copiado** — un valor declarado en `colors_and_type.css` escrito a
   mano en otro archivo. En hexadecimal (`#e8003d`) o como triplete rgb
   (`rgba(232,0,61,.2)`), que es como se coló en el manifiesto de componentes
   que sirve el MCP.

2. **manifiesto-desincronizado** — `products/products.json` declara el acento
   de un producto con un hex que ya no coincide con su token en el CSS. Ese
   manifiesto es un segundo domicilio legítimo (el MCP lo cruza en cada
   `get_accent`), así que aquí no se exime: se cruza. Un manifiesto que se
   desvía en silencio miente con la autoridad de un archivo canónico.

**Este guardián no lleva ni un valor dentro.** Lee la paleta de
`colors_and_type.css` en cada ejecución, igual que el MCP. Añade mañana un
acento de producto al CSS y queda protegido sin tocar este archivo; cambia el
rojo y el guardián persigue el nuevo. Un guardián con la paleta hardcodeada
sería la misma avería que persigue.

Genéricos que NO vigila: negro y blanco puros. Salen en cualquier `color: #fff`
legítimo sobre el rojo y en cualquier SVG. Vigilarlos daría el rojo falso que
desactiva un guardián el primer día.

Sobre la exención por acentos graves: aquí NO se aplica, igual que en
`guard_punteros.py` y al revés que en `guard_huella.py`. Un valor se escribe
casi siempre entrecomillado (`` `#e8003d` ``), así que eximir los acentos
graves dejaría el guardián sin nada que morder — y la copia que más engaña es
justo la que va en un bloque de código de un doc, porque parece un ejemplo
verificado.

Lo que NO cubre, dicho para que nadie lo dé por vigilado: los SVG de `assets/`
y `products/` llevan el rojo pintado dentro. Eso es el artefacto, no una cita
— si el rojo cambia hay que reexportarlos, y eso ningún script lo automatiza.

Sin dependencias: stdlib, como el resto de tools.

Uso:  python3 tools/guard_valores.py
Sale: 0 limpio · 1 valores copiados o manifiesto desviado · 2 no se pudo comprobar.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSS = RAIZ / "colors_and_type.css"
MANIFIESTO = RAIZ / "products" / "products.json"

# Lo que escribe una persona para CONSUMIR la marca. Los binarios y los SVG
# quedan fuera a propósito (ver el docstring).
EXTENSIONES = {".css", ".html", ".jsx", ".js", ".ts", ".tsx", ".md", ".json", ".py", ".sh"}

EXENTOS = (
    "colors_and_type.css",   # la casa: aquí es donde el valor vive
    "products/products.json",  # segundo domicilio declarado — se CRUZA, no se exime
    "tools/",                # los guardianes tienen que poder nombrar lo que persiguen
)
EXENTOS_CONTIENE = ("/vendor/",)  # dependencias vendorizadas: no las escribimos nosotros

# Negro y blanco puros. No identifican a nadie.
GENERICOS = {"#000", "#000000", "#fff", "#ffffff"}

# Mismo recorte que usa el MCP (brand.py `_all_tokens`), para que guardián y
# servidor no puedan discrepar sobre qué cuenta como token.
ROOT = re.compile(r":root\s*\{(.*?)\}", re.DOTALL)
DECL = re.compile(r"--([a-zA-Z0-9-]+)\s*:\s*([^;]+);")
SIN_COMENTARIOS = re.compile(r"/\*[\s\S]*?\*/")

# Los modos de color redefinen los MISMOS tokens con otros valores. Si no se
# leen, media paleta queda sin vigilar: `rgba(0,0,0,.72)` es `--color-muted` en
# claro y hasta hoy no lo perseguía nadie. Mismo recorte que usa el paquete
# (`scripts/build-tokens.mjs`, constante MODOS), por la misma razón por la que
# este guardián comparte forma con el MCP: tres recortes que divergen mienten.
MODOS = {"light": re.compile(r'\[data-theme="light"\]\s*\{(.*?)\n\}', re.DOTALL)}


def declaraciones_root():
    """Las declaraciones VIVAS de :root, ya sin comentarios.

    El filtrado está aquí y no en cada sitio que parsea porque este archivo
    recorta el CSS en DOS puntos, y dos copias del mismo recorte divergen: es la
    misma razón por la que este guardián comparte forma con el MCP.

    Sin quitar comentarios, una declaración aparcada dentro de :root cuenta como
    viva y el guardián vigila un valor que ya no es de nadie. El fallo solo
    aparece si la comentada va DESPUÉS de la viva — antes, gana la viva y pasa
    desapercibido.
    """
    if not CSS.is_file():
        return None
    m = ROOT.search(CSS.read_text(encoding="utf-8"))
    if not m:
        return None
    return DECL.findall(SIN_COMENTARIOS.sub("", m.group(1)))
HEX = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}(?:[0-9a-fA-F]{2})?)?\b")


def paleta() -> dict[str, list[str]] | None:
    """{valor hex -> [tokens que lo declaran]}, leído en vivo del CSS canónico."""
    decls = declaraciones_root()
    if decls is None:
        return None
    out: dict[str, list[str]] = {}
    for nombre, valor in decls:
        for h in HEX.findall(valor):
            h = h.lower()
            if h in GENERICOS:
                continue
            out.setdefault(h, []).append(f"--{nombre}")
    return out


def sondas(valores: dict[str, list[str]]) -> list[tuple[re.Pattern, str, str]]:
    """Para cada valor, cómo puede aparecer copiado: en hex y en triplete rgb."""
    fuera = []
    for h, tokens in valores.items():
        # Un valor puede tener más de un token (el verde es a la vez corporativo
        # y acento de DESIGN SYSTEM). Se propone el primero y se nombran los
        # otros: elegir por el consumidor sería adivinar su intención.
        pista = tokens[0]
        if len(tokens) > 1:
            pista += "  [también: " + ", ".join(tokens[1:]) + "]"

        # El hex tal cual, admitiendo el par de alfa (`#e8003dff` es el mismo
        # rojo) pero sin tragarse un hex más largo que solo empiece igual.
        fuera.append((
            re.compile(re.escape(h) + r"(?:[0-9a-fA-F]{2})?(?![0-9a-fA-F])", re.IGNORECASE),
            h, tokens[0], pista,
        ))

        if len(h) == 7:  # #rrggbb
            r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
            # El mismo color escrito como rgb()/rgba() — así se coló en el
            # manifiesto de componentes que sirve el MCP. Se exige el `rgb(`
            # delante: un triplete suelto no es un color, y perseguir tres
            # números sin contexto es cómo se fabrica un rojo falso.
            fuera.append((
                re.compile(rf"rgba?\(\s*{r}\s*[,\s]\s*{g}\s*[,\s]\s*{b}\b"),
                f"rgb({r} {g} {b})", tokens[0], pista,
            ))
            # Forma corta, cuando el valor la admite: #ffcc00 == #fc0.
            if h[1] == h[2] and h[3] == h[4] and h[5] == h[6]:
                corto = f"#{h[1]}{h[3]}{h[5]}"
                fuera.append((
                    re.compile(re.escape(corto) + r"(?![0-9a-fA-F])", re.IGNORECASE),
                    corto, tokens[0], pista,
                ))
    return fuera


# ── Las familias que no son un hex ──────────────────────────────────────────
#
# Cada sonda de aquí abajo entra porque su literal es AUTO-IDENTIFICABLE en este
# repo, comprobado contándolo. Lo que no lo es, no entra — y el porqué está en
# el docstring, familia por familia, para que nadie lo dé por vigilado.

# Un valor con unidad. `rem` NO está: el mismo `3rem` es un espaciado y un
# tamaño de letra, y distinguirlos exige saber en qué propiedad cae.
UNIDAD = re.compile(r"^-?(?:\d+\.?\d*|\.\d+)(em|ms|px)$")
CUBIC = re.compile(r"^cubic-bezier\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)$")
FUNC_RGB = re.compile(r"^rgba?\(\s*(\d+)\s*[,\s]\s*(\d+)\s*[,\s]\s*(\d+)\s*(?:[,/]\s*([\d.%]+)\s*)?\)$")
FAMILIA = re.compile(r"^\s*['\"]([^'\"]+)['\"]")


def _anclada(literal: str) -> re.Pattern:
    """El literal, sin dejar que se lo trague un número más largo.

    Es la diferencia entre `5rem` y el `5rem` que vive dentro de `0.5rem`. Sin
    esto, `--space-20` gritaba en cada `0.5rem` del specimen de espaciados: un
    rojo falso por coincidencia de substring, que es cómo se desactiva una
    guarda el primer día.

    La cola NO puede rechazar un punto a secas: `1280px.` al final de una frase
    es puntuación, no un número más largo. Rechazarlo dejaba escapar toda copia
    escrita en prosa — que es justo donde más engaña, porque parece verificada.
    Lo cazó la batería, no la lectura: dos escapes de nueve.
    """
    return re.compile(r"(?<![\w.%-])" + re.escape(literal) + r"(?![\w%]|\.\d)")


def _alfas(alfa: str) -> list[str]:
    """Todas las grafías del MISMO alfa: `0.20`, `.20`, `0.2`, `.2`, `20%`.

    El alfa es lo único que separa `--color-border` de `--color-border-strong`
    —los dos son blanco— así que la sonda tiene que exigirlo. Y si lo exige por
    su grafía literal, una copia escrita `0.2` en vez de `0.20` se le escapa
    siendo el mismo color. Se comparan como números, no como texto.
    """
    try:
        n = float(alfa.rstrip("%")) / (100 if alfa.endswith("%") else 1)
    except ValueError:
        return [alfa]
    corto = f"{n:g}"                       # 0.20 -> 0.2 · 0.08 -> 0.08
    fuera = {alfa, corto, corto.lstrip("0") or "0"}
    if alfa.startswith("0."):
        fuera.add(alfa[1:])
    pct = n * 100
    fuera.add(f"{pct:g}%")
    return sorted(fuera, key=len, reverse=True)   # la más larga primero


def declaraciones_modos() -> list[tuple[str, str]]:
    """Las declaraciones de los bloques de modo, ya sin comentarios."""
    if not CSS.is_file():
        return []
    css = CSS.read_text(encoding="utf-8")
    fuera = []
    for patron in MODOS.values():
        m = patron.search(css)
        if m:
            fuera += DECL.findall(SIN_COMENTARIOS.sub("", m.group(1)))
    return fuera


def sondas_familias() -> list[tuple[re.Pattern, str, str, str]]:
    """Sondas de los tokens que no se declaran con un hex."""
    decls = declaraciones_root()
    if decls is None:
        return []

    # Un valor puede tener más de un token, igual que el verde es a la vez
    # corporativo y acento de DESIGN SYSTEM. Se nombra el primero y se citan los
    # otros: elegir por el consumidor sería adivinar su intención.
    duenos: dict[str, list[str]] = {}
    for nombre, valor in decls + declaraciones_modos():
        duenos.setdefault(valor.strip(), []).append(f"--{nombre}")

    fuera = []
    vistos = set()
    for valor, tokens in duenos.items():
        pista = tokens[0]
        if len(tokens) > 1:
            pista += "  [también: " + ", ".join(dict.fromkeys(tokens[1:])) + "]"

        def añadir(patron, etiqueta):
            clave = (patron.pattern, tokens[0])
            if clave not in vistos:
                vistos.add(clave)
                fuera.append((patron, etiqueta, tokens[0], pista))

        if UNIDAD.match(valor):
            añadir(_anclada(valor), valor)
            continue

        m = CUBIC.match(valor)
        if m:
            a, b, c, d = m.groups()
            añadir(re.compile(
                rf"cubic-bezier\(\s*{re.escape(a)}\s*,\s*{re.escape(b)}\s*,"
                rf"\s*{re.escape(c)}\s*,\s*{re.escape(d)}\s*\)"), valor)
            continue

        m = FUNC_RGB.match(valor)
        if m:
            r, g, b, alfa = m.groups()
            # El mismo color escrito con coma o con espacio, y con el alfa
            # escrito `0.72` o `.72`. Sin el alfa no se distingue un borde de
            # otro: es lo único que separa --color-border de --color-text.
            cola = ""
            if alfa:
                cola = rf"\s*[,/]\s*(?:{'|'.join(re.escape(a) for a in _alfas(alfa))})(?![\d%])"
            añadir(re.compile(rf"rgba?\(\s*{r}\s*[,\s]\s*{g}\s*[,\s]\s*{b}{cola}"), valor)
            continue

        m = FAMILIA.match(valor)
        if m and any(t.startswith("--font-") for t in tokens):
            # Por el NOMBRE de la familia, no por la pila entera: las copias
            # cambian el fallback y el valor completo solo caza un octavo.
            nombre = m.group(1)
            añadir(re.compile(rf"['\"]{re.escape(nombre)}['\"]"), f"'{nombre}'")
    return fuera


def archivos_versionados() -> list[Path] | None:
    try:
        salida = subprocess.run(
            ["git", "-C", str(RAIZ), "ls-files"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    fuera = []
    for linea in salida.splitlines():
        if not linea or Path(linea).suffix not in EXTENSIONES:
            continue
        if linea.startswith(EXENTOS) or any(t in f"/{linea}" for t in EXENTOS_CONTIENE):
            continue
        fuera.append(RAIZ / linea)
    return fuera


def cruzar_manifiesto(valores: dict[str, list[str]]) -> list[tuple]:
    """products.json declara acentos; el CSS declara los mismos tokens. Que no
    se separen en silencio."""
    if not MANIFIESTO.is_file():
        return []
    try:
        datos = json.loads(MANIFIESTO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [(Path("products/products.json"), 0, "manifiesto-ilegible", str(e),
                 "el MCP no puede servir identidad de producto con el manifiesto roto", "")]

    css_tokens = {}
    for nombre, valor in (declaraciones_root() or []):
        css_tokens[f"--{nombre}"] = valor.strip()

    lineas = MANIFIESTO.read_text(encoding="utf-8").splitlines()

    def linea_de(aguja: str) -> int:
        for i, l in enumerate(lineas, 1):
            if aguja in l:
                return i
        return 0

    hallazgos = []
    for p in datos.get("products", []):
        acento = p.get("accent") or {}
        pares = [(acento.get("token"), acento.get("hex"), "acento")]
        sec = acento.get("secondary")
        if isinstance(sec, dict):
            pares.append((sec.get("token"), sec.get("hex"), "acento secundario"))
        for token, hexa, etiqueta in pares:
            if not token or not hexa:
                continue
            en_css = css_tokens.get(token)
            if en_css is None:
                hallazgos.append((
                    Path("products/products.json"), linea_de(token), "manifiesto-desincronizado",
                    f"{p.get('id')}: {token}",
                    f"el {etiqueta} declara un token que no existe en colors_and_type.css",
                    f'"token": "{token}"',
                ))
            elif en_css.lower() != hexa.lower():
                hallazgos.append((
                    Path("products/products.json"), linea_de(hexa), "manifiesto-desincronizado",
                    f"{p.get('id')}: {hexa} vs {en_css}",
                    f"el {etiqueta} del manifiesto y su token en el CSS ya no dicen lo mismo; "
                    "manda el CSS",
                    f'"hex": "{hexa}"',
                ))
    return hallazgos


def main() -> int:
    valores = paleta()
    if valores is None:
        print("guard-valores: no puedo leer la paleta de colors_and_type.css.", file=sys.stderr)
        return 2
    if not valores:
        print("guard-valores: la paleta salió vacía. Sin valores que perseguir no hay nada\n"
              "  que vigilar: fallo a propósito para no dar un verde vacío.", file=sys.stderr)
        return 2

    docs = archivos_versionados()
    if docs is None:
        print("guard-valores: no puedo listar los archivos versionados (¿git?).", file=sys.stderr)
        return 2
    if not docs:
        print("guard-valores: no encuentro ningún archivo que vigilar. Fallo a propósito\n"
              "  para no dar un verde vacío.", file=sys.stderr)
        return 2

    pruebas = sondas(valores) + sondas_familias()
    hallazgos = []
    for f in docs:
        rel = f.relative_to(RAIZ)
        try:
            texto = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            # Una vez por línea y sonda: el parte tiene que caber en una
            # pantalla o nadie lo lee entero.
            encontrados = []
            for patron, etiqueta, token, pista in pruebas:
                m = patron.search(linea)
                if m:
                    encontrados.append((m.span(), etiqueta, token, pista))

            for span, etiqueta, token, pista in encontrados:
                # La copia más específica gana a la que vive dentro de ella.
                # `rgba(252,252,252,0.72)` es --color-muted, y el triplete sin
                # alfa que contiene es --color-text: si se reportan los dos, la
                # misma línea recibe dos consejos y el genérico es el
                # EQUIVOCADO — consumir --color-text pierde el 0.72 y pinta
                # otro color. Un guardián que enseña mal es peor que ninguno.
                if any(otro != span and otro[0] <= span[0] and span[1] <= otro[1]
                       for otro, *_ in encontrados):
                    continue
                hallazgos.append((
                    rel, n, "valor-copiado", etiqueta,
                    f"es el valor de {pista} — consúmelo por token: `var({token})` "
                    "en CSS, `get_token` por MCP",
                    linea.strip()[:120],
                ))

    hallazgos += cruzar_manifiesto(valores)

    if not hallazgos:
        print(f"guard-valores: OK — {len(pruebas)} sonda(s) sobre {len(valores)} color(es) "
              f"y las familias auto-identificables del canon, en {len(docs)} archivo(s); "
              "ninguno copiado a mano.")
        return 0

    print(f"guard-valores: {len(hallazgos)} valor(es) de marca fuera de su casa\n", file=sys.stderr)
    for rel, linea, regla, encontrado, porque, contexto in hallazgos:
        donde = f"{rel}:{linea}" if linea else str(rel)
        print(f"  {donde}  [{regla}]  → {encontrado!r}", file=sys.stderr)
        print(f"      {porque}", file=sys.stderr)
        if contexto:
            print(f"      {contexto}\n", file=sys.stderr)
    print(
        "  La regla: el valor vive en colors_and_type.css y se consume por token\n"
        "  (`var(--…)` en CSS, `get_token`/`get_accent` por el MCP). Para una variante\n"
        "  con alfa, derívala: color-mix(in srgb, var(--color-brand) 20%, transparent).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
