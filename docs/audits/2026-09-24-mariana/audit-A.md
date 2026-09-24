# Fase A — Superficie: accesibilidad, uso, rendimiento

Auditoría `aglaya-design-system-2026-09-24-mariana` · commit auditado `17d95cc` · modo `report` (no se ha tocado nada).

## Cuadro de evidencias — Fase A

| Confianza    | Nº | % de la fase |
|--------------|----|--------------|
| PROVEN       | 23 | 85 %         |
| UNVERIFIABLE | 4  | 15 %         |
| **Total**    | **27** | 100 %    |

Fuente de la evidencia: code-read 15 · tool-external 8 · manual-verification 0.
En este repo, «tool-external» son los scripts de `evidencia/`, que leen el CSS canónico en vivo, más `npm pack`. Los cuatro UNVERIFIABLE lo son porque el navegador integrado no carga ficheros locales y porque no hay `axe` ni `lighthouse` instalados.

Salud: 85 % PROVEN, por encima del 60 %.

## Cómo se ha calibrado (léelo antes que la tabla)

- **Base:** la tabla del rubric. Un fallo WCAG de nivel A es CRÍTICA, AA es ALTA y AAA es MEDIA.
- **Regla de reducción 2, «sin camino hasta un usuario»:** `preview/` y `ui_kits/` no se sirven a nadie. GitHub Pages devuelve 404 (`evidencia/github-ajustes.txt`) y no hay configuración de Netlify ni Vercel. Sus fallos bajan **un** escalón, y en la tabla va marcado «(−1)».
- **Sin reducción:** lo que sí llega a otras naves. Eso es el CSS del paquete, `components/components.json` (lo sirve `get_component`) y `docs/BRAND-RULES.md` (lo sirve `get_nonnegotiables`).
- **Token que nadie usa hoy:** baja un escalón porque es un defecto latente. Se ha medido con `quien_lee` sobre 10 de 10 naves.
- **Rendimiento, marca y copyright** no tienen tabla en el rubric. Se dice en cada caso con qué tabla se mide; si no encaja ninguna, va como INFO.
- **Los contrastes se dan sin redondear a dos decimales.** El propio canon lo exige (`docs/BRAND-RULES.md:36`), porque un 4,4985 redondeado a 4,50 parece que pasa y no pasa.

## Tabla de hallazgos

