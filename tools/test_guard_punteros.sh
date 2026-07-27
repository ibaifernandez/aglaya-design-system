#!/usr/bin/env bash
# Prueba que guard_punteros.py MUERDE — no que exista.
#
# Mismo motivo que su hermano: un guardián puede correr y dar verde estando
# roto, y un verde vacío es peor que ningún guardián porque además tranquiliza.
# Aquí hay dos formas de dar un verde falso, y las dos se prueban abajo:
#   · no encontrar los docs (verde por no mirar) → tiene que salir rc=2
#   · eximir los acentos graves, que es donde SIEMPRE se escribe una ruta
#
# Sabotea CLAUDE.md en el sitio y lo restaura SIEMPRE (trap EXIT), incluso al fallar.
# Uso: bash tools/test_guard_punteros.sh   ·   Sale: 0 todo mordió · N = N escapes.

set -u
cd "$(dirname "$0")/.."
GUARD="tools/guard_punteros.py"
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
      echo "  FALSO ROJO $regla   ← $texto"; printf '%s\n' "$salida" | head -4; fallos=$((fallos+1))
    fi
  fi
}

echo "== 1. los punteros de hoy resuelven =="
python3 "$GUARD" || { echo "  ya hay punteros rotos — arregla eso antes de probar el guardián"; exit 1; }

echo "== 2. un enlace a un archivo que no está debe ponerse rojo =="
probar enlace-roto "Ver [el contrato](docs/CONTRATO.md) para el detalle."                    RED
probar enlace-roto "Los tokens viven en [colors.css](colors.css)."                            RED
probar enlace-roto "El glyph está en [aquí](products/pulse/glyphs/pulse-glyph-accent.svg)."   RED
probar enlace-roto "Enlace relativo fuera de sitio: [x](../colors_and_type.css)."             RED

echo "== 3. la lección del acento grave: aquí NO exime =="
echo "   (así estaba escrita la ruta caduca que motivó todo esto)"
probar ruta-de-atlas "Los contratos los custodia él (\`atlas/contratos/README.md\`)."          RED
probar ruta-de-atlas "Su ficha vive en \`atlas/repos/aglaya-design-system/\`."                 RED
probar ruta-de-atlas "Ver atlas/flota/contratos/README.md para el registro."                  RED
probar ruta-de-atlas "Enlace disfrazado: [registro](atlas/flota/contratos/README.md)."         RED

echo "== 4. lo legítimo NO puede ponerse rojo =="
probar enlace-valido    "Ver [el contrato](docs/CONTRACT.md) — este sí existe."               GREEN
probar enlace-externo   "El repo está en [GitHub](https://github.com/ibaifernandez)."         GREEN
probar enlace-ancla     "Salta a [la doctrina](#reglas-duras)."                               GREEN
probar enlace-glob      "Los specimens: [componentes](preview/components-*.html)."            GREEN
probar atlas-en-prosa   "Aquí no se escriben rutas internas del atlas; se preguntan."         GREEN
probar atlas-tool       "Se pide con \`contrato(\"marca\")\` al MCP \`aglaya-atlas\`."         GREEN

echo "== 5. no encontrar docs no puede dar verde =="
cp "$BK" "$DOC"
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_punteros as g
g.docs_versionados = lambda: []          # simula «no veo ningún doc»
rc = g.main()
print("  ROJO  ok   sin-docs (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-docs (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 6. restauración =="
cp "$BK" "$DOC"
python3 "$GUARD" && echo "  $DOC restaurado y verde"

echo
if [ "$fallos" -eq 0 ]; then
  echo "SABOTAJE: todo mordió (0 escapes)"
else
  echo "SABOTAJE: $fallos escape(s) — el guardián corre pero no protege"
fi
exit "$fallos"
