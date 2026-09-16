#!/usr/bin/env python3
"""Lee una cifra pública de la salida de un comando de CI.

Contrato `cifras-publicas` v1: cada valor sale de la salida de un comando DE LA
MISMA EJECUCIÓN, nunca tecleado. Los jobs que miden guardan su salida y este
lector saca de ella el número.

    medir_cifras.py tokens       <salida de node scripts/build-tokens.mjs>
    medir_cifras.py herramientas <salida de aglaya-ds-mcp/selftest.py>
    medir_cifras.py llamadas     <salida de aglaya-ds-mcp/selftest.py>
    medir_cifras.py contestan    <salida de aglaya-ds-mcp/selftest.py>
    medir_cifras.py niegan       <salida de aglaya-ds-mcp/selftest.py>
    medir_cifras.py sabotajes    <salida de aglaya-ds-mcp/test_selftest.sh>

TOLERANTE A PROPÓSITO: si no encuentra lo que busca imprime VACÍO y sale 0. Un
cambio de formato no debe poner rojos los jobs que miden en cada PR. Quien
decide si la cifra vale es `publicar_cifras.sh`, que es ESTRICTO y no publica un
vacío ni un 0.

Stdlib pura: corre con el python del runner sin instalar nada.
"""

import ast
import re
import sys
from pathlib import Path


def tokens(texto: str) -> str:
    m = re.findall(r"build-tokens: (\d+) token\(s\)", texto)
    return m[-1] if m else ""


def herramientas(texto: str) -> str:
    # La línea que sigue a «== TOOLS REGISTERED ==» es la lista que devuelve el
    # propio servidor. Se cuenta la lista, no se busca un número escrito.
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if linea.strip() == "== TOOLS REGISTERED ==" and i + 1 < len(lineas):
            try:
                lista = ast.literal_eval(lineas[i + 1].strip())
            except (ValueError, SyntaxError):
                return ""
            if isinstance(lista, list) and all(isinstance(x, str) for x in lista):
                return str(len(set(lista)))
    return ""


def llamadas(texto: str) -> str:
    # Solo cuenta si el selftest salió en VERDE: esa línea no existe en un rojo.
    m = re.findall(r"^SELFTEST: (\d+) llamadas, todas con el veredicto esperado", texto, re.M)
    return m[-1] if m else ""


def _veredictos(texto: str, marca: str) -> str:
    # Cada llamada del selftest imprime `== [ok] …` si debía contestar y
    # `== [rechaza] …` si debía negarse. Las cabeceras `[contenido]` y `[canon]`
    # también empiezan por `== [`, pero NO son llamadas: por eso se exige la
    # marca exacta seguida de espacio. Y solo cuenta un selftest en VERDE: en un
    # rojo aparecen `[FALLO]` y la cifra no vale.
    if not llamadas(texto):
        return ""
    return str(len(re.findall(rf"^== \[{marca}\] ", texto, re.M)))


def contestan(texto: str) -> str:
    return _veredictos(texto, "ok")


def niegan(texto: str) -> str:
    return _veredictos(texto, "rechaza")


def sabotajes(texto: str) -> str:
    # test_selftest.sh no imprime un total, así que se cuentan las líneas. Y
    # solo si la batería terminó sin escapes: con un escape, la cifra no vale.
    if "SABOTAJE: todo mordió (0 escapes)" not in texto:
        return ""
    return str(len(re.findall(r"^\s*ROJO  ok\b", texto, re.M)))


LECTORES = {"tokens": tokens, "herramientas": herramientas,
            "llamadas": llamadas, "contestan": contestan, "niegan": niegan,
            "sabotajes": sabotajes}


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in LECTORES:
        print(__doc__, file=sys.stderr)
        return 2
    texto = Path(argv[2]).read_text(encoding="utf-8", errors="replace")
    print(LECTORES[argv[1]](texto))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
