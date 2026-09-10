#!/usr/bin/env bash
# Prueba que guard_valores.py MUERDE — no que exista.
#
# Tercera batería del repo, por el mismo motivo que las dos primeras: un
# guardián puede correr y dar verde estando roto, y un verde vacío es peor que
# ningún guardián porque además tranquiliza. Aquí hay tres formas de dar un
# verde falso, y las tres se prueban abajo:
#   · leer una paleta vacía (verde por no tener nada que perseguir) → rc=2
#   · no encontrar archivos que vigilar (verde por no mirar)        → rc=2
#   · eximir los acentos graves, que es donde SIEMPRE se escribe un hex
#
# Y una forma de morder de más, que mata un guardián igual de rápido: perseguir
# tres números sueltos como si fueran un color. También se prueba.
#
# Sabotea CLAUDE.md en el sitio y lo restaura SIEMPRE (trap EXIT), incluso al fallar.
# Uso: bash tools/test_guard_valores.sh   ·   Sale: 0 todo mordió · N = N escapes.

set -u
cd "$(dirname "$0")/.."
GUARD="tools/guard_valores.py"
DOC="CLAUDE.md"

BK="$(mktemp)"; cp "$DOC" "$BK"
trap 'cp "$BK" "$DOC"; rm -f "$BK"' EXIT

fallos=0

probar() { # regla | texto a inyectar | RED = debe fallar · GREEN = debe pasar
  local regla="$1" texto="$2" esperado="$3" salida rc
  cp "$BK" "$DOC"
  printf '\n%s\n' "$texto" >> "$DOC"
  salida=$(python3 "$GUARD" 2>&1); rc=$?
  if [ "$esperado" = RED ]; then
    if [ "$rc" -eq 1 ] && printf '%s' "$salida" | grep -q "\[$regla\]"; then
      echo "  ROJO  ok   $regla   ← $texto"
    else
      echo "  ESCAPÓ     $regla   ← $texto   (rc=$rc)"; fallos=$((fallos+1))
    fi
  else
    if [ "$rc" -eq 0 ]; then
      echo "  VERDE ok   $regla   ← $texto"
    else
      echo "  FALSO ROJO $regla   ← $texto"; printf '%s\n' "$salida" | head -5; fallos=$((fallos+1))
    fi
  fi
}

echo "== 1. hoy ningún valor de marca está fuera de su casa =="
python3 "$GUARD" || { echo "  ya hay valores copiados — arregla eso antes de probar el guardián"; exit 1; }

echo "== 1b. ¿de verdad está mirando algo? =="
# Un verde puede venir de que todo esté limpio o de que no se haya inspeccionado
# nada. Esto lo distingue: cuenta valores de la paleta y archivos vistos, y
# confirma que el archivo que la batería sabotea está DENTRO del alcance.
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_valores as g
pal = g.paleta() or {}
docs = g.archivos_versionados() or []
vigilado = any(d.name == "CLAUDE.md" for d in docs)
sondas = len(g.sondas(pal)) if pal else 0
print(f"  valores en la paleta: {len(pal)} · sondas: {sondas} · "
      f"archivos vigilados: {len(docs)} · ¿CLAUDE.md dentro?: {vigilado}")
# Si la paleta se vacía o CLAUDE.md sale del alcance, las sondas de abajo
# pasarían en vacío: el sabotaje se inyecta justo en ese archivo.
sys.exit(0 if (pal and docs and vigilado) else 1)
PY
[ $? -eq 0 ] || { echo "  el guardián no está mirando lo que la batería sabotea — las sondas serían vacías"; exit 1; }

echo "== 2. un valor de marca copiado a mano debe ponerse rojo =="
probar valor-copiado "El rojo de marca es #e8003d y no se discute."                       RED
probar valor-copiado "Acento de KANBAN DESK: #4a8fd6."                                    RED
probar valor-copiado "El fondo de tarjeta sube a #0c0c0c."                                RED
probar valor-copiado "Plata técnica: #e2e2e2 para bordes finos."                          RED

echo "== 3. la lección de la mayúscula y del alfa: mismas formas, disfrazadas =="
probar valor-copiado "EL ROJO DE MARCA ES #E8003D."                                       RED
probar valor-copiado "Con alfa al final: #e8003dff."                                      RED
probar valor-copiado "Mezcla de cajas: #E8003d."                                          RED

echo "== 4. el mismo color escrito como rgb() =="
echo "   (así se coló en el manifiesto de componentes que sirve el MCP)"
probar valor-copiado "Hover: rgba(232,0,61,0.2) sobre el borde."                          RED
probar valor-copiado "Con espacios: rgba(232, 0, 61, 0.40)."                              RED
probar valor-copiado "Sintaxis moderna: rgb(232 0 61 / 20%)."                             RED

echo "== 5. la lección del acento grave: aquí NO exime =="
echo "   (un hex en prosa se escribe casi siempre entrecomillado)"
probar valor-copiado "El rojo es \`#e8003d\` — así estaba escrito en el README."          RED
probar valor-copiado "    color: #e8003d;   /* bloque de código indentado */"             RED

echo "== 6. lo legítimo NO puede ponerse rojo =="
probar token-por-nombre  "El rojo se pide con \`var(--color-brand)\`, nunca copiado."      GREEN
probar token-por-mcp     "Por MCP: \`get_token(\"color-brand\")\`."                        GREEN
probar generico-negro    "El lienzo es negro puro: #000 (o #000000)."                      GREEN
probar generico-blanco   "Texto sobre el rojo: #fff, siempre."                             GREEN
probar derivado          "Alfa derivada: color-mix(in srgb, var(--color-brand) 20%, transparent)." GREEN
probar hex-ajeno         "Un azul cualquiera que no es nuestro: #123456."                  GREEN
probar hex-descartado    "El README descarta el casi-negro #0a0a0a a propósito."           GREEN

