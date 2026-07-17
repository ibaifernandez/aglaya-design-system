# CLAUDE.md — aglaya-design-system

## Qué es este repo

**La fuente CANÓNICA y SOBERANA de la identidad de marca AGLAYA** — tokens, tipografía, voz y logos. Todas las superficies AGLAYA **consumen de aquí**, nunca al revés: un token cambia *aquí primero* y las superficies siguen. Nada aguas arriba de esta carpeta es autoritativo.

## Orden de lectura

1. [`README.md`](README.md) — el canon: tokens, tipografía, voz, no-negociables.
2. [`SKILL.md`](SKILL.md) — la skill de marca (fuente de los no-negociables que sirve el MCP).
3. [`docs/CONTRACT.md`](docs/CONTRACT.md) — **el contrato de marca local** (v1.0.0, tag `v1.0.0`): qué expone este repo, qué excluye (los 6 dummies de `ui_kits/`), y el puntero al registro de contratos de la flota.
4. `aglaya-ds-mcp/` — el **servidor MCP `aglaya-ds`** (7 tools read-only: `get_token`, `list_tokens`, `get_logo`, `get_voice_rules`, `check_voice`, `is_allowed_word`, `get_nonnegotiables`). Es la vía programática de consumo de marca para toda la flota.

## Reglas duras

- Los **no-negociables de marca** los sirve el MCP (`get_nonnegotiables`) desde `SKILL.md` — no los parafrasees: consúltalos.
- Los 6 kits de `ui_kits/` marcados como dummy en `docs/CONTRACT.md` **no son marca AGLAYA** — no los cites como referencia.
- Regla de marca AGLAYA: **eliminar > legacy**. Lo obsoleto se borra, no se archiva.
- `graphify-out/`: se versionan solo los esenciales (`graph.json`, `GRAPH_REPORT.md`, `manifest.json`, `cost.json`); el resto es regenerable.

## AGLAYA · Flota — el capitán

Este repo es una **nave de la flota AGLAYA**. Existe un orquestador (el «capitán», repo `aglaya-orchestrator` en `/Users/AGLAYA/Local Sites/aglaya-orchestrator`) cuyo atlas es la fuente de verdad **de flota**: registro de contratos inter-nave (`atlas/contratos/README.md`), fichas por nave (`atlas/repos/aglaya-design-system/`) y tablero global (`atlas/tablero.md`).

Reglas para cualquier hilo que trabaje aquí:
- **Antes de un cambio estructural** (tokens, voz, contrato de marca, tools del MCP), consulta el registro de contratos del atlas — toda superficie AGLAYA consume de este repo.
- **El capitán puede haber tocado docs de este repo**: sus commits van identificados. Este repo no lleva CHANGELOG — el registro es el git log.
- La verdad comercial (precios, ofertas, GTM) NO vive aquí: vive en el atlas del capitán (`atlas/gtm.md`).

**Último pase del capitán: 2026-07-17** — re-verificación 7/7 (cerrada por primera vez el 15-jul): MCP vivo (7 tools), `CONTRACT.md` + tag `v1.0.0` verificados, este `CLAUDE.md` creado (no existía entrada para agentes), grafo fresco commiteado y republicado al global.
