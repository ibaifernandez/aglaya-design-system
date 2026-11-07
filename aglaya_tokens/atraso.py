#!/usr/bin/env python3
"""Imprime cuántas versiones por detrás va el consumidor.

Es el hermano de `bin/aglaya-tokens-version.mjs`, para el consumidor que no
tiene Node. Misma pregunta, mismas salidas, mismos códigos de retorno — un
consumidor de Python no se queda sin el aviso solo por hablar otro idioma.

    aglaya-tokens-version            → humano
    aglaya-tokens-version --json     → para un paso de CI
    aglaya-tokens-version --strict   → sale 1 si va por detrás (gate de CI)

Salidas: 0 al día (o atrasado sin --strict) · 1 atrasado con --strict
         · 2 no se pudo comprobar (sin git, sin red, sin tags).

El 2 importa: «no pude mirar» NUNCA se imprime como «estás al día». Ese es el
verde vacío que desactiva una comprobación el primer día que falla la red.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# De dónde se pregunta. Es la misma URL que declara `repository.url` del
# paquete de npm, y se escribe aquí porque el paquete instalado NO lleva el
# `package.json` del repo dentro: lo que viaja es este módulo.
REMOTO = "https://github.com/ibaifernandez/aglaya-design-system.git"

# Solo se comparan versiones de release. Un tag con pre-release (`v2.0.0-rc.1`)
# se ignora a propósito: publicar un candidato no deja atrasado a nadie.
SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def _parse(s: str):
    m = SEMVER.match(s.strip())
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def _fmt(v) -> str:
    return ".".join(str(x) for x in v)


def _salir(codigo: int, humano: str, datos: dict, como_json: bool):
    print(json.dumps(datos, ensure_ascii=False, indent=2) if como_json else humano)
    raise SystemExit(codigo)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="salida para un paso de CI")
    ap.add_argument("--strict", action="store_true", help="sale 1 si va por detrás")
    args = ap.parse_args(argv)

    def fallo(mensaje: str, **extra):
        _salir(
            2,
            f"aglaya-tokens-version: no se pudo comprobar — {mensaje}",
            {"ok": False, "error": mensaje, **extra},
            args.json,
        )

    try:
        from . import VERSION
    except ImportError as e:
        return fallo(f"el paquete no trae versión: {e}")

    instalada = _parse(VERSION)
    if not instalada:
        return fallo(f"la versión instalada no es semver: {VERSION}")

    try:
        salida = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", REMOTO],
            capture_output=True, text=True, timeout=20, check=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        ).stdout
    except FileNotFoundError:
        return fallo("no hay git en esta máquina", remote=REMOTO)
    except subprocess.TimeoutExpired:
        return fallo(f"git ls-remote tardó demasiado sobre {REMOTO}", remote=REMOTO)
    except subprocess.CalledProcessError as e:
        return fallo(
            f"git ls-remote falló sobre {REMOTO} ({e.returncode})", remote=REMOTO
        )

    publicadas = sorted(
        v for v in (
            _parse(l.split("refs/tags/")[1]) for l in salida.splitlines()
            if "refs/tags/" in l
        ) if v
    )
    if not publicadas:
        return fallo(f"el remoto no publica ningún tag de versión: {REMOTO}", remote=REMOTO)

    ultima = publicadas[-1]
    detras = [v for v in publicadas if v > instalada]
    # Un mayor por delante no es «vas dos versiones tarde»: es «te van a romper
    # nombres de token». Se dice aparte porque la acción es distinta.
    mayor_por_delante = any(v[0] > instalada[0] for v in detras)

    datos = {
        "ok": True,
        "package": "aglaya-design-tokens",
        "installed": _fmt(instalada),
        "latest": _fmt(ultima),
        "behind": len(detras),
        "behindVersions": [_fmt(v) for v in detras],
        "majorAhead": mayor_por_delante,
        "remote": REMOTO,
    }

    if not detras:
        adelantada = instalada > ultima
        _salir(
            0,
            f"aglaya-design-tokens {_fmt(instalada)} — por delante del último tag "
            f"publicado ({_fmt(ultima)}). Estás sobre una rama sin taggear."
            if adelantada else
            f"aglaya-design-tokens {_fmt(instalada)} — al día "
            f"(último publicado: {_fmt(ultima)}).",
            {**datos, "ahead": adelantada},
            args.json,
        )

    lineas = [
        f"aglaya-design-tokens {_fmt(instalada)} — {len(detras)} versión(es) por detrás.",
        f"  último publicado: {_fmt(ultima)}",
        f"  te faltan:        {', '.join(_fmt(v) for v in detras)}",
    ]
    if mayor_por_delante:
        lineas += [
            "  AVISO: hay un MAYOR por delante — algún token cambió de nombre o desapareció.",
            "         Lee docs/PACKAGE.md del repo antes de subir; el build puede romperse.",
        ]
    _salir(1 if args.strict else 0, "\n".join(lineas), datos, args.json)


if __name__ == "__main__":
    sys.exit(main())