| ID | Confianza | Dim | Hallazgo | Evidencia | Severidad | Esfuerzo |
|----|-----------|-----|----------|-----------|-----------|----------|
| A-01 | PROVEN | a11y | El token de texto `--fg-brand` es el rojo, que no llega al mínimo de texto normal en ningún modo | `colors_and_type.css:115`, `docs/BRAND-RULES.md:32` | MEDIA | 0,5 h |
| A-02 | PROVEN | a11y | Las fichas de componente fallan en modo claro: 8 de 11 pares, 3 de ellos invisibles (1:1) | `components/components.json:14-15`, `:86-92`, `:106-109` | ALTA | 2 h |
| A-03 | PROVEN | a11y | El canon no dice qué tinta va sobre el relleno de un acento de producto, y la regla del rojo copiada a los acentos falla en 7 de 8 | `docs/BRAND-RULES.md:34`, `:43` | MEDIA | 1 h |
| A-04 | PROVEN | canon | `docs/BRAND-RULES.md:47` afirma algo falso sobre el carmín de ConsentFlow | `docs/BRAND-RULES.md:47` | MEDIA | 0,5 h |
| A-05 | PROVEN | a11y | La marquesina y los puntos que laten no se pueden parar, y no hay `prefers-reduced-motion` | `ui_kits/website/styles.css:128`, `ui_kits/website/SystemsGrid.jsx:109-113`, `ui_kits/website/AntiClient.jsx:115` | ALTA (−1) | 1 h |
| A-06 | PROVEN | a11y | La etiqueta del formulario Dispatch no está asociada a su campo | `ui_kits/website/Footer.jsx:17-29` | ALTA (−1) | 0,25 h |
| A-07 | PROVEN | a11y/uso | `PrimaryButton` siempre es un enlace a `#`, también cuando envía el formulario, y el clic se salta la validación | `ui_kits/website/Primitives.jsx:12-15`, `ui_kits/website/Footer.jsx:8-13`, `:30` | ALTA (−1) | 1 h |
| A-08 | PROVEN | a11y | Los mensajes de estado del formulario no se anuncian a los lectores de pantalla | `ui_kits/website/Footer.jsx:31`, `:39` | MEDIA (−1) | 0,25 h |
| A-09 | PROVEN | a11y | Hay tres textos pequeños del kit por debajo del mínimo | `ui_kits/website/Header.jsx:29`, `ui_kits/website/AntiClient.jsx:23`, `:92-94` | MEDIA (−1) | 0,5 h |
| A-10 | PROVEN | a11y/spec | El input del kit quita el anillo de foco que pide la spec | `ui_kits/website/Footer.jsx:28`, `components/components.json:96`, `:98` | BAJA | 0,25 h |
| A-11 | PROVEN | a11y | El kit no tiene ni una regla responsive, y a 320 px el texto de las tarjetas queda recortado | `ui_kits/website/Problem.jsx:18`, `:66`, `ui_kits/website/Header.jsx:10-14` | MEDIA (−1) | 3 h |
| A-12 | PROVEN | a11y | Las 23 páginas de `preview/` no tienen idioma, título ni viewport | 23 de 23 ficheros (tabla abajo) | ALTA (−1) | 0,5 h |
| A-13 | PROVEN | a11y | 12 de las 23 páginas de muestra pintan texto por debajo del mínimo | `evidencia/contraste-preview.txt` | MEDIA (−1) | 1 h |
| A-14 | PROVEN | spec | El «render de referencia» no coincide con la spec que dice representar | `preview/components-buttons.html:29`, `preview/components-card.html:25` | BAJA | 0,25 h |
| A-15 | PROVEN | docs | La portada promete que las muestras no pueden enseñar un valor viejo, y solo lo cumplen 3 de 23 | `README.md:37` | MEDIA | 1 h |
| A-16 | PROVEN | sistema | Se usan 40 valores de espaciado entre letras que no existen en la escala del canon (18 valores distintos en 22 ficheros) | `evidencia/tracking-fuera-de-escala.txt` | BAJA | 2 h |
| A-17 | PROVEN | marca | El kit incumple tres reglas del propio canon, y la lista de excepciones del radio no coincide entre ficheros | `ui_kits/website/Header.jsx:53-54`, `ui_kits/website/README.md:37` | BAJA | 0,5 h |
| A-18 | PROVEN | marca | El eyebrow pide un peso que su tipografía no tiene. Decisión abierta y documentada | `colors_and_type.css:136` | BAJA | 0,25 h |
| A-19 | PROVEN | marca | 12 lockups dependen de que la máquina tenga instaladas las fuentes | `products/kanban-desk/lockups/aglaya-kanban-desk-lockup.svg:2`, `:9-10` | MEDIA | 3 h |
| A-20 | PROVEN | marca | El lockup horizontal de ConsentFlow lleva un fondo marrón opaco pegado | `products/consent-flow/lockups/aglaya-consent-flow-lockup.svg:26`, `:30` | BAJA | 0,25 h |
| A-21 | PROVEN | uso | El eslogan de la cabecera está a 7 px | `ui_kits/website/Header.jsx:20` | BAJA | 0,1 h |
| A-22 | PROVEN | rendimiento | Las fuentes solo se entregan en OTF/TTF, ninguna en WOFF2 | `colors_and_type.css:9-44`, `evidencia/npm-pack.txt` | BAJA | 2 h |
| A-23 | PROVEN | rendimiento | El kit carga un compilador de 3,1 MB en el navegador en cada visita | `ui_kits/website/index.html:34-42` | INFO | — |
| A-24 | UNVERIFIABLE · NV_RUNTIME | rendimiento | Outfit está declarada dos veces para los mismos pesos, y cuál gana lo decide el navegador | `colors_and_type.css:15-24` | — | — |
| A-NV-01 | UNVERIFIABLE · NV_RUNTIME | rendimiento | Métricas web reales (LCP/INP/CLS) de quien consume las fuentes | — | — | — |
| A-NV-02 | UNVERIFIABLE · NV_RUNTIME | uso | Si el kit arranca abierto como fichero local | `README.md:209`, `ui_kits/website/index.html:36-42` | — | — |
| A-NV-03 | UNVERIFIABLE · NV_TOOL | a11y | No se ha pasado ningún escáner automático de accesibilidad | — | — | — |

