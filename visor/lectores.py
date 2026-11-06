#!/usr/bin/env python3
"""lectores.py — lo que el visor responde en `/api/*`, en UN solo sitio.

POR QUÉ EXISTE ESTE FICHERO. El visor se sirve de dos maneras: en vivo con
`servidor.py` y como página estática generada por `construir.py`. Si cada uno
armara su respuesta, serían **dos intérpretes del canon**, y esa es la avería
que esta casa ya se ha comido varias veces (el kit con su `:root` propio, las
muestras con los hex tecleados, el docstring que contaba colores). Aquí no
puede pasar: los dos importan estas cuatro funciones, así que **es imposible
que el servidor y el generador respondan cosas distintas**.

Y estas cuatro funciones tampoco interpretan nada: llaman a
`aglaya-ds-mcp/brand.py`, el mismo lector que usa el MCP. Lo que el visor
enseña es exactamente lo que recibe cualquier nave que pregunte.

Sin dependencias: el `python3` del sistema basta, porque `brand.py` tampoco
tiene ninguna.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "aglaya-ds-mcp"))

import brand  # noqa: E402  (después de tocar sys.path, a propósito)


def normas() -> dict:
    """Las normas, tal como las recibe cualquier nave que pregunte."""
    return {
        "no_negociables_madre": brand.get_nonnegotiables(),
        "no_negociables_producto": brand.get_nonnegotiables("product"),
        "voz": brand.get_voice_rules(),
    }


def valores() -> dict:
    """Los tokens en los dos modos. El contraste NO se calcula aquí: lo calcula
    la página con estos mismos valores, para que no haya dos sitios donde un
    número pueda discrepar."""
    return {
        "oscuro": brand.list_tokens(mode="dark"),
        "claro": brand.list_tokens(mode="light"),
    }


def componentes() -> dict:
    fichas = brand.list_components()
    ids = [c["id"] for c in fichas.get("components", fichas.get("items", []))] \
        if isinstance(fichas, dict) else []
    return {"indice": fichas, "fichas": [brand.get_component(i) for i in ids]}


def productos() -> dict:
    lista = brand.list_products()
    ids = [p["id"] for p in lista.get("products", lista.get("items", []))] \
        if isinstance(lista, dict) else []
    return {"indice": lista, "acentos": [brand.get_accent(i) for i in ids]}


# Las cuatro rutas que pide `visor.js`. La página las pide con `r.json()`, que
# NO mira el `Content-Type`: por eso la versión estática puede escribir cuatro
# ficheros sin extensión con estos mismos nombres y el JavaScript no se toca.
def a_json(datos) -> bytes:
    """El ÚNICO serializador del visor. Está aquí por el mismo motivo que las
    cuatro funciones de arriba: si el servidor y el generador eligieran su
    propio `indent` o su propio `ensure_ascii`, dirían lo mismo con bytes
    distintos y la comparación entre los dos dejaría de significar nada."""
    return json.dumps(datos, ensure_ascii=False, indent=1).encode()


RUTAS = {
    "/api/normas": normas,
    "/api/valores": valores,
    "/api/componentes": componentes,
    "/api/productos": productos,
}
