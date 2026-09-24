# Auditoría Mariana — aglaya-design-system

**ID:** `aglaya-design-system-2026-09-24-mariana`
**Modo:** `report`. Solo informe: no se ha tocado nada del repo fuera de esta carpeta.
**Empezó:** 2026-09-24 17:33 UTC · pausa a las 17:57 UTC para reiniciar Claude · retomada con `--resume` y terminada el mismo día.
**Commit auditado:** `17d95cc` al empezar y al terminar (`git rev-parse HEAD`, sin cambios).
**Auditor:** skill `mariana-audit` v3. Se auditó leyendo el código, sin instalar nada. Todo lo que escribe, compila o muta se corrió en un clon del repo dentro de un temporal.

---

## Integridad de la evidencia

| Nivel | Hallazgos | % |
|---|---|---|
| PROVEN (archivo:línea o salida de herramienta) | 45 | 86,5 % |
| UNVERIFIABLE (hace falta acceso o entorno externo) | 7 | 13,5 % |
| **Total** | **52** | 100 % |

Cada hallazgo lleva su cita. Lo que no se pudo citar no está en el informe: se descartó, no se rebajó.

Fuente: `code-read` 26 · `tool-external` 19 · `manual-verification` 0. En este repo, «tool-external» es la salida guardada en `evidencia/` de `gh api`, `npm view`, `npm pack`, `pip-audit`, los scripts de contraste (leen el CSS en vivo), las mutaciones sobre un clon y la ejecución directa del core del MCP.

**Herramientas disponibles:** `npm`, `node`, `pip-audit`. **Ausentes:** `axe`, `radon`, `eslint`, `semgrep`, `trivy`, `lighthouse`. Lo que dependía de ellas está marcado como `NV_TOOL`: es un hueco de herramienta, no un «todo bien».

**Delta de regresión:** no aplica. Es la primera auditoría Mariana de este repo, así que los 52 hallazgos son `NEW`.

---

## Resumen ejecutivo

- **Salud: 🟡 ámbar.** El núcleo está sano: cuatro guardianes con sus baterías de sabotaje, la prueba de mutación, CI en verde en `17d95cc`, ningún dato personal y ningún hallazgo CRÍTICO. Lo que falla está en lo que sale del repo:
  - el canon servido se rompe en modo claro;
  - la compuerta no bloquea (el CI no se exige y los tags se pueden mover);
  - hay una vía de suministro abierta (`npx`).
- **Exposición legal: baja.** El RGPD y la Ley 21.719 no aplican porque no se tratan datos personales. Hay un incumplimiento de licencia MIT que se arregla en media hora (C-01) y derechos sin constancia sobre ConsentFlow (C-02).
- **Las tres acciones que más rinden:**
  1. **B-01.** Cambiar `npx aglaya-tokens-version` por `npm exec --no -- aglaya-tokens-version` en la doc. Media hora, y cierra el único hallazgo ALTO de seguridad.
  2. **D-03 y D-04.** Checks obligatorios para fusionar y tags protegidos. Media hora entre los dos: los guardianes dejan de ser un aviso y pasan a ser una compuerta, y una versión publicada ya no se puede reescribir.
  3. **A-02 y A-01.** Fichas de componente y `--fg-brand` correctos en los dos modos. Dos horas y media: lo que consume la flota deja de romperse en modo claro, que legal-reg-tech ya usa en producción.
- **Riesgo si no se hace nada en 3 meses:**
  - una superficie en modo claro construida con `get_component` publica texto invisible (contraste 1:1);
  - un PR en rojo o un tag movido llega a los consumidores;
  - si alguien registra el nombre en npm, un CI ajeno ejecuta su código con sus secretos;
  - la portada sigue enseñando a copiar la marca.
- **Recursos externos:** unas horas de revisión legal de propiedad intelectual (C-02, C-03, C-04) y herramientas gratuitas (axe o Lighthouse, secret scanning, Dependabot, trivy). No hace falta pentest.

---

## Recuento por severidad

| Severidad | Nº |
|---|---|
| CRÍTICA mitigada durante la auditoría | 0 |
| CRÍTICA abierta | 0 |
| ALTA | 6 |
| MEDIA | 17 |
| BAJA | 21 |
| INFO | 1 |
| UNVERIFIABLE | 7 |
| **Total** | **52** |

Por prioridad: **P0 1 · P1 6 · P2 16 · P3 22**. Los 7 UNVERIFIABLE no tienen prioridad: necesitan una acción externa.

## Cómo se calibró

