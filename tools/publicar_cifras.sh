#!/usr/bin/env bash
# publicar_cifras.sh — publica las cifras de esta nave en la rama huérfana
# `cifras`, según el contrato `cifras-publicas` v1. El formato es del capitán
# (repo `aglaya-orchestrator`): pregúntalo con `contrato("cifras-publicas")` del
# MCP `aglaya-atlas`.
#
# PARA QUÉ. El portafolio de Ibai publicaba cifras de esta nave escritas a mano,
# y se pudrían: el encargo decía `v1.3.2` con el repo ya en `1.3.6`. Con esto la
# cifra la mide quien la custodia, en CI, con fecha, y quien la publica la lee de
# aquí.
#
# QUÉ PUBLICA, y de dónde sale cada valor —SIEMPRE de esta misma ejecución—:
#
#   version             ← package.json del commit medido
#   tokens              ← salida de `node scripts/build-tokens.mjs` (job `paquete`)
#   herramientas_mcp    ← lista TOOLS REGISTERED de `selftest.py` (job `mcp`):
#                         el registro vivo del servidor, no un conteo tecleado
#   llamadas_autotest   ← línea `SELFTEST: N llamadas` de `selftest.py` (job `mcp`)
#   sabotajes_autotest  ← líneas `ROJO  ok` de `test_selftest.sh` (job `mcp`)
#
# LA REGLA QUE MÁS IMPORTA: una cifra que llega 0, vacía o sin forma NO SE
# PUBLICA. Hace fallar el job y deja en la rama la última medición buena, que
# con su fecha sigue siendo verdad. `sabotajes_autotest` se cuenta por líneas de
# salida porque `test_selftest.sh` no imprime un total: si esa línea cambia de
# forma, el conteo da 0 — y un 0 publicado sería exactamente la cifra podrida
# con fecha que este contrato existe para impedir.
#
# CÓMO NO DEJA LA RAMA A MEDIAS. Todo se valida ANTES de tocar git. Después se
# arma un commit completo en un directorio aparte y se publica con UN push, sin
# forzar: si otra ejecución publicó en medio, este falla en vez de pisarla.
#
# Entradas (entorno):
#   CIFRAS_TOKENS, CIFRAS_HERRAMIENTAS, CIFRAS_LLAMADAS, CIFRAS_SABOTAJES
#   CIFRAS_COMMIT      sha completo de main que se midió
#   CIFRAS_EJECUCION   URL de la ejecución de CI
# Costuras para la batería (sin red):
#   CIFRAS_REMOTO      repositorio al que se publica (por defecto `origin`)
#   CIFRAS_MEDIDO_EL   fecha fija
#   CIFRAS_SOLO_JSON   ruta: escribe ahí el JSON y no publica
#
# Exit: 0 publicado · 1 una cifra falta o no es válida (no se publica) ·
#       2 no se pudo construir o publicar (no se publica).

set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTO="${CIFRAS_REMOTO:-origin}"
RAMA="cifras"

falla() {
  echo "::error::publicar-cifras: $2"
  echo "No se publica nada: la última medición publicada sigue siendo la válida."
  exit "$1"
}

version="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['version'])" "$RAIZ/package.json" 2>/dev/null)" \
  || falla 2 "no pude leer la versión de package.json"
tokens="${CIFRAS_TOKENS:-}"
herramientas="${CIFRAS_HERRAMIENTAS:-}"
llamadas="${CIFRAS_LLAMADAS:-}"
sabotajes="${CIFRAS_SABOTAJES:-}"
commit="${CIFRAS_COMMIT:-}"
ejecucion="${CIFRAS_EJECUCION:-}"
medido_el="${CIFRAS_MEDIDO_EL:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"

# ── validar, antes de tocar git ──────────────────────────────────────────────
positivo() { [[ "$2" =~ ^[0-9]+$ ]] && [ "$2" -gt 0 ] \
  || falla 1 "$1 «$2» no es un recuento mayor que cero: el job que mide no lo emitió o su salida cambió de forma"; }

