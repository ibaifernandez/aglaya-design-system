#!/usr/bin/env python3
"""lockups_a_contornos.py — pasa a CONTORNOS el texto de los lockups de
`products/`, usando las tipografías que este mismo repo entrega.

PARA QUÉ. Un lockup es la firma de un producto AGLAYA. Con el texto vivo, el SVG
pide la tipografía POR SU NOMBRE: en una máquina que no la tenga instalada —o
insertado como `<img>`, donde ni siquiera se consulta— la firma se pinta con la
que haya. `products/products.json` deja constancia de que ConsentFlow se pasó a
contornos exactamente por esto; los otros doce lo hicieron el 2026-09-25 con
este guion.

POR QUÉ ESTÁ VERSIONADO, que no es obvio. Reexportar un lockup es un acto
manual y puntual, así que la tentación es no guardar la herramienta. El motivo
de guardarla es el kerning: al pasar a contornos se pierde el ajuste entre
letras del motor de texto, y el reparto cambia hasta 2-3 px sobre palabras de
unos 240. Ese desvío es idéntico en los doce **porque los produjo este guion**.
Rehacer la herramienta mañana daría otro desvío, y el lockup nuevo no casaría
con los doce de hoy — la marca expresándose distinto entre superficies por no
haber guardado una decisión ya tomada.

CÓMO SE EJECUTA. Necesita `fontTools`, que NO está en el `python3` del sistema
ni en el venv del MCP. Se monta uno aparte, fuera del repo:

    python3 -m venv /tmp/lockups && /tmp/lockups/bin/pip install fonttools
    /tmp/lockups/bin/python tools/lockups_a_contornos.py .

El argumento es la raíz del repo. Sin argumento no hace nada: un guion que
adivina sobre qué trabaja acaba escribiendo donde no debe.

QUÉ HACE, EXACTAMENTE. Por cada `<text …>CONTENIDO</text>` de
`products/*/lockups/*.svg`:

  · elige el archivo de fuente por familia + peso, de `fonts/` — las mismas que
    entrega el paquete, nunca una instalada en el sistema;
  · saca el contorno de cada glifo y lo coloca en la línea base que declara el
    propio `<text>` (`x`, `y`), aplicando su `letter-spacing` tal cual;
  · sustituye el elemento por un `<g fill="…">` con un `<path>` por glifo, con
    el MISMO `fill` que tenía el texto;
  · quita el `font-family` del `<svg>` raíz, que ya no usa nadie y haría creer
    que sigue haciendo falta una fuente instalada.

QUÉ NO HACE, y es la parte que importa:

  · NO toca el color. Ni uno. Si un día hiciera falta cambiarlo, eso es marca y
    se decide en el canon, no aquí.
  · NO toca nada fuera de los elementos de texto.
  · NO renombra ficheros: `get_lockup` los sirve por su nombre.
  · NO inventa una fuente. Si una familia o un peso no están en `fonts/`, se
    para y lo dice, en vez de sustituirlo por lo más parecido.
  · NO se mete en la CI: no hay nada que comprobar en cada push, porque los
    lockups son artefactos y reexportarlos es deliberado.

QUE REPRODUCE LO PUBLICADO ESTÁ MEDIDO: corriéndolo sobre los originales
—los de antes de la conversión— devuelve los catorce ficheros de
`products/*/lockups/` **idénticos byte a byte** a los que hay en `main`.
"""

import re
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FUENTES_POR_FAMILIA = {
    ("outfit", "900"): "Outfit-Black.ttf",
    ("outfit", "700"): "Outfit-Bold.ttf",
    ("space mono", "700"): "SpaceMono-Bold.ttf",
    ("space mono", "400"): "SpaceMono-Regular.ttf",
}

TEXTO = re.compile(r"<text\b([^>]*)>([^<]*)</text>")
ATRIB = re.compile(r'([\w-]+)\s*=\s*"([^"]*)"')


