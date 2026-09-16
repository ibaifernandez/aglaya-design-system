# IMPLEMENTS — aglaya-design-system

Registro de qué contratos inter-nave **firma** esta nave, y cómo los cumple.
El texto de cada contrato vive en su dueño; aquí solo se declara la versión
firmada y dónde está la implementación. `firmas()` del MCP `aglaya-atlas` lee
este fichero en vivo.

**Lo que este fichero NO declara:** el contrato `marca`. De ese, esta nave es
**dueña**, no firmante. Su texto es [`docs/CONTRACT.md`](../CONTRACT.md).

---

## `cifras-publicas` · v1 — declarado 2026-09-16

**Papel:** productora. Esta nave mide sus propias cifras en su CI y las deja en
su rama huérfana `cifras`, para que quien las publique fuera las lea de ahí y
nunca las teclee. **Dueño del formato:** `aglaya-orchestrator`. Se pide con
`contrato("cifras-publicas")` al MCP `aglaya-atlas`.

| Cláusula del contrato | Implementación |
|---|---|
| `cifras.json` en la raíz de la rama huérfana `cifras` | job `publicar-cifras` de [`.github/workflows/huella.yml`](../../.github/workflows/huella.yml) → [`tools/publicar_cifras.sh`](../../tools/publicar_cifras.sh) |
| Solo desde una ejecución **en verde** sobre `main`, en un job que depende de los que miden | `if: push && refs/heads/main` · `needs: [docs, mcp, paquete]` |
| Cada valor sale de la salida de un comando **de esa misma ejecución** | los jobs `paquete` y `mcp` guardan la salida de sus comandos y [`tools/medir_cifras.py`](../../tools/medir_cifras.py) saca el número, que viaja como *output* del job |
| `contents: write` solo en ese job | `permissions: contents: read` arriba del workflow; `write` declarado solo en `publicar-cifras` |
| Solo cifras que la nave acepta publicar | las siete de abajo. Nada de clientes ni de datos de terceros: son cifras del propio sistema |

### Las cifras que publica

| Clave | Sale de |
|---|---|
| `version` | `package.json` del commit medido |
| `tokens` | salida de `node scripts/build-tokens.mjs` |
| `herramientas_mcp` | lista `TOOLS REGISTERED` que imprime `aglaya-ds-mcp/selftest.py`: el registro vivo del servidor |
| `llamadas_autotest` | línea `SELFTEST: N llamadas` de `aglaya-ds-mcp/selftest.py`, que solo existe si el selftest sale en verde |
| `llamadas_contestan` | cabeceras `== [ok] ` de `aglaya-ds-mcp/selftest.py`: las llamadas que deben contestar. No cuenta `[contenido]` ni `[canon]` |
| `llamadas_niegan` | cabeceras `== [rechaza] ` de `aglaya-ds-mcp/selftest.py`: las que deben negarse. Si sale 0 no se publica, porque un selftest sin rechazos lo pasaría un servidor que nunca falla |
| `sabotajes_autotest` | líneas `ROJO  ok` de `aglaya-ds-mcp/test_selftest.sh`, contadas solo si la batería termina sin escapes |

### Una medición mala no se convierte en cifra publicada

`tools/publicar_cifras.sh` **no publica** un recuento que llegue en 0, vacío o
sin forma, ni un `commit`, una `ejecucion` o un `medido_el` mal formados: sale en
rojo y no escribe nada. Tampoco publica si el desglose no cuadra
(`llamadas_contestan + llamadas_niegan ≠ llamadas_autotest`). La rama se queda con
la última medición buena. Lo fija
[`tools/test_publicar_cifras.sh`](../../tools/test_publicar_cifras.sh), que corre
en el job `docs` y publica contra un repositorio desnudo para comprobar tres
cosas: que la primera publicación crea una rama huérfana, que la segunda se
apila sin forzar y que un intento rechazado deja la rama intacta.

**Estado:** qué hay hoy publicado se lee en la propia rama
(`git show origin/cifras:cifras.json`), no en este fichero.