[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || falla 1 "version «$version» no es una versión"
positivo tokens             "$tokens"
positivo herramientas_mcp   "$herramientas"
positivo llamadas_autotest  "$llamadas"
positivo sabotajes_autotest "$sabotajes"
[[ "$commit" =~ ^[0-9a-f]{40}$ ]]                    || falla 1 "commit «$commit» no es un sha completo"
[[ "$ejecucion" =~ ^https://[^[:space:]]+$ ]]         || falla 1 "ejecucion «$ejecucion» no es una URL"
[[ "$medido_el" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] \
  || falla 1 "medido_el «$medido_el» no es UTC ISO 8601"

# ── construir el JSON ────────────────────────────────────────────────────────
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

VERSION="$version" TOKENS="$tokens" HERRAMIENTAS="$herramientas" LLAMADAS="$llamadas" \
SABOTAJES="$sabotajes" COMMIT="$commit" EJECUCION="$ejecucion" MEDIDO="$medido_el" \
python3 - > "$TMP/cifras.json" <<'PY' || falla 2 "no pude construir cifras.json"
import json, os
e = os.environ
print(json.dumps({
    "contrato": "cifras-publicas",
    "version": 1,
    "nave": "aglaya-design-system",
    "commit": e["COMMIT"],
    "medido_el": e["MEDIDO"],
    "ejecucion": e["EJECUCION"],
    "cifras": {
        "version": {"valor": e["VERSION"], "fuente": "package.json"},
        "tokens": {"valor": int(e["TOKENS"]), "unidad": "tokens",
                   "fuente": "node scripts/build-tokens.mjs (job `paquete` de esta ejecución)"},
        "herramientas_mcp": {"valor": int(e["HERRAMIENTAS"]), "unidad": "herramientas",
                             "fuente": "aglaya-ds-mcp/selftest.py: lista TOOLS REGISTERED del servidor (job `mcp`)"},
        "llamadas_autotest": {"valor": int(e["LLAMADAS"]), "unidad": "llamadas",
                              "fuente": "aglaya-ds-mcp/selftest.py: línea SELFTEST: N llamadas (job `mcp`)"},
        "sabotajes_autotest": {"valor": int(e["SABOTAJES"]), "unidad": "sabotajes",
                               "fuente": "aglaya-ds-mcp/test_selftest.sh: líneas «ROJO  ok» (job `mcp`)"},
    },
}, ensure_ascii=False, indent=2))
PY

if [ -n "${CIFRAS_SOLO_JSON:-}" ]; then
  cp "$TMP/cifras.json" "$CIFRAS_SOLO_JSON"
  echo "publicar-cifras: JSON escrito en $CIFRAS_SOLO_JSON (sin publicar)."
  exit 0
fi

# ── publicar: un commit completo, un push, sin forzar ────────────────────────
PUB="$TMP/pub"
git init -q "$PUB"
git -C "$PUB" remote add destino "$(git -C "$RAIZ" remote get-url "$REMOTO" 2>/dev/null || echo "$REMOTO")"
# Hereda las credenciales que deja actions/checkout, si las hay.
cabecera="$(git -C "$RAIZ" config --get http.https://github.com/.extraheader 2>/dev/null || true)"
[ -n "$cabecera" ] && git -C "$PUB" config http.https://github.com/.extraheader "$cabecera"
git -C "$PUB" config user.name  "github-actions[bot]"
git -C "$PUB" config user.email "41898282+github-actions[bot]@users.noreply.github.com"

if git -C "$PUB" fetch -q destino "$RAMA" 2>/dev/null; then
  git -C "$PUB" checkout -q -b "$RAMA" FETCH_HEAD
else
  # Primera publicación: rama HUÉRFANA, sin la historia de main.
  git -C "$PUB" checkout -q --orphan "$RAMA"
fi

cp "$TMP/cifras.json" "$PUB/cifras.json"
git -C "$PUB" add cifras.json
git -C "$PUB" commit -q -m "cifras: $version · $tokens tokens · $herramientas herramientas MCP · medido en ${commit:0:7}" \
  || falla 2 "no pude crear el commit de cifras"
git -C "$PUB" push -q destino "$RAMA:$RAMA" \
  || falla 2 "el push a la rama $RAMA falló (¿otra ejecución publicó en medio?)"

echo "publicar-cifras: publicado en $RAMA — $version · $tokens tokens · $herramientas herramientas · $llamadas llamadas · $sabotajes sabotajes."