class Conversor:
    def __init__(self, raiz: Path):
        self.raiz = raiz
        self._cache: dict[tuple[str, str], TTFont] = {}

    def fuente(self, familia: str, peso: str) -> TTFont:
        # La entidad `&#39;` llega literal cuando el atributo se leyó del SVG
        # crudo: se deshace antes de comparar, o «'Space Mono'» no casa con nada.
        fam = familia.replace("&#39;", "'").split(",")[0].strip().strip("'\"").lower()
        clave = (fam, peso)
        if clave not in FUENTES_POR_FAMILIA:
            raise SystemExit(
                f"no tengo fuente para {clave!r} en fonts/ — no invento una. "
                f"Conocidas: {sorted(FUENTES_POR_FAMILIA)}"
            )
        if clave not in self._cache:
            ruta = self.raiz / "fonts" / FUENTES_POR_FAMILIA[clave]
            if not ruta.is_file():
                raise SystemExit(f"falta {ruta} — la fuente la entrega este repo")
            self._cache[clave] = TTFont(ruta)
        return self._cache[clave]

    def contornea(self, attrs: str, contenido: str, fam_svg: str, peso_svg: str) -> str:
        a = dict(ATRIB.findall(attrs))
        tam = float(a["font-size"])
        x, y = float(a.get("x", 0)), float(a.get("y", 0))
        tracking = float(a.get("letter-spacing", 0))
        fill = a.get("fill", "#000")

        f = self.fuente(a.get("font-family", fam_svg), a.get("font-weight", peso_svg))
        escala = tam / f["head"].unitsPerEm
        cmap, glifos, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]

        partes, cursor = [], x
        for ch in contenido:
            nombre = cmap.get(ord(ch))
            if nombre is None:
                raise SystemExit(f"la fuente no tiene el glifo {ch!r} — no lo sustituyo")
            pen = SVGPathPen(glifos, ntos=lambda v: f"{v:.3f}")
            glifos[nombre].draw(pen)
            d = pen.getCommands()
            if d:  # el espacio no dibuja nada, y así se queda
                partes.append(
                    f'<path transform="translate({cursor:.3f},{y:.3f}) '
                    f'scale({escala:.6f},{-escala:.6f})" d="{d}"></path>'
                )
            cursor += hmtx[nombre][0] * escala + tracking
        return f'<g fill="{fill}">' + "".join(partes) + "</g>"

    def procesa(self, p: Path) -> tuple[int, int, int]:
        svg = p.read_text(encoding="utf-8")
        raiz_attrs = dict(ATRIB.findall(re.search(r"<svg\b([^>]*)>", svg).group(1)))
        fam_svg = raiz_attrs.get("font-family", "")
        peso_svg = raiz_attrs.get("font-weight", "400")
        antes, n = len(svg.encode()), 0

        def reemplaza(m):
            nonlocal n
            n += 1
            return self.contornea(
                m.group(1), m.group(2).replace("&#39;", "'"), fam_svg, peso_svg
            )

        nuevo = re.sub(r'\s*font-family="[^"]*"', "", TEXTO.sub(reemplaza, svg), count=1)
        p.write_text(nuevo, encoding="utf-8")
        return n, antes, len(nuevo.encode())


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.split("CÓMO SE EJECUTA.")[1].split("QUÉ HACE")[0].strip())
        return 2
    raiz = Path(sys.argv[1]).resolve()
    conv = Conversor(raiz)
    total, tocados = 0, 0
    for p in sorted(raiz.glob("products/*/lockups/*.svg")):
        if "<text" not in p.read_text(encoding="utf-8"):
            print(f"  (ya en contornos) {p.relative_to(raiz)}")
            continue
        n, antes, despues = conv.procesa(p)
        total, tocados = total + n, tocados + 1
        print(
            f"  {p.relative_to(raiz)}: {n} texto(s) → contornos · "
            f"{antes} B → {despues} B ({despues / antes:.1f}×)"
        )
    print(f"\n{total} elemento(s) de texto contorneados en {tocados} fichero(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
