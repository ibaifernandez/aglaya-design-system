# Fase B — Seguridad, datos y arquitectura

Auditoría `aglaya-design-system-2026-09-24-mariana` · commit auditado `17d95cc` · modo `report`.

## Cuadro de evidencias — Fase B

| Confianza    | Nº | % de la fase |
|--------------|----|--------------|
| PROVEN       | 8  | 80 %         |
| UNVERIFIABLE | 2  | 20 %         |
| **Total**    | **10** | 100 %    |

Fuente de la evidencia: code-read 3 · tool-external 5 · manual-verification 0.
Aquí «tool-external» significa cuatro cosas: `npm view`, `pip-audit`, las mutaciones sobre un clon en un temporal y la ejecución directa del core del MCP. Esta última es la base de B-06.

Salud: 80 % PROVEN, por encima del 60 %.

## Qué se ha mirado, y qué no aplica

Este repo no tiene login, sesiones, subidas, API de red, webhooks, CORS, cabeceras HTTP servidas ni base de datos. Los puntos 1 a 7 y 9 de la lista de seguridad del protocolo, y la lista de base de datos entera, **no aplican**: no hay superficie. Lo que sí tiene superficie:

- **El paquete.** Otros repos lo instalan, y al instalarlo se ejecuta `prepare`.
- **El comando `aglaya-tokens-version`.** La documentación manda ejecutarlo con `npx`.
- **El servidor MCP.** Corre local, por stdio, y lee ficheros.
- **Las dependencias del MCP.**
- **Los tres lectores del CSS canónico y los guardianes.** Si alguno se equivoca, la flota recibe una marca equivocada.

## Tabla de hallazgos

| ID | Confianza | Dim | Hallazgo | Evidencia | OWASP / CVSS o ref. | Severidad | Esfuerzo |
|----|-----------|-----|----------|-----------|---------------------|-----------|----------|
| B-01 | PROVEN | seguridad | La doc manda `npx aglaya-tokens-version`, ese nombre está libre en npm y npm lo instalaría solo en un CI | `README.md:244`, `docs/PACKAGE.md:127`, `:132`, `evidencia/npm-registro.txt` | A08:2021 · CVSS 7.5 `AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` | ALTA | 0,5 h |
| B-02 | PROVEN | dependencias | El venv del MCP que monta cada sesión lleva 7 vulnerabilidades conocidas, y nada fija ni vigila las versiones | `evidencia/pip-audit-venv.txt`, `aglaya-ds-mcp/pyproject.toml:22-24`, `.github/workflows/huella.yml:85-87` | DevOps: dependencias con CVE; sin camino de explotación (regla de reducción 2) | BAJA | 1 h |
| B-03 | PROVEN | arquitectura | Un `}` dentro de un comentario de `:root` hace que el MCP sirva 1 token en vez de 87, sin avisar | `aglaya-ds-mcp/brand.py:87-88`, `scripts/build-tokens.mjs:35`, `:69`, `tools/guard_valores.py:118`, `:144-147`, `evidencia/mutaciones.txt` | robustez del canon | MEDIA | 1 h |
| B-04 | PROVEN | arquitectura | `guard_punteros` no mira las rutas `.otf`, y las 18 URLs de Inter quedan sin vigilar | `tools/guard_punteros.py` (constante `EXTENSIONES`), `evidencia/mutaciones.txt` | promesa de un guardián | MEDIA | 0,25 h |
| B-05 | PROVEN | contrato | El MCP no sirve el modo claro y el paquete sí: las dos vías de consumo dicen cosas distintas | `aglaya-ds-mcp/brand.py:84-92`, `scripts/build-tokens.mjs:43-45`, `:76-98`, `docs/CONTRACT.md:18`, `:30` | contrato de consumo | MEDIA | 2 h |
| B-06 | PROVEN | interfaz | Las descripciones de las tools y el README del MCP anuncian cosas que el código no hace | `aglaya-ds-mcp/server.py:70`, `:157`, `:165`, `aglaya-ds-mcp/README.md:26`, `:130`, `:153` | documentación de API | BAJA | 0,5 h |
| B-07 | PROVEN | canon | El manifiesto de productos se contradice con el CSS y conserva una «PROPUESTA» ya publicada | `products/products.json:71`, `:142`, `colors_and_type.css:63-64` | coherencia | BAJA | 0,25 h |
| B-08 | PROVEN | canon | `.t-codetag` no cambia con el modo y no casa con su ficha | `colors_and_type.css:324-329`, `components/components.json:108` | coherencia | BAJA | 0,25 h |
| B-NV-01 | UNVERIFIABLE · NV_TOOL | dependencias | React, ReactDOM y Babel vendorizados sin escanear | `ui_kits/website/vendor/` | — | — | — |
| B-NV-02 | UNVERIFIABLE · NV_CREDENTIALS | secretos | Historia de git sin revisar en busca de secretos | — | — | — | — |

