#!/usr/bin/env python3
"""Guardián de los valores de marca.

La avería que persigue: un valor de marca **copiado a mano** fuera del archivo
que lo declara. El día que el rojo se mueva, esa copia sigue pintando el rojo
viejo — y lo peor es dónde suele estar: en los specimens, que son justo lo que
alguien abre para ver «cuál es el rojo». Una copia en un sitio así no es un
descuido: es una segunda fuente de la verdad que nadie declaró.

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
HEX = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}(?:[0-9a-fA-F]{2})?)?\b")


def paleta() -> dict[str, list[str]] | None:
    """{valor hex -> [tokens que lo declaran]}, leído en vivo del CSS canónico."""
    if not CSS.is_file():
        return None
    m = ROOT.search(CSS.read_text(encoding="utf-8"))
    if not m:
        return None
    out: dict[str, list[str]] = {}
    for nombre, valor in DECL.findall(m.group(1)):
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
    m = ROOT.search(CSS.read_text(encoding="utf-8"))
    if m:
        for nombre, valor in DECL.findall(m.group(1)):
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

    pruebas = sondas(valores)
    hallazgos = []
    for f in docs:
        rel = f.relative_to(RAIZ)
        try:
            texto = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            for patron, etiqueta, token, pista in pruebas:
                if patron.search(linea):
                    hallazgos.append((
                        rel, n, "valor-copiado", etiqueta,
                        f"es el valor de {pista} — consúmelo por token: `var({token})` "
                        "en CSS, `get_token` por MCP",
                        linea.strip()[:120],
                    ))
                    # Una vez por línea y sonda: el parte tiene que caber en una
                    # pantalla o nadie lo lee entero.

    hallazgos += cruzar_manifiesto(valores)

    if not hallazgos:
        print(f"guard-valores: OK — {len(valores)} valor(es) de marca vigilados en "
              f"{len(docs)} archivo(s); ninguno copiado a mano.")
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