**Recuento:** CRÍTICA 0 · ALTA 5 · MEDIA 9 · BAJA 8 · INFO 1 · UNVERIFIABLE 4.

---

## Detalle

### A-01 · `--fg-brand` es una tinta que la propia marca prohíbe

- **Qué pasa.** `--fg-brand` es el token «color de texto de marca», y apunta a `--color-brand` (`colors_and_type.css:115`). Como texto normal, el rojo da entre 4.1062 y 4.4985 sobre los cinco fondos oscuros, y entre 4.0598 y 4.6682 sobre los claros. El mínimo es 4,5, así que falla en los dos modos (`evidencia/contraste-tokens.txt`).
- **Por qué es incoherente.** El canon ya lo sabe y lo prohíbe: «`--color-brand` no es tinta de TEXTO CORRIDO en ningún modo» (`docs/BRAND-RULES.md:32`). Pero el token con nombre de tinta sigue apuntando al rojo, y el modo claro no lo redefine (`colors_and_type.css:228-286`). El kit tuvo que inventarse su propio `--brand-ink` (`ui_kits/website/styles.css:31-49`, `:58-59`), justo lo que `docs/PACKAGE.md:176-178` prohíbe: si falta un token, se pide aquí, no se inventa allí.
- **Criterio.** WCAG 2.1 · 1.4.3 Contraste (mínimo) · AA · baja visión.
- **Severidad.** ALTA por el rubric; baja a MEDIA porque ninguna nave usa `--fg-brand` hoy (`quien_lee("--fg-brand")`: solo aparece en este repo, 10 de 10 naves medidas).
- **Arreglo.** Se deduce de la regla ya escrita: `--fg-brand` pasa a `--color-brand-light` en oscuro y a `--color-brand-dark` en claro. Es un cambio de valor, no de nombre, así que es un **parche** (`docs/PACKAGE.md:87`).

### A-02 · Las fichas de componente se rompen en modo claro

- **Qué pasa.** Casi todos los colores de `components/components.json` están escritos pensando en el fondo negro (blanco con transparencia, verde como letra). Al activar el modo claro, esto es lo que dan (`evidencia/contraste-usos.txt`):

| Par | Oscuro | Claro |
|---|---|---|
| botón primario: texto sobre rojo (`:14-15`) | 4.5501 | **4.4985** |
| input: texto (`:86`, `:90`) | 5.3169 | **1.0000** |
| input: borde, no-texto (`:87`) | 3.0096 | **1.0000** |
| input: etiqueta en verde (`:92`) | 10.2719 | **2.0444** |
| badge.default (`:106`) | 7.2751 | **1.0000** |
| badge.brand (`:107`) | 9.8809 | **1.7168** |
| badge.codetag: negro sobre `--color-text`, que en claro es negro (`:108`) | 20.4689 | **1.0000** |
| badge.ok (`:109`) | 10.2719 | **2.0444** |

- **Por qué importa.** El MCP sirve estas fichas a toda la flota (`get_component`), y hay una nave con el modo claro en producción: el sitio de legal-reg-tech abre con `data-theme="light"`, según `quien_lee`. Además la ficha contradice dos reglas del canon: «en modo claro un acento no es tinta» (`docs/BRAND-RULES.md:31`) y «sobre relleno rojo, la tinta es blanca» (`docs/BRAND-RULES.md:34`).
- **Criterio.** WCAG 2.1 · 1.4.3 (AA) y 1.4.11 Contraste no textual (AA) · baja visión.
- **Severidad.** ALTA, sin reducción: sale del repo por el MCP.
- **Arreglo.** Aplicar a las fichas lo que el kit ya hizo (`ui_kits/website/README.md:11`): mezclas con `color-mix` sobre `--color-text` para que la tinta siga al modo, `--fg-eyebrow` en vez del verde, blanco sobre el relleno rojo y, en codetag, el fondo en `--color-text` con la letra en `--color-bg`.

### A-03 · Falta la regla de tinta sobre el acento de producto

