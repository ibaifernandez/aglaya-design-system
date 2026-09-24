"""Contraste de las tintas escritas a mano en los specimens de preview/.

Importa el parser en vivo de contraste.py. Los literales de abajo son los que
aparecen en cada specimen (se citan por archivo:línea); ninguno es un valor de
token del canon.

Uso: python3 contraste_preview.py <ruta a colors_and_type.css>
"""
import sys
sys.argv = [sys.argv[0], sys.argv[1]]
import contraste as C
from contraste_usos import txt

T = C.DARK
print("== preview/ — literales de tinta en los specimens (todos pintan sobre negro salvo donde se dice) ==")
txt("oscuro", T, "rgba(255,255,255,0.45)", ["#000000"], "components-buttons .btn-link blanco 45% 10px sobre #000 [:29]")
txt("oscuro", T, "rgba(255,255,255,0.45)", ["color-surface-2"], "components-card .body blanco 45% 13px sobre --surface-2 [:25]")
txt("oscuro", T, "rgba(255,255,255,0.35)", ["#000000"], "components-badges .pill blanco 35% 9px sobre #000 [:21]")
txt("oscuro", T, "rgba(255,255,255,0.5)", ["#000000", "rgba(255,255,255,0.02)"], "components-comparison dt blanco 50% 9px sobre celda [:25]")
for bg in ["#000000", "color-bg-deep", "color-surface", "color-surface-2", "color-surface-3"]:
    txt("oscuro", T, "rgba(255,255,255,0.45)", [bg], f"colors-surface .hex blanco 45% 9px sobre {bg} [:25]")
txt("oscuro", T, "#ffffff", ["color-brand-light"], "colors-brand .brand-light .name/.hex blanco 10px/9px [:31]")
txt("oscuro", T, "rgba(255,255,255,0.4)", ["#000000"], "spacing-scale .px blanco 40% 9px sobre #000 [:12]")
txt("oscuro", T, "rgba(255,255,255,0.4)", ["#000000"], "type-inter/outfit-weights .label blanco 40% 9px [:18] / type-spacemono-weights [:17]")
txt("oscuro", T, "rgba(255,255,255,0.45)", ["#000000"], "type-mono .mono blanco 45% 11px sobre #000 [:12]")
txt("oscuro", T, "color-brand", ["#000000"], "spacing-radii-shadows .pill --color-brand 10px sobre #000 [:14]")
txt("oscuro", T, "rgba(255,255,255,0.55)", ["#000000"], "spacing-radii-shadows .rule blanco 55% 10px sobre #000 [:12]")
txt("oscuro", T, "rgba(0,0,0,0.6)", ["color-brand"], "brand-logo-variants .brand .label negro 60% 10px sobre relleno rojo [:16]")
txt("oscuro", T, "rgba(0,0,0,0.5)", ["#ffffff"], "brand-logo-variants .white .label negro 50% 10px sobre blanco [:14]")
txt("oscuro", T, "rgba(255,255,255,0.5)", ["#000000"], "brand-logo-variants .black .label blanco 50% 10px sobre negro [:15]")
txt("oscuro", T, "color-mix(in srgb, var(--color-text) 40%, transparent)", ["#000000"], "brand-product-identity .meta/.lbl/.note tinta 40% 9-11px [:7,:9,:14]")
txt("oscuro", T, "color-mix(in srgb, var(--color-text) 30%, transparent)", ["#000000"], "brand-product-identity .absent tinta 30% 10px [:13]")
txt("oscuro", T, "rgba(255,255,255,0.5)", ["#000000"], "brand-favicon .label blanco 50% 9px [:15] / brand-iconography .name [:12]")
