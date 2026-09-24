"""Contraste WCAG 2.x de los pares que usa la marca, leyendo el canon EN VIVO.

No lleva ningún valor de marca dentro: parsea colors_and_type.css (bloque :root
y bloque [data-theme="light"]), resuelve var() y compone los alfas sobre cada
fondo. Imprime nombres de token y ratios, nunca valores.

Uso: python3 contraste.py <ruta a colors_and_type.css>
"""
import re
import sys

css = open(sys.argv[1], encoding="utf-8").read()
css = re.sub(r"/\*[\s\S]*?\*/", "", css)


def bloque(selector_re):
    m = re.search(selector_re + r"\s*\{(.*?)\}", css, re.DOTALL)
    return dict(re.findall(r"--([a-zA-Z0-9-]+)\s*:\s*([^;]+);", m.group(1))) if m else {}


DARK = bloque(r":root")
LIGHT = dict(DARK)
LIGHT.update(bloque(r'\[data-theme="light"\]'))


def resolve(tokens, v, depth=0):
    v = v.strip()
    m = re.fullmatch(r"var\(--([a-zA-Z0-9-]+)\)", v)
    if m:
        return resolve(tokens, tokens[m.group(1)], depth + 1)
    return v


def parse(v):
    """-> (r, g, b, a) en 0..255 / 0..1"""
    v = v.strip().lower()
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        p = [x.strip() for x in m.group(1).split(",")]
        a = float(p[3]) if len(p) > 3 else 1.0
        return (float(p[0]), float(p[1]), float(p[2]), a)
    m = re.fullmatch(r"color-mix\(in srgb,\s*(.+?)\s+([\d.]+)%,\s*transparent\)", v)
    if m:
        base = parse(m.group(1))
        return (base[0], base[1], base[2], base[3] * float(m.group(2)) / 100)
    raise ValueError(v)


def col(tokens, spec):
    """spec: nombre de token ('color-brand') o literal ('#fff', 'rgba(...)')."""
    if spec.startswith(("#", "rgb", "color-mix")):
        s = spec
        # color-mix con var() dentro: resolver la var
        s = re.sub(r"var\(--([a-zA-Z0-9-]+)\)", lambda m: resolve(tokens, tokens[m.group(1)]), s)
        return parse(s)
    return parse(resolve(tokens, tokens[spec]))


def over(fg, bg):
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def lum(c):
    def ch(x):
        x = x / 255
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c[i]) for i in range(3))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


BGS = ["color-bg", "color-bg-deep", "color-surface", "color-surface-2", "color-surface-3"]


def fila(modo, tokens, fg_spec, etiqueta=None, fondos=BGS, opacidad=1.0):
    out = []
    for bgn in fondos:
        bg = col(tokens, bgn)
        fg = col(tokens, fg_spec)
        fg = (fg[0], fg[1], fg[2], fg[3] * opacidad)
        out.append(ratio(over(fg, bg), bg))
    lo, hi = min(out), max(out)
    print(f"{modo:6} {etiqueta or fg_spec:52} min {lo:7.4f}  max {hi:7.4f}  "
          f"texto4.5:{'PASA' if lo >= 4.5 else 'FALLA'}  grande3:{'PASA' if lo >= 3 else 'FALLA'}")
    return lo, hi


def sobre_relleno(modo, tokens, fg_spec, fill_spec, etiqueta):
    fill = col(tokens, fill_spec)
    fg = over(col(tokens, fg_spec), fill)
    r = ratio(fg, fill)
    print(f"{modo:6} {etiqueta:52} {r:7.4f}  texto4.5:{'PASA' if r >= 4.5 else 'FALLA'}  "
          f"grande3/no-texto3:{'PASA' if r >= 3 else 'FALLA'}")
    return r


if __name__ == "__main__":
    print("== 1. Tinta de token sobre los cinco fondos de cada modo ==")
    for modo, T in (("oscuro", DARK), ("claro", LIGHT)):
        for t in ["color-text", "color-muted", "color-faint", "color-accent", "fg-brand",
                  "color-brand", "color-brand-dark", "color-brand-light",
                  "color-corporate-green", "fg-eyebrow"]:
            fila(modo, T, t)
        for t in sorted(k for k in T if k.startswith("product-")):
            fila(modo, T, t)
        print()

    print("== 2. Tinta sobre relleno ==")
    for modo, T in (("oscuro", DARK), ("claro", LIGHT)):
        sobre_relleno(modo, T, "color-text", "color-brand", "--color-text sobre relleno --color-brand")
        sobre_relleno(modo, T, "#ffffff", "color-brand", "blanco puro sobre relleno --color-brand")
        sobre_relleno(modo, T, "#000000", "color-brand", "negro puro sobre relleno --color-brand")
        sobre_relleno(modo, T, "#ffffff", "color-brand-light", "blanco puro sobre relleno --color-brand-light")
        sobre_relleno(modo, T, "#ffffff", "color-brand-dark", "blanco puro sobre relleno --color-brand-dark")
        print()
    for t in sorted(k for k in DARK if k.startswith("product-")):
        sobre_relleno("-", DARK, "#000000", t, f"negro puro sobre relleno --{t}")
        sobre_relleno("-", DARK, "#ffffff", t, f"blanco puro sobre relleno --{t}")
    print()

    print("== 3. No-texto (1.4.11, suelo 3:1): anillo de foco --color-brand ==")
    for modo, T in (("oscuro", DARK), ("claro", LIGHT)):
        lo = min(ratio(col(T, "color-brand"), col(T, b)) for b in BGS)
        hi = max(ratio(col(T, "color-brand"), col(T, b)) for b in BGS)
        print(f"{modo:6} foco --color-brand contra fondos                      min {lo:7.4f}  max {hi:7.4f}  3:{'PASA' if lo >= 3 else 'FALLA'}")
    print()

    print("== 4. ::selection — blanco sobre --color-brand ==")
    sobre_relleno("ambos", DARK, "#ffffff", "color-brand", "::selection (color #fff, fondo --color-brand)")