- **Qué pasa.** Para el producto, el canon dice «acento libre en CTA» (`docs/BRAND-RULES.md:43`), pero no dice qué color de letra va encima. La única regla parecida es la de la marca madre: blanco sobre el rojo (`docs/BRAND-RULES.md:34`). Aplicada a los acentos, el blanco falla en 7 de 8: CRM 3.3387, KANBAN 3.3919, OUTREACH 2.5338, ORCHESTRATOR 2.6795, LEGAL 2.2739, DESIGN SYSTEM 2.0444 y el verde de ConsentFlow 3.5506. El negro pasa en todos menos en el carmín de ConsentFlow (3.1244), que necesita blanco (6.7212) (`evidencia/contraste-tokens.txt`, sección 2).
- **Criterio.** WCAG 1.4.3 (AA), latente: hace falta que alguien elija la tinta equivocada. Se mide con la tabla de docs, como API sin documentar.
- **Severidad.** MEDIA.
- **Arreglo.** Una línea en `## Non-negotiables — producto` y un campo por producto en `products/products.json` con su tinta sobre relleno.

### A-04 · El canon dice algo falso sobre el carmín de ConsentFlow

- **Qué pasa.** `docs/BRAND-RULES.md:47` dice que «ninguno de los acentos de producto llega al suelo de texto sobre los fondos claros — se eligieron para brillar sobre negro». Medido, el carmín de ConsentFlow **sí** llega en claro (5.8453–6.7212) y en oscuro **no llega ni al 3:1 de texto grande** en 4 de los 5 fondos (2.8520–3.1244) (`evidencia/contraste-tokens.txt`).
- **Por qué importa.** Esa frase la sirve `get_nonnegotiables(scope="product")` a toda la flota. Quien la crea usará el carmín como letra sobre negro.
- **Severidad.** MEDIA, por exactitud de un canon que se sirve.
- **Arreglo.** Decir la excepción: el carmín es tinta en claro y no en oscuro.

### A-05 · Animaciones infinitas sin forma de pararlas

- **Qué pasa.** La marquesina se mueve sin fin (`animation: marquee 80s linear infinite`, `ui_kits/website/styles.css:128`; se aplica en `ui_kits/website/SystemsGrid.jsx:109-113`) y los cuatro puntos del AntiClient laten sin parar (`ui_kits/website/AntiClient.jsx:115`). No hay botón de pausa, y no hay `prefers-reduced-motion` en ninguna parte: `grep -rn prefers-reduced-motion ui_kits preview colors_and_type.css` sale vacío.
- **Criterio.** WCAG 2.1 · 2.2.2 Pausar, detener, ocultar · **A** · déficit de atención, vestibular y lectura lenta. También 2.3.3 (AAA).
- **Por qué importa.** El kit es «la composición canónica: así va todo junto» (`CLAUDE.md`) y la portada promete que «`prefers-reduced-motion` is honored — marquee stops» (`README.md:145`). El kit no lo hace.
- **Severidad.** CRÍTICA por el rubric; baja a ALTA porque no se sirve a nadie.

### A-06 · La etiqueta del email no está atada a su campo

- **Qué pasa.** `<label className="t-eyebrow">CORPORATE_EMAIL</label>` no tiene `htmlFor`, y el `<input>` no tiene `id` ni `aria-*` (`ui_kits/website/Footer.jsx:17-29`). El lector de pantalla solo ofrece el placeholder («operator@company.com»).
- **Criterio.** WCAG 2.1 · 1.3.1 Información y relaciones · **A** · usuarios de lector de pantalla.
- **Severidad.** CRÍTICA → ALTA (−1).

### A-07 · El botón principal es un enlace, y el formulario acepta cualquier cosa

- **Qué pasa.** `PrimaryButton` decide la etiqueta con `href ? 'a' : 'button'`, pero `href` vale `'#'` por defecto (`ui_kits/website/Primitives.jsx:12-13`). Resultado: siempre pinta `<a href="#">`, también como botón de envío (`ui_kits/website/Footer.jsx:30`), y la rama `button` no se ejecuta nunca. Al pulsarlo se llama a `submit` directamente, sin pasar por la validación del navegador:
  - con el campo vacío no pasa nada y no se dice nada (`Footer.jsx:10`);
  - con un email inválido, el formulario termina en «SYNCED» (`Footer.jsx:11-12`).
