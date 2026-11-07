#!/usr/bin/env python3
"""construir.py — escribe el visor como sitio estático, leyendo el canon.

PARA QUÉ. Para que la marca esté en una dirección pública sin que nadie tenga
que levantar un proceso. Un servidor vivo es algo que mantener, que se cae y
que nadie vigila; una página regenerada en cada empujón a `main` no puede ir
por detrás del canon.

LO QUE NO HACE, y es la regla de esta nave: **no copia el canon a mano a
ninguna parte**. Las cuatro respuestas de `/api/*` las produce `lectores.py`,
que es también lo que sirve `servidor.py`, así que la página publicada y la
local no pueden discrepar — y ninguna de las dos interpreta el canon por su
cuenta: las dos preguntan a `aglaya-ds-mcp/brand.py`, el lector del MCP.

EL DETALLE QUE PERMITE NO TOCAR EL JAVASCRIPT. `visor.js` pide `/api/normas` y
compañía con `r.json()`, que no mira el `Content-Type`. Así que aquí se
escriben cuatro ficheros SIN extensión con exactamente esos nombres, y el
JavaScript se copia tal cual, sin una línea cambiada.

Las tipografías viajan con su licencia al lado, como exige
`tools/guard_paquete.py` para el paquete: no se redistribuye una familia sin
su `LICENSE-<Familia>.txt`. Si falta una, esto se niega a construir.

USO, desde la raíz del repo:

    python3 visor/construir.py              # escribe visor/publico/
    python3 visor/construir.py --salida DIR # o donde se le diga

Sin dependencias: el `python3` del sistema basta.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from fuentes import familias_de, fuentes_citadas, licencias_que_faltan  # noqa: E402
from lectores import RAIZ, RUTAS, a_json  # noqa: E402  (tras tocar sys.path)

AQUI = Path(__file__).resolve().parent
SALIDA_POR_DEFECTO = AQUI / "publico"

# Lo mismo que `servidor.py` entrega como fichero, con la MISMA ruta: el CSS
# canónico en la raíz (porque sus `@font-face` apuntan a `./fonts/`) y los dos
# ficheros propios del visor.
COPIAS = {
    "colors_and_type.css": RAIZ / "colors_and_type.css",
    "visor.css": AQUI / "visor.css",
    "visor.js": AQUI / "visor.js",
    "index.html": AQUI / "index.html",
}

# Qué tipografías pide el canon lo contesta `tools/fuentes.py`, y lo contesta
# para todo el que entregue fuentes —este visor y el paquete de Python—. Dos
# expresiones regulares distintas acabarían entregando listas distintas, y la
# que se quedara corta dejaría una familia sin su licencia sin que nadie lo
# viera. La lista no está escrita en ningún sitio: se lee del CSS.


def construir(salida: Path) -> int:
    if not salida.exists():
        salida.mkdir(parents=True)

    escritos = []

    # 1 · Las cuatro respuestas, por los mismos lectores que el servidor.
    api = salida / "api"
    api.mkdir(exist_ok=True)
    for ruta, lector in RUTAS.items():
        destino = salida / ruta.lstrip("/")
        destino.write_bytes(a_json(lector()))
        escritos.append((destino, destino.stat().st_size))

    # 2 · Los ficheros que el servidor entrega tal cual.
    for nombre, origen in COPIAS.items():
        if not origen.is_file():
            print(f"ERROR: no encuentro {origen}", file=sys.stderr)
            return 1
        destino = salida / nombre
        shutil.copyfile(origen, destino)
        escritos.append((destino, destino.stat().st_size))

    # 3 · Las tipografías que el CSS pide, cada familia con su licencia. Si
    #     falta una licencia NO se construye: redistribuir una familia sin ella
    #     es la avería que ya ocurrió cuando el repo se hizo público.
    css = (RAIZ / "colors_and_type.css").read_text(encoding="utf-8")
    citadas = fuentes_citadas(css)
    if not citadas:
        print("ERROR: el CSS canónico no cita ninguna tipografía", file=sys.stderr)
        return 1

    fuentes = salida / "fonts"
    fuentes.mkdir(exist_ok=True)
    familias = familias_de(citadas)

    faltan = licencias_que_faltan(familias, RAIZ / "fonts")
    if faltan:
        for f in faltan:
            print(f"ERROR: {f} se serviría sin su LICENSE-{f}.txt", file=sys.stderr)
        return 1

    for nombre in citadas:
        origen = RAIZ / "fonts" / nombre
        if not origen.is_file():
            print(f"ERROR: el CSS pide {nombre} y no está en fonts/", file=sys.stderr)
            return 1
        shutil.copyfile(origen, fuentes / nombre)
    for f in familias:
        shutil.copyfile(RAIZ / "fonts" / f"LICENSE-{f}.txt", fuentes / f"LICENSE-{f}.txt")

    print(f"visor estático → {salida}")
    for destino, tam in escritos:
        print(f"  {destino.relative_to(salida)}  {tam} bytes")
    print(f"  fonts/  {len(citadas)} fichero(s) de "
          f"{len(familias)} familia(s): {', '.join(familias)}")
    print(f"  fonts/  {len(familias)} licencia(s) al lado, una por familia")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--salida", type=Path, default=SALIDA_POR_DEFECTO,
                    help="directorio de salida (por defecto visor/publico/)")
    args = ap.parse_args()
    return construir(args.salida.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