**Recuento:** CRÍTICA 0 · ALTA 1 · MEDIA 3 · BAJA 4 · UNVERIFIABLE 2.

---

## Detalle

### B-01 · `npx aglaya-tokens-version` puede ejecutar código de un tercero

- **Qué pasa.** La doc manda comprobar la versión con `npx aglaya-tokens-version` (`README.md:244`, `docs/PACKAGE.md:127`, y en `CLAUDE.md`), y propone `--strict` como «gate para un paso de CI» (`docs/PACKAGE.md:132`). `npx` busca primero el comando en el `node_modules` del proyecto. Si no lo encuentra, lo pide al registro público de npm. Y la documentación de npm dice que **en CI, o sin terminal interactiva, instala sin preguntar**: «When standard input is not a TTY or a CI environment is detected, `--yes` is assumed» (`evidencia/npm-registro.txt`, citando `npm-exec.md:28-29`).
- **El nombre está libre.** `npm view aglaya-tokens-version` devuelve 404 (`evidencia/npm-registro.txt`). Cualquiera puede registrarlo mañana.
- **Contexto.** El ámbito `@aglaya` del registro npm ya lo usa otra organización (publica `@aglaya/eslint-config`, repo AglayaInnovation). AGLAYA no puede reclamar ese ámbito, y `@aglaya/design-tokens` no existe allí (404).
- **Cadena del ataque.**
  1. Alguien publica `aglaya-tokens-version` en npm.
  2. Un job de CI de una nave ejecuta `npx aglaya-tokens-version --strict` sin tener instalado el paquete: un job de comprobación que corre antes de `npm ci`, o un repo que ya quitó la dependencia.
  3. npx descarga ese paquete y lo ejecuta con los secretos del CI.
- **Campos del rubric.**
  - OWASP A08:2021, Fallos de integridad de software y datos.
  - CVSS 3.1 `AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` = **7.5**. AC:H porque depende de que el entorno no tenga el paquete instalado.
  - Atacante: ninguno previo. Interacción: sí, alguien tiene que ejecutar el comando. Alcance: sin cambio. Impacto: C, I y A altos.
  - Hoy nadie lo explota: el nombre está sin registrar.
- **Quién usa el comando hoy.** Según `quien_lee("aglaya-tokens-version")`, aglaya.biz lo nombra en su `package.json`. Si lo llama desde un script de npm, usa el binario local y está a salvo. El riesgo es la instrucción con `npx` escrita en la doc.
- **Arreglo.** Cualquiera de estas tres opciones, o varias:
  - que la doc diga `npm exec --no -- aglaya-tokens-version`, que falla en vez de descargar;
  - registrar el nombre en npm como marcador defensivo;
  - decir en la doc que el comando solo es válido después de `npm ci`.

### B-02 · Dependencias del MCP sin fijar ni vigilar