La base es la tabla del rubric: para accesibilidad, nivel A = CRÍTICA, AA = ALTA y AAA = MEDIA; para seguridad, CVSS 3.1. Sobre esa base se aplicaron tres ajustes, y cada hallazgo dice cuál:

1. **Regla de reducción 2, «sin camino hasta un usuario».** `preview/` y `ui_kits/` no se sirven a nadie: Pages da 404 y no hay despliegue. Sus fallos bajan un escalón.
2. **Latente.** Un token que ninguna nave usa baja un escalón. Se midió con `quien_lee` sobre 10 de 10 naves.
3. **Sin reducción** para lo que sí sale del repo: el CSS del paquete, `components/components.json` y `docs/BRAND-RULES.md`, que sirve el MCP.

Los contrastes se dan sin redondear, como exige `docs/BRAND-RULES.md:36`.

## Alcance

| # | Dimensión | ¿Aplica? | Motivo |
|---|---|---|---|
| 1 | Seguridad | Sí, reducida | Suministro (paquete, `npx`, actions, dependencias) y MCP local por stdio. Sin login, subidas ni API |
| 2 | Accesibilidad WCAG 2.1 | Sí | Contraste del canon en los dos modos, fichas de componente, kit y `preview/` |
| 3 | Usabilidad | En parte | Experiencia de quien consume, y el kit |
| 4 | Rendimiento | En parte | Peso del paquete y de las fuentes. Métricas web reales: `NV_RUNTIME` (no hay despliegue) |
| 5 | Bases de datos | No | No hay |
| 6 | SEO técnico | No | Nada se sirve como web |
| 7 | Arquitectura y deuda | Sí | Lectores del CSS, guardianes, MCP |
| 8 | Cumplimiento legal | En parte | Solo propiedad intelectual: no se tratan datos personales |
| 9 | Cookies y consentimiento | No | Sin cookies, storage ni analítica (grep vacío) |
| 10 | Retención y DPA | No | Sin datos personales |
| 11 | DevOps / CI | Sí | |
| 12 | Despliegue y observabilidad | En parte | El despliegue es un tag. No hay servicio vivo que vigilar |
| 13 | Docs y mantenimiento | Sí | |

---

## Fase A — Superficie (27 hallazgos · detalle en `audit-A.md`)

ALTA 5 · MEDIA 9 · BAJA 8 · INFO 1 · UNVERIFIABLE 4.

| ID | Hallazgo | Evidencia | Criterio | Severidad |
|---|---|---|---|---|
| A-02 | Las fichas de componente fallan en modo claro: 8 de 11 pares; tres dan 1:1 (codetag negro sobre negro, texto e input invisibles) | `components/components.json:14-15`, `:86-92`, `:106-109` | 1.4.3 / 1.4.11 AA | ALTA |
| A-05 | Marquesina y puntos que laten sin pausa y sin `prefers-reduced-motion` | `ui_kits/website/styles.css:128` | 2.2.2 A | ALTA (−1) |
| A-06 | Etiqueta del email sin asociar a su campo | `ui_kits/website/Footer.jsx:17-29` | 1.3.1 A | ALTA (−1) |
| A-07 | `PrimaryButton` siempre es `<a href="#">`, también como envío; el clic salta la validación | `ui_kits/website/Primitives.jsx:12-15` | 4.1.2 A + 3.3.1 A | ALTA (−1) |
| A-12 | Las 23 páginas de `preview/` sin idioma, título ni viewport | 23 de 23 ficheros | 3.1.1 A + 2.4.2 A | ALTA (−1) |
| A-01 | `--fg-brand` es el rojo: falla como texto en los dos modos, contra la regla del propio canon | `colors_and_type.css:115`, `docs/BRAND-RULES.md:32` | 1.4.3 AA | MEDIA (latente) |
| A-04 | El canon dice algo falso sobre el carmín de ConsentFlow | `docs/BRAND-RULES.md:47` | exactitud | MEDIA |
| A-19 | 12 lockups dependen de que la máquina tenga instaladas las fuentes | `products/kanban-desk/lockups/aglaya-kanban-desk-lockup.svg:2` | marca | MEDIA |

## Fase B — Seguridad y arquitectura (10 hallazgos · detalle en `audit-B.md`)

ALTA 1 · MEDIA 3 · BAJA 4 · UNVERIFIABLE 2.

