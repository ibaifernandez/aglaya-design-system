#!/usr/bin/env bash
# La prueba de mutación: distingue CONSUMIR de COPIAR.
#
# Es la única comprobación que hace esa distinción. Una copia vendorizada pasa
# todo lo demás —instala, compila, se ve bien, el CI verde— y falla esta por
# construcción: se mueve un valor en el canon, se reconstruye en el consumidor
# sin tocar un solo archivo fuente suyo, y el valor entregado tiene que cambiar.
# Si no cambia, no está consumiendo: tiene una copia.
#
# Se montan DOS consumidores, y el segundo es el que da valor a la prueba:
#
#   A · depende del paquete por git   → el valor DEBE cambiar
#   B · copió el CSS a su repo        → el valor NO DEBE cambiar
#
# Sin B, esta prueba no demuestra nada: un script que siempre dice «cambió»
# también diría «cambió» de una copia. B es el control negativo que prueba que
# la prueba sabe distinguir. Es la misma lección que las baterías de sabotaje
# de los guardianes — una comprobación que no puede fallar no está comprobando.
#
# El canon se clona a un temporal y se muta AHÍ. Este repo no se toca: el clon
# es de lo COMMITEADO, que además es justo lo que verá un consumidor real.
#
# Se instala por `git+file://` en vez de `git+https://` para no depender de la
# red ni de que el tag ya esté empujado. Es el mismo camino de código de npm
# —clon de git, `prepare`, empaquetado—, solo cambia el transporte.
#
# Uso:  bash tools/test_mutacion.sh
# Sale: 0 el paquete se consume · 1 no se consume (o la prueba no discrimina)
#       · 2 no se pudo comprobar (sin node/npm/git, o nada que clonar).

set -u
cd "$(dirname "$0")/.."
RAIZ="$(pwd)"

TOKEN="--color-brand"
MUTADO="#1234ff"   # no está en la paleta: si aparece, viene de la mutación

for req in node npm git; do
  command -v "$req" >/dev/null 2>&1 || {
    echo "test-mutacion: NO SE PUDO COMPROBAR — falta '$req'"; exit 2; }
done

# El consumidor se ancla SIEMPRE a este nombre de rama, creado dentro del clon.
# Así su especificador de dependencia no cambia entre la instalación y la
# reinstalación — que es justo lo que la prueba tiene que demostrar que no hace
# falta tocar. Además evita depender de en qué rama esté HEAD aquí: en un CI de
# pull request está desprendido y `rev-parse --abbrev-ref` devuelve "HEAD".
RAMA="prueba-mutacion"

