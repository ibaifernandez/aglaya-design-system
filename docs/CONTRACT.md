# CONTRACT - AGLAYA Design System

- **Propietario canónico:** este mismo repo.
- **Registro en el atlas:** el registro de contratos inter-nave lo custodia el capitán (repo `aglaya-orchestrator`) y se pide por la puerta: `contrato("marca")` del MCP `aglaya-atlas` — contesta citando su fuente. Ahí vive la fila de este contrato: quién lo posee y quién lo consume. La ficha de la nave, `ficha("aglaya-design-system")`, es contexto: describe el diseño acordado, no lo que hay en disco. *(No se escriben aquí rutas internas del atlas: caducan en cuanto el capitán reorganiza.)* La fuente de la verdad es este repo y en cualquier caso, manda la _codebase_ del repo. En definitiva:

codebase → MCP que lee la codebase → docs del repo → ficha del atlas

## Misión

- Este repo rige el sistema de diseño de la identidad de la marca AGLAYA: tokens, tipografía, voz, logos.
- A nivel de identidad de marca, esta carpeta manda y las demás consumen de ella (nunca al revés): `aglaya.biz` y toda otra superficie con marca AGLAYA (materiales, portafolio de agencia), incluyendo contenidos para redes sociales.

## Interfaces (tres formas de consumir)

- **PAQUETE `@aglaya/design-tokens`**: depender de los tokens desde otro repo, anclado a un tag por `git+https`. Es la única vía que sobrevive a un CI ajeno, que clona el repo del consumidor y no este. Cómo se depende, cómo se versiona y qué pasa cuando un nombre choca: [`PACKAGE.md`](PACKAGE.md).
- **SKILL `aglaya-design`** (`SKILL.md`, en la raíz de este repo): generar artefactos/código _on-brand_/no-negociables (ver MCP a continuación).
- **MCP `aglaya-ds`**: consultar en vivo (`aglaya-ds-mcp/server.py`, en este repo)

Las tres leen los mismos archivos canónicos. Ninguna guarda una copia, y esa es la propiedad que se defiende: la prueba de mutación (`tools/test_mutacion.sh`) mueve un valor aquí y exige que le cambie al consumidor sin que él toque nada.

## No consumidores

- Los **dummies de `aglaya-web`**: cada uno tiene su propio sistema de diseño: **jamás cablear un _dummy_ a esta marca**.

## Qué impone al consumidor

Esto es lo que hace de esto un contrato y no una descripción. Son obligaciones, no sugerencias:

- **Construir con estos tokens y esta voz**, pedidos a `aglaya-ds` (`get_token`, `list_tokens`, `get_voice_rules`) — no copiados a un archivo del consumidor.
- **Respetar los no-negociables**, que sirve `get_nonnegotiables()` leyendo `SKILL.md` en vivo. No se parafrasean ni se listan aquí: un no-negociable copiado es un no-negociable que caduca sin avisar.
- **No derivar marca de ningún otro repo.** La dirección es esta carpeta → el consumidor, nunca al revés ni de lado.
- **Depender, no vendorizar.** Si se consumen tokens, se hace por el paquete anclado a un tag — nada de `file:`, de rutas relativas ni de copiar el CSS al repo del consumidor. Una copia pasa cualquier comprobación menos la de mutación, que es la única que decide.
- **Renombrar en casa cuando un nombre choca.** El vocabulario de tokens lo fija este repo. Un consumidor que ya use uno de estos nombres con otro valor renombra el suyo: aquí no hay mapa de alias, ni lo va a haber.
- **Pedir aquí lo que falte.** Un token que el consumidor necesita y este repo no declara se pide aquí y se publica como versión menor. Inventarlo allí es empezar la deriva otra vez.