| ID | Hallazgo | Evidencia | OWASP / CVSS o ref. | Severidad | Estado |
|---|---|---|---|---|---|
| B-01 | La doc manda `npx aglaya-tokens-version`, el nombre está libre en npm y en CI npm lo instala sin preguntar | `README.md:244`, `docs/PACKAGE.md:127`, `:132`, `evidencia/npm-registro.txt` | A08 · 7.5 `AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` | ALTA | ABIERTO |
| B-03 | Un `}` dentro de un comentario de `:root` deja al MCP sirviendo 1 token en vez de 87, sin avisar | `aglaya-ds-mcp/brand.py:87-88`, `evidencia/mutaciones.txt` | robustez | MEDIA | ABIERTO |
| B-04 | `guard_punteros` no mira `.otf`: 18 URLs de fuente sin vigilar | `tools/guard_punteros.py:96`, `evidencia/mutaciones.txt` | promesa del guardián | MEDIA | ABIERTO |
| B-05 | El MCP no sirve el modo claro y el paquete sí | `aglaya-ds-mcp/brand.py:84-92`, `scripts/build-tokens.mjs:43-45` | contrato | MEDIA | ABIERTO |

**Verificaciones en positivo:**
- ✓ `get_logo` sin traversal: valida contra listas cerradas.
- ✓ `bin/aglaya-tokens-version.mjs` llama a git sin shell y con tiempo máximo.
- ✓ `tools/publicar_cifras.sh` valida cada valor antes de tocar git.
- ✓ El workflow es de solo lectura, y solo el job que publica las cifras tiene escritura.
- ✓ El paquete no tiene dependencias npm.
- ✓ `aglaya-ds-mcp/brand.py` tiene 496 líneas de código, por debajo del umbral de 700, y es cohesivo.
- ✓ No hay ciclos de importación. La profundidad máxima es 3.

## Fase C — Legal (4 hallazgos · detalle en `audit-C.md`)

MEDIA 1 · BAJA 2 · UNVERIFIABLE 1.

| ID | Hallazgo | Norma | Afecta a | Severidad |
|---|---|---|---|---|
| C-01 | React, ReactDOM y Babel (MIT) redistribuidos sin su licencia, bajo «todos los derechos reservados» | Licencia MIT | autores de React y Babel | MEDIA |
| C-02 | ConsentFlow, concepto de otra persona, reclamado como marca propia sin constancia de cesión | marca y derecho de autor | la autora | UNVERIFIABLE |

**Verificaciones en positivo:**
- ✓ Las tres familias tipográficas cumplen el OFL: licencia al lado, nombres sin tocar y un guardián que empareja cada fichero con su licencia.
- ✓ Protección de datos no aplica: no se trata ningún dato personal.

**Acciones legales que requieren a una persona:** confirmar el acuerdo con la autora de ConsentFlow (C-02) y una revisión legal breve de C-03 y C-04.

## Fase D — Operaciones y docs (11 hallazgos · detalle en `audit-D.md`)

MEDIA 4 · BAJA 7.

| ID | Hallazgo | Evidencia | Severidad |
|---|---|---|---|
| D-01 | La portada enseña a copiar la marca, que es lo que prohíben el contrato y la guía del paquete | `README.md:206`, `:224-228`, `:254` | MEDIA |
| D-03 | `main` exige PR pero no el CI en verde, ni aprobaciones | `evidencia/github-ajustes.txt` | MEDIA |
| D-04 | Los tags, que son la versión publicada, se pueden mover o borrar | `evidencia/github-ajustes.txt`, `docs/PACKAGE.md:82` | MEDIA |
| D-08 | No hay linter, formateador ni comprobación de tipos | (ausencia de configuración) | MEDIA |

---

## Mitigaciones aplicadas durante la auditoría

Ninguna. El modo es `report`, y además no hubo ningún hallazgo CRÍTICO inmediato.

## No verificable

| ID | Subtipo | Qué es | Por qué no se pudo | Acción externa |
|---|---|---|---|---|
| A-24 | NV_RUNTIME | Outfit declarada dos veces para los mismos pesos | Lo decide el navegador | Servir la muestra por HTTP y mirarlo en DevTools |
| A-NV-01 | NV_RUNTIME | Métricas web reales | No hay despliegue | PageSpeed sobre aglaya.biz |
| A-NV-02 | NV_RUNTIME | El kit abierto como fichero local | El navegador integrado no carga recursos locales | Abrirlo en Chrome |
| A-NV-03 | NV_TOOL | Escaneo automático de accesibilidad | `axe` y `lighthouse` ausentes | axe DevTools o Lighthouse |
| B-NV-01 | NV_TOOL | Librerías vendorizadas | `trivy` ausente | `trivy fs` u `osv-scanner` |
| B-NV-02 | NV_CREDENTIALS | Secretos en la historia de git | El enganche bloquea la búsqueda | Secret scanning de GitHub |
| C-02 | NV_CREDENTIALS | Derechos sobre ConsentFlow | El acuerdo, si existe, no está en el repo | Confirmarlo con la autora |

