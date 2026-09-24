# Hoja de ruta de remediación — aglaya-design-system

**Auditoría de origen:** `REPORT.md` de esta misma carpeta · commit `17d95cc` · generada el 2026-09-24.

**Esto es una propuesta, no obra en marcha.** No se ha arrancado nada: decide Ibai qué entra, cuándo y quién.

La prioridad sale de la severidad:
- **P0:** CRÍTICA, o exposición legal.
- **P1:** ALTA.
- **P2:** MEDIA.
- **P3:** BAJA o INFO.

El protocolo pone P0 en el sprint 1 y P1 en el 2. Aquí P0 es media hora de trabajo, así que se juntan.

**Columna «Paquete».** «sí» quiere decir que el arreglo toca un fichero que viaja en `@aglaya/design-tokens` (`files` de `package.json`, más README, LICENSE y el propio `package.json`, que npm incluye siempre). No le llega a nadie hasta que se publique una versión, y el nivel lo fija `docs/PACKAGE.md:85-92`. «no» quiere decir que el cambio llega en vivo por el MCP, o que no sale del repo.

---

## Sprint 1 — P0 y P1 (≈ 5,75 h)

| Hallazgo | P | Esfuerzo | Paquete | Qué hacer |
|---|---|---|---|---|
| C-01 · código MIT redistribuido sin su licencia | P0 | 0,5 h | sí (`LICENSE`) | Poner el texto MIT de React y de Babel junto a los minificados y exceptuar la carpeta vendor en la sección 1 de `LICENSE` |
| B-01 · `npx aglaya-tokens-version` puede bajar código ajeno | P1 | 0,5 h | sí (`docs/PACKAGE.md`) | Cambiar la instrucción a `npm exec --no -- aglaya-tokens-version` en `README.md:244`, `docs/PACKAGE.md:127` y `CLAUDE.md`. Opcional: registrar el nombre en npm como marcador |
| A-02 · fichas de componente rotas en modo claro | P1 | 2 h | no (MCP en vivo) | Pasar las tintas a `color-mix` sobre `--color-text`, el verde a `--fg-eyebrow`, blanco sobre el rojo y el codetag con `--color-bg` de letra |
| A-05 · animaciones infinitas sin pausa | P1 | 1 h | no | `@media (prefers-reduced-motion: reduce)` y un control de pausa para la marquesina |
| A-06 · etiqueta sin asociar | P1 | 0,25 h | no | `htmlFor` e `id` |
| A-07 · `PrimaryButton` siempre es un enlace | P1 | 1 h | no | `<button type="submit">` cuando no haya `href`, y mensaje de error accesible |
| A-12 · preview/ sin idioma, título ni viewport | P1 | 0,5 h | no | Tres líneas en cada uno de los 23 ficheros |

## Sprint 2 — P2 (≈ 17 h)

Dentro del sprint, primero lo barato y con más palanca: las tres primeras filas son 45 minutos y convierten el sistema de guardianes en una compuerta de verdad.

| Hallazgo | Esfuerzo | Paquete | Qué hacer |
|---|---|---|---|
| D-03 · el CI no se exige para fusionar | 0,25 h | no | Checks obligatorios en el ruleset de `main` |
| D-04 · los tags se pueden mover | 0,25 h | no | Ruleset de tags `v*`: sin actualizar ni borrar |
| B-04 · guardián ciego a `.otf` | 0,25 h | no | Añadir `otf`, `woff` y `woff2` a `EXTENSIONES` y un caso a su batería |
| B-03 · `}` en un comentario deja la marca en 1 token | 1 h | sí (`scripts/`) | Quitar los comentarios antes de recortar el bloque, en los tres lectores, y añadir el caso a la prueba de paridad |
| A-01 · `--fg-brand` es una tinta prohibida | 0,5 h | sí (parche) | Sale de la regla ya escrita (`docs/BRAND-RULES.md:32`): `--color-brand-light` en oscuro y `--color-brand-dark` en claro |
| A-03 · falta la regla de tinta sobre acentos | 1 h | sí (`docs/BRAND-RULES.md`) | Una línea en los no-negociables de producto y una tinta por producto en `products/products.json` |
| A-04 · frase falsa sobre el carmín | 0,5 h | sí (`docs/BRAND-RULES.md`) | Escribir la excepción del carmín |
| B-05 · el MCP no sirve el modo claro | 2 h | no | Modo en `get_token` y `list_tokens`. Antes, consultar el registro de contratos, como pide `CLAUDE.md` |
| D-01 · la portada enseña a copiar | 0,5 h | sí (README) | La vía del paquete primero; fuera las instrucciones de copiar |
| A-15 · garantía falsa sobre las muestras | 1 h | sí (README) | Que las muestras lean los tokens, o acotar la frase |
| A-13 · 12 muestras bajo el mínimo | 1 h | no | Pasar a los tres registros del canon (y de paso cierra A-14) |
| A-09 · tres textos del kit bajo el mínimo | 0,5 h | no | Quitar la opacidad; tinta con `--brand-ink` |
| A-08 · estados sin anunciar | 0,25 h | no | `role="status"` |
| A-19 · 12 lockups dependen de fuentes instaladas | 3 h | no | Exportar a contornos, como ConsentFlow |
| A-11 · el kit no es responsive | 3 h | no | Puntos de ruptura con los tokens `--bp-*` |
| D-08 · sin linter ni tipos | 2 h | no | `ruff` y `mypy` para `aglaya-ds-mcp/` y `tools/`; `node --check` o ESLint para `scripts/` y `bin/` |