echo "== 6b. lo que SE LE PARECE tampoco puede ponerse rojo =="
echo "   (un guardián que grita de más lo desactiva el primero que lo sufra)"
probar numeros-sueltos   "Medidas del grid: 232, 0, 61 — píxeles, no un color."            GREEN
probar hex-mas-largo     "Un identificador cualquiera: #e8003dab3f."                       GREEN
probar nombre-del-token  "Los acentos viven en --product-kanban-desk-accent."              GREEN

echo "== 6c. las familias que NO son color: una copia de cada una debe morder =="
echo "   (el guardián se llamaba «de valores» y solo perseguía colores)"
probar valor-copiado "Eyebrow: \`letter-spacing: 0.3em\` y a correr."                      RED
probar valor-copiado "Titular con tracking apretado: -0.04em."                             RED
probar valor-copiado "La display es \`font-family: 'Outfit', sans-serif\`."                RED
probar valor-copiado "El cuerpo: font-family: 'Inter', sans-serif;"                        RED
probar valor-copiado "La mono va con 'Space Mono', monospace."                             RED
probar valor-copiado "Hover a 150ms, reveals a 700ms."                                     RED
probar valor-copiado "Curva: cubic-bezier(0.16, 1, 0.3, 1) en todo."                       RED
probar valor-copiado "Escritorio a partir de 1280px."                                      RED
probar valor-copiado "La píldora va \`border-radius: 9999px\`."                            RED

echo "== 6d. el color que NO es hex: rgb()/rgba() y los valores del MODO CLARO =="
echo "   (media paleta vivía fuera del alcance: --color-muted es un rgba, no un hex)"
probar valor-copiado "Gris de apoyo: rgba(252, 252, 252, 0.72)."                           RED
probar valor-copiado "Borde fino: rgba(255,255,255,0.08)."                                 RED
probar valor-copiado "Y con el alfa escrito corto: rgba(255,255,255,.2)."                  RED
probar valor-copiado "Y en porcentaje: rgb(255 255 255 / 8%)."                             RED
probar valor-copiado "El gris del modo CLARO: rgba(0, 0, 0, 0.72)."                        RED

echo "== 6e. lo que se le PARECE a estas familias tampoco puede ponerse rojo =="
echo "   (cada familia entra con su control legítimo, o la guarda grita de más)"
probar por-token-tracking "Se pide por token: \`letter-spacing: var(--tracking-widest)\`."  GREEN
probar por-token-font     "La display es \`var(--font-display)\`, no la pila a mano."       GREEN
probar em-fuera-de-escala "Un tracking que no está en la escala: 0.4em."                    GREEN
probar alfa-distinto      "Otro blanco translúcido: rgba(255,255,255,0.5)."                 GREEN
probar rem-no-vigilado    "Un espaciado de 3rem — \`rem\` no se vigila a propósito."        GREEN
probar substring-ms       "Una duración larga de verdad: 1150ms."                           GREEN
probar substring-px       "Un lienzo enorme: 11280px de ancho."                             GREEN
probar cero-no-identifica "Radios a 0 y tracking a 0: el literal no identifica nada."       GREEN
probar familia-sin-comilla "Se menciona Outfit en prosa, sin comillas: es el nombre."       GREEN

echo "== 7. el manifiesto de productos no puede desviarse en silencio =="
cp "$BK" "$DOC"
python3 - <<'PY'
import re, sys; sys.path.insert(0, "tools")
import guard_valores as g

original = g.MANIFIESTO.read_text(encoding="utf-8")
ok = False
try:
    # Desvía UN acento del manifiesto respecto de su token en el CSS. El hex
    # de reemplazo NO está en la paleta, así que el único rojo posible es el
    # cruce — si saliera «valor-copiado» estaríamos probando otra cosa.
    roto, n = re.subn(r'"hex":\s*"#4a8fd6"', '"hex": "#0badc0"', original, count=1)
    assert n == 1, "no encontré el acento a desviar — ¿cambió el manifiesto?"
    g.MANIFIESTO.write_text(roto, encoding="utf-8")
    rc = g.main()
    ok = rc == 1
    print("  ROJO  ok   manifiesto-desincronizado" if ok
          else f"  ESCAPÓ     manifiesto-desincronizado (rc={rc})")
finally:
    g.MANIFIESTO.write_text(original, encoding="utf-8")
    assert g.MANIFIESTO.read_text(encoding="utf-8") == original, "NO restauré products.json"
sys.exit(0 if ok else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 8. una paleta vacía no puede dar verde =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_valores as g
g.paleta = lambda: {}                    # simula «el CSS no me dio ni un valor»
rc = g.main()
print("  ROJO  ok   paleta-vacia (rc=2)" if rc == 2 else f"  ESCAPÓ     paleta-vacia (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 9. no encontrar archivos tampoco =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_valores as g
g.archivos_versionados = lambda: []      # simula «no veo ningún archivo»
rc = g.main()
print("  ROJO  ok   sin-archivos (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-archivos (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 10. restauración =="
cp "$BK" "$DOC"
python3 "$GUARD" && echo "  $DOC restaurado y verde"

echo
if [ "$fallos" -eq 0 ]; then
  echo "SABOTAJE: todo mordió (0 escapes)"
else
  echo "SABOTAJE: $fallos escape(s) — el guardián corre pero no protege"
fi
exit "$fallos"
