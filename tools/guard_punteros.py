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

Alcance: los `.md` versionados, salvo `graphify-out/` (artefacto regenerable,
no lo escribe una persona).

Sobre la exención por acentos graves: aquí NO se aplica. En `guard_huella.py`
sí, porque aquel doc necesita poder nombrar los patrones que prohíbe. Este es
el caso contrario: una ruta se escribe casi siempre entre acentos graves, así
que eximirlos dejaría el guardián sin nada que morder — que es exactamente
como estaba escrita la ruta caduca que motivó todo esto.

Sin dependencias: stdlib, como el resto de tools.

Uso:  python3 tools/guard_punteros.py
Sale: 0 limpio · 1 punteros rotos · 2 no se pudo comprobar.
"""

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIDOS = ("graphify-out/",)

# [texto](ruta) — el puntero que un humano o un agente van a seguir.
ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Una ruta interna del atlas del capitán. Deliberadamente sin exención de
# acentos graves (ver el docstring).
RUTA_ATLAS = re.compile(r"\batlas/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*")


def docs_versionados() -> list[Path] | None:
    try:
        salida = subprocess.run(
            ["git", "-C", str(RAIZ), "ls-files", "*.md"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [
        RAIZ / linea
        for linea in salida.splitlines()
        if linea and not linea.startswith(EXCLUIDOS)
    ]


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


def main() -> int:
    docs = docs_versionados()
    if docs is None:
        print("guard-punteros: no puedo listar los .md versionados (¿git?).", file=sys.stderr)
        return 2
    if not docs:
        print("guard-punteros: no encuentro ningún .md versionado. Sin docs no hay nada\n"
              "  que vigilar: fallo a propósito para no dar un verde vacío.", file=sys.stderr)
        return 2

    hallazgos = []
    for doc in docs:
        rel = doc.relative_to(RAIZ)
        for n, linea in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for destino in ENLACE.findall(linea):
                if es_externo(destino) or resuelve(doc, destino):
                    continue
                hallazgos.append((
                    rel, n, "enlace-roto", destino,
                    "el archivo no está donde el enlace dice; muévelo o corrige el enlace",
                    linea.strip(),
                ))
            for ruta in RUTA_ATLAS.findall(linea):
                hallazgos.append((
                    rel, n, "ruta-de-atlas", ruta,
                    "las rutas del capitán caducan cuando él reorganiza: pregunta por la "
                    "puerta (ficha, contrato, donde_pregunto, buscar)",
                    linea.strip(),
                ))

    if not hallazgos:
        print(f"guard-punteros: OK — {len(docs)} doc(s) versionados, todos los punteros resuelven.")
        return 0

    print(f"guard-punteros: {len(hallazgos)} puntero(s) que no resuelven\n", file=sys.stderr)
    for rel, linea, regla, encontrado, porque, contexto in hallazgos:
        print(f"  {rel}:{linea}  [{regla}]  → {encontrado!r}", file=sys.stderr)
        print(f"      {porque}", file=sys.stderr)
        print(f"      {contexto}\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
