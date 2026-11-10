#!/usr/bin/env python3
"""guard_vias.py — las tres vías entregan LO MISMO, no solo leen lo mismo.

LA PROMESA QUE VIGILA. `docs/CONTRACT.md` dice a toda la flota: «Leer los
mismos archivos no basta: hay que entregar lo mismo. […] Lo que cambia entre
ellas es la forma de preguntar, nunca el contenido». Desde que esta marca se
publica por tres vías —paquete de npm, paquete de Python y MCP—, esa frase es
una obligación sin nadie que la compruebe.

POR QUÉ HACE FALTA, Y NO ES HIPOTÉTICO. Esa avería ya ocurrió con esta misma
promesa: durante un tiempo la frase era verdad en el documento y falsa en los
hechos — el paquete publicaba los dos modos y el MCP solo leía `:root`. Se
arregló y no se le puso guardián. Luego nació una vía más.

CÓMO COMPARA, y aquí está lo fino:

  · **Clave a clave, nunca por recuento.** Dos diccionarios de 92 con un valor
    distinto miden lo mismo. Un guardián que compare `len()` da verde sobre
    una deriva de valor, que es justo la que duele.
  · **Lo DECLARADO, no lo que cambia.** El modo claro declara dos tintas con el
    mismo valor que `:root` a propósito (`colors_and_type.css`, «Las tintas
    sobre relleno NO giran»). Un guardián que compare «qué cambia» discrepa
    justo ahí y llama defecto a una decisión.
  · **Los dos modos**, porque la avería histórica fue exactamente de modo.

LA REGLA QUE ESTE GUARDIÁN APLICA Y QUE NO ESTABA ESCRITA EN NINGÚN SITIO:

  **Para afirmar sobre un modo se lee lo DECLARADO (`MODES[modo]`), nunca lo
  RESUELTO (`mode(modo)`).**

La vista resuelta hereda del base cuando el modo no redefine, así que hace que
«no está» parezca «está». Sirve para pintar; no sirve para afirmar.

Y de ahí lo que de verdad hay que recordar: **una tabla por modos tiene TRES
estados, no dos** — redefine · hereda · no existe. Una salida que solo
distingue dos acierta en unos tokens por casualidad, porque el bloque claro
repite a propósito tintas que no giran: «hereda» y «redefine con el mismo
valor» se leen igual y no son lo mismo.

EL CASO QUE LO DESTAPÓ, medido al publicar `v1.7.0`. Un acta imprimía el
acento de un producto en una columna «light» con el valor del base, que se lee
como declarado en claro, y la condición de cierre exigía que NO lo estuviera:

    '<acento de producto>' in MODES['light']  → False     ← lo declarado
    mode('light')['<acento de producto>']     → el de :root  ← lo que se imprimió
    '<color de estado>'    in MODES['light']  → True      ← control, sí gira

(Sin los valores a propósito: una regla que lleva su hexadecimal dentro deja de
ser verdad el día que ese valor se mueve, y los nombres concretos los sirve
`list_tokens`. Aquí vale la forma del fallo, no la fila.)

El dato era correcto; la presentación decía lo contrario. Se escribe aquí
—y no en el canon— porque es una regla sobre **cómo se afirma**, no sobre la
marca. Y porque **ningún guardián la puede sustituir**: si el CSS declarara ese
acento en claro, las tres vías lo servirían igual y este guardián daría verde.
El único freno es que quien escribe lo sepa.

NO LLEVA NI UN VALOR NI UN CONTEO DENTRO. Lee el canon en vivo por las tres
puertas y compara lo que salga: un token nuevo mañana entra sin tocar esto.

Y NO DA VERDE SIN MIRAR. Si falta Node, si una vía no se puede leer o si
alguna devuelve vacío, sale con 2 —«no se pudo comprobar»—, nunca con 0. Un
guardián de igualdad que no encuentra qué comparar da el verde más falso que
hay.

Uso:  python3 tools/guard_vias.py
Sale: 0 las tres coinciden · 1 discrepan · 2 no se pudo comprobar.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Los modos que se comparan salen del canon, no de aquí: esta lista se rellena
# preguntando al lector del MCP cuáles hay.
MODO_BASE = "base"   # etiqueta interna de `:root`, para los mensajes


class NoSePudo(Exception):
    """No se pudo leer una vía. Sale con 2, nunca con 0."""


# ── las tres puertas ────────────────────────────────────────────────────────
def via_mcp() -> tuple[dict, dict]:
    """Lo que el MCP sirve a la flota: base y lo que declara cada modo."""
    sys.path.insert(0, str(RAIZ / "aglaya-ds-mcp"))
    try:
        import brand
    except Exception as e:
        raise NoSePudo(f"no pude importar aglaya-ds-mcp/brand.py: {e}") from e
    try:
        base = brand.list_tokens()["tokens"]
        modos = {m: brand.mode_overrides(m) for m in brand._MODOS
                 if m != brand._MODO_POR_DEFECTO}
    except Exception as e:
        raise NoSePudo(f"brand.py no contestó: {e}") from e
    return base, modos


def via_python() -> tuple[dict, dict]:
    """Lo que el paquete de Python escribirá en `aglaya_tokens/tokens.py`.

    Se le pregunta a la función que lo fabrica, no al fichero: así esto mide lo
    que se va a publicar aunque nadie haya instalado nada en este disco.
    """
    sys.path.insert(0, str(RAIZ / "scripts"))
    try:
        import backend_tokens
        return backend_tokens._leer_tokens()
    except SystemExit as e:        # el backend se niega a derivar
        raise NoSePudo(f"el backend de Python se negó: {e}") from e
    except Exception as e:
        raise NoSePudo(f"no pude derivar la vía de Python: {e}") from e


def via_npm() -> tuple[dict, dict]:
    """Lo que el paquete de npm publica en `dist/tokens.json`.

    Se construye en un temporal: este guardián no ensucia `dist/`, que es del
    build de verdad.
    """
    guion = RAIZ / "scripts" / "build-tokens.mjs"
    if not guion.is_file():
        raise NoSePudo(f"no encuentro {guion.relative_to(RAIZ)}")
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "dist"
        try:
            subprocess.run(
                ["node", str(guion), str(destino)], cwd=RAIZ,
                capture_output=True, text=True, check=True,
            )
        except FileNotFoundError as e:
            raise NoSePudo("no hay node en esta máquina") from e
        except subprocess.CalledProcessError as e:
            raise NoSePudo(f"build-tokens falló: {e.stderr.strip()[:200]}") from e
        fichero = destino / "tokens.json"
        if not fichero.is_file():
            raise NoSePudo("build-tokens no escribió tokens.json donde se le dijo")
        datos = json.loads(fichero.read_text(encoding="utf-8"))
    return datos.get("tokens") or {}, datos.get("modes") or {}


VIAS = {
    "MCP": via_mcp,
    "paquete de Python": via_python,
    "paquete de npm": via_npm,
}


# ── la comparación ──────────────────────────────────────────────────────────
def diferencias(ref: dict, otra: dict) -> list[str]:
    """Clave a clave. Nunca por recuento: dos mapas del mismo tamaño pueden
    discrepar en un valor y eso es exactamente lo que duele."""
    fallos = []
    for nombre in sorted(set(ref) | set(otra)):
        if nombre not in otra:
            fallos.append(f"falta {nombre}")
        elif nombre not in ref:
            fallos.append(f"sobra {nombre}")
        elif ref[nombre] != otra[nombre]:
            fallos.append(f"{nombre}: {ref[nombre]!r} vs {otra[nombre]!r}")
    return fallos


def revisar(lecturas: dict[str, tuple[dict, dict]]) -> list[tuple[str, str]]:
    referencia, (base_ref, modos_ref) = next(iter(lecturas.items()))
    fallos: list[tuple[str, str]] = []

    for nombre, (base, modos) in list(lecturas.items())[1:]:
        for d in diferencias(base_ref, base):
            fallos.append((MODO_BASE, f"{referencia} vs {nombre} — {d}"))
        for modo in sorted(set(modos_ref) | set(modos)):
            if modo not in modos:
                fallos.append((modo, f"{nombre} no entrega el modo {modo!r}"))
            elif modo not in modos_ref:
                fallos.append((modo, f"{referencia} no entrega el modo {modo!r}"))
            else:
                for d in diferencias(modos_ref[modo], modos[modo]):
                    fallos.append((modo, f"{referencia} vs {nombre} — {d}"))
    return fallos


def main() -> int:
    lecturas: dict[str, tuple[dict, dict]] = {}
    for nombre, puerta in VIAS.items():
        try:
            base, modos = puerta()
        except NoSePudo as e:
            print(f"guard-vias: NO SE PUDO COMPROBAR — {nombre}: {e}")
            return 2
        if not base:
            print(f"guard-vias: NO SE PUDO COMPROBAR — {nombre} entregó cero "
                  "tokens; comparar contra el vacío daría verde por no mirar")
            return 2
        if not modos:
            print(f"guard-vias: NO SE PUDO COMPROBAR — {nombre} no entregó "
                  "ningún modo; la avería histórica fue exactamente de modo")
            return 2
        lecturas[nombre] = (base, modos)

    if len(lecturas) < 2:
        print("guard-vias: NO SE PUDO COMPROBAR — hace falta más de una vía")
        return 2

    fallos = revisar(lecturas)
    if not fallos:
        primera = next(iter(lecturas.values()))
        modos = ", ".join(f"{m}: {len(t)}" for m, t in sorted(primera[1].items()))
        print(f"guard-vias: OK — {len(lecturas)} vías ({', '.join(lecturas)}) "
              f"entregan lo mismo, clave a clave: {len(primera[0])} token(s) "
              f"de base y los modos [{modos}].")
        return 0

    print(f"guard-vias: {len(fallos)} discrepancia(s) — las vías dejaron de "
          "entregar lo mismo\n")
    for modo, explicacion in fallos:
        print(f"  [{modo}] {explicacion}")
    print("\nLa promesa de docs/CONTRACT.md es que lo que cambia entre vías es "
          "la forma de preguntar, nunca el contenido.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
