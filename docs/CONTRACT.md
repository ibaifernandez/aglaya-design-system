# CONTRACT - AGLAYA Design System

- **Propietario canónico:** este mismo repo.
- **Registro en el atlas:** el registro de contratos inter-nave, repo `aglaya-orchestrator` → `atlas/contratos/README.md`, o pregúntalo sin saber dónde vive: `contrato("marca")`. Ahí vive la fila de este contrato: quién lo posee y quién lo consume. *(La ficha de la nave, `ficha("aglaya-design-system")`, es contexto — describe el diseño acordado, no lo que hay en disco.)* La fuente de la verdad es este repo y en cualquier caso, manda la _codebase_ del repo. En definitiva:

codebase → MCP que lee la codebase → docs del repo → ficha del atlas

## Misión

- Este repo rige el sistema de diseño de la identidad de la marca AGLAYA: tokens, tipografía, voz, logos.
- A nivel de identidad de marca, esta carpeta manda y las demás consumen de ella (nunca al revés): `aglaya.biz` y toda otra superficie con marca AGLAYA (materiales, portafolio de agencia), incluyendo contenidos para redes sociales.

## Interfaces (dos formas de consumir)

- **SKILL `aglaya-design`** (`SKILL.md`, en la raíz de este repo): generar artefactos/código _on-brand_/no-negociables (ver MCP a continuación).
- **MCP `aglaya-ds`**: consultar en vivo (`aglaya-ds-mcp/server.py`, en este repo)

## No consumidores

- Los **dummies de `aglaya-web`**: cada uno tiene su propio sistema de diseño: **jamás cablear un _dummy_ a esta marca**.

## Qué impone al consumidor

Esto es lo que hace de esto un contrato y no una descripción. Son obligaciones, no sugerencias:

- **Construir con estos tokens y esta voz**, pedidos a `aglaya-ds` (`get_token`, `list_tokens`, `get_voice_rules`) — no copiados a un archivo del consumidor.
- **Respetar los no-negociables**, que sirve `get_nonnegotiables()` leyendo `SKILL.md` en vivo. No se parafrasean ni se listan aquí: un no-negociable copiado es un no-negociable que caduca sin avisar.
- **No derivar marca de ningún otro repo.** La dirección es esta carpeta → el consumidor, nunca al revés ni de lado.
