#!/usr/bin/env python3
"""Guardián de los punteros de los docs.

Dos averías distintas, las dos silenciosas, las dos vistas en la flota:

1. **Enlace roto a un archivo propio.** Reorganizas el repo, mueves un archivo,
   y el enlace que lo citaba sigue ahí apuntando al vacío. Nadie se entera
   hasta que alguien hace clic — o hasta que un agente lee el doc, va a la
   ruta, no encuentra nada y se inventa el resto.

2. **Ruta interna del atlas del capitán.** El capitán reorganiza SU repo y
   nuestras rutas caducan sin que nada se ponga rojo aquí. La regla acordada
   con él es no citarlas: el único puntero fijo es el nombre de su repo, y lo
   demás se pregunta al MCP `aglaya-atlas` — `ficha()`, `contrato()`,
   `donde_pregunto()`, `buscar()` — que contestan citando su fuente.

ALCANCE, Y LO QUE DELIBERADAMENTE QUEDA FUERA
---------------------------------------------
Este guardián se llamaba «de punteros» y solo miraba `.md`. Dio verde sobre el
PR que borró `SKILL.md` dejando tres referencias vivas —en `LICENSE`, en
`colors_and_type.css` y en `aglaya-ds-mcp/pyproject.toml`—, ninguna de las
cuales es markdown. Falló en el escenario más obvio que existe: alguien borra
un fichero y quedan referencias.

Ficheros: los versionados de texto. Fuera quedan `graphify-out/` (artefacto
regenerable), `/vendor/` (dependencias que no escribimos), `tools/` —los
sabotajes de las baterías nombran rutas rotas a propósito, y esa exención es la
misma que ya lleva `guard_valores.py` por la misma razón—, `.claude/` (config
local, apunta fuera del repo) y `package.json`, cuyas rutas de `exports`,
`files` y `bin` las verifica `guard_paquete.py`: quien las vigila es él, no
este. No es silenciar, es que tienen dueño.

Formas de puntero que reconoce: el enlace markdown `[texto](ruta)` y la RUTA
—una cadena con separador y extensión—, que es una ruta por construcción y no
prosa.

**Lo que NO reconoce, y hay que saberlo antes de darlo por vigilado: el nombre
de fichero suelto.** No es un recorte de esfuerzo, es que no se puede decidir.
Cuando se retiró `SKILL.md`, dos de las tres referencias rotas lo escribían
igual que lo escriben las retractaciones legítimas que quedaron después:

    LICENSE (rota)        non-negotiables in `README.md`, `SKILL.md` and ...
    CONTRACT.md (buena)   `SKILL.md` declaraba en su frontmatter una skill ...

Byte a byte, la misma grafía. Un detector de nombre suelto pondría en rojo las
retractaciones —que son correctas y tienen que quedarse— junto con los punteros
rotos. Medido además sobre el árbol: 742 coincidencias, 6 de ellas reales. Un
guardián que grita así lo desactiva el primero que lo sufra.

Consecuencia práctica que hay que aceptar: si alguien borra un fichero y deja
su nombre suelto en prosa, esto no lo caza. Lo que sí caza es la ruta y el
enlace, que es como se escribe un puntero cuando de verdad manda ir a leer.

Sobre la exención por acentos graves: aquí NO se aplica. En `guard_huella.py`
sí, porque aquel doc necesita poder nombrar los patrones que prohíbe. Este es
el caso contrario: una ruta se escribe casi siempre entre acentos graves, así
que eximirlos dejaría el guardián sin nada que morder — que es exactamente
como estaba escrita la ruta caduca que motivó todo esto.

Sin dependencias: stdlib, como el resto de tools.

Uso:  python3 tools/guard_punteros.py
Sale: 0 limpio · 1 punteros rotos · 2 no se pudo comprobar.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIDOS = ("graphify-out/", "tools/", ".claude/", "package.json")
EXCLUIDOS_CONTIENE = ("/vendor/",)

# Lo que lleva dentro un puntero escrito por una persona. Los binarios y los
# artefactos quedan fuera: una fuente o un PNG no citan rutas.
BINARIOS = {".svg", ".png", ".ttf", ".woff", ".woff2", ".ico", ".jpg", ".jpeg", ".zip"}

# [texto](ruta) — el puntero que un humano o un agente van a seguir.
ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Una RUTA: lleva separador y extensión. Es lo que separa un puntero de la
# prosa — `docs/CONTRACT.md` solo puede ser una ruta, mientras que `SKILL.md`
# suelto puede ser tanto una instrucción como una retractación (ver el
# docstring: por eso el nombre suelto no se vigila).
EXTENSIONES = "md|css|json|py|sh|mjs|js|toml|yml|yaml|txt|html|jsx|ts|tsx|svg|ttf"
RUTA = re.compile(
    rf"(?<![\w.-])(@?(?:/|\.{{1,2}}/)?(?:[\w.@-]+/)+[\w.-]+\.(?:{EXTENSIONES}))\b"
)

# Una ruta interna del atlas del capitán. Deliberadamente sin exención de
# acentos graves (ver el docstring).
#
# El lookbehind evita el falso positivo que más duele: `aglaya-atlas` es el
# nombre del MCP y se cita a todas horas, así que `aglaya-atlas/mcp/...` no es
# una ruta del atlas — es el servidor. Sin esto el guardián grita en la línea
# que precisamente enseña a preguntar por la puerta, y un guardián que grita de
# más lo desactiva el primero que lo sufra.
RUTA_ATLAS = re.compile(r"(?<!aglaya-)\batlas/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*")

# URLs, para decidir si una coincidencia va dentro de un enlace externo.
URL = re.compile(r"https?://[^\s)\]`\"'<>]+")

# El repo del capitán. Una URL a SU atlas caduca igual que una ruta suelta
# —cuando reorganiza, GitHub devuelve 404— así que esa sí se vigila. Una URL
# ajena que casualmente lleve `atlas/` en su ruta no es asunto nuestro.
REPO_CAPITAN = "aglaya-orchestrator"


def nombre_del_paquete() -> str:
    """`@aglaya/design-tokens`. Un import que empieza por ahí no es una ruta de
    este repo: lo resuelve npm en el disco del consumidor, y aquí no existe."""
    try:
        return json.loads((RAIZ / "package.json").read_text(encoding="utf-8"))["name"]
    except (OSError, ValueError, KeyError):
        return ""


def docs_versionados() -> list[Path] | None:
    """Los ficheros de texto versionados. Ver el docstring para el porqué de
    cada exclusión — ninguna se añadió para callar un rojo concreto."""
    try:
        salida = subprocess.run(
            ["git", "-C", str(RAIZ), "ls-files"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    fuera = []
    for linea in salida.splitlines():
        if not linea or linea.startswith(EXCLUIDOS):
            continue
        if any(t in f"/{linea}" for t in EXCLUIDOS_CONTIENE):
            continue
        ruta = RAIZ / linea
        if Path(linea).suffix.lower() in BINARIOS:
            continue          # atajo barato: no leer megabytes de tipografía
        try:
            ruta.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            # Lo decide el CONTENIDO, no la extensión. Una lista de extensiones
            # binarias se queda corta con la siguiente que entre —`.otf` ya se
            # coló—, y esa es justo la avería que este guardián acaba de sufrir:
            # estrechar por una lista y volver a fallar con lo que no está en ella.
            continue
        fuera.append(ruta)
    return fuera


def es_externo(destino: str) -> bool:
    return destino.startswith(("http://", "https://", "mailto:", "#"))


def resuelve(doc: Path, destino: str) -> bool:
    """¿El destino existe, mirando junto al doc y desde la raíz del repo?"""
    limpio = destino.split("#")[0].strip()
    if not limpio:
        return True  # ancla pura dentro del mismo doc
    candidatos = [doc.parent / limpio, RAIZ / limpio]
    if any(c.exists() for c in candidatos):
        return True
    if "*" in limpio:  # patrón tipo preview/components-*.html
        return bool(list(doc.parent.glob(limpio)) or list(RAIZ.glob(limpio)))
    return False


def resuelve_ruta(doc: Path, ruta: str, paquete: str) -> bool:
    """Como `resuelve`, más lo que una ruta puede ser sin estar en el disco."""
    if ruta.startswith("/"):
        # Absoluta: nunca es de este repo. Los docs las usan como marcador de
        # posición («/ABS/PATH/…» en el README del MCP).
        return True
    if paquete and ruta.lstrip("@").startswith(paquete.lstrip("@")):
        return True
    if ruta.startswith("../"):
        # Relativa al doc que la escribe: siempre se comprueba. Es la forma que
        # tenía el puntero roto de `aglaya-ds-mcp/pyproject.toml`.
        #
        # OJO con `lstrip("./")`: quita CARACTERES, no un prefijo, así que
        # convierte «../SKILL.md» en «SKILL.md» y la ruta se cuela por la rama
        # de «ajena». Escrito aquí porque ya me pasó, y la batería no lo vio
        # —inyecta en CLAUDE.md, donde no hay rutas con `../`.
        return resuelve(doc, ruta)

    limpio = ruta[2:] if ruta.startswith("./") else ruta

    if limpio.startswith("dist/"):
        # `dist/` se genera en cada instalación y está en .gitignore a
        # propósito: un tokens.json commiteado sería una segunda casa para cada
        # valor de marca. Citarlo es correcto aunque aquí no exista.
        return True

    # ¿Es una ruta NUESTRA? Solo si su primer segmento existe aquí. Sin esto el
    # guardián grita en `aglaya-atlas/mcp/server.py` —el servidor del capitán,
    # que vive en otro repo y se cita a propósito— y en cualquier ruta ajena
    # que aparezca en prosa. Un guardián que grita de más lo desactiva el
    # primero que lo sufra, y ese caso ya estaba en la batería como control.
    #
    # El precio, dicho para que nadie lo dé por vigilado: si se borra un
    # DIRECTORIO entero, las rutas que apuntaban dentro dejan de comprobarse,
    # porque su primer segmento tampoco existe ya.
    if not (RAIZ / limpio.split("/", 1)[0]).exists():
        return True

    return resuelve(doc, ruta)


def main() -> int:
    docs = docs_versionados()
    if docs is None:
        print("guard-punteros: no puedo listar los ficheros versionados (¿git?).", file=sys.stderr)
        return 2
    if not docs:
        print("guard-punteros: no encuentro ningún fichero versionado. Sin nada que leer\n"
              "  no hay nada que vigilar: fallo a propósito para no dar un verde vacío.",
              file=sys.stderr)
        return 2

    paquete = nombre_del_paquete()
    hallazgos = []
    for doc in docs:
        rel = doc.relative_to(RAIZ)
        try:
            texto = doc.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, linea in enumerate(texto.splitlines(), 1):
            for m in RUTA.finditer(linea):
                if resuelve_ruta(doc, m.group(1), paquete):
                    continue
                hallazgos.append((
                    rel, n, "ruta-rota", m.group(1),
                    "la ruta no lleva a ningún sitio; corrígela o quítala — si el fichero "
                    "se borró, el puntero se borra con él",
                    linea.strip()[:120],
                ))
            for destino in ENLACE.findall(linea):
                if es_externo(destino) or resuelve(doc, destino):
                    continue
                hallazgos.append((
                    rel, n, "enlace-roto", destino,
                    "el archivo no está donde el enlace dice; muévelo o corrige el enlace",
                    linea.strip(),
                ))
            urls = [(m.start(), m.end(), m.group(0)) for m in URL.finditer(linea)]
            for m in RUTA_ATLAS.finditer(linea):
                dentro = next(
                    (u for ini, fin, u in urls if ini <= m.start() and m.end() <= fin), None
                )
                # Una URL ajena que lleve `atlas/` no es cosa nuestra; una que
                # apunte al repo del capitán sí, porque caduca igual.
                if dentro is not None and REPO_CAPITAN not in dentro:
                    continue
                hallazgos.append((
                    rel, n, "ruta-de-atlas", m.group(0),
                    "las rutas del capitán caducan cuando él reorganiza: pregunta por la "
                    "puerta (ficha, contrato, donde_pregunto, buscar)",
                    linea.strip(),
                ))

    if not hallazgos:
        print(f"guard-punteros: OK — {len(docs)} fichero(s) de texto versionados; "
              "todo enlace y toda ruta resuelven.")
        return 0

    print(f"guard-punteros: {len(hallazgos)} puntero(s) que no resuelven\n", file=sys.stderr)
    for rel, linea, regla, encontrado, porque, contexto in hallazgos:
        print(f"  {rel}:{linea}  [{regla}]  → {encontrado!r}", file=sys.stderr)
        print(f"      {porque}", file=sys.stderr)
        print(f"      {contexto}\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
