#!/usr/bin/env bash
# Prueba que guard_paquete.py MUERDE — no que exista.
#
# Cuarta batería del repo, por el motivo de siempre: un guardián puede correr y
# dar verde estando roto. Aquí duele más que en los otros tres, porque lo que
# vigila no se puede ver desde este disco: un `file:` a un repo hermano instala
# perfectamente aquí y solo se rompe en el CI del consumidor, que clona su repo
# y no el nuestro. Si este guardián da un verde falso, nadie se entera hasta que
# el build ajeno está rojo.
#
# Tres formas de dar un verde vacío, las tres probadas abajo:
#   · no encontrar el manifiesto            → rc=2
#   · que git no conteste qué está versionado → rc=2
#   · un manifiesto que no promete nada (sin exports/files/bin) → rc=2
#
# Y una forma de morder de más, que mata un guardián igual de rápido: llamar
# ruta-local a una dependencia normal de registro. También se prueba.
#
# Sabotea package.json en el sitio y lo restaura SIEMPRE (trap EXIT).
# Uso: bash tools/test_guard_paquete.sh   ·   Sale: 0 todo mordió · N = N escapes.

set -u
cd "$(dirname "$0")/.."
GUARD="tools/guard_paquete.py"
PKG="package.json"

BK="$(mktemp)"; cp "$PKG" "$BK"
trap 'cp "$BK" "$PKG"; rm -f "$BK"; chmod +x bin/aglaya-tokens-version.mjs 2>/dev/null' EXIT

fallos=0

probar() { # regla | descripción | RED|GREEN | sentencia python sobre `pkg`
  local regla="$1" desc="$2" esperado="$3" mutacion="$4" salida rc
  cp "$BK" "$PKG"
  python3 - "$mutacion" <<'PY'
import json, pathlib, sys
p = pathlib.Path("package.json")
pkg = json.loads(p.read_text(encoding="utf-8"))
exec(sys.argv[1])
p.write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
PY
  salida=$(python3 "$GUARD" 2>&1); rc=$?
  if [ "$esperado" = RED ]; then
    if [ "$rc" -eq 1 ] && printf '%s' "$salida" | grep -q "\[$regla\]"; then
      echo "  ROJO  ok   $regla   ← $desc"
    else
      echo "  ESCAPÓ     $regla   ← $desc   (rc=$rc)"; fallos=$((fallos+1))
    fi
  else
    if [ "$rc" -eq 0 ]; then
      echo "  VERDE ok   $regla   ← $desc"
    else
      echo "  FALSO ROJO $regla   ← $desc"; printf '%s\n' "$salida" | head -6; fallos=$((fallos+1))
    fi
  fi
}

echo "== 1. hoy el paquete sobrevive a un clon ajeno =="
python3 "$GUARD" || { echo "  arregla el paquete antes de probar el guardián"; exit 1; }

echo "== 1b. ¿de verdad está mirando algo? =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
pkg = g.manifiesto() or {}
objetivos = g._objetivos(pkg)
versionados = g.rastreados() or []
print(f"  objetivos declarados: {len(objetivos)} · archivos versionados: {len(versionados)}")
sys.exit(0 if (objetivos and versionados) else 1)
PY
[ $? -eq 0 ] || { echo "  el guardián no está inspeccionando nada"; exit 1; }

echo "== 2. una dependencia atada a este disco (la avería que solo se ve en el CI ajeno) =="
probar ruta-local "file: a un repo hermano" RED \
  'pkg["dependencies"] = {"aglaya-tokens": "file:../aglaya-design-system"}'
probar ruta-local "link: a una carpeta local" RED \
  'pkg["dependencies"] = {"x": "link:../x"}'
probar ruta-local "workspace: de monorepo" RED \
  'pkg["dependencies"] = {"x": "workspace:*"}'
probar ruta-local "ruta relativa pelada" RED \
  'pkg["devDependencies"] = {"x": "../x"}'
probar ruta-local "un exports que se sale de la raíz" RED \
  'pkg["exports"]["./tokens.css"] = "../otro-repo/colors_and_type.css"'

echo "== 3. un remoto que un CI ajeno no puede consultar =="
probar remoto-inalcanzable "repository.url en SSH" RED \
  'pkg["repository"]["url"] = "git@github.com:ibaifernandez/aglaya-design-system.git"'
probar remoto-inalcanzable "repository.url vacío" RED \
  'pkg["repository"] = {}'

echo "== 4. prometer algo que no se entrega =="
probar objetivo-ausente "files con un archivo inexistente" RED \
  'pkg["files"].append("docs/NO_EXISTE.md")'
probar objetivo-ausente "exports a un archivo inexistente" RED \
  'pkg["exports"]["./nada.css"] = "./nada.css"'
probar objetivo-ausente "bin apuntando a la nada" RED \
  'pkg["bin"] = {"aglaya-tokens-version": "bin/no-esta.mjs"}'

echo "== 5. sin build no hay formas JS/JSON en el consumidor =="
probar sin-build "scripts.prepare eliminado" RED \
  'pkg["scripts"].pop("prepare", None)'

echo "== 6. el CSS exportado tiene que ser el canónico =="
probar css-no-canonico "exports apuntando a otra hoja" RED \
  'pkg["exports"]["./tokens.css"] = "./ui_kits/website/styles.css"'
probar css-no-canonico "sin vía CSS: todo dependería del build" RED \
  'pkg["exports"].pop("./tokens.css", None)'

