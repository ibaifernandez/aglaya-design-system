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

echo "== 1b. ¿de verdad está mirando algo? =="
# Un verde puede venir de que todo esté bien o de que no se haya inspeccionado
# nada. Esto lo distingue: cuenta docs y enlaces de verdad vistos.
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_punteros as g
docs = g.docs_versionados() or []
enlaces = sum(len(g.ENLACE.findall(d.read_text(encoding="utf-8"))) for d in docs)
vigilado = any(d.name == "CLAUDE.md" for d in docs)
print(f"  docs vigilados: {len(docs)} · enlaces inspeccionados: {enlaces} · ¿CLAUDE.md dentro?: {vigilado}")
# Si el conjunto se encoge o CLAUDE.md sale del alcance, las sondas de abajo
# pasarían en vacío: el sabotaje se inyecta justo en ese archivo.
sys.exit(0 if (docs and enlaces and vigilado) else 1)
PY
[ $? -eq 0 ] || { echo "  el guardián no está mirando lo que la batería sabotea — las sondas serían vacías"; exit 1; }

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

echo "== 4b. lo que SE LE PARECE tampoco puede ponerse rojo =="
echo "   (un guardián que grita de más lo desactiva el primero que lo sufra)"
probar mcp-con-barra    "El servidor vive en \`aglaya-atlas/mcp/server.py\`."                  GREEN
probar url-ajena        "Un mapa cualquiera: [x](https://ejemplo.com/atlas/mundial/2026)."    GREEN
probar regex-del-patron "El guardián casa con \`atlas/[a-z]+\` — nombrarlo no es citarlo."     GREEN
probar palabra-suelta   "El atlas del capitán se consulta por MCP, no por ruta."              GREEN

echo "== 4c. una ruta rota FUERA de markdown: el fallo que este guardián no vio =="
echo "   (dio verde sobre el PR que borró SKILL.md dejando tres referencias vivas)"
# `probar` solo sabe inyectar en CLAUDE.md, y el fallo real ocurrió en ficheros
# que no son .md. Este helper sabotea cualquiera de ellos y lo restaura siempre.
probar_en() { # regla | fichero | texto | RED|GREEN
  local regla="$1" f="$2" texto="$3" esperado="$4" bk salida rc
  bk="$(mktemp)"; cp "$f" "$bk"
  printf '%s\n' "$texto" >> "$f"
  salida=$(python3 "$GUARD" 2>&1); rc=$?
  cp "$bk" "$f"; rm -f "$bk"
  if [ "$esperado" = RED ]; then
    if [ "$rc" -eq 1 ] && printf '%s' "$salida" | grep -q "\[$regla\]"; then
      echo "  ROJO  ok   $regla   ← $f: $texto"
    else
      echo "  ESCAPÓ     $regla   ← $f: $texto   (rc=$rc)"; fallos=$((fallos+1))
    fi
  else
    if [ "$rc" -eq 0 ]; then
      echo "  VERDE ok   $regla   ← $f: $texto"
    else
      echo "  FALSO ROJO $regla   ← $f: $texto"; printf '%s\n' "$salida" | head -4
      fallos=$((fallos+1))
    fi
  fi
}

probar_en ruta-rota "colors_and_type.css" "/* doctrina: ver docs/NO_EXISTE.md */"            RED
probar_en ruta-rota "LICENSE"              "See also \`docs/NO_EXISTE.md\` for the terms."    RED
# La forma exacta que se escapó: relativa con `../`, en un fichero de config.
# `lstrip("./")` quita CARACTERES y no un prefijo, así que convierte
# «../SKILL.md» en «SKILL.md» y la ruta se cuela por la rama de «ajena».
probar_en ruta-rota "aglaya-ds-mcp/pyproject.toml" "# ver ../NO_EXISTE.md"                    RED

echo "== 4d. y lo legítimo fuera de markdown sigue en verde =="
probar_en ruta-valida-css   "colors_and_type.css" "/* ver docs/CONTRACT.md */"                GREEN
probar_en ruta-relativa-ok  "aglaya-ds-mcp/pyproject.toml" "# ver ../README.md"               GREEN
probar_en dist-generado     "colors_and_type.css" "/* el build escribe dist/tokens.json */"   GREEN
probar_en import-del-paquete "colors_and_type.css" "/* import '@aglaya/design-tokens/tokens.css' */" GREEN
probar_en ruta-absoluta     "colors_and_type.css" "/* ejemplo: /ABS/PATH/repo/server.py */"   GREEN
probar_en repo-ajeno        "colors_and_type.css" "/* el capitán: aglaya-orchestrator/docs/x.md */" GREEN

echo "== 4e. sobre un CLON LIMPIO, que es lo que ve la CI =="
echo "   (en el disco de quien trabaja hay ficheros ignorados que en un clon no están)"
# Este bloque existe por un fallo real: `.gitignore` lista
# `.claude/settings.local.json`, que aquí existe y en un clon no, así que el
# guardián daba VERDE en local y ROJO en la CI. Medir sobre el árbol de trabajo
# no es medir lo que se publica.
CLON="$(mktemp -d)"
if git clone -q --depth 1 "file://$PWD" "$CLON/repo" 2>/dev/null; then
  salida=$(cd "$CLON/repo" && python3 tools/guard_punteros.py 2>&1); rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "  VERDE ok   clon-limpio   ← $(printf '%s' "$salida" | tail -1)"
  else
    echo "  FALSO ROJO clon-limpio   ← el guardián muerde en un clon y no aquí"
    printf '%s\n' "$salida" | head -6
    fallos=$((fallos+1))
  fi
else
  echo "  NO SE PUDO clon-limpio   ← no pude clonar (¿git?); no cuenta como verde"
  fallos=$((fallos+1))
fi
rm -rf "$CLON"

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
