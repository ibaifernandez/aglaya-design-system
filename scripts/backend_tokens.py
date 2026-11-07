#!/usr/bin/env python3
"""backend_tokens.py — el que fabrica el paquete de Python al instalarlo.

QUÉ ES. Un backend PEP 517 que envuelve a setuptools y, ANTES de empaquetar,
deriva los tokens desde `colors_and_type.css` y copia las tipografías con su
licencia. Es el equivalente exacto del `prepare` de npm: `pip install
"git+https://…@vX.Y.Z"` clona, llama aquí, y el consumidor recibe los valores
que había en el canon en ese commit.

POR QUÉ NO SE GUARDAN LOS TOKENS EN EL REPO. Porque serían una segunda casa
para cada valor de marca — lo que `tools/guard_valores.py` persigue y lo que
`dist/` evita del lado de npm. `aglaya_tokens/tokens.py` se escribe aquí, está
en `.gitignore`, y un clon limpio no trae ni un valor duplicado.

Y NO HAY UN PARSER NUEVO. Los tokens los lee `aglaya-ds-mcp/brand.py`, el mismo
lector que usa el MCP y el visor. Esta casa ya se comió la avería de tener dos
intérpretes del mismo documento; un cuarto parser de CSS para el paquete de
Python sería repetirla a sabiendas. Las tipografías las nombra
`tools/fuentes.py`, por el mismo motivo.

La versión tampoco se teclea: sale de `package.json`, que es donde vive la
versión de esta marca. Dos números de versión serían dos verdades.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

# setuptools lo pone pip en el entorno aislado de build; aquí puede no estar,
# y no pasa nada: sin él esto sigue sirviendo para mirar lo derivado a mano
# (`python3 scripts/backend_tokens.py`), que es como se depura un build raro.
try:
    from setuptools import build_meta as _setuptools
    from setuptools.build_meta import *  # noqa: F401,F403  (resto de ganchos PEP 517)
except ImportError:  # pragma: no cover - solo fuera del entorno de build
    _setuptools = None

RAIZ = Path(__file__).resolve().parent.parent
PAQUETE = RAIZ / "aglaya_tokens"


def _version() -> str:
    return json.loads((RAIZ / "package.json").read_text(encoding="utf-8"))["version"]


def _leer_tokens() -> tuple[dict, dict]:
    """Base y modos, por el lector del MCP. Mismo recorte que `dist/`."""
    sys.path.insert(0, str(RAIZ / "aglaya-ds-mcp"))
    import brand  # noqa: E402  (después de tocar sys.path, a propósito)

    base = brand.list_tokens()["tokens"]
    if not base:
        # Un build vacío es peor que un build roto: publica un paquete que
        # resuelve a nada y el consumidor pinta transparente sin ver un error.
        raise SystemExit("backend_tokens: el canon no devolvió ni un token")

    # Lo que cada modo DECLARA, por el mismo parser que todo lo demás. No se
    # calcula aquí comparando valores: un modo puede declarar un token con el
    # mismo valor que `:root` —hoy lo hacen dos tintas, a propósito— y esa
    # comparación los habría perdido, publicando un mapa de 13 donde el paquete
    # de npm publica 15. Medido: la diferencia eran `--fg-on-brand` y
    # `--fg-on-accent`.
    modos = {}
    for modo in ("light",):
        declarados = brand.mode_overrides(modo)
        if not declarados:
            raise SystemExit(f"backend_tokens: el modo '{modo}' no declara nada")
        huerfanos = [k for k in declarados if k not in base]
        if huerfanos:
            # Un nombre que no exista en `:root` sería un token que solo vive en
            # un modo — media marca, y nadie se enteraría.
            raise SystemExit(
                f"backend_tokens: el modo '{modo}' declara tokens que no existen "
                f"en :root: {', '.join(huerfanos)}"
            )
        modos[modo] = declarados
    return base, modos


def _escribir_tokens() -> None:
    base, modos = _leer_tokens()
    version = _version()
    destino = PAQUETE / "tokens.py"
    destino.write_text(
        "# GENERADO por scripts/backend_tokens.py desde colors_and_type.css.\n"
        "# No lo edites: se reescribe en cada instalación y no se versiona.\n"
        f"VERSION = {version!r}\n"
        f"SOURCE = 'colors_and_type.css'\n"
        f"TOKENS = {json.dumps(base, ensure_ascii=False, indent=4)}\n"
        "# Solo lo que cada modo REDEFINE. Modo completo: {**TOKENS, **MODES['light']}.\n"
        f"MODES = {json.dumps(modos, ensure_ascii=False, indent=4)}\n",
        encoding="utf-8",
    )
    print(
        f"backend_tokens: {len(base)} token(s) desde colors_and_type.css "
        f"-> aglaya_tokens/tokens.py (v{version}) · modos "
        f"[{', '.join(f'{n}: {len(t)}' for n, t in modos.items())}]"
    )


def _copiar_fuentes() -> None:
    """Las tipografías que el canon cita, cada familia con su licencia.

    Si falta una licencia NO se construye. Redistribuir una familia sin ella es
    la avería que ya ocurrió cuando este repo se hizo público.
    """
    sys.path.insert(0, str(RAIZ / "tools"))
    from fuentes import familias_de, fuentes_citadas, licencias_que_faltan  # noqa: E402

    css = (RAIZ / "colors_and_type.css").read_text(encoding="utf-8")
    citadas = fuentes_citadas(css)
    if not citadas:
        raise SystemExit("backend_tokens: el CSS canónico no cita ninguna tipografía")

    familias = familias_de(citadas)
    faltan = licencias_que_faltan(familias, RAIZ / "fonts")
    if faltan:
        raise SystemExit(
            "backend_tokens: se entregaría sin licencia: " + ", ".join(faltan)
        )

    destino = PAQUETE / "fonts"
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in citadas:
        origen = RAIZ / "fonts" / nombre
        if not origen.is_file():
            raise SystemExit(f"backend_tokens: el CSS pide {nombre} y no está en fonts/")
        shutil.copyfile(origen, destino / nombre)
    for f in familias:
        shutil.copyfile(RAIZ / "fonts" / f"LICENSE-{f}.txt", destino / f"LICENSE-{f}.txt")
    print(
        f"backend_tokens: {len(citadas)} tipografía(s) de {len(familias)} familia(s) "
        f"({', '.join(familias)}), cada una con su licencia"
    )


def _copiar_css() -> None:
    """El CSS canónico viaja tal cual, como en el paquete de npm: un consumidor
    que sirve una página lo quiere entero, no solo el mapa de valores."""
    shutil.copyfile(RAIZ / "colors_and_type.css", PAQUETE / "colors_and_type.css")


def _derivar() -> None:
    _escribir_tokens()
    _copiar_css()
    _copiar_fuentes()


# ── los ganchos PEP 517 que nos interesa interceptar ────────────────────────
# El resto los hereda del `import *` de arriba. Se interceptan los tres que
# empaquetan: si alguno no derivara, se publicaría un paquete sin valores.

def get_requires_for_build_wheel(config_settings=None):
    # ESTE es el primer gancho que llama pip, antes incluso que los metadatos.
    # setuptools resuelve aquí la versión dinámica leyendo `aglaya_tokens.tokens`,
    # que todavía no existe en un clon limpio — y la instalación moría con un
    # `ModuleNotFoundError` que parecía un paquete roto. Medido: `pip install
    # "git+file://…"` fallaba en «getting requirements to build wheel».
    # Así que se deriva aquí también. Derivar es idempotente: reescribe los
    # mismos ficheros desde el mismo canon.
    _derivar()
    return _setuptools.get_requires_for_build_wheel(config_settings)


def get_requires_for_build_sdist(config_settings=None):
    _derivar()
    return _setuptools.get_requires_for_build_sdist(config_settings)


def get_requires_for_build_editable(config_settings=None):
    _derivar()
    return _setuptools.get_requires_for_build_editable(config_settings)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    # pip pide los metadatos ANTES de construir, y ahí ya hace falta la versión
    # —que vive en el módulo derivado—. Sin este gancho, `pip install` moría
    # antes de llegar a `build_wheel` y parecía un paquete roto.
    _derivar()
    return _setuptools.prepare_metadata_for_build_wheel(
        metadata_directory, config_settings
    )


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    _derivar()
    return _setuptools.prepare_metadata_for_build_editable(
        metadata_directory, config_settings
    )


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _derivar()
    return _setuptools.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    _derivar()
    return _setuptools.build_sdist(sdist_directory, config_settings)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    _derivar()
    return _setuptools.build_editable(wheel_directory, config_settings, metadata_directory)


if __name__ == "__main__":
    # Para mirarlo a mano sin construir nada: `python3 scripts/backend_tokens.py`
    _derivar()