- **Criterio.** WCAG 2.1 · 4.1.2 Nombre, función, valor (**A**): se anuncia como enlace algo que es una acción. 3.3.1 Identificación de errores (**A**): el error no se identifica.
- **Severidad.** CRÍTICA → ALTA (−1). Quien copie la primitiva hereda el defecto.

### A-08 · Los cambios de estado no se anuncian

- **Qué pasa.** «SYNCING...», «SYNCED» y «DATA_SYNCHRONIZED…» cambian en pantalla (`ui_kits/website/Footer.jsx:31`, `:39`), pero no hay `aria-live` ni `role="status"` en todo el kit (grep vacío).
- **Criterio.** WCAG 2.1 · 4.1.3 Mensajes de estado · AA.
- **Severidad.** ALTA → MEDIA (−1).

### A-09 · Tres textos pequeños del kit por debajo del mínimo

Todos se miden sobre los fondos reales del kit (`evidencia/contraste-usos.txt`):

- Al pasar el ratón, el menú pinta en rojo texto de 13 px en negrita: 4.4985 (`ui_kits/website/Header.jsx:29`). El propio kit dice que el rojo no vale como tinta (`ui_kits/website/styles.css:31-39`).
- Eyebrow de 9 px con opacidad 0,55: 3.5476 (`ui_kits/website/AntiClient.jsx:23`).
- `OPERATIONAL_INTEGRITY` a 10 px con opacidad 0,6: 4.0384 (`ui_kits/website/AntiClient.jsx:92-94`).

La causa común es que se aplica opacidad encima de colores que el canon ya dejó justos en el mínimo (`colors_and_type.css:78-97`).

- **Criterio.** WCAG 1.4.3 · AA.
- **Severidad.** ALTA → MEDIA (−1).

### A-10 · El input del kit quita el anillo de foco

- **Qué pasa.** `outline: 'none'` (`ui_kits/website/Footer.jsx:28`) deja el foco en un cambio de color del borde de 1 px. La spec pide un anillo rojo de 2 px (`components/components.json:96`) y lo justifica: «Foco = anillo rojo de marca (accesible)» (`:98`).
- **Criterio.** WCAG 2.4.7 (AA): el foco sigue visible, así que no es un fallo, solo más débil. Es deriva respecto a la spec.
- **Severidad.** BAJA.

### A-11 · El kit no se adapta a pantallas pequeñas

- **Qué pasa.** En el kit hay cero `@media` (grep vacío). La rejilla es fija (`repeat(3, 1fr)`, `ui_kits/website/Problem.jsx:66`; dos columnas en `ui_kits/website/AntiClient.jsx:78` y en `ui_kits/website/Footer.jsx:96`) y la cabecera va en una sola fila sin salto (`ui_kits/website/Header.jsx:10-14`, `:26`, `:41`). La cuenta a 320 px:
  - La sección tiene 40 px de margen por lado, así que quedan 240 px.
  - Tres columnas con dos huecos de 24 px dan 64 px por tarjeta.
  - Con 32 px de relleno por lado, a cada tarjeta le quedan 0 px de contenido.
  - Como la tarjeta lleva `overflow: hidden` (`Problem.jsx:18`), el texto no desborda: se corta.
- **Criterio.** WCAG 1.4.10 Reflow · AA.
- **Confianza.** PROVEN: la ausencia de reglas se ve leyendo el código, y la cuenta es aritmética del propio CSS. Cómo se ve renderizado queda sin comprobar (ver A-NV-02).
- **Severidad.** ALTA → MEDIA (−1).

### A-12 · Las 23 páginas de muestra sin idioma, título ni viewport

- **Qué pasa.** `grep -c '<html lang='`, `grep -c '<title>'` y `grep -c 'name="viewport"'` dan 0 en los 23 ficheros de `preview/*.html`. El kit sí lo tiene (`ui_kits/website/index.html:2`, `:5-6`).
- **Criterio.** WCAG 2.1 · 3.1.1 Idioma de la página (**A**) y 2.4.2 Página titulada (**A**).
- **Severidad.** CRÍTICA → ALTA (−1). Es media hora de trabajo: tres líneas por fichero.

### A-13 · Doce páginas de muestra con texto por debajo del mínimo

