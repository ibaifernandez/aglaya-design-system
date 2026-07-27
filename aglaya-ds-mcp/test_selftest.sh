#!/usr/bin/env bash
# Prueba que selftest.py MUERDA — no que corra.
#
# Este archivo existe por una avería concreta, no por simetría: la versión
# anterior de selftest.py llamaba a las 15 tools y salía 0 pase lo que pase,
# porque un rechazo del servidor viaja con isError=False y un payload normal
# de {"error": …}. Corría, imprimía mucho, y no podía ponerse rojo. Un test así
# es peor que ninguno: certifica.
#
# Se sabotea server.py de tres formas y se comprueba que cada una sale roja:
#   · una tool que debe responder, devolviendo un error
#   · una tool que debe rechazar, respondiendo como si nada
#   · una tool que desaparece del registro
#
# Restaura SIEMPRE (trap EXIT), incluso al fallar.
# Uso: ./.venv/bin/python -V && bash test_selftest.sh   ·   Sale: 0 todo mordió · N escapes.

set -u
cd "$(dirname "$0")"
PY="./.venv/bin/python"
SRV="server.py"

[ -x "$PY" ] || { echo "no encuentro $PY — crea el venv (ver README)"; exit 2; }

BK="$(mktemp)"; cp "$SRV" "$BK"
trap 'cp "$BK" "$SRV"; rm -f "$BK"' EXIT

fallos=0

probar() { # etiqueta | script python que sabotea server.py
  local etiqueta="$1" parche="$2" rc
  cp "$BK" "$SRV"
  python3 - "$SRV" <<PY
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
$parche
p.write_text(t, encoding="utf-8")
PY
  if [ $? -ne 0 ]; then
    echo "  NO APLICÓ   $etiqueta   (el parche no encontró su ancla — ¿cambió server.py?)"
    fallos=$((fallos+1)); return
  fi
  "$PY" selftest.py >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq 1 ]; then
    echo "  ROJO  ok   $etiqueta"
  else
    echo "  ESCAPÓ     $etiqueta   (rc=$rc — el selftest dio verde con el servidor roto)"
    fallos=$((fallos+1))
  fi
}

echo "== 1. con el servidor sano, verde =="
"$PY" selftest.py >/dev/null 2>&1 || { echo "  el selftest ya está rojo — arregla eso antes de probarlo"; exit 1; }
echo "  verde"

echo "== 2. una tool que debe responder devuelve un error =="
echo "   (el fallo real: esto viaja con isError=False y colaba)"
probar "get_token responde {error}" '
viejo = "    val = _guard(brand.get_token, name)"
assert viejo in t, "ancla get_token"
t = t.replace(viejo, "    return {\"error\": \"sabotaje\"}\n" + viejo, 1)'

echo "== 3. una tool que debe rechazar responde como si nada =="
probar "get_product acepta cualquier id" '
viejo = "def get_product(id: str) -> dict:"
assert viejo in t, "ancla get_product"
i = t.index(viejo) + len(viejo)
j = t.index("\n", t.index("\"\"\"", t.index("\"\"\"", i) + 3))
t = t[:j] + "\n    return {\"id\": id, \"name\": \"INVENTADO\"}" + t[j:]'

echo "== 4. una tool desaparece del registro =="
probar "get_component sin @mcp.tool()" '
viejo = "@mcp.tool()\ndef get_component"
assert viejo in t, "ancla get_component"
t = t.replace(viejo, "def get_component", 1)'

echo "== 5. restauración =="
cp "$BK" "$SRV"
"$PY" selftest.py >/dev/null 2>&1 && echo "  $SRV restaurado y verde" || { echo "  !! $SRV NO quedó verde"; fallos=$((fallos+1)); }

echo
if [ "$fallos" -eq 0 ]; then
  echo "SABOTAJE: todo mordió (0 escapes)"
else
  echo "SABOTAJE: $fallos escape(s) — el selftest corre pero no protege"
fi
exit "$fallos"
