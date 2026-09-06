#!/usr/bin/env bash
# Los TRES parsers del CSS canónico tienen que coincidir, y ninguno puede servir
# una declaración comentada.
#
# Por qué existe. El canon lo parsean tres piezas distintas, en tres entornos
# distintos —el paquete con Node, el MCP con el python de su venv, el guardián
# con el python3 del sistema—, cada una con su copia de la expresión regular. No
# pueden compartir código. Lo único que se puede compartir es esta prueba.
#
# Lo que persigue. Una declaración comentada dentro de :root —un valor viejo que
# alguien aparcó— leída como si estuviera viva. Cuando eso pasa, el paquete y el
# MCP dicen cosas DISTINTAS sobre el mismo token: una nave que instala recibe el
# valor vivo y otra que pregunta al MCP recibe el muerto. Dos verdades sobre un
# valor de marca.
#
# ⚠️ EL ORDEN DEL SABOTAJE NO ES LIBRE. La comentada tiene que ir DESPUÉS de la
# viva: el diccionario se sobrescribe y manda la última aparición. Puesta antes,
# los tres aciertan y la prueba pasa sin demostrar nada — un guardián que corre,
# da verde y está roto, que es justo lo que esta casa persigue.
#
# El CSS canónico se edita en caliente y se restaura SIEMPRE (trap EXIT), igual
# que hace zerocopy_test.py.
#
# Uso:  bash tools/test_parsers_comentarios.sh
# Sale: 0 los tres coinciden y la prueba muerde · 1 alguno falla · 2 no se pudo.

set -u
cd "$(dirname "$0")/.."

CSS="colors_and_type.css"
TOKEN="--color-brand"
MUERTO="#dead00"          # no está en la paleta: si aparece, viene del comentario
PY_MCP="aglaya-ds-mcp/.venv/bin/python"

for req in node python3; do
  command -v "$req" >/dev/null 2>&1 || {
    echo "test-parsers: NO SE PUDO COMPROBAR — falta '$req'"; exit 2; }
done
[ -x "$PY_MCP" ] || {
  echo "test-parsers: NO SE PUDO COMPROBAR — falta el venv del MCP (ver aglaya-ds-mcp/README.md)"
  exit 2; }

BK="$(mktemp)"; cp "$CSS" "$BK"
trap 'cp "$BK" "$CSS"; rm -f "$BK"' EXIT

VIVO="$(sed -n "s/^[[:space:]]*$TOKEN:[[:space:]]*\([^;]*\);.*/\1/p" "$CSS" | head -1 | tr -d ' ')"
[ -n "$VIVO" ] || { echo "  el CSS no declara $TOKEN"; exit 2; }

fallos=0

# Cada parser responde con el valor que sirve para $TOKEN. Son las MISMAS
# consultas que hacen las piezas de verdad, no reimplementaciones.
leer_mcp()  { (cd aglaya-ds-mcp && ./.venv/bin/python -c "
import sys; sys.path.insert(0,'.')
import brand; print(brand.get_token('color-brand'))" 2>/dev/null); }
leer_build(){ node -e "
const {execSync}=require('child_process');
execSync('node scripts/build-tokens.mjs',{stdio:'ignore'});
delete require.cache[require.resolve('./dist/tokens.json')];
process.stdout.write(require('./dist/tokens.json').tokens['$TOKEN']||'');" 2>/dev/null; }
leer_guard(){ python3 -c "
import sys; sys.path.insert(0,'tools')
import guard_valores as g
d = dict(g.declaraciones_root() or [])
print(d.get('color-brand',''))" 2>/dev/null; }

comprobar() { # etiqueta | esperado
  local et="$1" esperado="$2" m b gu
  m="$(leer_mcp)"; b="$(leer_build)"; gu="$(leer_guard)"
  local ok=0
  for par in "MCP:$m" "paquete:$b" "guardián:$gu"; do
    if [ "${par#*:}" != "$esperado" ]; then
      echo "  ESCAPÓ   $et — ${par%%:*} sirve '${par#*:}' y se esperaba '$esperado'"
      ok=1
    fi
  done
  [ "$ok" -eq 0 ] && echo "  ok   $et — los tres sirven '$esperado'"
  return "$ok"
}

echo "== 1. con el CSS sano, los tres coinciden =="
comprobar "sano" "$VIVO" || fallos=$((fallos+1))

echo "== 2. con una declaración comentada DESPUÉS de la viva =="
python3 - "$CSS" "$TOKEN" "$MUERTO" <<'PY'
import sys, pathlib, re
p, tok, muerto = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text(encoding="utf-8")
m = re.search(rf"^([ \t]*){re.escape(tok)}:[^;]*;.*$", t, re.M)
assert m, "no encontré la declaración viva"
t = t[:m.end()] + f"\n{m.group(1)}/* {tok}: {muerto};  valor viejo aparcado */" + t[m.end():]
p.write_text(t, encoding="utf-8")
PY
comprobar "con la comentada detrás" "$VIVO" || fallos=$((fallos+1))

echo "== 3. ¿la prueba MUERDE? se retira el filtrado de cada uno =="
muerde() { # etiqueta | archivo | patrón sed que rompe el filtrado
  local et="$1" f="$2" patron="$3" bk out
  bk="$(mktemp)"; cp "$f" "$bk"
  perl -0pi -e "$patron" "$f"
  if [ "$(cmp -s "$f" "$bk"; echo $?)" -eq 0 ]; then
    echo "  NO APLICÓ   $et — el parche no encontró su ancla (¿cambió $f?)"
    cp "$bk" "$f"; rm -f "$bk"; return 1
  fi
  out="$(comprobar "$et (saboteado)" "$VIVO" 2>&1)"
  cp "$bk" "$f"; rm -f "$bk"
  if echo "$out" | grep -q "ESCAPÓ"; then
    echo "  ROJO ok   $et — sin el filtrado, sirve el valor comentado"
    return 0
  fi
  echo "  ESCAPÓ     $et — sin el filtrado la prueba siguió verde: no protege"
  return 1
}

muerde "MCP (brand.py)" "aglaya-ds-mcp/brand.py" \
  's/_SIN_COMENTARIOS\.sub\("", (root\.group\(1\) if root else css)\)/$1/' || fallos=$((fallos+1))
muerde "guardián (guard_valores.py)" "tools/guard_valores.py" \
  's/SIN_COMENTARIOS\.sub\("", m\.group\(1\)\)/m.group(1)/' || fallos=$((fallos+1))
muerde "paquete (build-tokens.mjs)" "scripts/build-tokens.mjs" \
  's/sinComentarios\(bloque\)\.matchAll/bloque.matchAll/' || fallos=$((fallos+1))

echo "== 4. restauración =="
cp "$BK" "$CSS"
comprobar "restaurado" "$VIVO" || fallos=$((fallos+1))

echo
if [ "$fallos" -eq 0 ]; then
  echo "PARSERS: los tres coinciden y ninguno sirve lo comentado (la prueba muerde)"
else
  echo "PARSERS: $fallos fallo(s)"
fi
exit "$fallos"