Medido en `evidencia/contraste-preview.txt`. En los doce fallan etiquetas y valores de 9 a 13 px:

| Specimen | Qué | Contraste |
|---|---|---|
| `preview/components-buttons.html:29` | botón link, blanco al 45 % | 4.4129 |
| `preview/components-badges.html:21` | pill, blanco al 35 % | 3.0096 |
| `preview/colors-surface.html:25` | valores, blanco al 45 % (falla en 3 de 5 fondos) | 4.4129–4.4818 |
| `preview/colors-brand.html:31` | blanco sobre `--color-brand-light` | 3.2073 |
| `preview/spacing-scale.html:12` | blanco al 40 % | 3.6574 |
| `preview/type-inter-weights.html:18`, `preview/type-outfit-weights.html:18`, `preview/type-spacemono-weights.html:17` | etiquetas, blanco al 40 % | 3.6574 |
| `preview/type-mono.html:12` | blanco al 45 % | 4.4129 |
| `preview/spacing-radii-shadows.html:14` | rojo como letra de 10 px | 4.4985 |
| `preview/brand-logo-variants.html:16` y `:14` | negro al 60 % sobre rojo · negro al 50 % sobre blanco | 3.0460 · 3.9767 |
| `preview/brand-product-identity.html:7`, `:9`, `:13`, `:14` | tinta al 40 % · tinta al 30 % | 3.5919 · 2.4301 |

- **Por qué es coherente con otra avería ya vista.** El kit ya se curó de esto: tenía «veinte usos de texto que no llegaban a AA sobre negro» y los retiró (`ui_kits/website/README.md:7-11`). Las páginas de muestra conservan el mismo patrón, y `guard_valores` no puede verlo porque el blanco puro está exento a propósito (`tools/guard_valores.py:71-73`).
- **Criterio.** WCAG 1.4.3 · AA.
- **Severidad.** ALTA → MEDIA (−1).

### A-14 · El render de referencia no coincide con la spec

- **Qué pasa.** La spec dice que el render de referencia vive en `preview/` (`components/components.json:2`), pero no coinciden:
  - el botón link es `--color-muted` en la spec (`:47`) y blanco al 45 % en el specimen (`preview/components-buttons.html:29`), con 10.2917 frente a 4.4129;
  - el cuerpo de la tarjeta es `--color-muted` en la spec (`:71`) y blanco al 45 % en el specimen (`preview/components-card.html:25`).
- **Severidad.** BAJA, por deriva. Se arregla junto con A-13.

### A-15 · La portada promete una garantía que solo cumplen 3 de 23 páginas

- **Qué pasa.** `README.md:37` dice que las muestras «read their values from `colors_and_type.css` at paint time, so a specimen cannot show a value the canon no longer holds». Solo tres cargan `_tokens.js`: `preview/colors-brand.html`, `preview/colors-semantic.html` y `preview/colors-surface.html`. El resto escribe los valores a mano:
  - `preview/spacing-scale.html:16-21`: anchos y etiquetas de la escala de espaciado;
  - `preview/type-display.html:17-19`: tamaños fijos en px en vez de los tokens `--text-display-*`, y un espaciado entre letras que no está en la escala;
  - `preview/spacing-radii-shadows.html:21`: copia a mano del valor de `--glow-brand`. `guard_valores` no lo vigila porque excluye los compuestos por diseño (`tools/guard_valores.py:47-50`).
- **Severidad.** MEDIA: es una afirmación falsa en la portada sobre una garantía de consistencia. Se mide con la tabla de docs.
- **Arreglo.** Hacer que las demás lean los tokens, o acotar la frase a las muestras de color.

### A-16 · Espaciado entre letras fuera de la escala

- **Qué pasa.** La escala `--tracking-*` tiene 7 valores. En el kit, las muestras, `components/components.json` y el propio canon aparecen **40 usos de 18 valores que no están en esa escala, en 22 ficheros**. El lote más repetido son 7 usos del mismo valor (`evidencia/tracking-fuera-de-escala.txt`). Hay dos casos que pesan más:
  - `colors_and_type.css:313`: la clase canónica `.t-h4` usa uno de ellos;
  - `components/components.json:106` y `:108`: la spec que sirve el MCP.