- **Qué pasa.** `pip-audit` sobre el venv local del MCP, que es el que monta `.mcp.json` en cada sesión de esta nave, encuentra **7 vulnerabilidades conocidas en 3 paquetes**: `anyio`, `cryptography` y `httpx2`, las tres con versión arreglada disponible (`evidencia/pip-audit-venv.txt`). Se corrió con `--no-deps --disable-pip`, sin instalar nada.
- **Por qué nada lo detecta.** El repo solo declara `mcp>=2.0.0` (`aglaya-ds-mcp/pyproject.toml:22-24`). No hay lockfile ni hashes. El CI instala lo último que haya en cada ejecución (`.github/workflows/huella.yml:85-87`), así que no se puede reproducir, y el venv local nadie lo refresca. Dependabot no está configurado (D-05).
- **Por qué es BAJA y no MEDIA.**
  - Por el rubric de DevOps, dependencias con CVE conocidos es MEDIA.
  - Los avisos tocan TLS con dominios internacionalizados, pools de procesos, descifrado PKCS7 y un cliente HTTP.
  - El MCP no usa nada de eso: habla por stdio y `aglaya-ds-mcp/brand.py` solo lee ficheros con la biblioteca estándar.
  - Por eso se aplica la regla de reducción 2 (sin camino de explotación).
- **Arreglo.** Fijar las versiones con hashes (`pip-compile --generate-hashes`), dar a Dependabot el ecosistema `pip` y recrear el venv local.

### B-03 · Un `}` en un comentario deja la marca en un token

- **Qué pasa.** Los tres lectores del CSS canónico recortan `:root` con la misma expresión, `:root\s*\{(.*?)\}`, que se para en la **primera** llave de cierre. Y lo hacen **antes** de quitar los comentarios:
  - `aglaya-ds-mcp/brand.py:87-88`
  - `scripts/build-tokens.mjs:35`, `:69`
  - `tools/guard_valores.py:118`, `:144-147`
- **Mutación.** Sobre un clon en un temporal (el repo no se toca), se añade `/* nota: ver {x} */` dentro de `:root` (`evidencia/mutaciones.txt`):
  - **el MCP sirve 1 token en vez de 87, sin error**, y `get_token("color-brand-dark")` responde que no existe;
  - el build del paquete sale con código 1 y un error que no nombra la causa: «el modo 'light' declara tokens que no existen en :root»;
  - `guard_valores` se pone rojo por otro motivo: «manifiesto-desincronizado».
- **Por qué la prueba de paridad no lo caza.** `tools/test_parsers_comentarios.sh` compara que los tres lectores coincidan. Con esta avería coinciden, porque los tres fallan igual.
- **Atenuante.** En CI se pondría rojo (el build y el selftest caen), así que no llegaría a publicarse en silencio **si** alguien exige el verde antes de fusionar. Hoy nadie lo exige (D-03). Y en local, el MCP montado en la sesión serviría 1 token sin decir nada.
- **Severidad.** MEDIA. Arquitectura: lógica duplicada con un defecto compartido.
- **Arreglo.** Quitar los comentarios **antes** de recortar el bloque, en los tres lectores, y añadir este caso a la prueba de paridad.

### B-04 · Guardián de punteros ciego a `.otf`

- **Qué pasa.** `tools/guard_punteros.py` reconoce una ruta por su extensión, y en su lista (`EXTENSIONES`) está `ttf` pero no `otf`.
- **Mutación en un clon** (`evidencia/mutaciones.txt`):
  - se renombra la URL de `Inter-Regular.otf` en `colors_and_type.css`, y **los cuatro guardianes dan 0**;
  - se renombra la de `SpaceMono-Regular.ttf`, y `guard_punteros` sale con 1.
- **Consecuencia.** Las 18 caras de Inter (`colors_and_type.css:27-44`) pueden apuntar a un fichero que no existe sin que nada lo avise. El navegador tiraría de la fuente de reserva en todas las superficies. `CLAUDE.md` promete que este guardián caza «una ruta rota escrita fuera de markdown».
- **Severidad.** MEDIA: la promesa de un guardián no se cumple para 18 de 31 URLs de fuente.
- **Arreglo.** Añadir `otf` (y `woff`/`woff2`) a `EXTENSIONES`, y un caso a `tools/test_guard_punteros.sh`.

### B-05 · El MCP y el paquete no sirven lo mismo