echo "== 7. lo legítimo NO puede ponerse rojo =="
probar dep-de-registro   "una dependencia normal de npm"        GREEN \
  'pkg["dependencies"] = {"some-lib": "^1.2.3"}'
probar dep-por-git       "una dependencia por git+https"        GREEN \
  'pkg["dependencies"] = {"otra": "git+https://github.com/x/y.git#v1.0.0"}'
probar glob-de-fuentes   "un exports con glob (./fonts/*)"      GREEN \
  'pkg["exports"]["./fonts/*"] = "./fonts/*"'
probar objetivo-construido "un exports a dist/, que no existe en un clon limpio" GREEN \
  'pkg["exports"]["./otro.json"] = "./dist/otro.json"'

echo "== 8. un bin no ejecutable se entrega roto =="
cp "$BK" "$PKG"
chmod -x bin/aglaya-tokens-version.mjs
salida=$(python3 "$GUARD" 2>&1); rc=$?
if [ "$rc" -eq 1 ] && printf '%s' "$salida" | grep -q "\[objetivo-ausente\]"; then
  echo "  ROJO  ok   objetivo-ausente   ← bin sin permiso de ejecución"
else
  echo "  ESCAPÓ     objetivo-ausente   ← bin sin permiso de ejecución (rc=$rc)"
  fallos=$((fallos+1))
fi
chmod +x bin/aglaya-tokens-version.mjs

echo "== 9. dist/ versionado abre una segunda casa para cada valor =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
real = g.rastreados()
g.rastreados = lambda: (real or []) + ["dist/tokens.json"]   # simula el commit
rc = g.main()
print("  ROJO  ok   copia-rastreada" if rc == 1 else f"  ESCAPÓ     copia-rastreada (rc={rc})")
sys.exit(0 if rc == 1 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 9b. una fuente redistribuida sin su licencia al lado =="
echo "   (la avería real: el repo se hizo público y el paquete las llevaba sin licencia)"
LIC="fonts/LICENSE-Inter.txt"
LIC_BK="$(mktemp)"
cp "$LIC" "$LIC_BK"
rm -f "$LIC"
salida=$(python3 "$GUARD" 2>&1); rc=$?
if [ "$rc" -eq 1 ] && printf '%s' "$salida" | grep -q "\[fuente-sin-licencia\]"; then
  echo "  ROJO  ok   fuente-sin-licencia   ← falta la licencia de Inter"
else
  echo "  ESCAPÓ     fuente-sin-licencia   ← falta la licencia de Inter (rc=$rc)"
  fallos=$((fallos+1))
fi
cp "$LIC_BK" "$LIC"; rm -f "$LIC_BK"
cmp -s "$LIC" fonts/LICENSE-Inter.txt || { echo "  NO restauré $LIC"; exit 1; }

echo "== 9c. una familia NUEVA sin licencia también =="
echo "   (empareja por nombre, así que protege a la familia que aún no existe)"
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from pathlib import Path
import guard_paquete as g
reales = g.fuentes() or []
g.fuentes = lambda: reales + [g.FUENTES / "Recoleta-Regular.otf"]   # familia inventada
rc = g.main()
print("  ROJO  ok   fuente-sin-licencia (familia nueva)" if rc == 1
      else f"  ESCAPÓ     fuente-sin-licencia (familia nueva) (rc={rc})")
sys.exit(0 if rc == 1 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 9d. no ver ninguna fuente no puede dar verde =="
echo "   (un guardián de licencias que no encuentra fuentes da el verde más falso que hay)"
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
g.fuentes = lambda: []                   # el directorio está, pero no se ve nada
rc = g.main()
print("  ROJO  ok   sin-fuentes (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-fuentes (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 9e. la licencia y el README de fonts/ NO son fuentes =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
vistos = {p.name for p in (g.fuentes() or [])}
intrusos = sorted(n for n in vistos if not n.lower().endswith(tuple(g.EXT_FUENTE)))
familias = sorted({g._familia(p) for p in (g.fuentes() or [])})
print(f"  familias detectadas: {', '.join(familias)}")
if intrusos:
    print(f"  ESCAPÓ  se colaron archivos que no son fuentes: {intrusos}")
sys.exit(1 if intrusos else 0)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 10. sin manifiesto no se puede dar verde =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
g.manifiesto = lambda: None
rc = g.main()
print("  ROJO  ok   sin-manifiesto (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-manifiesto (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 11. si git no contesta, tampoco =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
g.rastreados = lambda: None
rc = g.main()
print("  ROJO  ok   sin-git (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-git (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 12. un manifiesto que no promete nada tampoco puede dar verde =="
python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import guard_paquete as g
pkg = g.manifiesto()
for k in ("exports", "files", "bin"):
    pkg.pop(k, None)
g.manifiesto = lambda: pkg
rc = g.main()
print("  ROJO  ok   sin-promesas (rc=2)" if rc == 2 else f"  ESCAPÓ     sin-promesas (rc={rc})")
sys.exit(0 if rc == 2 else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== 13. restauración =="
cp "$BK" "$PKG"
chmod +x bin/aglaya-tokens-version.mjs
python3 "$GUARD" && echo "  $PKG restaurado y verde"

echo
if [ "$fallos" -eq 0 ]; then
  echo "SABOTAJE: todo mordió (0 escapes)"
else
  echo "SABOTAJE: $fallos escape(s) — el guardián corre pero no protege"
fi
exit "$fallos"
