#!/usr/bin/env bash
# Prueba que publicar_cifras.sh MUERDE — no que exista.
#
# Lo que tiene que garantizar el contrato `cifras-publicas`, y lo que se rompe
# en silencio si no se prueba:
#   · una cifra 0, vacía o sin forma NO se publica (sale rojo y no escribe nada)
#   · lo publicado es JSON válido, con las cinco claves y sus tipos
#   · la primera publicación crea una rama HUÉRFANA que solo lleva cifras.json
#   · la segunda añade un commit encima, SIN forzar
#   · un intento rechazado deja la rama exactamente como estaba
#   · los lectores devuelven vacío —no un número inventado— si la salida cambió
#
# Publica contra un repositorio desnudo en un temporal: no toca la red ni este
# repo. Uso: bash tools/test_publicar_cifras.sh · Sale: 0 todo mordió · N escapes.

set -u
cd "$(dirname "$0")/.."
PUB="tools/publicar_cifras.sh"
LEE="tools/medir_cifras.py"

T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fallos=0
ok()     { echo "  ok       $1"; }
escapo() { echo "  ESCAPÓ   $1"; fallos=$((fallos+1)); }

SHA="0123456789abcdef0123456789abcdef01234567"
URL="https://github.com/ibaifernandez/aglaya-design-system/actions/runs/1"
base() { env CIFRAS_TOKENS=87 CIFRAS_HERRAMIENTAS=15 CIFRAS_LLAMADAS=32 CIFRAS_SABOTAJES=3 \
             CIFRAS_COMMIT="$SHA" CIFRAS_EJECUCION="$URL" CIFRAS_MEDIDO_EL=2026-09-16T10:00:00Z "$@"; }

echo "== 1. con cifras sanas se construye un JSON válido =="
base CIFRAS_SOLO_JSON="$T/ok.json" bash "$PUB" >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 0 ] && python3 - "$T/ok.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d["contrato"] == "cifras-publicas" and d["version"] == 1 and d["nave"] == "aglaya-design-system"
c = d["cifras"]
assert set(c) == {"version", "tokens", "herramientas_mcp", "llamadas_autotest", "sabotajes_autotest"}, set(c)
assert isinstance(c["version"]["valor"], str)
for k in ("tokens", "herramientas_mcp", "llamadas_autotest", "sabotajes_autotest"):
    assert isinstance(c[k]["valor"], int) and c[k]["valor"] > 0 and c[k]["fuente"] and c[k]["unidad"], k
PY
then ok "JSON válido, cinco claves, enteros > 0 con fuente y unidad"; else escapo "el JSON sano no salió bien (rc=$rc)"; fi

echo "== 2. una cifra mala no se publica, ni deja fichero =="
for caso in "CIFRAS_TOKENS=0" "CIFRAS_HERRAMIENTAS=0" "CIFRAS_LLAMADAS=0" "CIFRAS_SABOTAJES=0" \
            "CIFRAS_TOKENS=" "CIFRAS_SABOTAJES=" "CIFRAS_LLAMADAS=treinta" \
            "CIFRAS_COMMIT=abc123" "CIFRAS_EJECUCION=no-es-url" "CIFRAS_MEDIDO_EL=ayer"; do
  rm -f "$T/malo.json"
  base "$caso" CIFRAS_SOLO_JSON="$T/malo.json" bash "$PUB" >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq 1 ] && [ ! -e "$T/malo.json" ]; then ok "rechaza $caso"
  else escapo "$caso salió rc=$rc $( [ -e "$T/malo.json" ] && echo 'y ESCRIBIÓ el JSON')"; fi
done

echo "== 3. publicación real contra un repositorio desnudo =="
git init -q --bare "$T/remoto.git"
base CIFRAS_REMOTO="$T/remoto.git" bash "$PUB" >/dev/null 2>&1; rc=$?
ficheros="$(git --git-dir="$T/remoto.git" ls-tree --name-only cifras 2>/dev/null)"
padres="$(git --git-dir="$T/remoto.git" rev-list --count cifras 2>/dev/null)"
if [ "$rc" -eq 0 ] && [ "$ficheros" = "cifras.json" ] && [ "$padres" = "1" ]; then
  ok "primera publicación: rama huérfana con solo cifras.json"
else escapo "primera publicación rc=$rc ficheros=[$ficheros] commits=$padres"; fi

antes="$(git --git-dir="$T/remoto.git" rev-parse cifras 2>/dev/null)"
base CIFRAS_TOKENS=0 CIFRAS_REMOTO="$T/remoto.git" bash "$PUB" >/dev/null 2>&1; rc=$?
despues="$(git --git-dir="$T/remoto.git" rev-parse cifras 2>/dev/null)"
if [ "$rc" -eq 1 ] && [ "$antes" = "$despues" ]; then ok "un intento rechazado deja la rama como estaba"
else escapo "intento rechazado: rc=$rc, rama movida=$([ "$antes" != "$despues" ] && echo sí || echo no)"; fi

base CIFRAS_TOKENS=88 CIFRAS_REMOTO="$T/remoto.git" bash "$PUB" >/dev/null 2>&1; rc=$?
padres="$(git --git-dir="$T/remoto.git" rev-list --count cifras 2>/dev/null)"
padre="$(git --git-dir="$T/remoto.git" rev-parse cifras~1 2>/dev/null)"
valor="$(git --git-dir="$T/remoto.git" show cifras:cifras.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["cifras"]["tokens"]["valor"])')"
if [ "$rc" -eq 0 ] && [ "$padres" = "2" ] && [ "$padre" = "$antes" ] && [ "$valor" = "88" ]; then
  ok "segunda publicación: commit encima del anterior, sin forzar"
else escapo "segunda publicación rc=$rc commits=$padres padre_ok=$([ "$padre" = "$antes" ] && echo sí || echo no) valor=$valor"; fi

echo "== 4. los lectores no se inventan un número si la salida cambia =="
printf 'algo distinto\n' > "$T/raro.log"
for k in tokens herramientas llamadas sabotajes; do
  v="$(python3 "$LEE" "$k" "$T/raro.log")"
  [ -z "$v" ] && ok "$k devuelve vacío ante salida desconocida" || escapo "$k inventó «$v»"
done
printf '  ROJO  ok   uno\n  ESCAPÓ     dos\nSABOTAJE: 1 escape(s)\n' > "$T/escape.log"
v="$(python3 "$LEE" sabotajes "$T/escape.log")"
[ -z "$v" ] && ok "sabotajes con un escape no se cuenta" || escapo "sabotajes contó «$v» con un escape"
printf 'SELFTEST: 2 fallo(s)\n' > "$T/rojo.log"
v="$(python3 "$LEE" llamadas "$T/rojo.log")"
[ -z "$v" ] && ok "llamadas de un selftest en rojo no se cuenta" || escapo "llamadas contó «$v» en rojo"

echo
if [ "$fallos" -eq 0 ]; then echo "CIFRAS: todo mordió (0 escapes)"; else echo "CIFRAS: $fallos escape(s)"; fi
exit "$fallos"
