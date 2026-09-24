"""Contraste de USOS concretos: specs de components.json y composiciones del kit.

Importa el parser en vivo de contraste.py. Los literales de abajo son los que
aparecen escritos en components.json / ui_kits (se citan por archivo:línea en el
informe); no son valores de token.
"""
import sys
sys.argv = [sys.argv[0], sys.argv[1]]
import contraste as C

D, L = C.DARK, C.LIGHT


def txt(modo, T, fg, bg_capas, etiqueta, opacidad=1.0, umbral=4.5):
    """bg_capas: lista de specs de fondo, del más profundo al más alto."""
    bg = C.col(T, bg_capas[0])
    for capa in bg_capas[1:]:
        bg = C.over(C.col(T, capa), bg)
    f = C.col(T, fg)
    f = (f[0], f[1], f[2], f[3] * opacidad)
    r = C.ratio(C.over(f, bg), bg)
    print(f"{modo:6} {etiqueta:70} {r:7.4f}  umbral {umbral}: {'PASA' if r >= umbral else 'FALLA'}")
    return r


print("== components.json — specs de color, en los dos modos ==")
for modo, T in (("oscuro", D), ("claro", L)):
    # button.primary: color var(--color-text) sobre var(--color-brand) — components.json:14-15
    txt(modo, T, "color-text", ["color-brand"], "button.primary texto (--color-text) sobre --color-brand [:14-15]")
    # button.ghost: bg rgba(255,255,255,0.1), color --color-text — :30-31
    txt(modo, T, "color-text", ["color-bg", "rgba(255,255,255,0.1)"], "button.ghost texto sobre su fondo, pagina --color-bg [:30-31]")
    # input: bg rgba(255,255,255,0.03), color rgba(255,255,255,0.5) — :86,:90
    txt(modo, T, "rgba(255,255,255,0.5)", ["color-bg", "rgba(255,255,255,0.03)"], "input texto rgba(.5) sobre su fondo, pagina --color-bg [:86,:90]")
    # input border rgba(255,255,255,0.35) — :87 (no-texto, 1.4.11)
    txt(modo, T, "rgba(255,255,255,0.35)", ["color-bg"], "input borde rgba(.35) contra --color-bg (1.4.11) [:87]", umbral=3)
    # input label: var(--color-corporate-green) 9px — :92
    txt(modo, T, "color-corporate-green", ["color-bg"], "input label --color-corporate-green 9px [:92]")
    # badge.default: bg rgba(.05), color rgba(.6) — :106
    txt(modo, T, "rgba(255,255,255,0.6)", ["color-bg", "rgba(255,255,255,0.05)"], "badge.default texto rgba(.6) sobre rgba(.05) [:106]")
    # badge.brand: color green, bg brand 10% — :107
    txt(modo, T, "color-corporate-green", ["color-bg", "color-mix(in srgb, var(--color-brand) 10%, transparent)"], "badge.brand texto green sobre brand 10% [:107]")
    # badge.codetag: bg var(--color-text), color #000 — :108
    txt(modo, T, "#000000", ["color-text"], "badge.codetag #000 sobre var(--color-text) [:108]")
    # badge.ok: color green — :109
    txt(modo, T, "color-corporate-green", ["color-bg"], "badge.ok texto green [:109]")
    # card body: var(--color-muted) 13px sobre surface-2 — :65,:71
    txt(modo, T, "color-muted", ["color-surface-2"], "card.body --color-muted sobre --color-surface-2 [:65,:71]")
    # button.link: var(--color-muted) — :47
    txt(modo, T, "color-muted", ["color-bg"], "button.link --color-muted [:47]")
    print()

print("== ui_kits/website — composiciones con opacidad o tinta roja (oscuro, el modo del kit) ==")
T = D
txt("oscuro", T, "color-brand", ["color-bg"], "Header nav :hover --brand 13px/700 sobre negro [Header.jsx:29]")
txt("oscuro", T, "color-corporate-green", ["color-surface-2"], "Problem eyebrow 9px opacity .7 sobre --surface-2 [Problem.jsx:26]", opacidad=0.7)
txt("oscuro", T, "color-corporate-green", ["color-surface"], "AntiClient eyebrow 9px opacity .55 sobre --surface-1 [AntiClient.jsx:23]", opacidad=0.55)
txt("oscuro", T, "color-corporate-green", ["color-bg"], "AntiClient OPERATIONAL_INTEGRITY 10px opacity .6 [AntiClient.jsx:92-94]", opacidad=0.6)
txt("oscuro", T, "color-text", ["color-bg"], "Problem REF_ID 10px en contenedor opacity .5 [Problem.jsx:72-75]", opacidad=0.5)
txt("oscuro", T, "color-brand-light", ["color-surface-2"], "SystemCard etiqueta --brand-ink 10px sobre --surface-2 [SystemsGrid.jsx:30]")
txt("oscuro", T, "color-faint", ["color-surface"], "ExclusionCard cuerpo --color-faint 15px sobre --surface-1 [AntiClient.jsx:33]")
txt("oscuro", T, "color-faint", ["color-bg-deep", "color-mix(in srgb, var(--color-text) 2%, transparent)"], "Footer PRIMARY_CHANNELS --color-faint sobre bg-deep+2% [Footer.jsx:131-134]")
txt("oscuro", T, "color-faint", ["color-bg-deep", "color-mix(in srgb, var(--color-text) 2.5%, transparent)", "color-mix(in srgb, var(--color-text) 3%, transparent)"], "Footer input placeholder? (no: color --color-text) — referencia")
