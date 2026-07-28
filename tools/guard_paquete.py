#!/usr/bin/env python3
"""Guardián del paquete publicado.

La avería que persigue: que el paquete deje de ser instalable **desde fuera de
esta máquina**. Es un fallo silencioso por naturaleza — todo funciona en el
disco donde se escribió y solo se rompe en el CI de otro, que clona su repo y
no el nuestro. Un `file:../aglaya-design-system` pasa cualquier prueba local y
tumba el build del consumidor en Netlify.

Cuatro formas de romperlo, las cuatro vigiladas:

1. **ruta-local** — una dependencia (o un objetivo de `exports`/`files`/`bin`)
   que apunta a este disco: `file:`, `link:`, `workspace:`, `portal:`, o un
   `../` que se sale de la raíz del paquete. Funciona aquí, no existe allí.

2. **remoto-inalcanzable** — `repository.url` en SSH (`git@github.com:...`).
   Un CI ajeno no tiene llaves: no puede instalar ni preguntar qué versión hay
   publicada. Y sin esa pregunta se acabó la ventaja de depender.

3. **objetivo-ausente** — algo declarado en `exports`, `files` o `bin` que no
   existe. npm no falla al empaquetar: entrega el paquete sin ese archivo y el
   consumidor descubre el hueco en su build.

4. **copia-rastreada** — `dist/` versionado. Ese directorio lleva los 87
   valores de marca derivados del CSS; commitearlo abre una segunda casa para
   cada uno, que es exactamente lo que `guard_valores.py` persigue dentro del
   repo y lo que este paquete existe para cerrar fuera. Se genera al instalar
   o no se genera.

Y dos más que no son del paquete sino de su honestidad:

**El CSS que exporta tiene que ser el canónico**, no una copia con otro nombre.
Si algún día `./tokens.css` deja de apuntar a `colors_and_type.css`, el paquete
puede publicar valores que el MCP no sirve, y ahí ya hay dos fuentes de la
verdad con la misma cara.

**Ninguna tipografía se redistribuye sin su licencia al lado.** Las tres
familias de `fonts/` son de terceros bajo OFL 1.1, que exige que la licencia y
el aviso de copyright viajen con los archivos. Este repo se hizo público y el
paquete las redistribuyó sin ese archivo: la avería ya ocurrió. Aquí se empareja
cada archivo de fuente con un `LICENSE-<Familia>.txt` en su mismo directorio, de
modo que una cuarta familia sin licencia pone el CI rojo antes de llegar a
nadie. Emparejar por nombre —no por una lista de familias escrita dentro— es lo
que hace que proteja también a la familia que aún no existe.

**No lleva ni un valor de marca dentro**, como el resto de guardianes: lee el
manifiesto en cada ejecución.

Sin dependencias: stdlib.

Uso:  python3 tools/guard_paquete.py
Sale: 0 limpio · 1 el paquete no sobrevive a un clon ajeno · 2 no se pudo comprobar.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PKG = RAIZ / "package.json"
CSS_CANONICO = "colors_and_type.css"
FUENTES = RAIZ / "fonts"

# Lo que cuenta como «font software» a efectos del OFL.
EXT_FUENTE = {".otf", ".ttf", ".woff", ".woff2", ".ttc", ".otc"}

# Directorios que el paquete fabrica al instalar y que por tanto NO tienen que
# existir en un clon limpio. Cualquier otro objetivo declarado sí.
CONSTRUIDOS = ("dist/",)

# Prefijos de especificador que atan una dependencia a este disco.
PROTOCOLOS_LOCALES = ("file:", "link:", "workspace:", "portal:")

BLOQUES_DEPS = (
    "dependencies",
    "devDependencies",
    "peerDependencies",
    "optionalDependencies",
    "overrides",
    "resolutions",
)


def manifiesto() -> dict | None:
    """El package.json, leído en vivo. None si no se puede leer."""
    if not PKG.is_file():
        return None
    try:
        return json.loads(PKG.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def rastreados() -> list[str] | None:
    """Rutas versionadas, según git. None si git no contesta."""
    try:
        salida = subprocess.run(
            ["git", "-C", str(RAIZ), "ls-files"],
            capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [l for l in salida.stdout.splitlines() if l]


def fuentes() -> list[Path] | None:
    """Los archivos de fuente que el paquete redistribuye.

    None si el directorio no existe — el paquete no entrega tipografías y la
    regla no aplica. Lista vacía significa otra cosa muy distinta (el
    directorio está pero no se ve nada dentro) y arriba se trata como
    «no se pudo comprobar»: un guardián de licencias que no encuentra fuentes
    da el verde más tranquilizador y más falso que hay.
    """
    if not FUENTES.is_dir():
        return None
    return sorted(p for p in FUENTES.iterdir()
                  if p.is_file() and p.suffix.lower() in EXT_FUENTE)


def _familia(archivo: Path) -> str:
    """`Inter-BoldItalic.otf` -> `Inter`. El nombre antes del primer guion."""
    return archivo.stem.split("-")[0]


def _es_construido(destino: str) -> bool:
    limpio = destino.lstrip("./")
    return any(limpio.startswith(d) for d in CONSTRUIDOS)


def _objetivos(pkg: dict) -> list[tuple[str, str]]:
    """(dónde se declara, ruta) para todo lo que el paquete promete entregar."""
    fuera: list[tuple[str, str]] = []

    def exportar(nodo, camino):
        if isinstance(nodo, str):
            fuera.append((camino, nodo))
        elif isinstance(nodo, dict):
            for k, v in nodo.items():
                exportar(v, f"{camino}[{k}]")

    exportar(pkg.get("exports", {}), "exports")
    for ruta in pkg.get("files", []):
        fuera.append(("files", ruta))
    binarios = pkg.get("bin", {})
    if isinstance(binarios, str):
        fuera.append(("bin", binarios))
    else:
        for k, v in binarios.items():
            fuera.append((f"bin[{k}]", v))
    return fuera


def revisar(pkg: dict, versionados: list[str], tipografias: list[Path] | None) -> list[tuple[str, str]]:
    """[(regla, explicación)] — vacío si el paquete sobrevive a un clon ajeno."""
    fallos: list[tuple[str, str]] = []

    # 0 · ninguna tipografía se redistribuye sin su licencia al lado.
    # Se agrupa por familia: una familia sin licencia son sus 18 archivos, y
    # 18 líneas iguales esconden el problema en vez de enseñarlo.
    huerfanas: dict[str, list[Path]] = {}
    for archivo in tipografias or []:
        familia = _familia(archivo)
        if not (archivo.parent / f"LICENSE-{familia}.txt").is_file():
            huerfanas.setdefault(familia, []).append(archivo)
    for familia, archivos in huerfanas.items():
        fallos.append((
            "fuente-sin-licencia",
            f"la familia {familia!r} se redistribuye ({len(archivos)} archivo/s, "
            f"p. ej. {archivos[0].relative_to(RAIZ)}) y falta "
            f"fonts/LICENSE-{familia}.txt — el OFL exige que la licencia y el "
            "aviso de copyright viajen con los archivos",
        ))

    # 1 · ninguna dependencia atada a este disco
    for bloque in BLOQUES_DEPS:
        for nombre, spec in (pkg.get(bloque) or {}).items():
            if not isinstance(spec, str):
                continue
            if spec.startswith(PROTOCOLOS_LOCALES) or spec.startswith((".", "/", "~")):
                fallos.append((
                    "ruta-local",
                    f"{bloque}.{nombre} = {spec!r} — apunta a este disco; "
                    f"el CI del consumidor clona solo su repo y no lo encontrará",
                ))

    # 2 · el remoto tiene que poder consultarse sin llaves
    url = (pkg.get("repository") or {}).get("url", "")
    if not url:
        fallos.append((
            "remoto-inalcanzable",
            "repository.url está vacío — sin él, el consumidor no puede "
            "instalar por git+https ni preguntar cuántas versiones va por detrás",
        ))
    elif not url.replace("git+", "", 1).startswith("https://"):
        fallos.append((
            "remoto-inalcanzable",
            f"repository.url = {url!r} no es https — un CI ajeno no tiene "
            "llaves SSH y fallará al clonar",
        ))

    # 3 · lo declarado existe (o lo fabrica el build)
    for donde, destino in _objetivos(pkg):
        if _es_construido(destino):
            continue
        if ".." in Path(destino).parts:
            fallos.append((
                "ruta-local",
                f"{donde} = {destino!r} se sale de la raíz del paquete; "
                "fuera del tarball eso no existe",
            ))
            continue
        # Un objetivo puede ser un glob (`./fonts/*`): basta con que exista el
        # directorio que lo contiene, no cada archivo.
        ruta = RAIZ / destino.lstrip("./").split("*")[0].rstrip("/")
        if not ruta.exists():
            fallos.append((
                "objetivo-ausente",
                f"{donde} = {destino!r} no existe en el repo — npm empaqueta "
                "sin él y el hueco aparece en el build del consumidor",
            ))

    # 4 · los binarios tienen que poder ejecutarse
    binarios = pkg.get("bin", {})
    binarios = {"": binarios} if isinstance(binarios, str) else binarios
    for nombre, destino in binarios.items():
        ruta = RAIZ / destino.lstrip("./")
        if ruta.is_file() and not os.access(ruta, os.X_OK):
            fallos.append((
                "objetivo-ausente",
                f"bin[{nombre}] = {destino!r} existe pero no es ejecutable",
            ))

    # 5 · el build declarado es el que fabrica lo construido
    prepare = (pkg.get("scripts") or {}).get("prepare", "")
    if not prepare:
        fallos.append((
            "sin-build",
            "no hay scripts.prepare — npm no fabricará dist/ al instalar desde "
            "git y el paquete llegará sin sus formas JS/JSON",
        ))

    # 6 · lo construido no se versiona
    for ruta in versionados:
        if _es_construido(ruta):
            fallos.append((
                "copia-rastreada",
                f"{ruta} está versionado — es un derivado del CSS canónico y "
                "commitearlo abre una segunda casa para cada valor de marca",
            ))

    # 7 · el CSS exportado es el canónico, no una copia
    destino_css = (pkg.get("exports") or {}).get("./tokens.css")
    if destino_css is None:
        fallos.append((
            "css-no-canonico",
            "exports no expone './tokens.css' — es la única vía de consumo que "
            "no necesita build; sin ella el paquete depende de que corran los scripts",
        ))
    elif destino_css.lstrip("./") != CSS_CANONICO:
        fallos.append((
            "css-no-canonico",
            f"exports['./tokens.css'] = {destino_css!r} y no {CSS_CANONICO!r} — "
            "el paquete estaría publicando una copia con otra cara",
        ))

    return fallos


def main() -> int:
    pkg = manifiesto()
    if pkg is None:
        print("guard-paquete: NO SE PUDO COMPROBAR — package.json ausente o ilegible")
        return 2

    versionados = rastreados()
    if versionados is None:
        print("guard-paquete: NO SE PUDO COMPROBAR — git no contestó `ls-files`")
        return 2

    tipografias = fuentes()
    if tipografias is not None and not tipografias:
        print("guard-paquete: NO SE PUDO COMPROBAR — existe fonts/ pero no se "
              "vio ni un archivo de fuente; la regla de licencias pasaría en vacío")
        return 2

    objetivos = _objetivos(pkg)
    if not objetivos:
        # Verde por no mirar: un manifiesto sin exports/files/bin no promete
        # nada y pasaría todas las reglas de arriba sin tocar disco.
        print("guard-paquete: NO SE PUDO COMPROBAR — el manifiesto no declara "
              "ni exports ni files ni bin; no hay nada que verificar")
        return 2

    fallos = revisar(pkg, versionados, tipografias)
    if not fallos:
        familias = sorted({_familia(f) for f in (tipografias or [])})
        print(f"guard-paquete: OK — {pkg.get('name')} v{pkg.get('version')}, "
              f"{len(objetivos)} objetivo(s) declarados, ninguno atado a este disco; "
              f"{len(familias)} familia(s) tipográfica(s), todas con su licencia al lado.")
        return 0

    print(f"guard-paquete: {len(fallos)} problema(s) — el paquete no sobrevive a un clon ajeno\n")
    for regla, explicacion in fallos:
        print(f"  [{regla}] {explicacion}")
    print("\nUn paquete que solo instala en el disco donde se escribió no está publicado.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