## Matriz de prioridad

La lista completa, con esfuerzo y si toca el paquete, está en `roadmap.md`. El detalle por hallazgo, en `findings.json`.

| Prioridad | Hallazgos | Esfuerzo |
|---|---|---|
| P0 | C-01 | 0,5 h |
| P1 | B-01, A-02, A-05, A-06, A-07, A-12 | 5,25 h |
| P2 | D-03, D-04, B-04, B-03, A-01, A-03, A-04, B-05, D-01, A-15, A-13, A-09, A-08, A-19, A-11, D-08 | 17 h |
| P3 | A-10, A-14, A-16, A-17, A-18, A-20, A-21, A-22, A-23, B-02, B-06, B-07, B-08, C-03, C-04, D-02, D-05, D-06, D-07, D-09, D-10, D-11 | ≈ 10,5 h y una revisión legal |

## Lo que solo puede decidir Ibai

1. **A-16:** el tracking fuera de escala, ¿se lleva a la escala o se añaden tokens?
2. **A-18:** el peso del eyebrow, ¿400 o 700?
3. **B-07:** ¿ConsentFlow es «sagrado»? ¿Se confirma DESIGN SYSTEM?
4. **C-02:** ¿hay acuerdo escrito con la autora de ConsentFlow?
5. **D-07:** que el enganche cierre en falso fuera de esta máquina, ¿es a propósito?

El resto se deduce de reglas ya escritas, y el informe lo da como arreglo, no como pregunta.

---

## Conclusiones

Este repo defiende muy bien una propiedad concreta: **que nadie copie un valor de marca.** Para eso tiene guardianes que se sabotean a sí mismos, una prueba de mutación que distingue consumir de copiar y docs que se niegan a repetir valores. En esa propiedad la auditoría no encuentra fugas: `guard_valores` pasa y los valores viven en un solo sitio.

Los hallazgos están en las propiedades de al lado, las que nadie vigila:

- **Que lo servido sea correcto en los dos modos.** El modo claro llegó después y las fichas de componente no lo siguieron (A-02).
- **Que la tinta de marca sea legible.** El canon prohíbe el rojo como texto, pero su token de texto es el rojo (A-01).
- **Que las muestras enseñen lo que dicen enseñar** (A-13, A-15).
- **Que el sistema inmune muerda de verdad.** Hay dos casos en los que un guardián o la paridad de lectores no ven la avería (B-03, B-04), y en ninguno el CI bloquea la fusión (D-03).

Nada de esto es grave hoy. Pero todo es de la clase que la casa ya sabe que sale cara: una segunda verdad que nadie mira.

La acción de mejor retorno es barata. En la primera hora caben B-01, D-03, D-04 y B-04: el suministro queda cerrado, los guardianes pasan de consejo a compuerta, los tags se vuelven inmutables y el guardián de punteros ve las fuentes.

Después vienen unas 2,5 horas para que lo que consume la flota sea correcto en modo claro (A-02, A-01), con la regla de tinta sobre acentos (A-03) y la corrección del carmín (A-04). El kit y las muestras pueden esperar al sprint 2: no se sirven a nadie. Aun así, son lo que se cita como «así va todo junto», y hoy enseñan patrones que fallan WCAG A.

---

## Ficheros de esta auditoría

- `REPORT.md`: este resumen.
- `audit-A.md`, `audit-B.md`, `audit-C.md`, `audit-D.md`: detalle por fase, cada uno con su cuadro de evidencias.
- `findings.json`: los 52 hallazgos con sus metadatos (schema 3.0).
- `roadmap.md`: la hoja de ruta por sprints y lo que decide Ibai.
- `state.json`: estado para `--resume`.
- `evidencia/`: las salidas de las herramientas y los scripts que las reproducen. Ninguno lleva un valor de marca dentro: leen el CSS en vivo.

**Si decides commitear la auditoría,** el mensaje que propone el protocolo es `docs(audit): mariana-trench full audit — 52 findings (P0:1 P1:6 P2:16 P3:22)`. La carpeta se ha pasado por los cuatro guardianes sobre una copia en un clon (ver el mensaje de entrega).