- **Qué pasa.** El paquete publica el modo claro (`modes.light`, `scripts/build-tokens.mjs:43-45`, `:76-98`). El MCP solo lee `:root` (`aglaya-ds-mcp/brand.py:84-92`), así que `get_token` y `list_tokens` devuelven los valores del oscuro sin mencionar que hay otro modo. En el MCP no aparece `light` ni `data-theme` (grep).
- **Por qué importa.** El contrato dice que «las dos leen los mismos archivos canónicos» (`docs/CONTRACT.md:18`) y obliga a construir con tokens «pedidos a `aglaya-ds`» (`docs/CONTRACT.md:30`). Quien siga el contrato para montar el modo claro recibe valores equivocados. Hay una nave con el modo claro en producción (legal-reg-tech, según `quien_lee`).
- **Severidad.** MEDIA: contrato de consumo incumplido por una de las dos vías.
- **Arreglo.** Que `list_tokens` y `get_token` acepten un modo, o que devuelvan los dos valores. Es un cambio de interfaz del MCP: consultar antes el registro de contratos, como dice `CLAUDE.md`.

### B-06 · Descripciones del MCP que no coinciden con el código

Lo que lee un agente antes de llamar a una tool no coincide con lo que la tool hace. Se ha comprobado llamando al core (`BrandError`):

| Dónde | Qué dice | Qué pasa |
|---|---|---|
| `aglaya-ds-mcp/server.py:157` (y `aglaya-ds-mcp/brand.py:650`) | ConsentFlow tiene glifo `'color' \| 'light'` | `get_glyph("consent-flow","light")` → «Available: color». El propio manifiesto dice que no hay variante clara (`products/products.json:79`) |
| `aglaya-ds-mcp/server.py:165` (y `aglaya-ds-mcp/brand.py:678-679`) | lockups `'lockup-outlined'`, `'lockup-ondark'` | los dos → «Available: lockup, stacked» |
| `aglaya-ds-mcp/server.py:70` | las categorías son color, type, spacing, radius, motion, shadow, other | falta `product`, que vale y devuelve 8 tokens |
| `aglaya-ds-mcp/README.md:26` | llamar a `list_tokens()` sin argumento enseña las categorías | devuelve todos los tokens, y las categorías solo salen en el mensaje de error de una inválida (`aglaya-ds-mcp/brand.py:114-135`) |
| `aglaya-ds-mcp/README.md:130` | «sacred ConsentFlow has no glyph» | ConsentFlow tiene glifo (`products/products.json:76-78`) y `sacred: false` |
| `aglaya-ds-mcp/README.md:153` | «`server.py` — FastMCP server» | usa `MCPServer` (`aglaya-ds-mcp/server.py:30`); FastMCP se retiró con mcp 2.0 (`aglaya-ds-mcp/pyproject.toml:9-13`) |

- **Severidad.** BAJA. Se mide con la tabla de docs y API. Baja porque el error de la tool devuelve la lista buena y el agente se corrige solo.

### B-07 · El manifiesto de productos contradice el CSS

- **Qué pasa.** ConsentFlow tiene `"sacred": false` (`products/products.json:71`), mientras que el CSS marca sus dos acentos como «sacred» (`colors_and_type.css:63-64`). `list_products` sirve el `false`.
- **Qué más.** DESIGN SYSTEM lleva «PROPUESTA — confirmar color y nombre» (`products/products.json:142`), aunque su token `--product-design-system-accent` ya se publicó en v1.3.6 y el MCP lo sirve como canon.
- **Severidad.** BAJA. **Decide Ibai:** si ConsentFlow es sagrado, y si se confirma la propuesta.

### B-08 · `.t-codetag` no sigue al modo

- **Qué pasa.** La clase canónica lleva el fondo casi blanco y el `#000 !important` escritos a mano (`colors_and_type.css:324-329`). En claro sigue siendo legible, pero es una ficha blanca sobre página blanca. Y no casa con su ficha, que pone el fondo en `var(--color-text)` (`components/components.json:108`) y en claro da negro sobre negro (A-02).
- **Severidad.** BAJA.

### B-NV-01 · Librerías vendorizadas sin escanear · UNVERIFIABLE (NV_TOOL)