- **Por qué no lo caza nadie.** `guard_valores` persigue **copias** de valores del canon, no valores inventados fuera de él (`tools/guard_valores.py:26-27`).
- **Severidad.** BAJA (smell de arquitectura: el sistema tiene una escala y la composición usa otra).
- **Decide Ibai.** Si esos valores se pasan a la escala (cambia el aspecto) o si alguno se añade como token (versión menor).

### A-17 · El kit contradice reglas del canon

- **Radio.** La píldora de WhatsApp es redonda (`borderRadius: 999`, `ui_kits/website/Header.jsx:54`), y la regla dice radio cero y ninguna esquina redondeada salvo el cursor (`docs/BRAND-RULES.md:25`, `:27`). La spec del badge lo dice expresamente: «pill NO es redonda» (`components/components.json:112`). `ui_kits/website/README.md:37` afirma que el radio cero se «impone globalmente» en `styles.css`, pero `ui_kits/website/styles.css:63` no lleva `!important` y el estilo inline le gana. Los puntos del AntiClient también son redondos (`ui_kits/website/AntiClient.jsx:113`).
- **Una sola CTA roja por vista** (`components/components.json:55`). Con la cabecera fija, la píldora roja de WhatsApp (`Header.jsx:53`) y el CTA rojo del héroe (`ui_kits/website/Hero.jsx:48`) se ven a la vez.
- **Lista de excepciones del radio.** `docs/BRAND-RULES.md:27` dice «salvo el cursor». En cambio `colors_and_type.css:168`, `README.md:107` y `preview/spacing-radii-shadows.html:23` dicen «cursor y pips de bandera».
- **Severidad.** BAJA (coherencia).

### A-18 · El eyebrow pide un peso que no existe

- **Qué pasa.** `--text-eyebrow` declara 900 (`colors_and_type.css:136`), pero Space Mono solo trae 400 y 700 (`colors_and_type.css:9-12`). La decisión está documentada como abierta: «cuál manda no está decidido» (`components/components.json:68`; `ui_kits/website/styles.css:96-103`).
- **Severidad.** BAJA. **Decide Ibai (gusto):** 400 o 700.

### A-19 · Doce lockups dependen de las fuentes de la máquina

- **Qué pasa.** Los lockups horizontal y apilado de CRM, DESIGN SYSTEM, KANBAN DESK, LEGAL REG TECH, ORCHESTRATOR y OUTREACH escriben el nombre con `<text>` vivo y piden la fuente por nombre, sin incrustarla. Ejemplo: `products/kanban-desk/lockups/aglaya-kanban-desk-lockup.svg:2`, `:9-10`; el recuento de los 12 sale de `grep -c '<text'` sobre `products/*/lockups/*.svg`.
- **Por qué importa.** Un SVG usado como `<img>`, como fondo CSS, en una tarjeta social o importado en otra herramienta no puede cargar fuentes web: usa las instaladas en el sistema. En cualquier máquina sin Outfit, el nombre del producto sale en una tipografía genérica. ConsentFlow se pasó a contornos justo por esto: «cero dependencia de fuentes, renderiza idéntico en cualquier máquina» (`products/products.json:84`). `README.md:184` da por bueno que el repo trae las fuentes, pero eso no le sirve a un SVG usado como imagen. El MCP entrega estos ficheros con `get_lockup`.
- **Severidad.** MEDIA. Se mide con la tabla de docs y contrato: un activo servido cuyo render depende del entorno, sin avisarlo.
- **Arreglo.** Exportarlos a contornos, como ConsentFlow.

### A-20 · El lockup de ConsentFlow trae fondo pegado

- **Qué pasa.** `products/consent-flow/lockups/aglaya-consent-flow-lockup.svg:26`, `:30`: un rectángulo opaco marrón oscuro (clase `cfl-6`) cubre todo el lienzo. Los demás lockups son transparentes. Sobre el negro de la marca se ve una caja marrón.
- **Severidad.** BAJA. Parece un residuo de la exportación (`products/products.json:84`: «exportados por el usuario»).

### A-21 · Eslogan a 7 px

- **Qué pasa.** `fontSize: 7` (`ui_kits/website/Header.jsx:20`). WCAG no tiene un criterio que lo falle, pero es ilegible para buena parte de los lectores.
- **Severidad.** BAJA.

### A-22 · Fuentes sin WOFF2