git -C "$RAIZ" cat-file -e "HEAD:package.json" 2>/dev/null || {
  echo "test-mutacion: NO SE PUDO COMPROBAR — package.json no está commiteado;"
  echo "               un consumidor clona lo commiteado, no tu working tree"
  exit 2; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

CANON="$TMP/canon"
fallos=0

valor_de() { # archivo css | token -> el valor declarado
  sed -n "s/^[[:space:]]*$2:[[:space:]]*\([^;]*\);.*/\1/p" "$1" | head -1 | tr -d ' '
}

echo "== 1. clon limpio del canon (lo commiteado) =="
git clone --quiet --no-hardlinks "$RAIZ" "$CANON" || {
  echo "  no pude clonar"; exit 2; }
git -C "$CANON" checkout --quiet -B "$RAMA" || {
  echo "  no pude fijar la rama de prueba en el clon"; exit 2; }
CANON_CSS="$CANON/colors_and_type.css"
ORIGINAL="$(valor_de "$CANON_CSS" "$TOKEN")"
[ -n "$ORIGINAL" ] || { echo "  el clon no declara $TOKEN"; exit 2; }
echo "  canon declara $TOKEN"

# ── consumidor A: depende ───────────────────────────────────────────────────
A="$TMP/consumidor-a"
mkdir -p "$A/src"
cat > "$A/package.json" <<JSON
{ "name": "consumidor-a", "version": "0.0.0", "private": true }
JSON
# Su hoja no contiene NI UN VALOR. Todo lo que pinta sale del paquete.
cat > "$A/src/marca.css" <<'CSS'
@import "@aglaya/design-tokens/tokens.css";
.hero { background: var(--color-brand); }
CSS

# ── consumidor B: copió (control negativo) ──────────────────────────────────
B="$TMP/consumidor-b"
mkdir -p "$B/src"
cp "$CANON_CSS" "$B/src/tokens-copia.css"
cat > "$B/src/marca.css" <<'CSS'
@import "./tokens-copia.css";
.hero { background: var(--color-brand); }
CSS

echo "== 2. el consumidor A no lleva ningún valor de marca escrito =="
if grep -Eq '#[0-9a-fA-F]{3,8}\b' "$A/src/marca.css"; then
  echo "  ESCAPÓ  el consumidor de prueba tiene valores propios — la prueba no valdría"
  fallos=$((fallos+1))
else
  echo "  ok  su hoja solo tiene var(--color-brand)"
fi

echo "== 3. instalación desde un clon de git (como haría un CI ajeno) =="
( cd "$A" && npm install --silent --no-audit --no-fund \
    "git+file://$CANON#$RAMA" >/dev/null 2>&1 ) || {
  echo "  la instalación falló"; exit 2; }

INSTALADO="$A/node_modules/@aglaya/design-tokens"
[ -f "$INSTALADO/colors_and_type.css" ] || {
  echo "  el paquete instalado no trae el CSS canónico"; exit 2; }

A_ANTES="$(valor_de "$INSTALADO/colors_and_type.css" "$TOKEN")"
B_ANTES="$(valor_de "$B/src/tokens-copia.css" "$TOKEN")"
echo "  A recibe del paquete el mismo valor que el canon: $([ "$A_ANTES" = "$ORIGINAL" ] && echo sí || echo NO)"
[ "$A_ANTES" = "$ORIGINAL" ] || fallos=$((fallos+1))

echo "== 3b. dist/ se fabricó al instalar (no venía commiteado) =="
if [ -f "$INSTALADO/dist/tokens.json" ]; then
  echo "  ok  el consumidor tiene tokens.json sin que el repo lo versione"
else
  echo "  ESCAPÓ  no hay dist/tokens.json — 'prepare' no corrió en la instalación"
  fallos=$((fallos+1))
fi

# Huella de los archivos FUENTE del consumidor. El lockfile queda fuera a
# propósito: reescribirlo es lo que significa «reconstruir», y lo hace npm.
huella() { find "$1/src" "$1/package.json" -type f -exec shasum {} \; | sort | shasum; }
A_HUELLA_ANTES="$(huella "$A")"

echo "== 4. se mueve el valor en el canon =="
sed -i.bak "s|^\([[:space:]]*$TOKEN:[[:space:]]*\)[^;]*;|\1$MUTADO;|" "$CANON_CSS"
rm -f "$CANON_CSS.bak"
[ "$(valor_de "$CANON_CSS" "$TOKEN")" = "$MUTADO" ] || {
  echo "  no conseguí mutar el canon"; exit 2; }
# Identidad explícita: un runner de CI limpio no tiene user.name configurado y
# `git commit` fallaría por eso, no por lo que la prueba mide.
git -C "$CANON" \
  -c user.email=mutacion@aglaya.invalid -c user.name="prueba de mutación" \
  commit --quiet -am "mutación de prueba" || {
  echo "  no pude commitear la mutación"; exit 2; }
echo "  $TOKEN mutado y commiteado en el clon"

echo "== 5. el consumidor A reconstruye sin tocar un archivo fuente suyo =="
( cd "$A" && npm install --silent --no-audit --no-fund \
    "git+file://$CANON#$RAMA" >/dev/null 2>&1 ) || {
  echo "  la reinstalación falló"; exit 2; }

A_DESPUES="$(valor_de "$INSTALADO/colors_and_type.css" "$TOKEN")"
B_DESPUES="$(valor_de "$B/src/tokens-copia.css" "$TOKEN")"
A_HUELLA_DESPUES="$(huella "$A")"

if [ "$A_HUELLA_ANTES" = "$A_HUELLA_DESPUES" ]; then
  echo "  ok  sus archivos fuente están byte a byte igual que antes"
else
  echo "  ESCAPÓ  cambiaron archivos del consumidor — entonces no prueba nada"
  fallos=$((fallos+1))
fi

echo "== 6. veredicto =="
if [ "$A_DESPUES" = "$MUTADO" ] && [ "$A_DESPUES" != "$A_ANTES" ]; then
  echo "  CONSUME  ok   A: el valor entregado cambió con el canon"
else
  echo "  COPIA    ESCAPÓ   A: el valor NO cambió — el paquete entrega algo congelado"
  fallos=$((fallos+1))
fi

if [ "$B_DESPUES" = "$B_ANTES" ]; then
  echo "  COPIA    ok   B (control negativo): su copia siguió pintando el valor viejo"
else
  echo "  ESCAPÓ   B cambió sin depender — la prueba no está midiendo lo que cree"
  fallos=$((fallos+1))
fi

echo
if [ "$fallos" -eq 0 ]; then
  echo "MUTACIÓN: el paquete se consume (y la prueba distingue una copia)"
else
  echo "MUTACIÓN: $fallos fallo(s)"
fi
exit "$fallos"
