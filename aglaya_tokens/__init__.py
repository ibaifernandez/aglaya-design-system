"""aglaya_tokens — la marca AGLAYA para un consumidor de Python.

    pip install "git+https://github.com/ibaifernandez/aglaya-design-system@v1.6.0"

Lo mismo que entrega `@aglaya/design-tokens` a quien tiene Node, por la puerta
del otro ecosistema: los valores de marca, los dos modos de color, el CSS
canónico y las tipografías con su licencia.

    from aglaya_tokens import TOKENS, MODES, VERSION, css_path, fonts_path

    TOKENS["--color-brand"]              # el valor del modo por defecto
    {**TOKENS, **MODES["light"]}         # el modo claro, completo
    css_path()                           # el CSS canónico, para servirlo tal cual

EL NOMBRE DEL TOKEN NO SE TRADUCE. La clave es `--color-brand`, no
`color_brand`. Un segundo vocabulario es un segundo sitio donde discrepar, y la
deriva que este paquete existe para cerrar empezó justo así.

LOS VALORES NO ESTÁN EN ESTE FICHERO NI EN NINGÚN OTRO VERSIONADO. Se derivan
de `colors_and_type.css` al instalar, con el mismo lector que usa el MCP. Por
eso un valor movido en el canon llega al consumidor con solo reinstalar, sin
tocar una línea de su código — que es la diferencia entre depender y copiar.
"""

from __future__ import annotations

from pathlib import Path

try:
    from .tokens import MODES, SOURCE, TOKENS, VERSION
except ImportError as e:  # pragma: no cover - solo en un árbol sin construir
    # El mensaje importa: sin él, quien clone el repo y haga `import
    # aglaya_tokens` desde la raíz ve un ImportError pelado y cree que el
    # paquete está roto. No lo está: es que los valores se fabrican al
    # instalar, a propósito.
    raise ImportError(
        "aglaya_tokens.tokens no existe todavía. No es un fallo: los valores de "
        "marca NO se versionan, se derivan de colors_and_type.css al instalar. "
        "Instala el paquete (`pip install .`) o, para mirarlo a mano, corre "
        "`python3 scripts/backend_tokens.py` desde la raíz del repo."
    ) from e

__all__ = [
    "MODES",
    "SOURCE",
    "TOKENS",
    "VERSION",
    "css_path",
    "fonts_path",
    "mode",
]

_AQUI = Path(__file__).resolve().parent


def mode(name: str) -> dict[str, str]:
    """El mapa COMPLETO de un modo: la base con lo que ese modo redefine.

    Se niega ante un modo que no existe en vez de devolver la base, que es lo
    que haría un `.get(name, {})`: un consumidor que pide el modo claro y
    recibe el oscuro sin un error pinta la marca al revés y no se entera.
    """
    if name not in MODES:
        raise KeyError(f"modo desconocido: {name!r}. Hay: {', '.join(sorted(MODES))}")
    return {**TOKENS, **MODES[name]}


def css_path() -> Path:
    """El `colors_and_type.css` canónico que viaja en el paquete."""
    return _AQUI / "colors_and_type.css"


def fonts_path() -> Path:
    """El directorio de tipografías, cada familia con su LICENSE al lado."""
    return _AQUI / "fonts"