- **Qué hay.** `ui_kits/website/vendor/` lleva React y ReactDOM 18.3.1 y Babel standalone. Sus helpers internos están en la 7.27 o posterior, y el comentario del kit dice 7.29.0 (`ui_kits/website/index.html:31`). A la fecha de corte de mi conocimiento no hay CVE conocidos para esas versiones que afecten a este uso, pero sin un escáner no se puede afirmar más.
- **Acción externa.** `trivy fs ui_kits/website/vendor` u `osv-scanner`.

### B-NV-02 · Historia de git sin revisar en busca de secretos · UNVERIFIABLE (NV_CREDENTIALS)

- **Qué se intentó.** Buscar en la historia patrones de secreto y ficheros de entorno. El enganche de esta nave lo bloqueó: «leer o escribir un fichero de secretos». No hay `gitleaks` ni `trufflehog`, y el secret scanning de GitHub está apagado (D-05).
- **Acción externa.** Activar el secret scanning de GitHub, que en un repo público es gratis y revisa toda la historia al activarse, o pasar `gitleaks detect` a mano.

---

## Arquitectura: las tres señales del protocolo

- **Dependencias internas.** El script de fan-in del protocolo no encuentra ninguna relación, porque busca el nombre entre comillas. La única importación interna es `import brand` en `aglaya-ds-mcp/server.py:32`. Las piezas del kit se hablan por `window`, no por imports. No hay centro de gravedad ni ciclos.
- **Tamaños.**
  - El fichero más grande es `aglaya-ds-mcp/brand.py`, con 795 líneas: 103 en blanco, 131 de comentario, unas 65 de docstring y **unas 496 de código**, en 30 funciones. La más larga es `check_voice`, con 96 líneas.
  - Medido en líneas de código, queda por debajo del umbral de 700 del protocolo. Es cohesivo: seis secciones, una por fuente canónica. **No se recomienda partirlo.**
  - Le siguen `tools/guard_valores.py` (475) y `tools/guard_paquete.py` (313). Son guardianes con docstrings largos a propósito.
- **Profundidad y reparto.** El nivel máximo es 3 (`ui_kits/website/vendor/`). El directorio más poblado es `fonts/`, con 35 ficheros binarios. Nada se hunde.
- **Duplicación consciente.** Los tres lectores del CSS son deliberados: están en Node, en el Python del venv y en el `python3` del sistema (`tools/test_parsers_comentarios.sh:5-8`). Que el guardián no reutilice el lector del MCP también tiene sentido, porque un vigilante que usa el mismo código que vigila no puede cazar sus fallos. El coste de esta decisión es B-03.

## Verificaciones en positivo

- **`get_logo` no permite traversal.** Valida tipo, color y formato contra listas cerradas antes de construir la ruta (`aglaya-ds-mcp/brand.py:542-558`). Las rutas de glifos y lockups salen del manifiesto canónico, no de lo que envía quien llama.
- **`bin/aglaya-tokens-version.mjs`** llama a `git` con `execFileSync` y los argumentos en lista, sin shell, con un tiempo máximo de 20 s y `GIT_TERMINAL_PROMPT=0` (`bin/aglaya-tokens-version.mjs:83-88`). «No pude comprobar» nunca sale como «al día»: sale con código 2.
- **`scripts/build-tokens.mjs`** solo escribe en `dist/` y falla alto si un bloque sale vacío o si un modo inventa nombres (`:59-63`, `:89-94`).
- **El paquete no tiene dependencias npm**, así que `npm audit` no tiene nada que auditar.
- **`tools/publicar_cifras.sh` valida cada valor con una expresión cerrada antes de tocar git** (`:77-92`). Los valores no se pueden inyectar en el mensaje del commit ni en el JSON. Publica sin forzar y, si otra ejecución se adelantó, falla.
- **El workflow declara permisos de solo lectura** y concede `contents: write` solo al job que publica las cifras (`.github/workflows/huella.yml:23-24`, `:201-202`).
- **El selftest del MCP declara qué llamadas deben fallar** y lo comprueba, para que un servidor que nunca falla no pase (`aglaya-ds-mcp/selftest.py:1-20`).
- **El CI de `main` está en verde en el commit auditado:** `gh run list --branch main` devuelve `17d95cc push guardianes → completed/success`.
