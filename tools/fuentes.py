#!/usr/bin/env python3
"""fuentes.py — qué tipografías pide el canon, y con qué licencia viajan.

POR QUÉ ESTÁ AQUÍ Y NO DENTRO DE QUIEN LO USA. Dos cosas entregan hoy las
tipografías de la marca: el visor estático (`visor/construir.py`) y el paquete
de Python (`scripts/backend_tokens.py`). Si cada una se escribiera su propia
expresión regular, un día entregarían listas distintas — y la que se quedara
corta dejaría una familia sin su licencia sin que nadie lo notara.

La lista NO está escrita aquí: se lee del CSS canónico. Una familia nueva entra
sola el día que el canon la cite, y entra con su licencia exigida.

Sin dependencias: `python3` del sistema y nada más.
"""

from __future__ import annotations

import re
from pathlib import Path

# `./fonts/Outfit-Bold.ttf` dentro de un `url(...)` del CSS canónico.
_FUENTE = re.compile(r"\./fonts/([A-Za-z0-9][A-Za-z0-9._-]*\.(?:ttf|otf|woff2?))")


def fuentes_citadas(css: str) -> list[str]:
    """Los ficheros de tipografía que el CSS canónico pide, sin repetir."""
    return sorted(set(_FUENTE.findall(css)))


def familia_de(nombre: str) -> str:
    """Una tipografía la nombra su fichero: `Outfit-Bold.ttf` es de Outfit."""
    return nombre.split("-", 1)[0].split(".", 1)[0]


def familias_de(nombres: list[str]) -> list[str]:
    return sorted({familia_de(n) for n in nombres})


def licencias_que_faltan(familias: list[str], dir_fuentes: Path) -> list[str]:
    """Las familias que se redistribuirían SIN su `LICENSE-<Familia>.txt`.

    Quien llama decide qué hacer, pero la respuesta correcta es siempre la
    misma: negarse a entregar. Esa avería ya ocurrió — el repo se hizo público
    y el paquete llevaba las tres familias sin licencia.
    """
    return [f for f in familias if not (dir_fuentes / f"LICENSE-{f}.txt").is_file()]
