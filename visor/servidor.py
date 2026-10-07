#!/usr/bin/env python3
"""servidor.py — sirve el visor de marca. Lee; no escribe nada, nunca.

PARA QUÉ. Para tener la marca delante: las normas primero, los valores después.
No es documentación de la marca: es **una ventana a la fuente**.

LA REGLA QUE DECIDE TODO LO DEMÁS. Aquí no hay ni un dato de marca. Las normas
y los tokens salen de `aglaya-ds-mcp/brand.py`, **el mismo lector que usa el
MCP**, así que lo que esta página enseña es exactamente lo que recibe cualquier
nave que pregunte — no «las normas según la web». Y el CSS canónico se sirve
tal cual, sin copiarlo: los colores que se ven en pantalla los pinta el propio
`colors_and_type.css`.

Si algún día esto necesitara interpretar un fichero del canon por su cuenta,
**no se hace**: sería el segundo intérprete del mismo documento, que es la
avería que esta casa ya se ha comido varias veces (el kit con su `:root`
propio, las muestras con los hex tecleados, el docstring que contaba colores).

QUÉ NO HACE, y es tan importante como lo que hace:

  · No escribe. Ni un fichero, ni una línea.
  · No ejecuta guardianes ni baterías. Un visor lee; un panel que ejecuta es
    otra cosa y otra decisión, y está dicho que no.
  · No viaja en el paquete. `files` de `package.json` no lo incluye y no se
    toca: esto es herramienta de casa, no marca entregada.
  · No sustituye a `preview/`. Las muestras siguen donde están.

CÓMO SE ARRANCA, desde la raíz del repo:

    python3 visor/servidor.py

Sin dependencias: el `python3` del sistema basta, porque `brand.py` tampoco
tiene ninguna. Imprime la dirección y se queda esperando. Se corta con Ctrl-C.
"""

from __future__ import annotations

import http.server
import json
import mimetypes
import socketserver
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "aglaya-ds-mcp"))

import brand  # noqa: E402  (después de tocar sys.path, a propósito)

PUERTO = 8788

# Lo único del repo que el visor sirve como fichero. Todo lo demás pasa por
# `brand.py`. La lista es explícita para que nadie convierta esto en un
# servidor de ficheros del repo entero.
ESTATICOS = {
    "/colors_and_type.css": RAIZ / "colors_and_type.css",
    "/visor.css": Path(__file__).resolve().parent / "visor.css",
    "/visor.js": Path(__file__).resolve().parent / "visor.js",
}


def _normas() -> dict:
    """Las normas, tal como las recibe cualquier nave que pregunte."""
    return {
        "no_negociables_madre": brand.get_nonnegotiables(),
        "no_negociables_producto": brand.get_nonnegotiables("product"),
        "voz": brand.get_voice_rules(),
    }


def _valores() -> dict:
    """Los tokens en los dos modos. El contraste NO se calcula aquí: lo calcula
    la página con estos mismos valores, para que no haya dos sitios donde un
    número pueda discrepar."""
    return {
        "oscuro": brand.list_tokens(mode="dark"),
        "claro": brand.list_tokens(mode="light"),
    }


def _componentes() -> dict:
    fichas = brand.list_components()
    ids = [c["id"] for c in fichas.get("components", fichas.get("items", []))] \
        if isinstance(fichas, dict) else []
    return {"indice": fichas, "fichas": [brand.get_component(i) for i in ids]}


def _productos() -> dict:
    lista = brand.list_products()
    ids = [p["id"] for p in lista.get("products", lista.get("items", []))] \
        if isinstance(lista, dict) else []
    return {"indice": lista, "acentos": [brand.get_accent(i) for i in ids]}


RUTAS = {
    "/api/normas": _normas,
    "/api/valores": _valores,
    "/api/componentes": _componentes,
    "/api/productos": _productos,
}


class Visor(http.server.BaseHTTPRequestHandler):
    def _responde(self, codigo: int, cuerpo: bytes, tipo: str) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Sin caché: el visor existe para enseñar lo que hay AHORA. Una página
        # cacheada enseñando el canon de hace diez minutos sería exactamente la
        # copia que esto viene a evitar.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self) -> None:  # noqa: N802  (lo exige la clase base)
        ruta = self.path.split("?")[0]

        if ruta in RUTAS:
            try:
                datos = RUTAS[ruta]()
            except Exception as e:  # el canon roto se enseña, no se esconde
                cuerpo = json.dumps(
                    {"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False
                ).encode()
                return self._responde(500, cuerpo, "application/json; charset=utf-8")
            cuerpo = json.dumps(datos, ensure_ascii=False, indent=1).encode()
            return self._responde(200, cuerpo, "application/json; charset=utf-8")

        if ruta in ESTATICOS and ESTATICOS[ruta].is_file():
            tipo = mimetypes.guess_type(str(ESTATICOS[ruta]))[0] or "text/plain"
            return self._responde(
                200, ESTATICOS[ruta].read_bytes(), f"{tipo}; charset=utf-8"
            )

        if ruta.startswith("/fonts/"):
            # Las tipografías, para que lo que se ve sea la letra de la marca y
            # no la que tenga el sistema. Se resuelve y se comprueba que no sale
            # de fonts/: un visor no es una puerta al disco.
            archivo = (RAIZ / ruta.lstrip("/")).resolve()
            if archivo.is_file() and (RAIZ / "fonts").resolve() in archivo.parents:
                tipo = mimetypes.guess_type(str(archivo))[0] or "font/ttf"
                return self._responde(200, archivo.read_bytes(), tipo)

        if ruta in ("/", "/index.html"):
            pagina = Path(__file__).resolve().parent / "index.html"
            return self._responde(
                200, pagina.read_bytes(), "text/html; charset=utf-8"
            )

        self._responde(404, b"no existe", "text/plain; charset=utf-8")

    def log_message(self, *_args) -> None:
        pass  # sin ruido: lo que importa sale por pantalla una vez, al arrancar


def main() -> int:
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PUERTO), Visor) as servidor:
        print(f"visor de marca — http://127.0.0.1:{PUERTO}")
        print("lee el canon en cada petición; recarga la página y verás el cambio.")
        print("Ctrl-C para parar.")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nparado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
