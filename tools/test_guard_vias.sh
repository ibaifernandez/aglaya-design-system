#!/usr/bin/env bash
# Prueba que guard_vias.py MUERDE — no que exista.
#
# Quinta batería del repo, por el motivo de siempre: un guardián puede correr y
# dar verde estando roto. Aquí el riesgo tiene una forma concreta y conocida —
# **comparar por recuento**. Dos mapas de 92 con un valor distinto miden lo
# mismo, así que un guardián que compare `len()` da verde sobre la deriva que
# de verdad duele. El caso 2 existe para eso: cambia un valor sin cambiar el
# tamaño y exige rojo.
#
# Y un control VERDE que importa tanto como los rojos: el modo claro declara
# dos tintas con el MISMO valor que `:root`, a propósito. Un guardián que
# compare «qué cambia» en vez de «qué se declara» las llamaría defecto. El
# caso 5 comprueba que no lo hace.
#
# No sabotea ningún fichero: las vías se sustituyen en memoria, así que el
# árbol no se toca y no hay nada que restaurar.
#
# Uso: bash tools/test_guard_vias.sh   ·   Sale: 0 todo mordió · N = N escapes.

set -u
cd "$(dirname "$0")/.."

fallos=0

caso() { # descripción | RED|GREEN|DOS | python que redefine g.VIAS
  local desc="$1" esperado="$2" mutacion="$3" salida rc
  salida=$(python3 - "$mutacion" <<'PY' 2>&1
import sys
sys.path.insert(0, "tools")
import guard_vias as g
exec(sys.argv[1])
sys.exit(g.main())
PY
)
  rc=$?
  case "$esperado" in
    RED)   [ "$rc" -eq 1 ] && echo "  ROJO  ok   $desc" || { echo "  ESCAPÓ     $desc (rc=$rc)"; printf '%s\n' "$salida" | head -3; fallos=$((fallos+1)); } ;;
    GREEN) [ "$rc" -eq 0 ] && echo "  VERDE ok   $desc" || { echo "  FALSO ROJO $desc (rc=$rc)"; printf '%s\n' "$salida" | head -4; fallos=$((fallos+1)); } ;;
    DOS)   [ "$rc" -eq 2 ] && echo "  AVISO ok   $desc (rc=2)" || { echo "  ESCAPÓ     $desc (rc=$rc)"; printf '%s\n' "$salida" | head -3; fallos=$((fallos+1)); } ;;
  esac
}

echo "== 1. hoy las tres vías coinciden =="
python3 tools/guard_vias.py || { echo "  arregla las vías antes de probar el guardián"; exit 1; }

echo "== 2. un valor congelado en UNA vía (mismo tamaño: por recuento no se ve) =="
caso "la vía de Python entrega un valor viejo" RED '
real = g.via_python
def mentira():
    base, modos = real()
    base = dict(base); base[sorted(base)[0]] = "#000001"   # un valor, no un token
    return base, modos
g.VIAS["paquete de Python"] = mentira
'

echo "== 3. un token que falta en UNA vía =="
caso "la vía de npm pierde un token" RED '
real = g.via_npm
def mentira():
    base, modos = real()
    base = dict(base); base.pop(sorted(base)[0])
    return base, modos
g.VIAS["paquete de npm"] = mentira
'

echo "== 4. el modo claro desincronizado, con la base idéntica =="
echo "   (la avería histórica fue exactamente de modo: una vía con :root y otra con el bloque claro)"
caso "el MCP declara otro valor solo en claro" RED '
real = g.via_mcp
def mentira():
    base, modos = real()
    modos = {m: dict(t) for m, t in modos.items()}
    modo = sorted(modos)[0]
    modos[modo][sorted(modos[modo])[0]] = "#000002"
    return base, modos
g.VIAS["MCP"] = mentira
'

caso "una vía se queda sin modos" RED '
real = g.via_python
g.VIAS["paquete de Python"] = lambda: (real()[0], {"light": {}}) if False else (real()[0], {"inventado": {"--x": "1"}})
'

echo "== 5. CONTROL VERDE: las tintas que el modo claro repite idénticas =="
echo "   (declaradas con el mismo valor que :root a propósito — no son un defecto)"
python3 - <<'PY'
import sys
sys.path.insert(0, "tools")
import guard_vias as g
base, modos = g.via_mcp()
repetidas = [n for n, v in modos["light"].items() if base.get(n) == v]
if not repetidas:
    print("  NO SE PUDO  el canon ya no repite ninguna tinta en claro;")
    print("              este control deja de medir lo que creía y hay que revisarlo")
    sys.exit(1)
print(f"  hay {len(repetidas)} token(s) declarados en claro con el valor de :root:")
for n in repetidas:
    print(f"    {n} = {base[n]}")
# Y las tres vías tienen que traerlos, o una estaría comparando «lo que cambia».
for nombre, puerta in g.VIAS.items():
    _, m = puerta()
    faltan = [n for n in repetidas if n not in m.get("light", {})]
    if faltan:
        print(f"  ESCAPÓ  {nombre} no declara {', '.join(faltan)} en claro")
        sys.exit(1)
print("  VERDE ok   las tres los declaran y el guardián no los llama defecto")
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 6. no se puede dar verde sin mirar =="
caso "una vía que no se deja leer" DOS '
def rota():
    raise g.NoSePudo("simulado: la puerta no abre")
g.VIAS["MCP"] = rota
'
caso "una vía que entrega cero tokens" DOS '
g.VIAS["paquete de npm"] = lambda: ({}, {"light": {"--x": "1"}})
'

echo "== 7. el guardián no lleva valores ni conteos dentro =="
echo "   (si los llevara, añadir un token obligaría a tocarlo)"
python3 - <<'PY'
import re, sys, pathlib
fuente = pathlib.Path("tools/guard_vias.py").read_text(encoding="utf-8")
codigo = "\n".join(
    l for l in fuente.splitlines()
    if not l.lstrip().startswith("#")
)
codigo = re.sub(r'""".*?"""', "", codigo, flags=re.S)
colores = re.findall(r"#[0-9a-fA-F]{3,8}\b", codigo)
nombres = re.findall(r"--[a-z][a-z0-9-]+", codigo)
if colores or nombres:
    print(f"  ESCAPÓ  lleva valores de marca dentro: {colores + nombres}")
    sys.exit(1)
print("  VERDE ok   ni un color ni un nombre de token escrito en el guardián")
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo
if [ "$fallos" -eq 0 ]; then
  echo "SABOTAJE: todo mordió (0 escapes)"
else
  echo "SABOTAJE: $fallos escape(s) — el guardián corre pero no protege"
fi
exit "$fallos"
