#!/usr/bin/env bash
# Prueba que guard_huella.py MUERDE — no que exista.
#
# Por qué está en el repo y no en el escritorio de nadie: un guardián puede
# correr y dar verde estando roto. Pasó tres veces el día que se escribió esto.
# Dos de esos fallos los cazó exactamente esta batería:
#   · un patrón que no casaba en MAYÚSCULAS
#   · `2500 €` colándose porque `\b` no casa tras un símbolo no alfanumérico
# Si tocas las reglas de guard_huella.py, esto es lo único que dice si siguen mordiendo.
#
# Sabotea CLAUDE.md en el sitio y lo restaura SIEMPRE (trap EXIT), incluso al fallar.
# Uso: bash tools/test_guard_huella.sh   ·   Sale: 0 todo mordió · N = N escapes.

set -u
cd "$(dirname "$0")/.."
GUARD="tools/guard_huella.py"
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
      echo "  FALSO ROJO $regla   ← $texto"; printf '%s\n' "$salida" | head -3; fallos=$((fallos+1))
    fi
  fi
}

echo "== 1. la huella de hoy está limpia =="
python3 "$GUARD" || { echo "  la huella actual ya falla — arregla eso antes de probar el guardián"; exit 1; }

echo "== 2. cada forma prohibida debe ponerse roja =="
probar fecha-de-pase       "Último pase del capitán: 2026-07-17 — todo en orden."           RED
probar fecha-de-pase       "Revisado el 15-jul por el capitán."                             RED
probar marca-de-progreso   "Re-chequeo del capitán: 7/7."                                   RED
probar conteo              "El MCP expone 7 tools read-only."                               RED
probar version-a-mano      "El contrato de marca va por v1.0.0."                            RED
probar precio              "La auditoría de marca se vende a 2500 €."                       RED
probar precio              "Precio: 2.500€ / mes."                                          RED
probar precio              "El paquete sale por 1200 EUR."                                  RED
probar precio              'Arranque desde $900.'                                           RED
probar sello-de-verificado "CONTRACT.md y el tag quedan verificados."                       RED
probar estado-encendido    "El MCP está vivo y el servicio desplegado."                     RED
probar valor-de-marca      "La paleta real, de nuestro CSS: #e8003d, #9fc243."              RED

echo "== 3. la lección de la mayúscula: las mismas formas, gritando =="
probar sello-de-verificado "CONTRACT.MD Y EL TAG QUEDAN VERIFICADOS."                       RED
probar estado-encendido    "EL MCP ESTÁ VIVO."                                              RED
probar fecha-de-pase       "ÚLTIMO PASE: 2026-07-17."                                       RED
probar valor-de-marca      "PALETA: #E8003D."                                               RED

echo "== 4. la puerta de garaje: la cita exime el fragmento, no la línea =="
probar exencion-frag  "> El guardián prohíbe escribir aquí un \`v1.0.0\` a mano."           GREEN
probar version-a-mano "> Prohibido el \`v1.0.0\` a mano; por eso este doc va por v2.0.0."   RED
probar fecha-de-pase  "El patrón \`2026-07-17\` está prohibido en prosa."                   GREEN
probar fecha-de-pase  "El patrón \`2026-07-17\` está prohibido; último pase 2026-07-17."    RED

echo "== 5. borrar la sección no puede dar verde =="
cp "$BK" "$DOC"
python3 - "$DOC" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
p.write_text(p.read_text(encoding="utf-8").split("## AGLAYA · Flota — el capitán")[0], encoding="utf-8")
PY
python3 "$GUARD" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 2 ]; then
  echo "  ROJO  ok   seccion-ausente (rc=2)"
else
  echo "  ESCAPÓ     seccion-ausente (rc=$rc)"; fallos=$((fallos+1))
fi

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