## Sprint 3+ — P3 (≈ 10,5 h y una revisión legal)

| Hallazgo | Esfuerzo | Paquete | Nota |
|---|---|---|---|
| A-10 · el input quita el anillo de foco | 0,25 h | no | |
| A-14 · el render no coincide con la spec | 0,25 h | no | Se cierra con A-13 |
| A-16 · tracking fuera de escala | 2 h | según decisión | **Decide Ibai** (ver abajo) |
| A-17 · el kit contradice el canon | 0,5 h | no | |
| A-18 · peso del eyebrow | 0,25 h | sí (parche) | **Decide Ibai** |
| A-20 · fondo pegado en el lockup de ConsentFlow | 0,25 h | no | Reexportar sin la mesa de trabajo |
| A-21 · eslogan a 7 px | 0,1 h | no | |
| A-22 · fuentes sin WOFF2 | 2 h | sí (menor: añade formato) | |
| A-23 · Babel en el navegador | — | no | INFO: solo si el kit se va a servir algún día |
| B-02 · dependencias del MCP sin fijar | 1 h | no | Lock con hashes y Dependabot `pip`; recrear el venv local |
| B-06 · descripciones del MCP desalineadas | 0,5 h | no | |
| B-07 · manifiesto contra CSS | 0,25 h | no | **Decide Ibai** |
| B-08 · `.t-codetag` no sigue al modo | 0,25 h | sí (parche) | |
| C-03 · autoría de IA frente a copyright | rev. legal | sí (`LICENSE`) | |
| C-04 · «ningún permiso» en un repo bifurcable | 0,25 h | sí (`LICENSE`) | |
| D-02 · la portada describe aglaya.biz | 0,5 h | sí (README) | |
| D-05 · defensas de GitHub apagadas | 0,25 h | no | Cubre también B-NV-02 |
| D-06 · actions ancladas a tags | 0,5 h | no | |
| D-07 · el enganche solo sirve en esta máquina | 0,5 h | no | **Decide Ibai** si es intencionado |
| D-09 · commit con identidad de bot | 0,25 h | no | |
| D-10 · no está escrito qué hacer con una versión mala | 0,5 h | sí (`docs/PACKAGE.md`) | |
| D-11 · `CLAUDE.md` no lista dos baterías | 0,1 h | no | |

---

## No verificable — hace falta algo de fuera

| Hallazgo | Qué hace falta | Quién |
|---|---|---|
| A-24 · Outfit declarada dos veces | Servir la muestra de pesos por HTTP y mirar en DevTools qué ficheros baja | cualquiera con un navegador |
| A-NV-01 · métricas web reales | PageSpeed Insights sobre aglaya.biz | quien lleve aglaya.biz |
| A-NV-02 · el kit como fichero local | Abrir `ui_kits/website/index.html` con doble clic en Chrome | cualquiera |
| A-NV-03 · sin escáner de accesibilidad | axe DevTools o Lighthouse | cualquiera |
| B-NV-01 · librerías vendorizadas sin escanear | `trivy fs` u `osv-scanner` | cualquiera |
| B-NV-02 · secretos en la historia | Activar el secret scanning de GitHub (D-05) o `gitleaks detect` | Ibai (ajustes del repo) |
| C-02 · derechos sobre ConsentFlow | El acuerdo escrito con la autora | Ibai |

## Lo que solo puede decidir Ibai

1. **A-16:** los 40 usos de tracking fuera de escala. ¿Se llevan a la escala, lo que cambia el aspecto, o se añade alguno como token, que es versión menor?
2. **A-18:** el eyebrow, ¿400 o 700?
3. **B-07:** ¿ConsentFlow es «sagrado»? ¿Se confirman el color y el nombre de DESIGN SYSTEM?
4. **C-02:** ¿hay acuerdo escrito con la autora de ConsentFlow?
5. **D-07:** que el enganche bloquee todo fuera de esta máquina, ¿es a propósito?

Lo demás se deduce de reglas ya escritas y va arriba como arreglo, no como pregunta. Por ejemplo, el valor de `--fg-brand` sale de `docs/BRAND-RULES.md:32`, y la tinta sobre el rojo de `:34`.

## Recursos externos

- **Revisión legal** de C-02, C-03 y C-04: unas horas de un abogado de propiedad intelectual. No se ha pedido presupuesto, así que no se da cifra.
- **Herramientas gratuitas:** axe DevTools, Lighthouse, secret scanning de GitHub, Dependabot, trivy u osv-scanner.
- No hace falta pentest: no hay superficie de red.