- **Qué pasa.** Las 31 caras de `@font-face` apuntan a OTF o TTF (`colors_and_type.css:9-44`). Los bytes mágicos de los ficheros de `fonts/` dan 18 CFF (`OTTO`) y 13 TrueType, y ningún WOFF2. El paquete pesa 2,93 MB comprimido y 5,12 MB sin comprimir, y `fonts/` son 5,03 MB (`evidencia/npm-pack.txt`, `npm pack --dry-run` sobre un clon limpio). aglaya.biz importa el paquete (`quien_lee("@aglaya/design-tokens")`), así que sus visitantes descargan estos formatos.
- **Confianza.** PROVEN el formato y el peso. Cuánto se ahorraría con WOFF2 queda **NV_TOOL**: no hay `fonttools` ni `woff2_compress` instalados.
- **Severidad.** BAJA, por deuda de activos (tabla de arquitectura).

### A-23 · Babel en el navegador

- **Qué pasa.** El kit carga `babel.min.js` (3,1 MB) y compila el JSX en cada visita (`ui_kits/website/index.html:34-42`). Es una página de referencia, no se sirve.
- **Severidad.** INFO.

### A-24 · Outfit declarada dos veces · UNVERIFIABLE (NV_RUNTIME)

- **Qué pasa.** La fuente variable cubre de 100 a 900 (`colors_and_type.css:16`) y las ocho estáticas repiten de 200 a 900 (`:17-24`). El comentario la llama «static fallbacks» (`:15`), pero entre caras de `@font-face` no hay fallback por orden: cuál se descarga para cada peso lo decide el algoritmo de selección del navegador.
- **Acción externa.** Abrir `preview/type-outfit-weights.html` servido por HTTP y mirar en las herramientas de desarrollo qué ficheros de fuente se descargan.

### A-NV-01 · Métricas web reales · UNVERIFIABLE (NV_RUNTIME)

- Este repo no está desplegado. El efecto de las fuentes y del CSS del paquete en LCP, INP y CLS solo se ve en quien lo consume.
- **Acción externa.** Pasar PageSpeed Insights a aglaya.biz.

### A-NV-02 · El kit abierto como fichero local · UNVERIFIABLE (NV_RUNTIME)

- La portada dice que se abra en el navegador (`README.md:209`). El kit carga sus `.jsx` con `<script type="text/babel" src>` (`ui_kits/website/index.html:36-42`), y Babel las pide por XHR, que Chromium bloquea con `file://`.
- **Intento documentado.** El navegador integrado de esta sesión abre los ficheros locales como una copia `data:` sin recursos relativos, así que no sirve para comprobarlo.
- **Acción externa.** Abrir `ui_kits/website/index.html` con doble clic en Chrome y mirar la consola.

### A-NV-03 · Sin escaneo automático · UNVERIFIABLE (NV_TOOL)

- `axe` y `lighthouse` no están instalados. Todo lo de esta fase sale de leer el código y de cálculos.
- **Acción externa.** Pasar axe DevTools o Lighthouse por el kit y por una muestra de `preview/` servidos por HTTP.

---

## Verificaciones en positivo

- El anillo de foco (`--color-brand`) pasa el 3:1 de no-texto en los dos modos, con valores de 4.0598 a 4.6682 (`evidencia/contraste-tokens.txt`, sección 3).
- `::selection` da 4.6682 (`colors_and_type.css:344`).
- Los tres registros de texto del canon pasan el mínimo en los dos modos. El más bajo es `--color-faint`, con 4.6523 en oscuro y 4.9361 en claro. El suelo que fijó Ibai se cumple.
- El eyebrow en claro, por `--fg-eyebrow`, da 8.6151.
- Las 31 caras declaran `font-display: swap` (`colors_and_type.css:9-44`).
- El kit y las muestras no hacen peticiones externas ni usan cookies, storage o analítica: los greps de `document.cookie`, `localStorage`, `fetch(`, `gtag` y `src="https?://` salen vacíos.
- No hay `alert()`, `confirm()` ni modales (grep vacío). El kit tiene landmarks (`header`, `nav`, `main`, `footer`) y un solo `h1` (`ui_kits/website/Hero.jsx:23`).
- SEO no aplica: nada se sirve como web.
